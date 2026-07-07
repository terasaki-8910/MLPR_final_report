"""Phase 5 + 6: `data/processed/<key>/graph.pt`を読み、R-GCN + 2ベースラインを学習・評価し、
`docs/results_<key>.md`・`docs/class_separation_<key>.png`を生成する。

複数エンドポイントを実行すると、最後に`docs/class_separation_summary.md`(エンドポイント
横断のクラス分離度比較、本プロジェクト唯一の独創性の根拠。CLAUDE.md 0.5節・決定事項#3)を
出力する。エンドポイント固有ロジックは持たない(アーキテクチャ原則#1)。今回の対象はNDLと
DBLP(決定事項#21)。
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from rdf2graph.convert.graph_builder import load_graph
from rdf2graph.eval.cost import CostRecord, measure_with_memory
from rdf2graph.eval.embedding_similarity import (
    ClassSeparation,
    compute_class_centroids,
    compute_class_separation,
    summarize_separation,
)
from rdf2graph.eval.metrics import ClassificationMetrics, compute_classification_metrics
from rdf2graph.models import features_only_baseline, majority_baseline
from rdf2graph.models import rgcn as rgcn_model
from rdf2graph.utils.device import select_device
from rdf2graph.utils.logging import get_logger
from rdf2graph.utils.seed import set_seed

logger = get_logger(__name__)

ENDPOINT_KEYS = ["ndl_authorities", "dblp"]
SEED = 42


@dataclass
class ModelResult:
    name: str
    metrics: ClassificationMetrics
    train_cost: CostRecord
    predict_cost: CostRecord


def _short(uri: str) -> str:
    return uri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def _evaluate_on_test(y_pred, data) -> ClassificationMetrics:
    test_mask = data.test_mask
    return compute_classification_metrics(
        data.y[test_mask], y_pred[test_mask], class_names=[_short(c) for c in data.class_names]
    )


def evaluate_endpoint(endpoint_key: str) -> dict:
    graph_path = Path("data/processed") / endpoint_key / "graph.pt"
    data = load_graph(graph_path)
    device = select_device()
    logger.info(
        "%s: loaded graph (%d nodes, %d edges, %d classes) -- training on device=%s",
        endpoint_key,
        data.num_nodes,
        data.edge_index.shape[1],
        data.num_classes,
        device,
    )
    set_seed(SEED)

    results: list[ModelResult] = []

    # --- R-GCN ---
    (model, history), rgcn_train_cost = measure_with_memory(
        lambda: rgcn_model.fit(data, seed=SEED, device=device), device
    )
    (rgcn_pred, rgcn_emb), rgcn_predict_cost = measure_with_memory(
        lambda: rgcn_model.predict(model, data, device=device), device
    )
    results.append(ModelResult("R-GCN", _evaluate_on_test(rgcn_pred, data), rgcn_train_cost, rgcn_predict_cost))

    # --- 多数派ベースライン ---
    maj_model, maj_train_cost = measure_with_memory(lambda: majority_baseline.fit(data), device)
    maj_pred, maj_predict_cost = measure_with_memory(lambda: majority_baseline.predict(maj_model, data), device)
    results.append(
        ModelResult("Majority", _evaluate_on_test(maj_pred, data), maj_train_cost, maj_predict_cost)
    )

    # --- 特徴量のみベースライン ---
    feat_model, feat_train_cost = measure_with_memory(
        lambda: features_only_baseline.fit(data, seed=SEED), device
    )
    feat_pred, feat_predict_cost = measure_with_memory(
        lambda: features_only_baseline.predict(feat_model, data), device
    )
    results.append(
        ModelResult(
            "Features-only (LogReg)", _evaluate_on_test(feat_pred, data), feat_train_cost, feat_predict_cost
        )
    )

    # --- クラス分離度(R-GCN埋め込みから、target全体で算出) ---
    centroids = compute_class_centroids(rgcn_emb, data.y, data.target_mask, data.num_classes)
    separation = compute_class_separation(centroids, class_names=[_short(c) for c in data.class_names])
    mean_separation = summarize_separation(separation)

    _render_results_markdown(endpoint_key, data, results, history, separation, mean_separation)
    _render_separation_heatmap(endpoint_key, separation)

    return {
        "endpoint_key": endpoint_key,
        "num_target_nodes": int(data.target_mask.sum().item()),
        "num_classes": int(data.num_classes),
        "mean_class_separation": mean_separation,
        "rgcn_macro_f1": results[0].metrics.macro_f1,
        "majority_macro_f1": results[1].metrics.macro_f1,
        "features_only_macro_f1": results[2].metrics.macro_f1,
    }


def _fmt_mem(record: CostRecord) -> str:
    if record.peak_gpu_memory_bytes is not None:
        return f"GPU {record.peak_gpu_memory_bytes / 1e6:.0f} MB"
    if record.peak_cpu_memory_bytes is not None:
        return f"CPU {record.peak_cpu_memory_bytes / 1e6:.0f} MB (RSS peak)"
    return "n/a"


def _render_results_markdown(
    endpoint_key: str,
    data,
    results: list[ModelResult],
    history,
    separation: ClassSeparation,
    mean_separation: float,
) -> None:
    lines = [
        f"# {endpoint_key}: ノード分類の結果",
        "",
        f"- 分類対象ノード数(target_class): {int(data.target_mask.sum().item())}",
        f"- 総ノード数(1-hop隣接含む): {data.num_nodes}",
        f"- エッジ数(逆方向含む): {data.edge_index.shape[1]}、リレーションタイプ数: {data.num_relations}",
        f"- 特徴量次元: {data.x.shape[1]}（構造 {1 + data.num_relations} + テキスト {data.x.shape[1] - 1 - data.num_relations}）",
        f"- クラス数: {data.num_classes}",
        f"- クラス名: {', '.join(separation.class_names)}",
        "",
        "## モデル別 精度・コスト比較（test split）",
        "",
        "| モデル | macro-F1 | balanced acc | 学習時間 | 推論時間 | ピークメモリ(学習時) |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r.name} | {r.metrics.macro_f1:.4f} | {r.metrics.balanced_accuracy:.4f} | "
            f"{r.train_cost.seconds:.2f}s | {r.predict_cost.seconds:.3f}s | {_fmt_mem(r.train_cost)} |"
        )
    lines += [
        "",
        "多数派ベースラインと特徴量のみベースライン(グラフ構造を使わない)を併置することで、"
        "R-GCNの性能がグラフ構造由来なのか単にノード特徴由来なのかを切り分ける(CLAUDE.md決定事項#8)。",
        "",
        f"R-GCN学習: 最良val macro-F1はエポック{history.best_epoch}で得られた"
        f"（全{len(history.train_losses)}エポック、早期終了込み）。",
        "",
        "## R-GCN 混同行列（test split、行=正解 / 列=予測）",
        "",
        "| 正解＼予測 | " + " | ".join(separation.class_names) + " |",
        "|---|" + "---|" * len(separation.class_names),
    ]
    confusion = results[0].metrics.confusion
    for i, name in enumerate(separation.class_names):
        row = " | ".join(str(int(v)) for v in confusion[i])
        lines.append(f"| {name} | {row} |")
    lines += [
        "",
        "## クラス分離度（R-GCN埋め込みのクラスセントロイド間コサイン類似度）",
        "",
        f"- クラス間平均コサイン類似度（対角除く上三角の平均）: **{mean_separation:.4f}**",
        "- 値が低いほど、このエンドポイントのクラス群が埋め込み空間上でよく分離している"
        "（本プロジェクト唯一の独創性の根拠。CLAUDE.md 0.5節・決定事項#3）。",
        f"- ヒートマップ: `docs/class_separation_{endpoint_key}.png`",
        "",
    ]
    output_path = Path("docs") / f"results_{endpoint_key}.md"
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("wrote %s", output_path)


def _render_separation_heatmap(endpoint_key: str, separation: ClassSeparation) -> None:
    n = len(separation.class_names)
    fig, ax = plt.subplots(figsize=(1.5 + n, 1.5 + n))
    im = ax.imshow(separation.similarity, vmin=-1.0, vmax=1.0, cmap="coolwarm")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(separation.class_names, rotation=30, ha="right")
    ax.set_yticklabels(separation.class_names)
    ax.set_title(f"{endpoint_key}: class centroid cosine similarity")
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{separation.similarity[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    output_path = Path("docs") / f"class_separation_{endpoint_key}.png"
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    logger.info("wrote %s", output_path)


def _render_summary(summaries: list[dict]) -> None:
    lines = [
        "# クラス分離度: エンドポイント横断比較",
        "",
        "各エンドポイントは統合せず独立に学習しており、ラベル空間も共有しない（CLAUDE.md決定事項"
        "#2・#3）。したがって埋め込みベクトルそのものは比較できない。代わりに「クラスセントロイド間"
        "コサイン類似度の平均」という**要約統計量自体**をエンドポイント間で比較する（決定事項#3）。",
        "",
        "この値が低いほど、そのデータセットのクラス群は学習された埋め込み空間上でよく分離している"
        "＝分類しやすいことを意味する。",
        "",
        "| エンドポイント | 分類対象ノード数 | クラス数 | クラス間平均コサイン類似度 | R-GCN macro-F1 | 多数派 macro-F1 | 特徴量のみ macro-F1 |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in summaries:
        lines.append(
            f"| {s['endpoint_key']} | {s['num_target_nodes']} | {s['num_classes']} | "
            f"{s['mean_class_separation']:.4f} | {s['rgcn_macro_f1']:.4f} | "
            f"{s['majority_macro_f1']:.4f} | {s['features_only_macro_f1']:.4f} |"
        )
    lines += [
        "",
        "注意: この比較はクラス数・クラス不均衡・言語・スキーマが全く異なる2つのデータセット間の"
        "ものであり、値の大小だけで優劣を論じるのではなく、各データセットの性質(クラス数や不均衡度)"
        "と併せて解釈する必要がある。詳細は各`docs/results_<endpoint>.md`と報告書の考察節を参照。",
        "",
    ]
    output_path = Path("docs") / "class_separation_summary.md"
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("wrote %s", output_path)


def main() -> None:
    summaries = []
    for key in ENDPOINT_KEYS:
        graph_path = Path("data/processed") / key / "graph.pt"
        if not graph_path.exists():
            logger.warning("%s: %s not found; skipping (run run_graph_conversion.py first)", key, graph_path)
            continue
        logger.info("evaluating %s...", key)
        summaries.append(evaluate_endpoint(key))

    if summaries:
        _render_summary(summaries)


if __name__ == "__main__":
    main()
