"""Phase 2: 対象4エンドポイントに対するスキーマ偵察+述語プロファイラの実行スクリプト。

実エンドポイントへの依存があるため tests/ には含めず、check_endpoints.py と同様に
ここに分離する（build-lod-project.md Phase 1/2 の方針）。
`python scripts/run_profiler.py` として実行し、`docs/profile_<endpoint>.md` を生成する。

クラス発見・述語プロファイルの問い合わせは全て `SPARQLClient.query()` を経由する
（新しいHTTP呼び出し経路を作らない、CLAUDE.md 決定事項#13）。結果は `data/raw/` に
キャッシュされる（アーキテクチャ原則#2）。
"""
from pathlib import Path

from rdf2graph.sparql.client import SPARQLClient, SPARQLClientError
from rdf2graph.sparql.profiler import (
    DEFAULT_CLASS_LIMIT,
    DEFAULT_PREDICATE_SAMPLE_SIZE,
    DEFAULT_TOP_N_CLASSES_TO_PROFILE,
    discover_classes,
    profile_predicates,
    render_profile_markdown,
)
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

# キー(=configs/*.yamlのファイル名・docs/profile_*.mdのファイル名に対応)
ENDPOINTS = {
    "dblp": ("DBLP", "https://sparql.dblp.org/sparql"),
    "ndl_authorities": ("NDL Web NDL Authorities", "https://id.ndl.go.jp/auth/ndla/sparql"),
    "iccu_sbn": ("ICCU SBN", "https://triplestore.iccu.sbn.it/sparql"),
    "cervantes_virtual": ("Cervantes Virtual", "https://data.cervantesvirtual.com/sparql"),
}

# GROUP BY集計は全件スキャンになりうるため、疎通確認(check_endpoints.py)より長めのタイムアウト
# を与える。それでも失敗した場合は当該エンドポイントをスキップし、他の3件は続行する。
QUERY_TIMEOUT_SECONDS = 120.0


def profile_one_endpoint(key: str, endpoint_name: str, endpoint_url: str) -> str | None:
    cache_dir = Path("data/raw") / key
    client = SPARQLClient(endpoint_url, cache_dir=cache_dir, timeout=QUERY_TIMEOUT_SECONDS)

    try:
        class_candidates = discover_classes(client, limit=DEFAULT_CLASS_LIMIT)
    except SPARQLClientError as exc:
        logger.warning("discover_classes failed for %s (%s): %s", endpoint_name, endpoint_url, exc)
        return None

    top_classes = class_candidates[:DEFAULT_TOP_N_CLASSES_TO_PROFILE]
    class_profiles = []
    for candidate in top_classes:
        try:
            profile = profile_predicates(
                client, candidate.class_uri, sample_size=DEFAULT_PREDICATE_SAMPLE_SIZE
            )
        except SPARQLClientError as exc:
            logger.warning(
                "profile_predicates failed for %s class=%s: %s", endpoint_name, candidate.class_uri, exc
            )
            continue
        class_profiles.append(profile)

    return render_profile_markdown(
        endpoint_name=endpoint_name,
        endpoint_url=endpoint_url,
        class_candidates=class_candidates,
        class_profiles=class_profiles,
        requested_class_limit=DEFAULT_CLASS_LIMIT,
    )


def main() -> None:
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    for key, (endpoint_name, endpoint_url) in ENDPOINTS.items():
        logger.info("profiling %s (%s)...", endpoint_name, endpoint_url)
        markdown = profile_one_endpoint(key, endpoint_name, endpoint_url)
        if markdown is None:
            logger.warning("skipping doc generation for %s due to failure", endpoint_name)
            continue
        output_path = docs_dir / f"profile_{key}.md"
        output_path.write_text(markdown, encoding="utf-8")
        logger.info("wrote %s", output_path)


if __name__ == "__main__":
    main()
