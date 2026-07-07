"""SPARQLエンドポイントへの問い合わせを担うクライアント。

キャッシュ・リトライ・バックオフ・応答形式検証を一箇所に集約する
（CLAUDE.md アーキテクチャ原則#2「すべての外部呼び出しはキャッシュ必須」、
#3「SPARQLは安全側に倒す」、#6「例外を握りつぶさない」への対応）。

query()はSELECT系ならBindingの行リスト、ASK系ならboolを返す。paginate()は
query()を介して1ページずつ取得するだけで独自のパース処理を持たないため、
両者は必ず同じ経路（_parse_bindings）でSPARQL JSONを解釈する。
"""
import hashlib
import json
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from SPARQLWrapper import GET, JSON, POST, SPARQLWrapper
from SPARQLWrapper.SPARQLExceptions import (
    EndPointNotFound,
    QueryBadFormed,
    URITooLong,
    Unauthorized,
)

from rdf2graph.sparql.query_builder import int_literal
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

# クエリ内容そのものに起因し、リトライしても解決しないエラー群。
_NON_RETRYABLE_QUERY_ERRORS = (QueryBadFormed, Unauthorized, EndPointNotFound, URITooLong)


@dataclass(frozen=True)
class Binding:
    """SPARQL JSON結果の1行・1変数分の値。"""

    value: str
    type: str  # "uri" | "literal" | "bnode"
    datatype: str | None = None
    lang: str | None = None


class SPARQLClientError(Exception):
    """SPARQLClientが送出する例外の基底クラス。"""


class SPARQLTimeoutError(SPARQLClientError):
    """max_retries回リトライしても、タイムアウト・ネットワークエラー・5xxが解消しなかった場合。"""


class SPARQLQueryError(SPARQLClientError):
    """4xx等、クエリ・認証・エンドポイントURLに起因しリトライしても解決しないエラー。"""


class SPARQLResponseFormatError(SPARQLClientError):
    """応答がapplication/sparql-results+json系でない、またはJSONとして解釈できない場合。

    実際に「200 OKだがHTML/WAFのブロックページが返る」エンドポイントに遭遇した経験に基づく。
    """


def _content_type_of(info) -> str:
    """レスポンスヘッダからContent-Typeを取り出す。

    SPARQLWrapperの``QueryResult.info()``はKeyCaseInsensitiveDictを返すが、このクラスは
    ``__getitem__``（ブラケットアクセス）はキーを小文字化して比較する一方、``dict.get()``は
    オーバーライドされておらず大文字小文字を区別してしまう（実機のDBLP等4エンドポイント全てで
    ``.get("Content-Type", ...)``がヒットせず空文字を返す不具合を実際に踏んだ）。
    そのためここではブラケットアクセスのみを使う。
    """
    if info is None:
        return ""
    for key in ("content-type", "Content-Type"):
        try:
            return info[key]
        except KeyError:
            continue
    return ""


