"""Phase 3: ラベル抽出ロジック。

target_classインスタンスを素朴に`SELECT ?s WHERE {?s a <class>} LIMIT max_nodes`で
取得すると、決定事項#19で実証済みの物理格納順への強い相関（DBLPの200件サンプルが
94% `Incollection`に偏った実例、真の分布は`Article`50.7%/`Inproceedings`45.4%、
決定事項#20）を再現してしまう。`max_nodes`規模の抽出でもこの偏りは解消されない。

この実装は`count_label_values`（決定事項#20、GROUP BY全数集計）で得たtop-kラベル値
ごとの真の件数比率に`sampling.max_nodes`を按分し、ラベル値ごとに個別のSPARQLクエリで
抽出する「層化抽出」を採用する（CLAUDE.md決定事項#22）。層間（ラベル間）の比率は
全数集計の真の値に一致することが保証されるが、層内（同一ラベル値内）の抽出順序は
サーバーの既定順（挿入順等への相関の可能性）であり、真の一様ランダムではない
残存バイアスとして限界節に明記する。

`unmatched_policy`は現時点で"drop"のみ実装する。確定済みの2config
（dblp.yaml/ndl_authorities.yaml）がいずれも"drop"であるため、他の値を一般化して
実装する理由が今回のスコープにはない。
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from rdf2graph.convert.schema import EndpointConfig
from rdf2graph.sparql.client import SPARQLClient
from rdf2graph.sparql.profiler import ValueCount, count_label_values
from rdf2graph.sparql.query_builder import iri, string_literal
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class LabeledNode:
    """1つのtarget_classインスタンスと、その代表ラベル値。"""

    uri: str
    label: str


@dataclass(frozen=True)
class LabelExtractionResult:
    """Phase 3ラベル抽出の実行結果一式。"""

    nodes: list[LabeledNode]
    label_values: list[ValueCount]
    requested_per_class: dict[str, int]
    actual_per_class: "Counter[str]"
    duplicate_count: int


def assign_label(values: list[str], ranked_candidates: list[str]) -> str | None:
    """あるノードが持つラベル候補述語の値集合`values`から、`ranked_candidates`
    （頻度降順に並んだtop-kカテゴリ）の中で最初にマッチしたものを代表ラベルとして返す。

    どれにもマッチしない場合はNone（unmatched_policyの判断に委ねる）。
    build-lod-project.md Phase 3の仕様「頻度順で最初にマッチしたものを代表ラベルとする」
    の直接の実装であり、層化抽出で複数の層に同一URIが出現した場合の優先順位判定にも
    同じ関数を使う（`extract_labeled_nodes`参照）。
    """
    value_set = set(values)
    for candidate in ranked_candidates:
        if candidate in value_set:
            return candidate
    return None


def _value_term(value: str, value_type: str) -> str:
    if value_type == "uri":
        return iri(value)
    if value_type in ("literal", "typed-literal"):
        # 注意: 言語タグ・データ型付きリテラルとの厳密一致は保証しない(プレーン文字列
        # としての比較になる)。確定済みの2config(bibtexType/inSchemeはいずれもuri値)は
        # この分岐を通らない。
        return string_literal(value)
    raise ValueError(f"label value type {value_type!r} is not supported as a classification target")


def _allocate_per_class(label_values: list[ValueCount], max_nodes: int) -> dict[str, int]:
    """`label_values`(真の件数、降順)の比率に比例して`max_nodes`を按分する。

    端数は最頻値の層に寄せる。top_k件の層数に対して各層の真の件数が十分大きい
    (本プロジェクトの規模では常に成立、CLAUDE.md決定事項#22)限り、この単純な処理で足りる。
    """
    total = sum(v.count for v in label_values)
    if total == 0:
        raise ValueError("label_values have zero total count; cannot allocate")
    allocation = {v.value: int(max_nodes * v.count / total) for v in label_values}
    shortfall = max_nodes - sum(allocation.values())
    allocation[label_values[0].value] += shortfall
    return allocation


def extract_labeled_nodes(client: SPARQLClient, config: EndpointConfig) -> LabelExtractionResult:
    """`config`に基づき、target_classインスタンスをラベル値ごとに層化抽出する。"""
    if config.label.unmatched_policy != "drop":
        raise NotImplementedError(
            f"label.unmatched_policy={config.label.unmatched_policy!r} is not implemented; "
            "this submission's scope covers 'drop' only (both finalized configs use 'drop', "
            "see CLAUDE.md decision #22)"
        )

    label_values = count_label_values(
        client, config.target_class, config.label.property, limit=config.label.top_k
    )
    if not label_values:
        raise ValueError(
            f"count_label_values returned no rows for target_class={config.target_class!r}, "
            f"label.property={config.label.property!r}; cannot extract labeled nodes"
        )

    requested_per_class = _allocate_per_class(label_values, config.sampling.max_nodes)

    assigned: dict[str, str] = {}  # uri -> label (頻度順で先着したものを保持する)
    duplicate_count = 0
    for value_count in label_values:  # count_label_valuesは既に頻度降順で返す
        n = requested_per_class[value_count.value]
        if n <= 0:
            continue
        term = _value_term(value_count.value, value_count.value_type)
        # 決定事項#14: NDLはLIMIT要求値によらず1行の応答が最大1000行に無言で切り詰められる
        # ことを実証済み。単発のLIMIT nクエリではこの上限に頭打ちになる(層化抽出全体の
        # 実件数が要求より大幅に不足する)ため、`paginate()`でsampling.page_size単位に
        # OFFSETを進めながら要求件数nに達するまで取得する。
        query_template = (
            "SELECT ?s WHERE { "
            f"?s a {iri(config.target_class)} . "
            f"?s {iri(config.label.property)} {term} . "
            "} LIMIT {limit} OFFSET {offset}"
        )
        rows = client.paginate(query_template, page_size=config.sampling.page_size, max_total=n)
        for row in rows:
            node_uri = row["s"].value
            if node_uri in assigned:
                duplicate_count += 1
                logger.debug(
                    "node %s already assigned label %r; keeping it over lower-priority "
                    "candidate %r (frequency-first precedence, see assign_label)",
                    node_uri,
                    assigned[node_uri],
                    value_count.value,
                )
                continue
            assigned[node_uri] = value_count.value

    total_assigned = len(assigned)
    if total_assigned < config.sampling.max_nodes * 0.95:
        logger.warning(
            "extract_labeled_nodes: assigned only %d/%d requested nodes for %s "
            "(some strata may hold fewer true instances than allocated, or many "
            "cross-stratum duplicates were resolved)",
            total_assigned,
            config.sampling.max_nodes,
            config.target_class,
        )

    nodes = [LabeledNode(uri=node_uri, label=label) for node_uri, label in assigned.items()]
    return LabelExtractionResult(
        nodes=nodes,
        label_values=label_values,
        requested_per_class=requested_per_class,
        actual_per_class=Counter(assigned.values()),
        duplicate_count=duplicate_count,
    )
