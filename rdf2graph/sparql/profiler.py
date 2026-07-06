"""スキーマ偵察（クラス発見）と述語プロファイラ。

対象4エンドポイントは正確なオントロジーURIが未調査であるため、`target_class` やラベル
プロパティの決め打ちを禁止する（CLAUDE.md 決定事項#4）。ここでの出力はPhase 3で人間が
確定するための「候補」であり、自動探索の結果を鵜呑みにして確定させることはしない。

すべての問い合わせは`SPARQLClient.query()`を経由する（新しいHTTP呼び出し経路を作らない）。
クエリ文字列の組み立ては`query_builder`のヘルパーを再利用する。
"""
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from rdf2graph.sparql.client import Binding, SPARQLClient, SPARQLResponseFormatError
from rdf2graph.sparql.query_builder import int_literal, iri
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

DEFAULT_CLASS_LIMIT = 20
DEFAULT_PREDICATE_SAMPLE_SIZE = 200
DEFAULT_TOP_N_CLASSES_TO_PROFILE = 5
DEFAULT_VALUE_HISTOGRAM_TOP_N = 15
DEFAULT_LABEL_MIN_COVERAGE = 0.5
DEFAULT_LABEL_MAX_CARDINALITY_RATIO = 0.5
DEFAULT_LABEL_MIN_DISTINCT_VALUES = 2
DEFAULT_FEATURE_MIN_COVERAGE = 0.30

RDF_TYPE_URI = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

# NDLで実証済みのサーバー側result cap(LIMIT 5000->1000行、docs/endpoint_status.md参照)と
# 同種の「いかにも人為的な打ち切り」を示唆する丸い数字。GROUP BY集計でも同種の暗黙capが
# 起きうることを前提に、これらの値が出た場合は疑わしいとマークする(CLAUDE.md決定事項#14)。
_SUSPICIOUS_ROUND_COUNTS = {100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000}


@dataclass(frozen=True)
class ClassCandidate:
    """クラス発見クエリで得た、クラスURIとそのインスタンス数(集計値)。"""

    class_uri: str
    count: int
    suspicious: bool = False
    note: str = ""


@dataclass(frozen=True)
class PredicateProfile:
    """あるクラスのサンプルインスタンス集合に対する、ある述語の出現傾向。

    `distinct_value_basis`/`distinct_value_count`/`label_cardinality_ratio`/`value_histogram`は
    「分類ラベル候補として機能しうるか」を判定するための値の異なり数(カーディナリティ)指標。
    literalとuriの値が混在する述語（例: dc:subjectがLCSH文字列と人物URIを同居させている場合）は
    literal側の値だけを対象にする。uri側は別の意味の関係が混入している可能性が高いため
    （suggest_label_candidatesの判定基準の説明も参照）。
    """

    predicate_uri: str
    coverage: float
    is_multivalued: bool
    value_types: dict[str, int] = field(default_factory=dict)
    covered_subject_count: int = 0
    distinct_value_basis: str = "none"  # "literal" | "uri" | "none"(bnodeのみ、または値なし)
    distinct_value_count: int = 0
    label_cardinality_ratio: float | None = None
    value_histogram: dict[str, int] = field(default_factory=dict)  # basis側の値の頻度上位、多い順


@dataclass(frozen=True)
class ClassProfile:
    """1クラス分の述語プロファイル一式。"""

    class_candidate: ClassCandidate
    sample_size: int
    predicates: list[PredicateProfile]


def _looks_suspicious_round_count(count: int) -> bool:
    if count in _SUSPICIOUS_ROUND_COUNTS:
        return True
    return count >= 1000 and count % 1000 == 0


