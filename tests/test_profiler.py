import pytest

from rdf2graph.sparql.client import Binding, SPARQLClient
from rdf2graph.sparql.profiler import (
    ClassCandidate,
    ClassProfile,
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
    rows = [{"class": _uri("http://example.org/Thing"), "count": _literal("1000")}]
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


def test_profile_predicates_uses_total_instance_count_when_given(client, mocker):
    rows = [{"s": _uri("http://ex/s1"), "p": _uri("http://ex/title"), "o": _literal("Paper A")}]
    mocker.patch.object(client, "query", return_value=rows)

    profile = profile_predicates(client, "http://ex/Paper", sample_size=1, total_instance_count=8_625_948)

    assert profile.class_candidate.count == 8_625_948
    assert profile.sample_size == 1


def test_profile_predicates_computes_cardinality_for_free_text_predicate(client, mocker):
    # 5件のインスタンス全てが異なるタイトルを持つ -> カーディナリティ比 = 1.0 (分類ラベル不適)
    rows = [
        {"s": _uri(f"http://ex/s{i}"), "p": _uri("http://ex/title"), "o": _literal(f"Unique Title {i}")}
        for i in range(5)
    ]
    mocker.patch.object(client, "query", return_value=rows)

    profile = profile_predicates(client, "http://ex/Paper", sample_size=5)

    title = profile.predicates[0]
    assert title.distinct_value_basis == "literal"
    assert title.distinct_value_count == 5
    assert title.label_cardinality_ratio == pytest.approx(1.0)


def test_profile_predicates_computes_low_cardinality_for_closed_set_predicate(client, mocker):
    # 10件のインスタンスが2種類のスキームURIのいずれかを持つ -> カーディナリティ比が低い
    rows = []
    for i in range(10):
        scheme = "http://ex/scheme/A" if i % 2 == 0 else "http://ex/scheme/B"
        rows.append({"s": _uri(f"http://ex/s{i}"), "p": _uri("http://ex/inScheme"), "o": _uri(scheme)})
    mocker.patch.object(client, "query", return_value=rows)

    profile = profile_predicates(client, "http://ex/Concept", sample_size=10)

    in_scheme = profile.predicates[0]
    assert in_scheme.distinct_value_basis == "uri"
    assert in_scheme.distinct_value_count == 2
    assert in_scheme.label_cardinality_ratio == pytest.approx(2 / 10)
    assert in_scheme.value_histogram == {"http://ex/scheme/A": 5, "http://ex/scheme/B": 5}


def test_profile_predicates_mixed_literal_and_uri_uses_literal_only(client, mocker):
    # dc:subjectのような述語がliteral(主題語)とuri(人物リンク)を同居させているケース。
    # literal側だけがカーディナリティ判定の対象になるべき。
    rows = [
        {"s": _uri("http://ex/s1"), "p": _uri("http://ex/subject"), "o": _literal("History")},
        {"s": _uri("http://ex/s2"), "p": _uri("http://ex/subject"), "o": _literal("History")},
        {"s": _uri("http://ex/s3"), "p": _uri("http://ex/subject"), "o": _literal("Law")},
        {"s": _uri("http://ex/s1"), "p": _uri("http://ex/subject"), "o": _uri("http://ex/person/1")},
    ]
    mocker.patch.object(client, "query", return_value=rows)

    profile = profile_predicates(client, "http://ex/Work", sample_size=3)

    subject = profile.predicates[0]
    assert subject.distinct_value_basis == "literal"
    assert subject.distinct_value_count == 2  # "History", "Law" のみ(uriの人物リンクは除外)
    assert subject.value_histogram == {"History": 2, "Law": 1}


def test_profile_predicates_bnode_only_predicate_has_no_cardinality(client, mocker):
    rows = [
        {
            "s": _uri("http://ex/s1"),
            "p": _uri("http://ex/altLabel"),
            "o": Binding(value="_:b1", type="bnode"),
        }
    ]
    mocker.patch.object(client, "query", return_value=rows)

    profile = profile_predicates(client, "http://ex/Concept", sample_size=1)

    alt_label = profile.predicates[0]
    assert alt_label.distinct_value_basis == "none"
    assert alt_label.label_cardinality_ratio is None


def test_suggest_label_candidates_excludes_high_cardinality_free_text():
    predicates = [
        PredicateProfile(
            predicate_uri="http://ex/title",
            coverage=0.9,
            is_multivalued=False,
            covered_subject_count=90,
            distinct_value_basis="literal",
            distinct_value_count=90,
            label_cardinality_ratio=1.0,
        ),
        PredicateProfile(
            predicate_uri="http://ex/inScheme",
            coverage=0.95,
            is_multivalued=False,
            covered_subject_count=95,
            distinct_value_basis="uri",
            distinct_value_count=3,
            label_cardinality_ratio=3 / 95,
        ),
    ]

    candidates = suggest_label_candidates(predicates)

    assert [p.predicate_uri for p in candidates] == ["http://ex/inScheme"]


def test_suggest_label_candidates_excludes_constant_single_value_predicate():
    # dc:terms:createdが全インスタンスで同一値(例: 収集日時スタンプ)を持つ場合、
    # カーディナリティ比は最小(0に近い)になるが、分類ラベルとしては無意味なので除外されるべき。
    constant_valued = PredicateProfile(
        "http://ex/harvestedAt",
        coverage=1.0,
        is_multivalued=False,
        covered_subject_count=200,
        distinct_value_basis="literal",
        distinct_value_count=1,
        label_cardinality_ratio=1 / 200,
    )
    real_category = PredicateProfile(
        "http://ex/genre",
        coverage=0.8,
        is_multivalued=False,
        covered_subject_count=160,
        distinct_value_basis="uri",
        distinct_value_count=4,
        label_cardinality_ratio=4 / 160,
    )

    candidates = suggest_label_candidates([constant_valued, real_category])

    assert [p.predicate_uri for p in candidates] == ["http://ex/genre"]


def test_suggest_label_candidates_ignores_predicates_with_no_cardinality():
    predicates = [
        PredicateProfile(
            predicate_uri="http://ex/altLabel",
            coverage=0.9,
            is_multivalued=True,
            covered_subject_count=90,
            distinct_value_basis="none",
            distinct_value_count=0,
            label_cardinality_ratio=None,
        ),
    ]

    assert suggest_label_candidates(predicates) == []


def test_suggest_label_candidates_sorts_by_cardinality_ratio_ascending():
    high_cardinality = PredicateProfile(
        "http://ex/loose",
        coverage=0.9,
        is_multivalued=False,
        covered_subject_count=100,
        distinct_value_basis="uri",
        distinct_value_count=40,
        label_cardinality_ratio=0.4,
    )
    low_cardinality = PredicateProfile(
        "http://ex/tight",
        coverage=0.6,
        is_multivalued=False,
        covered_subject_count=100,
        distinct_value_basis="uri",
        distinct_value_count=5,
        label_cardinality_ratio=0.05,
    )

    candidates = suggest_label_candidates([high_cardinality, low_cardinality])

    assert [p.predicate_uri for p in candidates] == ["http://ex/tight", "http://ex/loose"]


def test_suggest_feature_candidates_filters_by_min_coverage():
    predicates = [
        PredicateProfile("http://ex/a", coverage=0.5, is_multivalued=False, value_types={"literal": 5}),
        PredicateProfile("http://ex/b", coverage=0.1, is_multivalued=False, value_types={"literal": 1}),
    ]

    candidates = suggest_feature_candidates(predicates, min_coverage=0.30)

    assert [p.predicate_uri for p in candidates] == ["http://ex/a"]


def test_render_profile_markdown_includes_required_sections():
    candidates = [ClassCandidate(class_uri="http://ex/Paper", count=100)]
    profile = ClassProfile(
        class_candidate=candidates[0],
        sample_size=10,
        predicates=[
            PredicateProfile(
                "http://ex/title",
                coverage=0.9,
                is_multivalued=False,
                value_types={"literal": 9},
                covered_subject_count=9,
                distinct_value_basis="literal",
                distinct_value_count=9,
                label_cardinality_ratio=1.0,
            ),
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
    assert "全体 100 件中 10 件をサンプリング" in markdown


def test_render_profile_markdown_warns_when_fewer_classes_than_requested():
    markdown = render_profile_markdown(
        endpoint_name="Test Endpoint",
        endpoint_url="https://example.org/sparql",
        class_candidates=[ClassCandidate(class_uri="http://ex/OnlyOne", count=5)],
        class_profiles=[],
        requested_class_limit=20,
    )

    assert "1件のみ" in markdown


def test_render_profile_markdown_flags_multivalued_rdf_type_as_subtype_hypothesis():
    from rdf2graph.sparql.profiler import RDF_TYPE_URI

    candidates = [ClassCandidate(class_uri="http://ex/Publication", count=8_625_948)]
    profile = ClassProfile(
        class_candidate=candidates[0],
        sample_size=200,
        predicates=[
            PredicateProfile(
                RDF_TYPE_URI,
                coverage=1.0,
                is_multivalued=True,
                value_types={"uri": 400},
                covered_subject_count=200,
                distinct_value_basis="uri",
                distinct_value_count=2,
                label_cardinality_ratio=2 / 200,
                value_histogram={"http://ex/Inproceedings": 120, "http://ex/Article": 80},
            ),
        ],
    )

    markdown = render_profile_markdown(
        endpoint_name="Test Endpoint",
        endpoint_url="https://example.org/sparql",
        class_candidates=candidates,
        class_profiles=[profile],
        requested_class_limit=20,
    )

    assert "サブタイプ由来のラベル候補" in markdown
    assert "http://ex/Inproceedings" in markdown
