"""Phase 4: RDF(Phase 3で抽出したtarget_classノード集合)から`torch_geometric.data.Data`
（`edge_type`付き単一Data、CLAUDE.md決定事項#15）を構築する。

設計上の要点（詳細はCLAUDE.md決定事項#23）:

- ノードの1-hopプロパティは`VALUES`句によるバッチクエリで取得する。Phase 3で既に確定した
  具体的なURI集合に対してLIMITなしで問い合わせるため、決定事項#19のサンプリングバイアス
  （サブクエリ+LIMIT方式）を持ち込まない。
- `label.property`と`rdf:type`はエッジ/特徴量の自動発見から無条件除外する
  （ラベルリーク防止。R-GCN原論文のAIFB/MUTAG前処理と同じ慣行）。
- エッジ生成対象はobject property（値の型が`uri`）に限定する。bnode値の述語は1-hopの
  安定したノードとして扱いにくいため対象外。
- 各リレーションについて逆方向のリレーションを明示的に追加する（双方向メッセージパッシング
  のため。PyGのEntities(AIFB/MUTAG等)データセットと同じ慣行）。
- ノード特徴量 = 構造特徴（次数 + リレーションタイプ別隣接数）+ `text_properties`の
  浅いテキスト特徴（決定事項#5）。
"""
from __future__ import annotations

import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import torch
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from torch_geometric.data import Data

from rdf2graph.convert.labels import LabeledNode
from rdf2graph.convert.schema import EndpointConfig, SplitConfig
from rdf2graph.sparql.client import Binding, SPARQLClient, SPARQLResponseFormatError
from rdf2graph.sparql.profiler import RDF_TYPE_URI
from rdf2graph.sparql.query_builder import iri
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

TEXT_FEATURE_DIM = 128
# VALUES句1つに含めるURI数。実地検証の結果、NDLのエンドポイントはSPARQLWrapper経由のPOST
# 要求を403で拒否した(生curlのPOSTとGETは200なので、SPARQLWrapperのPOST送出形式がNDLの
# WAFに弾かれたと判断)。そのため確実に動くGET経路(NDL/DBLP両方で200を確認済み)を使い、
# GETのURL長上限(多くのサーバで~8KB)に収まるようバッチを小さく保つ。URIを~70文字/件・
# URLエンコード込みで見積もっても60件なら~5KBに収まる。sampling.page_size(SPARQL結果の
# ページサイズ)とは別の技術的パラメータ。
PROPERTY_FETCH_BATCH_SIZE = 60

Triple = tuple[str, str, Binding]


@dataclass(frozen=True)
class ConversionTiming:
    """Phase 6の「変換時間」評価軸（CLAUDE.md決定事項#9）のための内訳。"""

    sparql_seconds: float
    build_seconds: float


