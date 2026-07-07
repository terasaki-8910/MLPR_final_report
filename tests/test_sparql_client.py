import json
import logging

import pytest
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed

from rdf2graph.sparql.client import (
    Binding,
    SPARQLClient,
    SPARQLQueryError,
    SPARQLResponseFormatError,
    SPARQLTimeoutError,
)


class FakeResponse:
    """SPARQLWrapperのQueryResultの代わりに使う、テスト用の最小フェイク。"""

    def __init__(self, payload=None, content_type="application/sparql-results+json", convert_error=None):
        self._payload = payload
        self._content_type = content_type
        self._convert_error = convert_error

    def info(self):
        return {"Content-Type": self._content_type}

    def convert(self):
        if self._convert_error is not None:
            raise self._convert_error
        return self._payload


def make_select_payload(rows: list[dict[str, str]]) -> dict:
    bindings = [{k: {"type": "uri", "value": v} for k, v in row.items()} for row in rows]
    return {"head": {"vars": list(rows[0].keys()) if rows else []}, "results": {"bindings": bindings}}


@pytest.fixture(autouse=True)
def no_real_sleep(mocker):
    """バックオフの実待機をなくし、テストを高速化する。"""
    mocker.patch("rdf2graph.sparql.client.time.sleep")


@pytest.fixture
def mock_wrapper(mocker):
    mock_cls = mocker.patch("rdf2graph.sparql.client.SPARQLWrapper")
    return mock_cls.return_value


def test_cache_hit_avoids_second_network_call(tmp_path, mock_wrapper):
    mock_wrapper.query.return_value = FakeResponse(make_select_payload([{"s": "http://x/1"}]))
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    query = "SELECT ?s WHERE { ?s ?p ?o }"

    result1 = client.query(query)
    result2 = client.query(query)

    assert mock_wrapper.query.call_count == 1
    assert result1 == result2 == [{"s": Binding(value="http://x/1", type="uri")}]


def test_cache_collision_or_corruption_is_detected_and_logged(tmp_path, mock_wrapper, caplog):
    mock_wrapper.query.return_value = FakeResponse(make_select_payload([{"s": "http://x/1"}]))
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    query = "SELECT ?s WHERE { ?s ?p ?o }"

    # 別のクエリ文字列で書き込まれたキャッシュファイルを、要求クエリのキャッシュパスに直接置く
    # （ハッシュ衝突・書き込み破損のいずれもこの経路で検知されることを確認する）。
    cache_path = client._cache_path(query)
    cache_path.write_text(
        json.dumps({"endpoint": client.endpoint, "query": "SOME OTHER QUERY", "result": {}}),
        encoding="utf-8",
    )

    with caplog.at_level(logging.WARNING):
        result = client.query(query)

    assert mock_wrapper.query.call_count == 1  # ミス扱いで再実行された
    assert result == [{"s": Binding(value="http://x/1", type="uri")}]
    assert any("collision" in record.message for record in caplog.records)


def test_paginate_stops_on_short_page_and_logs_warning(tmp_path, mock_wrapper, caplog):
    page1 = make_select_payload([{"s": f"http://x/{i}"} for i in range(3)])
    page2 = make_select_payload([{"s": f"http://x/{i}"} for i in range(3, 5)])  # page_size(3)未満
    mock_wrapper.query.side_effect = [FakeResponse(page1), FakeResponse(page2)]

    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    template = "SELECT ?s WHERE { ?s ?p ?o } LIMIT {limit} OFFSET {offset}"

    with caplog.at_level(logging.WARNING):
        rows = list(client.paginate(template, page_size=3))

    assert [row["s"].value for row in rows] == [f"http://x/{i}" for i in range(5)]
    assert mock_wrapper.query.call_count == 2
    assert any("page_size" in record.message for record in caplog.records)


