"""Phase 5: 多数派クラスベースライン。

CLAUDE.md決定事項#8: 精度比較の下限を示すために無条件で実装する。議論の対象にしない
（性能で工夫する部分ではない）。
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import torch
from torch_geometric.data import Data


@dataclass(frozen=True)
class MajorityBaseline:
    """`train_mask`内で最も頻度の高いクラスのインデックス。"""

    majority_class: int


def fit(data: Data) -> MajorityBaseline:
    train_labels = data.y[data.train_mask].tolist()
    majority_class = Counter(train_labels).most_common(1)[0][0]
    return MajorityBaseline(majority_class=majority_class)


def predict(model: MajorityBaseline, data: Data) -> torch.Tensor:
    """全ノードに対して常に多数派クラスを返す。"""
    return torch.full((data.num_nodes,), model.majority_class, dtype=torch.long)
