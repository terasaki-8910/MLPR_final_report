import pytest

import rdf2graph.convert.labels as labels_module
from rdf2graph.convert.labels import (
    _allocate_per_class,
    assign_label,
    extract_labeled_nodes,
)
from rdf2graph.convert.schema import (
    EndpointConfig,
    FeaturesConfig,
    LabelConfig,
    SamplingConfig,
    SplitConfig,
)
from rdf2graph.sparql.client import Binding, SPARQLClient
from rdf2graph.sparql.profiler import ValueCount


def _uri(value: str) -> Binding:
    return Binding(value=value, type="uri")


@pytest.fixture
def client(tmp_path):
    return SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)


def _config(max_nodes: int = 10, top_k: int = 2, unmatched_policy: str = "drop") -> EndpointConfig:
    return EndpointConfig(
        endpoint="https://example.org/sparql",
        target_class="http://example.org/Thing",
        sampling=SamplingConfig(max_nodes=max_nodes, max_edges=100, page_size=100, seed=1),
        label=LabelConfig(
            property="http://example.org/kind", top_k=top_k, unmatched_policy=unmatched_policy
        ),
        features=FeaturesConfig(
            auto_discover=True,
            min_coverage=0.3,
            max_properties=10,
            text_properties=[],
            text_vectorizer="hashing",
        ),
        split=SplitConfig(train=0.7, val=0.15, test=0.15, stratify=True),
    )


def test_assign_label_picks_first_match_in_frequency_order():
    # ノードがA, Bの両方の値を持つ(多値)場合、頻度上位(ranked_candidatesの先頭)を優先する。
    assert assign_label(["B", "A"], ranked_candidates=["A", "B"]) == "A"


def test_assign_label_returns_none_when_no_match():
    assert assign_label(["C"], ranked_candidates=["A", "B"]) is None


def test_allocate_per_class_is_proportional_to_true_counts():
    values = [
        ValueCount(value="A", value_type="uri", count=80),
        ValueCount(value="B", value_type="uri", count=20),
    ]

    allocation = _allocate_per_class(values, max_nodes=10)

    assert allocation == {"A": 8, "B": 2}


def test_allocate_per_class_puts_rounding_remainder_on_largest_stratum():
    values = [
        ValueCount(value="A", value_type="uri", count=1),
        ValueCount(value="B", value_type="uri", count=1),
        ValueCount(value="C", value_type="uri", count=1),
    ]

    allocation = _allocate_per_class(values, max_nodes=10)

    assert sum(allocation.values()) == 10
    assert allocation["A"] >= allocation["B"] == allocation["C"]


def test_extract_labeled_nodes_stratifies_by_true_proportion(client, mocker):
    label_values = [
        ValueCount(value="http://ex/A", value_type="uri", count=80),
        ValueCount(value="http://ex/B", value_type="uri", count=20),
    ]
    mocker.patch.object(labels_module, "count_label_values", return_value=label_values)

    def fake_query(query):
        if "http://ex/A" in query:
            return [{"s": _uri(f"http://ex/a{i}")} for i in range(8)]
        if "http://ex/B" in query:
            return [{"s": _uri(f"http://ex/b{i}")} for i in range(2)]
        raise AssertionError(f"unexpected query: {query}")

    mocker.patch.object(client, "query", side_effect=fake_query)

    result = extract_labeled_nodes(client, _config(max_nodes=10, top_k=2))

    assert len(result.nodes) == 10
    assert result.actual_per_class == {"http://ex/A": 8, "http://ex/B": 2}
    assert result.duplicate_count == 0


def test_extract_labeled_nodes_resolves_cross_stratum_duplicate_by_frequency(client, mocker):
    label_values = [
        ValueCount(value="http://ex/A", value_type="uri", count=80),
        ValueCount(value="http://ex/B", value_type="uri", count=20),
    ]
    mocker.patch.object(labels_module, "count_label_values", return_value=label_values)

    def fake_query(query):
        if "http://ex/A" in query:
            return [{"s": _uri("http://ex/shared")}] + [
                {"s": _uri(f"http://ex/a{i}")} for i in range(7)
            ]
        if "http://ex/B" in query:
            return [{"s": _uri("http://ex/shared")}, {"s": _uri("http://ex/b0")}]
        raise AssertionError(f"unexpected query: {query}")

    mocker.patch.object(client, "query", side_effect=fake_query)

    result = extract_labeled_nodes(client, _config(max_nodes=10, top_k=2))

    shared = next(n for n in result.nodes if n.uri == "http://ex/shared")
    assert shared.label == "http://ex/A"  # 頻度上位の層を優先(assign_labelと同じ規則)
    assert result.duplicate_count == 1


def test_extract_labeled_nodes_rejects_unimplemented_unmatched_policy(client):
    with pytest.raises(NotImplementedError, match="other"):
        extract_labeled_nodes(client, _config(unmatched_policy="other"))


def test_extract_labeled_nodes_raises_on_empty_census(client, mocker):
    mocker.patch.object(labels_module, "count_label_values", return_value=[])

    with pytest.raises(ValueError, match="no rows"):
        extract_labeled_nodes(client, _config())
