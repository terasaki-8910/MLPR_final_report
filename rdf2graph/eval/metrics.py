"""Phase 6: 分類精度の評価指標(macro-F1, balanced accuracy, 混同行列)。

CLAUDE.md決定事項#9の評価軸「精度: macro-F1, balanced accuracy」に対応する。
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, f1_score


@dataclass(frozen=True)
class ClassificationMetrics:
    macro_f1: float
    balanced_accuracy: float
    confusion: np.ndarray
    class_names: list[str]


def _to_numpy(values) -> np.ndarray:
    if isinstance(values, torch.Tensor):
        return values.detach().cpu().numpy()
    return np.asarray(values)


def compute_classification_metrics(
    y_true, y_pred, class_names: list[str]
) -> ClassificationMetrics:
    """`y_true`/`y_pred`はtarget_classノードのみ(マスク適用済み)を渡すこと。

    `class_names`のインデックス順を`labels=`に明示することで、あるクラスがtest split内に
    1件も出現しなくてもmacro平均の分母からクラスが欠落しない(0点として正しく数えられる)。
    """
    y_true = _to_numpy(y_true)
    y_pred = _to_numpy(y_pred)
    labels = list(range(len(class_names)))
    macro_f1 = f1_score(y_true, y_pred, average="macro", labels=labels, zero_division=0)
    balanced_acc = balanced_accuracy_score(y_true, y_pred)
    confusion = confusion_matrix(y_true, y_pred, labels=labels)
    return ClassificationMetrics(
        macro_f1=float(macro_f1),
        balanced_accuracy=float(balanced_acc),
        confusion=confusion,
        class_names=class_names,
    )
