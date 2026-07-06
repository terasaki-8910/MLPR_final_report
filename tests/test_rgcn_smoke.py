"""Phase 0 環境スモークテスト。

torch-scatter / torch-sparse / pyg-lib を導入しない判断（requirements.txt参照）が
本プロジェクトの想定規模で成立するかを、Phase 5 (rdf2graph/models/rgcn.py) の本実装に
着手する前に検証する。ここはPhase 5のモデル実装そのものではなく、環境検証のみが目的。
"""
import time

import pytest
import torch
from torch_geometric.nn import RGCNConv

from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

# CLAUDE.md 決定事項#6 の上限（ノード1万〜2万、エッジ10万程度）に近い規模で検証する。
NUM_NODES = 15_000
NUM_EDGES = 100_000
NUM_RELATIONS = 15
IN_CHANNELS = 32
HIDDEN_CHANNELS = 16


def _build_synthetic_graph(device: torch.device, seed: int = 42):
    generator = torch.Generator(device="cpu").manual_seed(seed)
    x = torch.randn(NUM_NODES, IN_CHANNELS, generator=generator).to(device)
    edge_index = torch.randint(0, NUM_NODES, (2, NUM_EDGES), generator=generator).to(device)
    edge_type = torch.randint(0, NUM_RELATIONS, (NUM_EDGES,), generator=generator).to(device)
    return x, edge_index, edge_type


def _run_forward_backward(device: torch.device) -> float:
    x, edge_index, edge_type = _build_synthetic_graph(device)
    model = RGCNConv(IN_CHANNELS, HIDDEN_CHANNELS, num_relations=NUM_RELATIONS, num_bases=8).to(device)

    start = time.perf_counter()
    out = model(x, edge_index, edge_type)
    assert out.shape == (NUM_NODES, HIDDEN_CHANNELS)
    assert torch.isfinite(out).all(), "RGCNConv output contains NaN/Inf"

    out.sum().backward()
    for name, param in model.named_parameters():
        assert param.grad is not None, f"no gradient computed for {name}"
        assert torch.isfinite(param.grad).all(), f"non-finite gradient for {name}"

    return time.perf_counter() - start


@pytest.mark.slow
def test_rgcn_forward_backward_cpu():
    """教員のGPU無し環境でも通る必要があるため無条件で実行する。"""
    elapsed = _run_forward_backward(torch.device("cpu"))
    logger.info(
        "CPU forward+backward took %.2fs (nodes=%d, edges=%d, relations=%d)",
        elapsed, NUM_NODES, NUM_EDGES, NUM_RELATIONS,
    )


@pytest.mark.slow
@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
def test_rgcn_forward_backward_cuda():
    elapsed = _run_forward_backward(torch.device("cuda"))
    logger.info(
        "CUDA forward+backward took %.2fs (nodes=%d, edges=%d, relations=%d)",
        elapsed, NUM_NODES, NUM_EDGES, NUM_RELATIONS,
    )
