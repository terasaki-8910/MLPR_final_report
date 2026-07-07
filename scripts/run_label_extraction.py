"""Phase 3: `configs/*.yaml`に基づきラベル抽出を実行し、
`docs/label_distribution_<endpoint>.png`を出力する。

今回の提出はNDL Web NDL AuthoritiesとDBLPの2エンドポイントのみ(CLAUDE.md決定事項#21)。
実エンドポイントへの依存があるため`tests/`には含めない（`scripts/run_profiler.py`と同じ方針）。
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rdf2graph.convert.labels import LabelExtractionResult, extract_labeled_nodes
from rdf2graph.convert.schema import load_config
from rdf2graph.sparql.client import SPARQLClient, SPARQLClientError
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

ENDPOINTS = {
    "ndl_authorities": "configs/ndl_authorities.yaml",
    "dblp": "configs/dblp.yaml",
}

QUERY_TIMEOUT_SECONDS = 120.0


def _short_label(uri: str) -> str:
    return uri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def _plot_label_distribution(endpoint_key: str, result: LabelExtractionResult, output_path: Path) -> None:
    # result.label_valuesの順(全数集計での頻度降順)をそのままグラフの並びに使う。
    ordered = [v.value for v in result.label_values if v.value in result.actual_per_class]
    counts = [result.actual_per_class[label] for label in ordered]
    total = sum(counts)

    # matplotlibのデフォルトフォント(DejaVu Sans)はCJKグリフを持たないため、図中の文言は
    # 英語で統一する(日本語を使うと文字化け/グリフ欠落になる)。データ値自体(URI由来の
    # クラス名)はラテン文字なので影響を受けない。
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(range(len(ordered)), counts)
    ax.set_xticks(range(len(ordered)))
    ax.set_xticklabels([_short_label(v) for v in ordered], rotation=30, ha="right")
    ax.set_ylabel("Number of extracted nodes")
    ax.set_title(f"{endpoint_key}: label distribution (stratified extraction, n={total})")
    for i, c in enumerate(counts):
        ax.text(i, c, f"{c}\n({c / total:.1%})", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def run_one(endpoint_key: str, config_path: str) -> LabelExtractionResult:
    config = load_config(config_path)
    cache_dir = Path("data/raw") / endpoint_key
    client = SPARQLClient(config.endpoint, cache_dir=cache_dir, timeout=QUERY_TIMEOUT_SECONDS)

    result = extract_labeled_nodes(client, config)

    total = len(result.nodes)
    max_share = (max(result.actual_per_class.values()) / total) if total else 0.0
    logger.info(
        "%s: extracted %d labeled nodes across %d classes (largest class share=%.1f%%, "
        "duplicate_count=%d)",
        endpoint_key,
        total,
        len(result.actual_per_class),
        max_share * 100,
        result.duplicate_count,
    )
    if max_share > 0.9:
        logger.warning(
            "%s: largest class share %.1f%% exceeds 90%% -- build-lod-project.md Phase 3 "
            "completion criteria says to reconsider top_k before finalizing.",
            endpoint_key,
            max_share * 100,
        )

    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)
    output_path = docs_dir / f"label_distribution_{endpoint_key}.png"
    _plot_label_distribution(endpoint_key, result, output_path)
    logger.info("wrote %s", output_path)

    return result


def main() -> None:
    for key, path in ENDPOINTS.items():
        logger.info("extracting labels for %s...", key)
        try:
            run_one(key, path)
        except SPARQLClientError as exc:
            logger.warning("skipping %s due to SPARQL error: %s", key, exc)


if __name__ == "__main__":
    main()
