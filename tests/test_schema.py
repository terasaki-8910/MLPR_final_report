import textwrap
from pathlib import Path

import pytest

from rdf2graph.convert.schema import ConfigError, load_config

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_load_config_parses_dblp_yaml():
    config = load_config(REPO_ROOT / "configs" / "dblp.yaml")

    assert config.endpoint == "https://sparql.dblp.org/sparql"
    assert config.target_class == "https://dblp.org/rdf/schema#Publication"
    assert config.sampling.max_nodes == 15000
    assert config.sampling.max_edges == 100000
    assert config.label.property == "https://dblp.org/rdf/schema#bibtexType"
    assert config.label.top_k == 5
    assert config.label.unmatched_policy == "drop"
    assert config.features.text_properties == ["https://dblp.org/rdf/schema#title"]
    assert config.features.text_vectorizer == "hashing"
    assert config.split.train == pytest.approx(0.7)
    assert config.split.stratify is True


def test_load_config_parses_ndl_authorities_yaml():
    config = load_config(REPO_ROOT / "configs" / "ndl_authorities.yaml")

    assert config.target_class == "http://www.w3.org/2004/02/skos/core#Concept"
    assert config.label.property == "http://www.w3.org/2004/02/skos/core#inScheme"
    assert config.sampling.page_size == 1000  # 決定事項#14: NDLのresult cap実証値


def _write(tmp_path: Path, body: str) -> Path:
    bad = tmp_path / "config.yaml"
    bad.write_text(textwrap.dedent(body), encoding="utf-8")
    return bad


_VALID_BODY = """\
    endpoint: "https://example.org/sparql"
    target_class: "http://example.org/Thing"
    sampling: {{max_nodes: 10, max_edges: 10, page_size: 10, seed: 1}}
    label: {{property: "http://example.org/p", top_k: 2, unmatched_policy: "{unmatched_policy}"}}
    features: {{auto_discover: true, min_coverage: 0.3, max_properties: 5, text_properties: [], text_vectorizer: "{vectorizer}"}}
    split: {{train: {train}, val: {val}, test: {test}, stratify: true}}
"""


def test_load_config_rejects_missing_key(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text('endpoint: "https://example.org/sparql"\n', encoding="utf-8")

    with pytest.raises(ConfigError, match="target_class"):
        load_config(bad)


def test_load_config_rejects_non_mapping_yaml(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- just\n- a\n- list\n", encoding="utf-8")

    with pytest.raises(ConfigError, match="mapping"):
        load_config(bad)


def test_load_config_rejects_bad_split_sum(tmp_path):
    bad = _write(
        tmp_path,
        _VALID_BODY.format(unmatched_policy="drop", vectorizer="hashing", train=0.5, val=0.3, test=0.3),
    )

    with pytest.raises(ConfigError, match="sum to 1.0"):
        load_config(bad)


def test_load_config_rejects_unknown_unmatched_policy(tmp_path):
    bad = _write(
        tmp_path,
        _VALID_BODY.format(unmatched_policy="explode", vectorizer="hashing", train=0.7, val=0.15, test=0.15),
    )

    with pytest.raises(ConfigError, match="unmatched_policy"):
        load_config(bad)


def test_load_config_rejects_unknown_text_vectorizer(tmp_path):
    bad = _write(
        tmp_path,
        _VALID_BODY.format(unmatched_policy="drop", vectorizer="word2vec", train=0.7, val=0.15, test=0.15),
    )

    with pytest.raises(ConfigError, match="text_vectorizer"):
        load_config(bad)


def test_load_config_accepts_other_unmatched_policy(tmp_path):
    ok = _write(
        tmp_path,
        _VALID_BODY.format(unmatched_policy="other", vectorizer="tfidf", train=0.7, val=0.15, test=0.15),
    )

    config = load_config(ok)

    assert config.label.unmatched_policy == "other"
    assert config.features.text_vectorizer == "tfidf"
