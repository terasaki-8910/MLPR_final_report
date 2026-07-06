"""全モジュール共通の乱数シード固定（CLAUDE.md アーキテクチャ原則#7）。"""
import random

import numpy as np
import torch


def set_seed(seed: int) -> None:
    """Python random, numpy, torch (CPU/CUDA) の乱数状態を単一のシードで固定する。"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