def discover_classes(client: SPARQLClient, limit: int = DEFAULT_CLASS_LIMIT) -> list[ClassCandidate]:
    """`?s a ?class`のインスタンス数を集計し、上位`limit`件のクラス候補を返す。

    サーバー側の暗黙のresult cap(CLAUDE.md決定事項#14、NDLで実証済み)がGROUP BY集計
    クエリにも及ぶ可能性を考慮し、不自然に丸い数字が出たクラスは`suspicious=True`で
    マークする(素通ししない)。これは疑いの可視化であり、判定の確定ではない。
    """
    query = (
        "SELECT ?class (COUNT(?s) AS ?count) WHERE { "
        "?s a ?class . "
        f"}} GROUP BY ?class ORDER BY DESC(?count) LIMIT {int_literal(limit)}"
    )
    rows = client.query(query)
    if not isinstance(rows, list):
        raise SPARQLResponseFormatError(
            "discover_classes() requires a SELECT-shaped query, but got an ASK-shaped "
            "(boolean) response"
        )

    candidates = []
    for row in rows:
        class_uri = row["class"].value
        count = int(row["count"].value)
        suspicious = _looks_suspicious_round_count(count)
        note = (
            f"count={count} is a suspiciously round number; a server-side implicit result "
            "cap was already confirmed for NDL (LIMIT 5000 -> 1000 rows, see "
            "docs/endpoint_status.md) -- treat this count as unverified until checked manually"
            if suspicious
            else ""
        )
        candidates.append(ClassCandidate(class_uri=class_uri, count=count, suspicious=suspicious, note=note))
    return candidates


def _sample_instance_count(rows: list[dict[str, Binding]]) -> int:
    return len({row["s"].value for row in rows})


def profile_predicates(
    client: SPARQLClient,
    class_uri: str,
    sample_size: int = DEFAULT_PREDICATE_SAMPLE_SIZE,
    total_instance_count: int | None = None,
) -> ClassProfile:
    """`class_uri`のインスタンスを`sample_size`件サンプリングし、述語ごとの被覆率・
    値の型・多値判定・分類ラベル候補用のカーディナリティ指標を計算する。

    サブクエリで先にインスタンス集合を固定してから`?s ?p ?o`と結合するため、外側に
    LIMITを掛けて途中の主語で打ち切る(=一部の主語だけ不完全な統計になる)ことを避ける。

    `total_instance_count`は`discover_classes`で得た真のインスタンス総数（分かっていれば）。
    渡された場合はレンダリング時に「全体X件中Y件をサンプリング」を表示できる。渡さない場合は
    サンプル件数をそのまま使う(真の総数は不明という意味)。
    """
    query = (
        "SELECT ?s ?p ?o WHERE { "
        f"{{ SELECT ?s WHERE {{ ?s a {iri(class_uri)} }} LIMIT {int_literal(sample_size)} }} "
        "?s ?p ?o . "
        "}"
    )
    rows = client.query(query)
    if not isinstance(rows, list):
        raise SPARQLResponseFormatError(
            "profile_predicates() requires a SELECT-shaped query, but got an ASK-shaped "
            "(boolean) response"
        )

    total_subjects = _sample_instance_count(rows)
    if total_subjects == 0:
        return ClassProfile(
            class_candidate=ClassCandidate(class_uri=class_uri, count=total_instance_count or 0),
            sample_size=0,
            predicates=[],
        )

    per_predicate_subjects: dict[str, set[str]] = defaultdict(set)
    per_predicate_triple_count: dict[str, int] = defaultdict(int)
    per_predicate_value_types: dict[str, Counter] = defaultdict(Counter)
    # 分類ラベル候補判定用: literal(typed-literal含む)とuriを別集計し、両方あればliteral優先で
    # 採用する(uri側は別の意味の関係が混入している可能性が高いため、混在時はliteral側のみ見る)。
    per_predicate_literal_values: dict[str, Counter] = defaultdict(Counter)
    per_predicate_literal_subjects: dict[str, set[str]] = defaultdict(set)
    per_predicate_uri_values: dict[str, Counter] = defaultdict(Counter)
    per_predicate_uri_subjects: dict[str, set[str]] = defaultdict(set)

    for row in rows:
        subject = row["s"].value
        predicate = row["p"].value
        obj: Binding = row["o"]
        per_predicate_subjects[predicate].add(subject)
        per_predicate_triple_count[predicate] += 1
        per_predicate_value_types[predicate][obj.type] += 1
        if obj.type in ("literal", "typed-literal"):
            per_predicate_literal_values[predicate][obj.value] += 1
            per_predicate_literal_subjects[predicate].add(subject)
        elif obj.type == "uri":
            per_predicate_uri_values[predicate][obj.value] += 1
            per_predicate_uri_subjects[predicate].add(subject)
        # bnodeは値そのものに再現性がないため、カーディナリティ判定の対象にしない

    profiles = []
    for predicate, subjects in per_predicate_subjects.items():
        coverage = len(subjects) / total_subjects
        is_multivalued = per_predicate_triple_count[predicate] > len(subjects)

        if per_predicate_literal_values[predicate]:
            basis = "literal"
            value_counter = per_predicate_literal_values[predicate]
            basis_subject_count = len(per_predicate_literal_subjects[predicate])
        elif per_predicate_uri_values[predicate]:
            basis = "uri"
            value_counter = per_predicate_uri_values[predicate]
            basis_subject_count = len(per_predicate_uri_subjects[predicate])
        else:
            basis = "none"
            value_counter = Counter()
            basis_subject_count = 0

        distinct_value_count = len(value_counter)
        label_cardinality_ratio = (
            distinct_value_count / basis_subject_count if basis_subject_count > 0 else None
        )

        profiles.append(
            PredicateProfile(
                predicate_uri=predicate,
                coverage=coverage,
                is_multivalued=is_multivalued,
                value_types=dict(per_predicate_value_types[predicate]),
                covered_subject_count=len(subjects),
                distinct_value_basis=basis,
                distinct_value_count=distinct_value_count,
                label_cardinality_ratio=label_cardinality_ratio,
                value_histogram=dict(value_counter.most_common(DEFAULT_VALUE_HISTOGRAM_TOP_N)),
            )
        )
    profiles.sort(key=lambda p: p.coverage, reverse=True)

    return ClassProfile(
        class_candidate=ClassCandidate(
            class_uri=class_uri,
            count=total_instance_count if total_instance_count is not None else total_subjects,
        ),
        sample_size=total_subjects,
        predicates=profiles,
    )


