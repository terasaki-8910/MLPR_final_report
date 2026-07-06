"""Phase 2追補: ラベル候補述語の全数集計（GROUP BY）による検証スクリプト。

決定事項#19（`profile_predicates`の行単位サンプリングが非ランダムである疑い）への対応。
ラベルプロパティの値分布に限っては、`discover_classes`と同じGROUP BY集計パターンで
対象クラス全数に対して直接集計できるため、サンプリングを一切経由しない。

実エンドポイントへの依存があるため tests/ には含めず、run_profiler.py と同様にここに分離する。
`python scripts/run_label_census.py` として実行し、各 `docs/profile_<key>.md` の末尾に
「全数集計によるラベル候補検証」節を追記する（既存の200件サンプル節は残す）。
"""
from pathlib import Path

from rdf2graph.sparql.client import SPARQLClient, SPARQLClientError
from rdf2graph.sparql.profiler import count_label_values, render_label_census_markdown
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

# (エンドポイントURL, 対象クラスURI, ラベル候補述語URI, class_total, limit, literal_only)
# class_totalは各docs/profile_*.mdに記録済みのdiscover_classes実測値（2026-07-06取得）。
CENSUS_TARGETS = {
    "dblp": {
        "endpoint": "https://sparql.dblp.org/sparql",
        "class_uri": "https://dblp.org/rdf/schema#Publication",
        "predicate_uri": "https://dblp.org/rdf/schema#bibtexType",
        "class_total": 8_625_948,
        "limit": 50,
        "literal_only": False,
    },
    "ndl_authorities": {
        "endpoint": "https://id.ndl.go.jp/auth/ndla/sparql",
        "class_uri": "http://www.w3.org/2004/02/skos/core#Concept",
        "predicate_uri": "http://www.w3.org/2004/02/skos/core#inScheme",
        "class_total": 1_490_689,
        "limit": 50,
        "literal_only": False,
    },
    "iccu_sbn": {
        "endpoint": "https://triplestore.iccu.sbn.it/sparql",
        "class_uri": "http://id.loc.gov/ontologies/bibframe/Work",
        "predicate_uri": "http://id.loc.gov/ontologies/bibframe/subject",
        "class_total": 8_796_317,
        "limit": 50,
        "literal_only": False,
    },
    "cervantes_virtual": {
        "endpoint": "https://data.cervantesvirtual.com/sparql",
        "class_uri": "http://rdaregistry.info/Elements/c/Work",
        "predicate_uri": "http://purl.org/dc/elements/1.1/subject",
        "class_total": 384_346,
        "limit": 50,
        "literal_only": True,  # literal(主題語)とuri(人物リンク)が混在するためliteralのみ集計
    },
}

# 全数GROUP BY集計は対象クラスの全トリプルを走査しうるため、長めのタイムアウトを与える。
QUERY_TIMEOUT_SECONDS = 300.0

CENSUS_SECTION_HEADER = "## 全数集計によるラベル候補検証"


def main() -> None:
    for key, target in CENSUS_TARGETS.items():
        logger.info("label census for %s (%s)...", key, target["endpoint"])
        client = SPARQLClient(
            target["endpoint"], cache_dir=Path("data/raw") / key, timeout=QUERY_TIMEOUT_SECONDS
        )
        try:
            value_counts = count_label_values(
                client,
                class_uri=target["class_uri"],
                predicate_uri=target["predicate_uri"],
                limit=target["limit"],
                literal_only=target["literal_only"],
            )
        except SPARQLClientError as exc:
            logger.warning("label census failed for %s: %s", key, exc)
            continue

        section = render_label_census_markdown(
            class_uri=target["class_uri"],
            predicate_uri=target["predicate_uri"],
            value_counts=value_counts,
            class_total=target["class_total"],
            limit=target["limit"],
            literal_only=target["literal_only"],
        )

        profile_path = Path("docs") / f"profile_{key}.md"
        if not profile_path.exists():
            logger.warning("%s does not exist; run scripts/run_profiler.py first", profile_path)
            continue
        content = profile_path.read_text(encoding="utf-8")
        if CENSUS_SECTION_HEADER in content:
            # 再実行時は既存の全数集計節（初出位置から末尾まで）を差し替える
            content = content[: content.index(CENSUS_SECTION_HEADER)].rstrip() + "\n"
        profile_path.write_text(content.rstrip() + "\n\n" + section, encoding="utf-8")
        logger.info("appended census section to %s (%d values)", profile_path, len(value_counts))


if __name__ == "__main__":
    main()