def test_paginate_respects_max_total(tmp_path, mock_wrapper):
    page1 = make_select_payload([{"s": f"http://x/{i}"} for i in range(3)])
    mock_wrapper.query.return_value = FakeResponse(page1)

    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)
    template = "SELECT ?s WHERE { ?s ?p ?o } LIMIT {limit} OFFSET {offset}"

    rows = list(client.paginate(template, page_size=3, max_total=2))

    assert len(rows) == 2


def test_retry_then_success_logs_warning(tmp_path, mock_wrapper, caplog):
    mock_wrapper.query.side_effect = [
        TimeoutError("simulated network timeout"),
        TimeoutError("simulated network timeout"),
        FakeResponse(make_select_payload([{"s": "http://x/1"}])),
    ]
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path, max_retries=3)

    with caplog.at_level(logging.WARNING):
        result = client.query("SELECT ?s WHERE { ?s ?p ?o }")

    assert result == [{"s": Binding(value="http://x/1", type="uri")}]
    assert mock_wrapper.query.call_count == 3
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(warnings) == 2


def test_max_retries_exceeded_raises_typed_timeout_error(tmp_path, mock_wrapper):
    mock_wrapper.query.side_effect = TimeoutError("simulated network timeout")
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path, max_retries=2)

    with pytest.raises(SPARQLTimeoutError):
        client.query("SELECT ?s WHERE { ?s ?p ?o }")

    assert mock_wrapper.query.call_count == 2


def test_query_bad_formed_raises_query_error_without_retry(tmp_path, mock_wrapper):
    mock_wrapper.query.side_effect = QueryBadFormed("bad syntax")
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path, max_retries=3)

    with pytest.raises(SPARQLQueryError):
        client.query("SELECT ??? malformed")

    assert mock_wrapper.query.call_count == 1


def test_non_json_content_type_raises_typed_format_error(tmp_path, mock_wrapper):
    mock_wrapper.query.return_value = FakeResponse(content_type="text/html; charset=utf-8")
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path, max_retries=3)

    with pytest.raises(SPARQLResponseFormatError):
        client.query("SELECT ?s WHERE { ?s ?p ?o }")

    assert mock_wrapper.query.call_count == 1  # 非一時的エラーなのでリトライされない


def test_undecodable_json_body_raises_typed_format_error(tmp_path, mock_wrapper):
    mock_wrapper.query.return_value = FakeResponse(convert_error=json.JSONDecodeError("bad", "doc", 0))
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path, max_retries=3)

    with pytest.raises(SPARQLResponseFormatError):
        client.query("SELECT ?s WHERE { ?s ?p ?o }")

    assert mock_wrapper.query.call_count == 1


def test_ask_query_returns_bool(tmp_path, mock_wrapper):
    mock_wrapper.query.return_value = FakeResponse({"head": {}, "boolean": True})
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)

    result = client.query("ASK { ?s ?p ?o }")

    assert result is True


def test_default_method_is_get(tmp_path, mock_wrapper):
    mock_wrapper.query.return_value = FakeResponse(make_select_payload([{"s": "http://x/1"}]))
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path)

    client.query("SELECT ?s WHERE { ?s ?p ?o }")

    mock_wrapper.setMethod.assert_called_once_with("GET")


def test_method_can_be_overridden_to_post(tmp_path, mock_wrapper):
    # Phase 4のgraph_builder.pyはVALUES句に多数のURIを埋め込む大きなクエリを送るため、
    # GETのURL長上限を避けてPOSTを使う(CLAUDE.md参照)。
    mock_wrapper.query.return_value = FakeResponse(make_select_payload([{"s": "http://x/1"}]))
    client = SPARQLClient("https://example.org/sparql", cache_dir=tmp_path, method="POST")

    client.query("SELECT ?s WHERE { ?s ?p ?o }")

    mock_wrapper.setMethod.assert_called_once_with("POST")


def test_invalid_method_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="method"):
        SPARQLClient("https://example.org/sparql", cache_dir=tmp_path, method="PATCH")
