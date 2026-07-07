"""Phase 4: `configs/*.yaml`を読んでラベル抽出→グラフ構築→`data/processed/<key>/graph.pt`
を生成する。

このスクリプトはエンドポイント固有のロジックを一切持たない（CLAUDE.md アーキテクチャ
原則#1）。ENDPOINTSのキー(=config名)を差し替えるだけで動くことがPhase 4完了の定義であり、
その事実を`docs/progress.md`に記録する。今回の対象はNDLとDBLPの2件(決定事項#21)。
"""
import json
from pathlib import Path

from rdf2graph.convert.graph_builder import build_graph, save_graph
from rdf2graph.convert.labels import extract_labeled_nodes
from rdf2graph.convert.schema import load_config
from rdf2graph.sparql.client import SPARQLClient
from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

ENDPOINTS = {
    "ndl_authorities": "configs/ndl_authorities.yaml",
    "dblp": "configs/dblp.yaml",
}

QUERY_TIMEOUT_SECONDS = 120.0


def convert_one(endpoint_key: str, config_path: str) -> dict:
    config = load_config(config_path)
    cache_dir = Path("data/raw") / endpoint_key
    # 既定のGETを使う。graph_builderのVALUES句クエリはNDLがSPARQLWrapperのPOSTを403で拒否した
    # ため、GETのURL長上限に収まるようバッチサイズを小さく抑える方式に切り替えた
    # (graph_builder.PROPERTY_FETCH_BATCH_SIZE のコメント参照)。
    client = SPARQLClient(config.endpoint, cache_dir=cache_dir, timeout=QUERY_TIMEOUT_SECONDS)

    labeled_nodes = extract_labeled_nodes(client, config)
    logger.info("%s: extracted %d labeled nodes", endpoint_key, len(labeled_nodes.nodes))

    data, timing = build_graph(client, config, labeled_nodes.nodes)
    logger.info(
        "%s: built graph with %d nodes, %d edges (%d relation types), %d feature dims, %d classes "
        "(sparql=%.1fs, build=%.1fs)",
        endpoint_key,
        data.num_nodes,
        data.edge_index.shape[1],
        data.num_relations,
        data.x.shape[1],
        data.num_classes,
        timing.sparql_seconds,
        timing.build_seconds,
    )

    output_dir = Path("data/processed") / endpoint_key
    save_graph(data, output_dir / "graph.pt")
    logger.info("%s: wrote %s", endpoint_key, output_dir / "graph.pt")

    meta = {
        "endpoint_key": endpoint_key,
        "endpoint": config.endpoint,
        "target_class": config.target_class,
        "num_nodes": int(data.num_nodes),
        "num_target_nodes": int(data.target_mask.sum().item()),
        "num_edges": int(data.edge_index.shape[1]),
        "num_relations": int(data.num_relations),
        "num_feature_dims": int(data.x.shape[1]),
        "num_classes": int(data.num_classes),
        "class_names": list(data.class_names),
        "relation_names": list(data.relation_names),
        "sparql_seconds": timing.sparql_seconds,
        "build_seconds": timing.build_seconds,
    }
    (output_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def main() -> None:
    for key, path in ENDPOINTS.items():
        logger.info("converting %s (config=%s)...", key, path)
        convert_one(key, path)


if __name__ == "__main__":
    main()