def save_graph(data: Data, path: Path | str) -> None:
    """`Data`をディスクに保存する。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(data, path)


def load_graph(path: Path | str) -> Data:
    """`save_graph`で保存した`Data`を読み込む。

    CLAUDE.md決定事項#24: torch>=2.6の`torch.load`はデフォルトで`weights_only=True`に
    なり、`Data`のような任意オブジェクトの読込みに失敗する。本プロジェクトが前提とする
    torch==2.11.0でも同様のため、信頼できるローカル生成物であることを踏まえ明示的に無効化する。
    """
    return torch.load(Path(path), weights_only=False)


def _fetch_properties_for_nodes(client: SPARQLClient, node_uris: list[str]) -> list[Triple]:
    """`node_uris`を主語とする全トリプルを`VALUES`句のバッチクエリで取得する。

    Phase 3で既に確定した具体的なURI集合に対する厳密指定であり、LIMITによる打ち切りが
    起きないため、決定事項#19のサンプリングバイアスをここに持ち込まない。
    """
    triples: list[Triple] = []
    for start in range(0, len(node_uris), PROPERTY_FETCH_BATCH_SIZE):
        batch = node_uris[start : start + PROPERTY_FETCH_BATCH_SIZE]
        values_clause = " ".join(iri(u) for u in batch)
        query = f"SELECT ?s ?p ?o WHERE {{ VALUES ?s {{ {values_clause} }} ?s ?p ?o . }}"
        rows = client.query(query)
        if not isinstance(rows, list):
            raise SPARQLResponseFormatError(
                "_fetch_properties_for_nodes() requires a SELECT-shaped query, but got an "
                "ASK-shaped (boolean) response"
            )
        for row in rows:
            triples.append((row["s"].value, row["p"].value, row["o"]))
    return triples


def _select_edge_predicates(
    triples: list[Triple],
    total_target_nodes: int,
    exclude: set[str],
    min_coverage: float,
    max_properties: int,
) -> list[str]:
    """object property（値がuri型）のうち、除外述語を除いて被覆率が高い順に選ぶ。

    被覆率は「target_classノードのうち、この述語でuri値を少なくとも1つ持つものの割合」。
    """
    subjects_by_predicate: dict[str, set[str]] = defaultdict(set)
    for subject, predicate, obj in triples:
        if predicate in exclude or obj.type != "uri":
            continue
        subjects_by_predicate[predicate].add(subject)

    coverage = {p: len(subs) / total_target_nodes for p, subs in subjects_by_predicate.items()}
    eligible = [p for p, c in coverage.items() if c >= min_coverage]
    eligible.sort(key=lambda p: coverage[p], reverse=True)
    return eligible[:max_properties]


def _collect_candidate_edges(
    triples: list[Triple], relation_names: list[str]
) -> list[tuple[str, str, int]]:
    relation_idx = {p: i for i, p in enumerate(relation_names)}
    edges = []
    for subject, predicate, obj in triples:
        if predicate in relation_idx and obj.type == "uri":
            edges.append((subject, obj.value, relation_idx[predicate]))
    return edges


def _assign_node_indices(
    target_uris: list[str], candidate_edges: list[tuple[str, str, int]]
) -> dict[str, int]:
    """target_classノードにインデックス0..N-1を先に割り当て、以後1-hop隣接ノードを追記する。"""
    uri_to_idx: dict[str, int] = {uri: i for i, uri in enumerate(target_uris)}
    for _subject, obj_uri, _relation in candidate_edges:
        if obj_uri not in uri_to_idx:
            uri_to_idx[obj_uri] = len(uri_to_idx)
    return uri_to_idx


def _build_edge_tensors(
    candidate_edges: list[tuple[str, str, int]],
    uri_to_idx: dict[str, int],
    num_forward_relations: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    """各エッジについて逆方向のリレーションを明示的に追加してテンソル化する。

    R-GCNの標準的な前処理（PyGのEntities(AIFB/MUTAG等)データセットと同じ慣行）。エッジを
    双方向にしないと、対象ノードが1-hop隣接エンティティからのメッセージを一切受け取れない。
    """
    src: list[int] = []
    dst: list[int] = []
    rel: list[int] = []
    for subject_uri, obj_uri, relation in candidate_edges:
        s_idx, o_idx = uri_to_idx[subject_uri], uri_to_idx[obj_uri]
        src.append(s_idx)
        dst.append(o_idx)
        rel.append(relation)
        src.append(o_idx)
        dst.append(s_idx)
        rel.append(relation + num_forward_relations)

    if not src:
        return torch.zeros((2, 0), dtype=torch.long), torch.zeros((0,), dtype=torch.long)
    edge_index = torch.tensor([src, dst], dtype=torch.long)
    edge_type = torch.tensor(rel, dtype=torch.long)
    return edge_index, edge_type


def _structural_features(
    num_nodes: int, edge_index: torch.Tensor, edge_type: torch.Tensor, num_relations: int
) -> torch.Tensor:
    """次数 + リレーションタイプ別隣接数（decision #5の構造特徴）。

    エッジは双方向化済み（`_build_edge_tensors`）のため、各ノードの「リレーションタイプ別
    "出"隣接数」を2R種類について集計するだけで、実質的な入次数・出次数の両方の情報を含む
    （元の有向エッジ(s,o,r)に対して逆エッジ(o,s,r+R)が必ず存在するため）。
    """
    relation_out_count = torch.zeros((num_nodes, num_relations), dtype=torch.float32)
    if edge_index.numel() > 0:
        src = edge_index[0]
        ones = torch.ones(edge_type.shape[0], dtype=torch.float32)
        relation_out_count.index_put_((src, edge_type), ones, accumulate=True)
    degree = relation_out_count.sum(dim=1, keepdim=True)
    return torch.cat([degree, relation_out_count], dim=1)


def _build_node_texts(
    triples: list[Triple], target_uris: list[str], text_properties: set[str]
) -> dict[str, str]:
    """target_classノードについてのみ、`text_properties`のliteral値を連結する。

    1-hop隣接ノード（著者・スキーム等）の文字列特徴は取得しない(1-hop先のプロパティを
    再帰的に取得しない設計上の簡略化。CLAUDE.md決定事項#23)。
    """
    texts: dict[str, list[str]] = defaultdict(list)
    for subject, predicate, obj in triples:
        if predicate in text_properties and obj.type in ("literal", "typed-literal"):
            texts[subject].append(obj.value)
    return {uri: " ".join(texts.get(uri, [])) for uri in target_uris}


def _build_text_vectorizer(vectorizer_kind: str):
    common_kwargs = {"analyzer": "char_wb", "ngram_range": (2, 4)}
    if vectorizer_kind == "hashing":
        return HashingVectorizer(n_features=TEXT_FEATURE_DIM, **common_kwargs)
    if vectorizer_kind == "tfidf":
        return TfidfVectorizer(max_features=TEXT_FEATURE_DIM, **common_kwargs)
    raise ValueError(f"unsupported text_vectorizer: {vectorizer_kind!r}")


def _text_feature_matrix(
    node_order: list[str], node_texts: dict[str, str], vectorizer_kind: str
) -> torch.Tensor:
    """`text_vectorizer`（decision #5: エンドポイントごとに独立学習）でテキスト特徴を作る。

    `analyzer="char_wb"`（文字n-gram）を採用することで、単語分かち書きが無い日本語
    テキストでも、英語・イタリア語・スペイン語と同じコードのままエンドポイント固有の
    if/elseなしに動作する（決定事項#5、アーキテクチャ原則#1）。
    """
    corpus = [node_texts.get(uri, "") for uri in node_order]
    vectorizer = _build_text_vectorizer(vectorizer_kind)
    matrix = vectorizer.fit_transform(corpus)
    return torch.from_numpy(matrix.toarray()).float()


def _split_indices(
    labels: list[str], split: SplitConfig, seed: int
) -> tuple[list[int], list[int], list[int]]:
    """target_classノードをtrain/val/testに分割する。`split.stratify`ならラベル層化。

    層化に必要な最小サンプル数をクラスが満たさない場合（小規模な合成グラフでのテスト等）は
    非層化分割にフォールバックする(警告ログを出す。例外を握りつぶすのではなく、テスト等の
    小規模データでも動作を継続できるようにするための意図的な緩和策)。
    """
    indices = list(range(len(labels)))
    stratify = labels if split.stratify else None
    try:
        train_idx, temp_idx = train_test_split(
            indices, train_size=split.train, stratify=stratify, random_state=seed
        )
    except ValueError as exc:
        logger.warning(
            "stratified train/temp split failed (%s); falling back to a non-stratified split",
            exc,
        )
        train_idx, temp_idx = train_test_split(indices, train_size=split.train, random_state=seed)
        stratify = None

    temp_labels = [labels[i] for i in temp_idx] if stratify is not None else None
    val_share_of_temp = split.val / (split.val + split.test)
    try:
        val_idx, test_idx = train_test_split(
            temp_idx, train_size=val_share_of_temp, stratify=temp_labels, random_state=seed
        )
    except ValueError as exc:
        logger.warning(
            "stratified val/test split failed (%s); falling back to a non-stratified split", exc
        )
        val_idx, test_idx = train_test_split(temp_idx, train_size=val_share_of_temp, random_state=seed)

    return train_idx, val_idx, test_idx


def _mask_from_indices(num_nodes: int, indices: list[int]) -> torch.Tensor:
    mask = torch.zeros(num_nodes, dtype=torch.bool)
    if indices:
        mask[torch.tensor(indices, dtype=torch.long)] = True
    return mask


def build_graph(
    client: SPARQLClient, config: EndpointConfig, labeled_nodes: list[LabeledNode]
) -> tuple[Data, ConversionTiming]:
    """Phase 3で抽出した`labeled_nodes`から`edge_type`付き単一`Data`を構築する。"""
    if not labeled_nodes:
        raise ValueError("labeled_nodes is empty; cannot build a graph")

    sparql_start = time.perf_counter()
    target_uris = [node.uri for node in labeled_nodes]
    triples = _fetch_properties_for_nodes(client, target_uris)
    sparql_seconds = time.perf_counter() - sparql_start

    build_start = time.perf_counter()

    exclude = {config.label.property, RDF_TYPE_URI}
    relation_names = _select_edge_predicates(
        triples,
        total_target_nodes=len(labeled_nodes),
        exclude=exclude,
        min_coverage=config.features.min_coverage,
        max_properties=config.features.max_properties,
    )
    if not relation_names:
        raise ValueError(
            f"no edge-eligible predicates found for target_class={config.target_class!r} "
            f"(min_coverage={config.features.min_coverage}); check features.min_coverage "
            "against the actual discovered schema"
        )
    num_forward_relations = len(relation_names)

    candidate_edges = _collect_candidate_edges(triples, relation_names)
    max_forward_edges = config.sampling.max_edges // 2
    if len(candidate_edges) > max_forward_edges:
        logger.warning(
            "candidate edge count %d exceeds max_edges//2=%d; randomly subsampling with "
            "seed=%d (CLAUDE.md architecture principle #4: memory discipline)",
            len(candidate_edges),
            max_forward_edges,
            config.sampling.seed,
        )
        candidate_edges = random.Random(config.sampling.seed).sample(candidate_edges, max_forward_edges)

    uri_to_idx = _assign_node_indices(target_uris, candidate_edges)
    num_nodes = len(uri_to_idx)
    node_order = [""] * num_nodes
    for uri, idx in uri_to_idx.items():
        node_order[idx] = uri

    edge_index, edge_type = _build_edge_tensors(candidate_edges, uri_to_idx, num_forward_relations)
    num_relations = 2 * num_forward_relations
    all_relation_names = relation_names + [f"{p} (inverse)" for p in relation_names]

    structural = _structural_features(num_nodes, edge_index, edge_type, num_relations)
    node_texts = _build_node_texts(triples, target_uris, set(config.features.text_properties))
    text_features = _text_feature_matrix(node_order, node_texts, config.features.text_vectorizer)
    x = torch.cat([structural, text_features], dim=1)

    label_counts = Counter(node.label for node in labeled_nodes)
    class_names = [label for label, _count in label_counts.most_common()]
    label_to_class_idx = {label: i for i, label in enumerate(class_names)}

    y = torch.full((num_nodes,), -1, dtype=torch.long)
    for node in labeled_nodes:
        y[uri_to_idx[node.uri]] = label_to_class_idx[node.label]

    target_mask = torch.zeros(num_nodes, dtype=torch.bool)
    target_mask[: len(labeled_nodes)] = True

    train_idx, val_idx, test_idx = _split_indices(
        [node.label for node in labeled_nodes], config.split, config.sampling.seed
    )

    data = Data(x=x, edge_index=edge_index, edge_type=edge_type, y=y)
    data.num_relations = num_relations
    data.num_classes = len(class_names)
    data.class_names = class_names
    data.relation_names = all_relation_names
    data.node_uris = node_order
    data.target_mask = target_mask
    data.train_mask = _mask_from_indices(num_nodes, train_idx)
    data.val_mask = _mask_from_indices(num_nodes, val_idx)
    data.test_mask = _mask_from_indices(num_nodes, test_idx)

    build_seconds = time.perf_counter() - build_start
    return data, ConversionTiming(sparql_seconds=sparql_seconds, build_seconds=build_seconds)
