import pytest

from rdf2graph.sparql.client import Binding, SPARQLClient
from rdf2graph.sparql.profiler import (
    ClassCandidate,
    PredicateProfile,
    discover_classes,
    profile_predicates,
    render_profile_markdown,
    suggest_feature_candidates,
    suggest_label_candidates,
)


def _uri(value: str) -> Binding:
    return Binding(value=value, type="uri")


def _literal(value: str) -> Binding:
    return Binding(value=value, type="literal")


@pytest.fixture
def client(tmp_path):
    return SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)


def test_discover_classes_parses_rows_in_order(client, mocker):
    rows = [
        {"class": _uri("http://example.org/Paper"), "count": _literal("1234")},
        {"class": _uri("http://example.org/Author"), "count": _literal("42")},
    ]
    mocker.patch.object(client, "query", return_value=rows)

    candidates = discover_classes(client, limit=20)

    assert candidates == [
        ClassCandidate(class_uri="http://example.org/Paper", count=1234, suspicious=False, note=""),
        ClassCandidate(class_uri="http://example.org/Author", count=42, suspicious=False, note=""),
    ]


def test_discover_classes_flags_suspiciously_round_counts(client, mocker):
    rows = [
        {"class": _uri("http://example.org/Thing"), "count": _literal("1000")},
    ]
    mocker.patch.object(client, "query", return_value=rows)

    candidates = discover_classes(client)

    assert candidates[0].suspicious is True
    assert "cap" in candidates[0].note


def test_discover_classes_does_not_flag_ordinary_counts(client, mocker):
    rows = [{"class": _uri("http://example.org/Thing"), "count": _literal("1234")}]
    mocker.patch.object(client, "query", return_value=rows)

    candidates = discover_classes(client)

    assert candidates[0].suspicious is False


def test_profile_predicates_computes_coverage_and_multivalue(client, mocker):
    # 3件のインスタンスをサンプリングしたと仮定:
    #  - s1: title(1件), author(2件, 多値)
    #  - s2: title(1件)
    #  - s3: authorのみ持たない(titleすら持たない、被覆率が下がる想定)
    rows = [
        {"s": _uri("http://ex/s1"), "p": _uri("http://ex/title"), "o": _literal("Paper A")},
        {"s": _uri("http://ex/s1"), "p": _uri("http://ex/author"), "o": _uri("http://ex/authorA")},
        {"s": _uri("http://ex/s1"), "p": _uri("http://ex/author"), "o": _uri("http://ex/authorB")},
        {"s": _uri("http://ex/s2"), "p": _uri("http://ex/title"), "o": _literal("Paper B")},
        {"s": _uri("http://ex/s3"), "p": _uri("http://ex/type"), "o": _uri("http://ex/Paper")},
    ]
    mocker.patch.object(client, "query", return_value=rows)

    profile = profile_predicates(client, "http://ex/Paper", sample_size=3)

    assert profile.sample_size == 3
    by_pred = {p.predicate_uri: p for p in profile.predicates}
    assert by_pred["http://ex/title"].coverage == pytest.approx(2 / 3)
    assert by_pred["http://ex/title"].is_multivalued is False
    assert by_pred["http://ex/author"].coverage == pytest.approx(1 / 3)
    assert by_pred["http://ex/author"].is_multivalued is True
    assert by_pred["http://ex/author"].value_types == {"uri": 2}
    # 被覆率の高い順にソートされている
    assert profile.predicates[0].coverage >= profile.predicates[-1].coverage


def test_profile_predicates_handles_empty_sample(client, mocker):
    mocker.patch.object(client, "query", return_value=[])

    profile = profile_predicates(client, "http://ex/Nothing", sample_size=10)

    assert profile.sample_size == 0
    assert profile.predicates == []


def test_suggest_label_candidates_prefers_name_hinted_predicates():
    predicates = [
        PredicateProfile(
            predicate_uri="http://ex/dblp-id",
            coverage=0.9,
            is_multivalued=False,
            value_types={"literal": 90},
        ),
        PredicateProfile(
            predicate_uri="http://ex/title",
            coverage=0.85,
            is_multivalued=False,
            value_types={"literal": 85},
        ),
        PredicateProfile(
            predicate_uri="http://ex/rarely-set",
            coverage=0.1,
            is_multivalued=False,
            value_types={"literal": 10},
        ),
    ]

    candidates = suggest_label_candidates(predicates, min_coverage=0.5)

    assert [p.predicate_uri for p in candidates] == ["http://ex/title", "http://ex/dblp-id"]


def test_suggest_feature_candidates_filters_by_min_coverage():
    predicates = [
        PredicateProfile("http://ex/a", coverage=0.5, is_multivalued=False, value_types={"literal": 5}),
        PredicateProfile("http://ex/b", coverage=0.1, is_multivalued=False, value_types={"literal": 1}),
    ]

    candidates = suggest_feature_candidates(predicates, min_coverage=0.30)

    assert [p.predicate_uri for p in candidates] == ["http://ex/a"]


def test_render_profile_markdown_includes_required_sections():
    candidates = [ClassCandidate(class_uri="http://ex/Paper", count=100)]
    from rdf2graph.sparql.profiler import ClassProfile

    profile = ClassProfile(
        class_candidate=candidates[0],
        sample_size=10,
        predicates=[
            PredicateProfile("http://ex/title", coverage=0.9, is_multivalued=False, value_types={"literal": 9}),
        ],
    )

    markdown = render_profile_markdown(
        endpoint_name="Test Endpoint",
        endpoint_url="https://example.org/sparql",
        class_candidates=candidates,
        class_profiles=[profile],
        requested_class_limit=20,
    )

    assert "主要クラス候補" in markdown
    assert "ラベル候補プロパティ" in markdown
    assert "特徴量候補プロパティ" in markdown
    assert "http://ex/Paper" in markdown
    assert "http://ex/title" in markdown


def test_render_profile_markdown_warns_when_fewer_classes_than_requested():
    markdown = render_profile_markdown(
        endpoint_name="Test Endpoint",
        endpoint_url="https://example.org/sparql",
        class_candidates=[ClassCandidate(class_uri="http://ex/OnlyOne", count=5)],
        class_profiles=[],
        requested_class_limit=20,
    )

    assert "1件のみ" in markdown