@dataclass(frozen=True)
class ValueCount:
    """全数集計クエリで得た、ラベル候補述語の1つの値とその出現件数。"""

    value: str
    value_type: str  # "uri" | "literal" | "typed-literal" | "bnode"
    count: int


def count_label_values(
    client: SPARQLClient,
    class_uri: str,
    predicate_uri: str,
    limit: int = 50,
    literal_only: bool = False,
) -> list[ValueCount]:
    """対象クラス全数に対するラベル候補述語の値分布を、GROUP BY集計で直接取得する。

    `profile_predicates`の行単位サンプリング（決定事項#19のサンプリングバイアス懸念あり）を
    経由せず、`discover_classes`と同じ集計パターンでサーバー側に全数を数えさせる。
    ランダムサンプリング機構の新規実装（`ORDER BY RAND()`は大規模クラスでサーバー側
    フルソートが必要になりタイムアウトの危険がある）を避けるための設計。

    `literal_only=True`はliteral/uri混在述語（例: Cervantes Virtualの`dc:subject`）で
    literal値のみを集計対象にする。
    """
    filter_clause = "FILTER(isLiteral(?v)) . " if literal_only else ""
    query = (
        "SELECT ?v (COUNT(?s) AS ?count) WHERE { "
        f"?s a {iri(class_uri)} . "
        f"?s {iri(predicate_uri)} ?v . "
        f"{filter_clause}"
        f"}} GROUP BY ?v ORDER BY DESC(?count) LIMIT {int_literal(limit)}"
    )
    rows = client.query(query)
    if not isinstance(rows, list):
        raise SPARQLResponseFormatError(
            "count_label_values() requires a SELECT-shaped query, but got an ASK-shaped "
            "(boolean) response"
        )
    return [
        ValueCount(value=row["v"].value, value_type=row["v"].type, count=int(row["count"].value))
        for row in rows
    ]


