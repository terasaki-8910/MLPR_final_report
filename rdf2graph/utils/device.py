"""GPU(あれば)優先、CPUフォールバックのデバイス選択(CLAUDE.md決定事項#7)。

`models/`と`eval/`の両方から参照されるため、どちらのモジュールにも属させず`utils/`に置く
（CLAUDE.md アーキテクチャ原則#5「モジュール境界を守る」）。
"""
import torch


def select_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
