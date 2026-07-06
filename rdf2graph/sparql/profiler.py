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
DEFAULT_MAX_SAMPLE_VALUES = 5
DEFAULT_LABEL_MIN_COVERAGE = 0.5
DEFAULT_FEATURE_MIN_COVERAGE = 0.30

# NDLで実証済みのサーバー側result cap(LIMIT 5000->1000行、docs/endpoint_status.md参照)と
# 同種の「いかにも人為的な打ち切り」を示唆する丸い数字。GROUP BY集計でも同種の暗黙capが
# 起きうることを前提に、これらの値が出た場合は疑わしいとマークする(CLAUDE.md決定事項#14)。
_SUSPICIOUS_ROUND_COUNTS = {100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000}

_LABEL_HINT_TOKENS = ("label", "title", "name", "preflabel", "caption", "heading")


class ProfilerError(Exception):
    """profiler.py固有のエラーの基底クラス。"""


@dataclass(frozen=True)
class ClassCandidate:
    """クラス発見クエリで得た、クラスURIとそのインスタンス数(集計値)。"""

    class_uri: str
    count: int
    suspicious: bool = False
    note: str = ""


@dataclass(frozen=True)
class PredicateProfile:
    """あるクラスのサンプルインスタンス集合に対する、ある述語の出現傾向。"""

    predicate_uri: str
    coverage: float
    is_multivalued: bool
    value_types: dict[str, int] = field(default_factory=dict)
    sample_values: list[str] = field(default_factory=list)


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
    max_sample_values: int = DEFAULT_MAX_SAMPLE_VALUES,
) -> ClassProfile:
    """`class_uri`のインスタンスを`sample_size`件サンプリングし、述語ごとの被覆率・
    値の型・多値判定を行う。

    サブクエリで先にインスタンス集合を固定してから`?s ?p ?o`と結合するため、外側に
    LIMITを掛けて途中の主語で打ち切る(=一部の主語だけ不完全な統計になる)ことを避ける。
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
            class_candidate=ClassCandidate(class_uri=class_uri, count=0),
            sample_size=0,
            predicates=[],
        )

    per_predicate_subjects: dict[str, set[str]] = defaultdict(set)
    per_predicate_triple_count: dict[str, int] = defaultdict(int)
    per_predicate_value_types: dict[str, Counter] = defaultdict(Counter)
    per_predicate_samples: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        subject = row["s"].value
        predicate = row["p"].value
        obj: Binding = row["o"]
        per_predicate_subjects[predicate].add(subject)
        per_predicate_triple_count[predicate] += 1
        per_predicate_value_types[predicate][obj.type] += 1
        if len(per_predicate_samples[predicate]) < max_sample_values:
            per_predicate_samples[predicate].append(obj.value)

    profiles = []
    for predicate, subjects in per_predicate_subjects.items():
        coverage = len(subjects) / total_subjects
        is_multivalued = per_predicate_triple_count[predicate] > len(subjects)
        profiles.append(
            PredicateProfile(
                predicate_uri=predicate,
                coverage=coverage,
                is_multivalued=is_multivalued,
                value_types=dict(per_predicate_value_types[predicate]),
                sample_values=per_predicate_samples[predicate],
            )
        )
    profiles.sort(key=lambda p: p.coverage, reverse=True)

    return ClassProfile(
        class_candidate=ClassCandidate(class_uri=class_uri, count=total_subjects),
        sample_size=total_subjects,
        predicates=profiles,
    )


def _tail_of(uri: str) -> str:
    return uri.rsplit("/", 1)[-1].rsplit("#", 1)[-1].lower()


def _looks_like_label_predicate(predicate_uri: str) -> bool:
    tail = _tail_of(predicate_uri)
    return any(token in tail for token in _LABEL_HINT_TOKENS)


def suggest_label_candidates(
    predicates: list[PredicateProfile], min_coverage: float = DEFAULT_LABEL_MIN_COVERAGE
) -> list[PredicateProfile]:
    """被覆率が高く、値の大半がliteralな述語をラベル候補として提示する(確定ではない)。"""
    candidates = []
    for p in predicates:
        total = sum(p.value_types.values())
        if total == 0 or p.coverage < min_coverage:
            continue
        literal_ratio = p.value_types.get("literal", 0) / total
        if literal_ratio >= 0.5:
            candidates.append(p)
    candidates.sort(key=lambda p: (not _looks_like_label_predicate(p.predicate_uri), -p.coverage))
    return candidates


def suggest_feature_candidates(
    predicates: list[PredicateProfile], min_coverage: float = DEFAULT_FEATURE_MIN_COVERAGE
) -> list[PredicateProfile]:
    """被覆率がしきい値(Phase3設定テンプレの`min_coverage`既定値0.30)以上の述語を
    特徴量候補として提示する(確定ではない)。"""
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
        lines.append(f"### `{cand.class_uri}`（サンプルインスタンス数: {profile.sample_size}）")
        lines.append("")
        if not profile.predicates:
            lines.append("(サンプルが0件だったため述語プロファイルなし)")
            lines.append("")
            continue
        lines.append("| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |")
        lines.append("|---|---|---|---|---|")
        for p in profile.predicates:
            value_types_str = ", ".join(f"{k}:{v}" for k, v in sorted(p.value_types.items()))
            samples_str = "; ".join(p.sample_values)
            lines.append(
                f"| `{p.predicate_uri}` | {p.coverage:.0%} | {'yes' if p.is_multivalued else 'no'} | "
                f"{value_types_str} | {samples_str} |"
            )
        lines.append("")

        label_candidates = suggest_label_candidates(profile.predicates)
        lines.append("**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:")
        lines.append("")
        if label_candidates:
            for p in label_candidates:
                lines.append(f"- `{p.predicate_uri}`（被覆率 {p.coverage:.0%}）")
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