class SPARQLClient:
    """SPARQLエンドポイントへの問い合わせをキャッシュ・リトライ付きで実行する。"""

    def __init__(
        self,
        endpoint: str,
        cache_dir: Path,
        timeout: float = 60.0,
        max_retries: int = 3,
        backoff_base: float = 2.0,
        method: str = GET,
    ) -> None:
        if method not in (GET, POST):
            raise ValueError(f"method must be {GET!r} or {POST!r}, got {method!r}")
        self.endpoint = endpoint
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        # 既定はGET(Phase1からの既存動作を変えない)。Phase 4のgraph_builder.pyはVALUES句に
        # 多数のURIを埋め込む大きなクエリを送るため、GETのURL長上限（SPARQLWrapperの
        # URITooLong）を避けるためPOSTを明示的に指定して構築する。
        self.method = method

    def query(self, query: str) -> list[dict[str, Binding]] | bool:
        """SELECT系はBindingの行リスト、ASK系はboolを返す。"""
        raw = self._execute(query)
        if "boolean" in raw:
            return bool(raw["boolean"])
        if "results" in raw:
            return self._parse_bindings(raw)
        raise SPARQLResponseFormatError(
            f"unrecognized SPARQL JSON response shape from {self.endpoint}: "
            f"keys={list(raw.keys())}"
        )

    def paginate(
        self, query_template: str, page_size: int, max_total: int | None = None
    ) -> Iterator[dict[str, Binding]]:
        """``{limit}``/``{offset}``プレースホルダを含むSELECTテンプレートから1行ずつyieldする。

        query_templateはPythonの``str.format``ではなく単純な文字列置換で埋め込む。SPARQLの
        グラフパターンは``{ ?s ?p ?o }``のように波括弧を多用するため、``str.format``を使うと
        テンプレート中の無関係な波括弧まで置換対象と解釈されてしまうため。
        """
        offset = 0
        yielded = 0
        while max_total is None or yielded < max_total:
            page_query = query_template.replace("{limit}", int_literal(page_size)).replace(
                "{offset}", int_literal(offset)
            )
            rows = self.query(page_query)
            if not isinstance(rows, list):
                raise SPARQLResponseFormatError(
                    "paginate() requires a SELECT-shaped query_template, but got an "
                    "ASK-shaped (boolean) response"
                )
            for row in rows:
                if max_total is not None and yielded >= max_total:
                    return
                yield row
                yielded += 1
            if len(rows) < page_size:
                logger.warning(
                    "paginate(): page at offset=%d returned %d rows (< page_size=%d); "
                    "treating this as end-of-data. NOTE: some triplestores silently cap "
                    "result windows below the requested LIMIT, which looks identical from "
                    "here -- this is a known, unresolved limitation (see docs/endpoint_status.md).",
                    offset,
                    len(rows),
                    page_size,
                )
                return
            offset += page_size

    def _cache_path(self, query: str) -> Path:
        digest = hashlib.sha256(f"{self.endpoint}\n{query}".encode("utf-8")).hexdigest()[:16]
        return self.cache_dir / f"{digest}.json"

    def _execute(self, query: str) -> dict:
        cache_path = self._cache_path(query)
        cached = self._read_cache(cache_path, query)
        if cached is not None:
            logger.debug("cache hit for query (%s)", cache_path.name)
            return cached

        raw = self._execute_with_retry(query)
        self._write_cache(cache_path, query, raw)
        return raw

    def _read_cache(self, cache_path: Path, query: str) -> dict | None:
        if not cache_path.exists():
            return None
        try:
            entry = json.loads(cache_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("cache file %s is unreadable/corrupt (%s); treating as miss", cache_path, exc)
            return None
        if entry.get("endpoint") != self.endpoint or entry.get("query") != query:
            logger.warning(
                "cache key collision or corruption detected at %s (stored query does not "
                "match the requested query); treating as a cache miss and re-executing",
                cache_path,
            )
            return None
        return entry["result"]

    def _write_cache(self, cache_path: Path, query: str, result: dict) -> None:
        entry = {"endpoint": self.endpoint, "query": query, "result": result}
        cache_path.write_text(json.dumps(entry), encoding="utf-8")

    def _execute_with_retry(self, query: str) -> dict:
        last_exc: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self._http_execute(query)
            except (SPARQLQueryError, SPARQLResponseFormatError):
                raise  # 非一時的なエラーはリトライしない
            except Exception as exc:  # ネットワークエラー・タイムアウト・5xx相当
                last_exc = exc
                if attempt == self.max_retries:
                    break
                self._backoff_and_warn(attempt, exc)
        raise SPARQLTimeoutError(
            f"giving up after {self.max_retries} attempts against {self.endpoint}: {last_exc}"
        ) from last_exc

    def _backoff_and_warn(self, attempt: int, exc: Exception) -> None:
        delay = self.backoff_base ** (attempt - 1)
        logger.warning(
            "SPARQL request to %s failed (attempt %d/%d): %s -- retrying in %.1fs",
            self.endpoint,
            attempt,
            self.max_retries,
            exc,
            delay,
        )
        time.sleep(delay)

    def _http_execute(self, query: str) -> dict:
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        sparql.setTimeout(int(self.timeout))
        sparql.setMethod(self.method)
        try:
            response = sparql.query()
        except _NON_RETRYABLE_QUERY_ERRORS as exc:
            raise SPARQLQueryError(f"query rejected by {self.endpoint}: {exc}") from exc

        content_type = _content_type_of(response.info())
        if "json" not in content_type.lower():
            raise SPARQLResponseFormatError(
                f"expected a JSON response from {self.endpoint}, got Content-Type={content_type!r}"
            )

        try:
            return response.convert()
        except ValueError as exc:  # json.JSONDecodeError is a ValueError subclass
            raise SPARQLResponseFormatError(
                f"response body from {self.endpoint} was not valid JSON: {exc}"
            ) from exc

    @staticmethod
    def _parse_bindings(raw: dict) -> list[dict[str, "Binding"]]:
        """``results.bindings``をBindingの行リストに変換する唯一の場所。"""
        rows = []
        for binding in raw["results"]["bindings"]:
            row = {
                var: Binding(
                    value=info["value"],
                    type=info["type"],
                    datatype=info.get("datatype"),
                    lang=info.get("xml:lang"),
                )
                for var, info in binding.items()
            }
            rows.append(row)
        return rows