def render_label_census_markdown(
    class_uri: str,
    predicate_uri: str,
    value_counts: list[ValueCount],
    class_total: int,
    limit: int,
    literal_only: bool,
) -> str:
    """「全数集計によるラベル候補検証」節のMarkdownを組み立てる(I/Oを持たない純関数)。

    決定事項#19（サンプリングバイアス懸念）への対応として、200件サンプル節とは独立に
    対象クラス全数へのGROUP BY集計結果を提示する。既存のサンプル節を置き換えるものではない。
    """
    labeled_total = sum(vc.count for vc in value_counts)
    lines = [
        "## 全数集計によるラベル候補検証",
        "",
        f"- 対象クラス: `{class_uri}`（全体 {class_total} 件）",
        f"- ラベル候補述語: `{predicate_uri}`" + ("（literal値のみ集計）" if literal_only else ""),
        f"- 集計方法: `GROUP BY ?v` による全数集計（上位{limit}件まで取得）。"
        "200件サンプルの述語プロファイル（決定事項#19のサンプリングバイアス懸念あり）を経由しない。",
        "",
    ]
    if not value_counts:
        lines.append("⚠️ 集計結果が0行だった。述語URIの誤りかエンドポイント側の問題を疑うこと。")
        lines.append("")
        return "\n".join(lines) + "\n"

    lines.append("| 順位 | 値 | 件数 | 対クラス全体比 |")
    lines.append("|---|---|---|---|")
    for i, vc in enumerate(value_counts, start=1):
        share = vc.count / class_total if class_total > 0 else 0.0
        lines.append(f"| {i} | `{vc.value}` | {vc.count} | {share:.1%} |")
    lines.append("")

    top_share_of_labeled = value_counts[0].count / labeled_total if labeled_total > 0 else 0.0
    coverage = labeled_total / class_total if class_total > 0 else 0.0
    lines.append(
        f"取得{len(value_counts)}値の合計は {labeled_total} 件"
        f"（クラス全体の {coverage:.1%}。多値述語では100%を超えうる）。"
        f"最頻値はラベル付き集合の {top_share_of_labeled:.1%} を占める。"
    )
    if top_share_of_labeled > 0.9:
        lines.append("")
        lines.append(
            "⚠️ **最頻値がラベル付き集合の90%超を占める極端な偏りがある。**"
            "このままlabel_propertyとして採用すると多数派クラス予測とほぼ区別がつかなくなるため、"
            "config確定前に人間の判断を仰ぐこと。"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def suggest_label_candidates(
    predicates: list[PredicateProfile],
    min_coverage: float = DEFAULT_LABEL_MIN_COVERAGE,
    max_cardinality_ratio: float = DEFAULT_LABEL_MAX_CARDINALITY_RATIO,
    min_distinct_values: int = DEFAULT_LABEL_MIN_DISTINCT_VALUES,
) -> list[PredicateProfile]:
    """被覆率が高く、かつ値の異なり数が(値を持つ主語数に対して)十分小さい述語を
    分類ラベル候補として提示する(確定ではない)。

    `rdfs:label`/`dc:title`/`dc:created`のような自由テキスト・タイムスタンプは被覆率が
    高くても主語ごとにほぼ1つの異なる値を持つため(cardinality_ratioがほぼ1.0)除外される。
    値の型がuriであることは除外理由にしない(例: `skos:inScheme`のような閉じた集合の
    URI述語は良い分類ラベル候補になりうる)。多値であること自体も除外理由にしない
    (Phase 3のラベル抽出ロジックは頻度上位カテゴリに複数値のいずれかがマッチすれば良い設計)。

    異なり値数が`min_distinct_values`未満(既定2、つまり実質1種類しか値を持たない)の述語は
    カーディナリティ比が最小(0に近い)になるため素朴なソートでは最上位に来てしまうが、
    分類先が実質1クラスしかない述語は分類ラベルとして無意味なので明示的に除外する
    (実例: Cervantes Virtualの`dc:terms:created`は全インスタンスで"02/02/2026"固定値
    ＝収集日時のスタンプであり、実データの属性ではない)。
    """
    candidates = [
        p
        for p in predicates
        if p.label_cardinality_ratio is not None
        and p.coverage >= min_coverage
        and p.label_cardinality_ratio <= max_cardinality_ratio
        and p.distinct_value_count >= min_distinct_values
    ]
    candidates.sort(key=lambda p: (p.label_cardinality_ratio, -p.coverage))
    return candidates


def suggest_feature_candidates(
    predicates: list[PredicateProfile], min_coverage: float = DEFAULT_FEATURE_MIN_COVERAGE
) -> list[PredicateProfile]:
    """被覆率がしきい値(Phase3設定テンプレの`min_coverage`既定値0.30)以上の述語を
    特徴量候補として提示する(確定ではない)。分類ラベルと異なり、特徴量は自由テキスト
    (タイトル等)でもハッシュ化/TF-IDFベクトル化すれば良いため、カーディナリティでは
    絞り込まない。"""
    return sorted((p for p in predicates if p.coverage >= min_coverage), key=lambda p: -p.coverage)


def render_profile_markdown(
    endpoint_name: str,
    endpoint_url: str,
    class_candidates: list[ClassCandidate],
    class_profiles: list[ClassProfile],
    requested_class_limit: int,
) -> str:
    """`docs/profile_<endpoint>.md`向けのMarkdown本文を組み立てる(I/Oを持たない純関数)。"""
    lines = [f"# {endpoint_name} スキーマ偵察結果", "", f"- エンドポイント: {endpoint_url}", ""]

    lines.append("## 主要クラス候補（インスタンス数上位）")
    lines.append("")
    if len(class_candidates) < requested_class_limit:
        lines.append(
            f"⚠️ 要求した上位{requested_class_limit}件に対し、実際に発見されたクラスは"
            f"{len(class_candidates)}件のみだった。スキーマが元々小さい可能性もあるが、"
            "GROUP BY集計自体が打ち切られている可能性も排除できない（素通しせず目視確認すること）。"
        )
        lines.append("")
    lines.append("| 順位 | クラスURI | インスタンス数(集計値) | 疑わしさ |")
    lines.append("|---|---|---|---|")
    for i, c in enumerate(class_candidates, start=1):
        flag = f"⚠️ {c.note}" if c.suspicious else "-"
        lines.append(f"| {i} | `{c.class_uri}` | {c.count} | {flag} |")
    lines.append("")

    lines.append("## クラスごとの述語プロファイル")
    lines.append("")
    for profile in class_profiles:
        cand = profile.class_candidate
        if cand.count and cand.count != profile.sample_size:
            header_note = f"全体 {cand.count} 件中 {profile.sample_size} 件をサンプリング"
        else:
            header_note = f"サンプルインスタンス数: {profile.sample_size}"
        lines.append(f"### `{cand.class_uri}`（{header_note}）")
        lines.append("")
        if not profile.predicates:
            lines.append("(サンプルが0件だったため述語プロファイルなし)")
            lines.append("")
            continue
        lines.append(
            "| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |"
        )
        lines.append("|---|---|---|---|---|---|")
        for p in profile.predicates:
            value_types_str = ", ".join(f"{k}:{v}" for k, v in sorted(p.value_types.items()))
            cardinality_str = (
                f"{p.distinct_value_count} ({p.label_cardinality_ratio:.0%})"
                if p.label_cardinality_ratio is not None
                else "-"
            )
            histogram_str = "; ".join(f"{v}({c})" for v, c in list(p.value_histogram.items())[:5])
            lines.append(
                f"| `{p.predicate_uri}` | {p.coverage:.0%} | {'yes' if p.is_multivalued else 'no'} | "
                f"{value_types_str} | {cardinality_str} | {histogram_str} |"
            )
        lines.append("")

        type_profile = next((p for p in profile.predicates if p.predicate_uri == RDF_TYPE_URI), None)
        if type_profile is not None and type_profile.is_multivalued:
            breakdown = "; ".join(f"`{v}`({c}件)" for v, c in type_profile.value_histogram.items())
            lines.append(
                f"⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある"
                f"（内訳: {breakdown}）。追加の述語取得なしに使えるサブタイプ由来のラベル候補に"
                "なりうるため検討する価値がある。"
            )
            lines.append("")

        label_candidates = suggest_label_candidates(profile.predicates)
        lines.append(
            "**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して"
            "小さい＝閉じた集合とみなせる述語。確定ではない）:"
        )
        lines.append("")
        if label_candidates:
            for p in label_candidates:
                lines.append(
                    f"- `{p.predicate_uri}`（被覆率 {p.coverage:.0%}、"
                    f"異なり値数 {p.distinct_value_count}/{p.covered_subject_count} "
                    f"= {p.label_cardinality_ratio:.0%}）"
                )
        else:
            lines.append("- (機械的な提案なし。人間による個別調査が必要)")
        lines.append("")

        feature_candidates = suggest_feature_candidates(profile.predicates)
        lines.append("**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:")
        lines.append("")
        if feature_candidates:
            for p in feature_candidates:
                lines.append(f"- `{p.predicate_uri}`（被覆率 {p.coverage:.0%}）")
        else:
            lines.append("- (機械的な提案なし。人間による個別調査が必要)")
        lines.append("")

    lines.append(
        "---\n"
        "**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、"
        "上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」は"
        "Phase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。"
    )
    return "\n".join(lines) + "\n"
