import torch

from rdf2graph.convert.graph_builder import build_graph, load_graph, save_graph
from rdf2graph.convert.labels import LabeledNode
from rdf2graph.convert.schema import (
    EndpointConfig,
    FeaturesConfig,
    LabelConfig,
    SamplingConfig,
    SplitConfig,
)
from rdf2graph.sparql.client import Binding, SPARQLClient
from rdf2graph.sparql.profiler import RDF_TYPE_URI

TARGET_CLASS = "http://ex/Thing"
LABEL_PROPERTY = "http://ex/kind"


def _row(s: str, p: str, o_value: str, o_type: str = "uri") -> dict:
    return {
        "s": Binding(value=s, type="uri"),
        "p": Binding(value=p, type="uri"),
        "o": Binding(value=o_value, type=o_type),
    }


def _make_triples(n: int) -> list[dict]:
    rows = []
    for i in range(n):
        s = f"http://ex/thing{i}"
        label = "A" if i < 12 else "B"
        rows.append(_row(s, LABEL_PROPERTY, label))  # ラベル根拠述語(エッジ対象外であるべき)
        rows.append(_row(s, RDF_TYPE_URI, TARGET_CLASS))  # rdf:type(エッジ対象外であるべき)
        rows.append(_row(s, "http://ex/knows", f"http://ex/neighbor{i % 3}"))  # 被覆率100%
        if i % 2 == 0:
            rows.append(_row(s, "http://ex/rare", f"http://ex/rareneighbor{i}"))  # 被覆率50%
        rows.append(_row(s, "http://ex/title", f"Title number {i}", o_type="literal"))
        rows.append(_row(s, "http://ex/bnodeprop", f"_:b{i}", o_type="bnode"))  # エッジ対象外
    return rows


def _config(
    max_nodes: int,
    max_edges: int = 1000,
    min_coverage: float = 0.6,
    max_properties: int = 10,
    text_properties: list[str] | None = None,
) -> EndpointConfig:
    return EndpointConfig(
        endpoint="https://example.org/sparql",
        target_class=TARGET_CLASS,
        sampling=SamplingConfig(max_nodes=max_nodes, max_edges=max_edges, page_size=100, seed=1),
        label=LabelConfig(property=LABEL_PROPERTY, top_k=2, unmatched_policy="drop"),
        features=FeaturesConfig(
            auto_discover=True,
            min_coverage=min_coverage,
            max_properties=max_properties,
            text_properties=text_properties or [],
            text_vectorizer="hashing",
        ),
        split=SplitConfig(train=0.7, val=0.15, test=0.15, stratify=True),
    )


def _labeled_nodes(n: int) -> list[LabeledNode]:
    return [LabeledNode(uri=f"http://ex/thing{i}", label=("A" if i < 12 else "B")) for i in range(n)]


def test_build_graph_excludes_label_and_rdf_type_and_filters_by_coverage(mocker, tmp_path):
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    mocker.patch.object(client, "query", return_value=_make_triples(20))
    labeled_nodes = _labeled_nodes(20)
    config = _config(max_nodes=20, text_properties=["http://ex/title"])

    data, timing = build_graph(client, config, labeled_nodes)

    # ラベルリーク防止(決定事項#23): label.propertyとrdf:typeはエッジに使われない
    assert LABEL_PROPERTY not in data.relation_names
    assert RDF_TYPE_URI not in data.relation_names
    # bnode値の述語はエッジ対象外
    assert "http://ex/bnodeprop" not in data.relation_names
    # 被覆率50%の述語はmin_coverage=0.6未満のため除外される
    assert "http://ex/rare" not in data.relation_names
    # 被覆率100%の述語は採用され、逆方向リレーションも追加される
    assert "http://ex/knows" in data.relation_names
    assert "http://ex/knows (inverse)" in data.relation_names
    assert data.num_relations == 2

    assert data.num_nodes == 20 + 3  # target 20件 + neighbor0/1/2の3件
    assert data.x.shape == (data.num_nodes, 1 + data.num_relations + 128)
    assert data.y.shape[0] == data.num_nodes

    assert data.class_names[0] == "A"  # 多数派(12件)がクラス0
    assert (data.y[:12] == 0).all()
    assert (data.y[12:20] == 1).all()
    assert (data.y[20:] == -1).all()  # 隣接ノードはtarget外(分類対象でない)

    assert int(data.target_mask.sum().item()) == 20
    union = data.train_mask | data.val_mask | data.test_mask
    assert int(union.sum().item()) == 20
    assert not (data.train_mask & data.val_mask).any()
    assert not (data.train_mask & data.test_mask).any()
    assert not (data.val_mask & data.test_mask).any()
    assert not (data.train_mask & ~data.target_mask).any()

    assert timing.sparql_seconds >= 0
    assert timing.build_seconds >= 0


def test_build_graph_subsamples_edges_to_max_edges(mocker, tmp_path):
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    n = 20
    rows = [_row(f"http://ex/thing{i}", "http://ex/knows", f"http://ex/neighbor{i}") for i in range(n)]
    mocker.patch.object(client, "query", return_value=rows)
    labeled_nodes = [LabeledNode(uri=f"http://ex/thing{i}", label="A") for i in range(n)]
    config = _config(max_nodes=n, max_edges=10, min_coverage=0.5)

    data, _ = build_graph(client, config, labeled_nodes)

    assert data.edge_index.shape[1] == 10  # max_edges//2 の順方向 + 同数の逆方向 = max_edges


def test_build_graph_raises_when_no_predicate_meets_coverage(mocker, tmp_path):
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    # label.property/rdf:type(除外対象)とliteral値の述語しか無く、uri値のobject propertyが
    # 一切無い(=coverage判定に乗る候補が最初からゼロの)状況を作る。
    rows = []
    for i in range(20):
        s = f"http://ex/thing{i}"
        rows.append(_row(s, LABEL_PROPERTY, "A" if i < 12 else "B"))
        rows.append(_row(s, RDF_TYPE_URI, TARGET_CLASS))
        rows.append(_row(s, "http://ex/title", f"Title number {i}", o_type="literal"))
    mocker.patch.object(client, "query", return_value=rows)
    labeled_nodes = _labeled_nodes(20)
    config = _config(max_nodes=20, min_coverage=0.1, text_properties=["http://ex/title"])

    import pytest

    with pytest.raises(ValueError, match="no edge-eligible predicates"):
        build_graph(client, config, labeled_nodes)


def test_save_and_load_graph_roundtrip(mocker, tmp_path):
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    mocker.patch.object(client, "query", return_value=_make_triples(10))
    labeled_nodes = [LabeledNode(uri=f"http://ex/thing{i}", label=("A" if i < 6 else "B")) for i in range(10)]
    config = _config(max_nodes=10, text_properties=["http://ex/title"])

    data, _ = build_graph(client, config, labeled_nodes)
    path = tmp_path / "graph.pt"
    save_graph(data, path)
    loaded = load_graph(path)

    assert torch.equal(loaded.x, data.x)
    assert torch.equal(loaded.edge_index, data.edge_index)
    assert torch.equal(loaded.edge_type, data.edge_type)
    assert loaded.class_names == data.class_names
    assert loaded.relation_names == data.relation_names
