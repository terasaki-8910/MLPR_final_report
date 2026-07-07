"""Phase 6: 学習・推論コスト(時間・GPU/CPUメモリ)の計測(CLAUDE.md決定事項#9)。"""
from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

import torch

from rdf2graph.utils.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


@dataclass(frozen=True)
class CostRecord:
    seconds: float
    peak_gpu_memory_bytes: int | None
    peak_cpu_memory_bytes: int | None


def peak_cpu_memory_bytes() -> int | None:
    """Unix系(`resource`モジュール)でのみ計測できる。Windows等では計測不能としてNoneを返す。

    CLAUDE.md決定事項#10(教員環境での再現性)を踏まえ、計測できない環境でもクラッシュ
    せず処理を続けられるようにする(欠落は正直にNoneとして記録し、握りつぶさない)。
    """
    try:
        import resource
    except ImportError:
        logger.warning("resource module unavailable on this platform; CPU memory not measured")
        return None
    # ru_maxrssはLinuxではKB単位、macOSではバイト単位という既知のプラットフォーム差があるが、
    # 本プロジェクトの実行対象(開発機・教員環境ともLinux/WSL2を想定)はLinux慣例(KB)。
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


def measure_seconds(fn: Callable[[], T]) -> tuple[T, float]:
    """引数無しcallable`fn`を実行し、戻り値と経過秒数を返す(GPUメモリは計測しない)。"""
    start = time.perf_counter()
    result = fn()
    return result, time.perf_counter() - start


def measure_with_memory(fn: Callable[[], T], device: torch.device) -> tuple[T, CostRecord]:
    """引数無しcallable`fn`を実行し、戻り値と`CostRecord`(時間・GPU/CPUメモリ)を返す。"""
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    gpu_peak = torch.cuda.max_memory_allocated(device) if device.type == "cuda" else None
    cpu_peak = peak_cpu_memory_bytes()
    return result, CostRecord(seconds=elapsed, peak_gpu_memory_bytes=gpu_peak, peak_cpu_memory_bytes=cpu_peak)
