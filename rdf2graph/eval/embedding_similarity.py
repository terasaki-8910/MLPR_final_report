"""Phase 6: クラスセントロイド間コサイン類似度。

本プロジェクトが主張する唯一の独創性の根拠(CLAUDE.md 0.5節・決定事項#3)。学習済み
R-GCNのノード埋め込みからラベルごとの平均ベクトル(セントロイド)を計算し、エンドポイント
内の全クラスペアに対してコサイン類似度を算出する。統合しない各エンドポイント間では
埋め込みベクトルそのものではなく、この指標(要約統計量)自体を比較する(決定事項#3)。
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch


@dataclass(frozen=True)
class ClassSeparation:
    class_names: list[str]
    similarity: np.ndarray  # [C, C]、対称行列、対角は1.0


def compute_class_centroids(
    embeddings: torch.Tensor, y: torch.Tensor, mask: torch.Tensor, num_classes: int
) -> torch.Tensor:
    """マスクされたノードについて、クラスごとの平均埋め込みベクトル(セントロイド)を計算する。"""
    masked_embeddings = embeddings[mask]
    masked_y = y[mask]
    centroids = torch.zeros((num_classes, embeddings.shape[1]), dtype=embeddings.dtype)
    for class_idx in range(num_classes):
        class_embeddings = masked_embeddings[masked_y == class_idx]
        if class_embeddings.shape[0] == 0:
            raise ValueError(f"class index {class_idx} has zero members under the given mask")
        centroids[class_idx] = class_embeddings.mean(dim=0)
    return centroids


def compute_class_separation(centroids: torch.Tensor, class_names: list[str]) -> ClassSeparation:
    """クラスセントロイドを正規化し、全クラスペア間のコサイン類似度行列を作る。"""
    normalized = torch.nn.functional.normalize(centroids, dim=1)
    similarity = (normalized @ normalized.T).numpy()
    return ClassSeparation(class_names=class_names, similarity=similarity)


def summarize_separation(separation: ClassSeparation) -> float:
    """対角を除いた上三角の平均値(クラス間の平均コサイン類似度)。

    値が低いほど、そのエンドポイントにおけるクラス群が埋め込み空間上でよく分離している
    ことを意味する。4エンドポイント横断で比較する単一の要約統計量(build-lod-project.md Phase 6)。
    """
    n = len(separation.class_names)
    if n < 2:
        raise ValueError("need at least 2 classes to summarize pairwise separation")
    upper = separation.similarity[np.triu_indices(n, k=1)]
    return float(upper.mean())
