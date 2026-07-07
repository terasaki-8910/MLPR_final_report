"""Phase 5: 特徴量のみベースライン(グラフ構造を一切使わず、ノード特徴量だけで分類)。

CLAUDE.md決定事項#8: これが無いと「R-GCNの性能向上がグラフ構造由来なのか、単にノード
特徴量が強いだけなのか」を切り分けられないため無条件で実装する。ロジスティック回帰を
採用したのは、MLPと比較して追加のハイパーパラメータ探索なしに確実に収束し、この
提出のタイムライン（CLAUDE.md 7節、緊急対応期間）に適しているため。
"""
from __future__ import annotations

import torch
from sklearn.linear_model import LogisticRegression
from torch_geometric.data import Data

DEFAULT_MAX_ITER = 1000


def fit(data: Data, seed: int = 42, max_iter: int = DEFAULT_MAX_ITER) -> LogisticRegression:
    x_train = data.x[data.train_mask].numpy()
    y_train = data.y[data.train_mask].numpy()
    model = LogisticRegression(max_iter=max_iter, random_state=seed)
    model.fit(x_train, y_train)
    return model


def predict(model: LogisticRegression, data: Data) -> torch.Tensor:
    """全ノードに対する予測クラス(グラフ構造=edge_index/edge_typeは一切参照しない)。"""
    predictions = model.predict(data.x.numpy())
    return torch.as_tensor(predictions, dtype=torch.long)
