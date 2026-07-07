"""Phase 5: R-GCNによるノード分類（CLAUDE.md決定事項#7: 2〜3層、`RGCNConv`使用）。

R-GCN(Schlichtkrull et al., 2018)そのものに新規性はない(CLAUDE.md 0.5節)。本プロジェクトの
新規性は評価・比較分析側にあり、ここでは標準的な実装を素直に用いる。

`RGCNClassifier`はRGCNConvを2層（関係を跨ぐメッセージパッシング）+ 分類ヘッド用のLinear層
1層に分離している。これにより「埋め込み」(conv2の出力、Phase 6のクラスセントロイド
コサイン類似度計算で必須)と「ロジット」(分類ヘッドの出力)を明確に区別できる。
"""
from __future__ import annotations

from dataclasses import dataclass, field

import torch
import torch.nn.functional as F
from sklearn.metrics import f1_score
from torch import nn
from torch_geometric.data import Data
from torch_geometric.nn import RGCNConv

from rdf2graph.utils.device import select_device
from rdf2graph.utils.logging import get_logger
from rdf2graph.utils.seed import set_seed

logger = get_logger(__name__)

DEFAULT_HIDDEN_CHANNELS = 64
DEFAULT_MAX_EPOCHS = 200
DEFAULT_PATIENCE = 20
DEFAULT_LR = 0.01
DEFAULT_WEIGHT_DECAY = 5e-4
DEFAULT_DROPOUT = 0.3
# num_basesを掛けすぎるとリレーション数が少ないエンドポイント(例: NDL)でnum_bases>num_relations
# になり無意味な設定になるため、min(num_relations, MAX_NUM_BASES)で自動的に抑える。
MAX_NUM_BASES = 30


class RGCNClassifier(nn.Module):
    """RGCNConv 2層 + Linear分類ヘッド1層(CLAUDE.mdの「2〜3層」の範囲)。"""

    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        num_relations: int,
        num_classes: int,
        dropout: float = DEFAULT_DROPOUT,
    ) -> None:
        super().__init__()
        num_bases = min(num_relations, MAX_NUM_BASES)
        self.conv1 = RGCNConv(in_channels, hidden_channels, num_relations=num_relations, num_bases=num_bases)
        self.conv2 = RGCNConv(
            hidden_channels, hidden_channels, num_relations=num_relations, num_bases=num_bases
        )
        self.classifier = nn.Linear(hidden_channels, num_classes)
        self.dropout = dropout

    def embed(self, x: torch.Tensor, edge_index: torch.Tensor, edge_type: torch.Tensor) -> torch.Tensor:
        """最終分類層の直前の出力（Phase 6のクラスセントロイド計算で使う「埋め込み」）。"""
        h = F.relu(self.conv1(x, edge_index, edge_type))
        h = F.dropout(h, p=self.dropout, training=self.training)
        h = F.relu(self.conv2(h, edge_index, edge_type))
        return h

    def forward(
        self, x: torch.Tensor, edge_index: torch.Tensor, edge_type: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        embeddings = self.embed(x, edge_index, edge_type)
        logits = self.classifier(F.dropout(embeddings, p=self.dropout, training=self.training))
        return logits, embeddings


@dataclass
class TrainingHistory:
    """学習曲線と早期終了の記録（`docs/results_<endpoint>.md`での可視化用）。"""

    train_losses: list[float] = field(default_factory=list)
    val_macro_f1: list[float] = field(default_factory=list)
    best_epoch: int = -1


def fit(
    data: Data,
    hidden_channels: int = DEFAULT_HIDDEN_CHANNELS,
    max_epochs: int = DEFAULT_MAX_EPOCHS,
    patience: int = DEFAULT_PATIENCE,
    lr: float = DEFAULT_LR,
    weight_decay: float = DEFAULT_WEIGHT_DECAY,
    seed: int = 42,
    device: torch.device | None = None,
) -> tuple[RGCNClassifier, TrainingHistory]:
    """`train_mask`で学習し、`val_mask`のmacro-F1が`patience`エポック改善しなければ早期終了する。

    CLAUDE.md決定事項#7: GPU（あれば）優先、CPUフォールバック。最良val macro-F1時点の
    重みを最終モデルとして復元する。
    """
    set_seed(seed)
    device = device or select_device()
    model = RGCNClassifier(
        in_channels=data.x.size(1),
        hidden_channels=hidden_channels,
        num_relations=data.num_relations,
        num_classes=data.num_classes,
    ).to(device)
    x = data.x.to(device)
    edge_index = data.edge_index.to(device)
    edge_type = data.edge_type.to(device)
    y = data.y.to(device)
    train_mask = data.train_mask.to(device)
    val_mask = data.val_mask.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

    best_val_f1 = -1.0
    best_state: dict[str, torch.Tensor] | None = None
    best_epoch = -1
    epochs_without_improvement = 0
    history = TrainingHistory()

    for epoch in range(max_epochs):
        model.train()
        optimizer.zero_grad()
        logits, _ = model(x, edge_index, edge_type)
        loss = F.cross_entropy(logits[train_mask], y[train_mask])
        loss.backward()
        optimizer.step()
        history.train_losses.append(loss.item())

        model.eval()
        with torch.no_grad():
            logits, _ = model(x, edge_index, edge_type)
            val_pred = logits[val_mask].argmax(dim=1).cpu().numpy()
            val_true = y[val_mask].cpu().numpy()
            val_f1 = f1_score(val_true, val_pred, average="macro", zero_division=0)
        history.val_macro_f1.append(val_f1)

        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
            best_epoch = epoch
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= patience:
                logger.info(
                    "early stopping at epoch %d (best val macro-F1=%.4f at epoch %d)",
                    epoch,
                    best_val_f1,
                    best_epoch,
                )
                break

    history.best_epoch = best_epoch
    if best_state is not None:
        model.load_state_dict(best_state)
    return model, history


def predict(
    model: RGCNClassifier, data: Data, device: torch.device | None = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """全ノードに対する予測クラスと埋め込みを返す(`(predictions, embeddings)`、build-lod-project.md Phase 5)。"""
    device = device or next(model.parameters()).device
    model.eval()
    with torch.no_grad():
        logits, embeddings = model(
            data.x.to(device), data.edge_index.to(device), data.edge_type.to(device)
        )
        predictions = logits.argmax(dim=1)
    return predictions.cpu(), embeddings.cpu()
