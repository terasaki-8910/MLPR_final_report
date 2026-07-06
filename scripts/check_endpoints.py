"""対象4エンドポイントへの疎通確認スクリプト。

実エンドポイントへの依存があるため tests/ には含めず、ここに分離する
（build-lod-project.md Phase 1 の方針）。`python scripts/check_endpoints.py` として実行し、
結果を docs/endpoint_status.md に書き出す。
"""
import tempfile
import time
from pathlib import Path

from rdf2graph.sparql.client import SPARQLClient, SPARQLClientError
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

ENDPOINTS = {
    "DBLP": "https://sparql.dblp.org/sparql",
    "NDL Web NDL Authorities": "https://id.ndl.go.jp/auth/ndla/sparql",
    "ICCU SBN": "https://triplestore.iccu.sbn.it/sparql",
    "Cervantes Virtual": "https://data.cervantesvirtual.com/sparql",
}

LARGE_LIMIT = 5000


def check_ask(client: SPARQLClient) -> tuple[bool, float, str]:
    start = time.perf_counter()
    try:
        result = client.query("ASK { ?s ?p ?o }")
        return True, time.perf_counter() - start, f"ASK -> {result}"
    except SPARQLClientError as exc:
        return False, time.perf_counter() - start, f"ASK failed: {exc}"


def check_large_limit(client: SPARQLClient) -> tuple[bool, float, str]:
    """意図的に大きいLIMITを投げ、サーバー側の無言のresult capを実地確認する（指摘#5対応）。"""
    query = f"SELECT * WHERE {{ ?s ?p ?o }} LIMIT {LARGE_LIMIT}"
    start = time.perf_counter()
    try:
        rows = client.query(query)
        elapsed = time.perf_counter() - start
        count = len(rows) if isinstance(rows, list) else -1
        honored = count == LARGE_LIMIT
        note = (
            f"LIMIT {LARGE_LIMIT} -> {count}行 "
            f"({'要求通り' if honored else '**要求件数と不一致 -- サーバー側capの可能性**'})"
        )
        return honored, elapsed, note
    except SPARQLClientError as exc:
        return False, time.perf_counter() - start, f"LIMIT検証失敗: {exc}"


def main() -> None:
    lines = [
        "# エンドポイント疎通確認結果",
        "",
        f"`scripts/check_endpoints.py` の実行結果。教員の実行環境ではネットワーク到達性が"
        f"異なる可能性があるため、教員自身の環境でも再実行して確認することを推奨する。",
        "",
        "**既知の未解決の限界（指摘#5）**: `SPARQLClient.paginate` のページング終了条件は"
        "「ページが`page_size`未満なら終了」であり、これは真の終端とサーバー側のresult cap"
        "（例: 一部トリプルストアが課す暗黙の上限）を区別できない。以下の`LIMIT {0}`検証は、"
        "この規模でサーバーが要求件数をそのまま返すかを実地確認するものであり、この限界自体を"
        "解消するものではない。`paginate`はページが短い場合にWARNINGログを出すのみの"
        "**緩和策であり、根本解決ではない**。".format(LARGE_LIMIT),
        "",
        "| エンドポイント | ASK | 応答時間 | LIMIT {0}検証 | 応答時間 |".format(LARGE_LIMIT),
        "|---|---|---|---|---|",
    ]

    # 疎通確認は「今」到達可能かを見るためのものなので、キャッシュは使い捨てにする
    # （通常運用でのSPARQLClientのキャッシュ機構はdata/raw/のまま活かす。ここだけ例外）。
    with tempfile.TemporaryDirectory() as tmp_cache:
        for name, endpoint in ENDPOINTS.items():
            client = SPARQLClient(endpoint, cache_dir=Path(tmp_cache) / name.replace(" ", "_"))
            ask_ok, ask_time, ask_note = check_ask(client)
            limit_ok, limit_time, limit_note = check_large_limit(client)
            lines.append(
                f"| {name} ({endpoint}) | {'OK' if ask_ok else 'NG'} | {ask_time:.2f}s | "
                f"{limit_note} | {limit_time:.2f}s |"
            )
            logger.info("%s: %s / %s", name, ask_note, limit_note)

    output_path = Path("docs/endpoint_status.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("wrote %s", output_path)


if __name__ == "__main__":
    main()
