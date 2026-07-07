import numpy as np
import torch

from rdf2graph.eval.cost import CostRecord, measure_seconds, measure_with_memory
from rdf2graph.eval.embedding_similarity import (
    compute_class_centroids,
    compute_class_separation,
    summarize_separation,
)
from rdf2graph.eval.metrics import compute_classification_metrics


def test_compute_classification_metrics_counts_absent_class_in_macro():
    # class "C"(index 2)はy_true/y_predのどちらにも出現しないが、class_namesに含めることで
    # macro平均の分母から欠落せず、そのクラスのF1=0が正しく平均に反映される。
    y_true = torch.tensor([0, 0, 1, 1])
    y_pred = torch.tensor([0, 0, 1, 1])
    metrics = compute_classification_metrics(y_true, y_pred, class_names=["A", "B", "C"])

    assert metrics.macro_f1 == 2.0 / 3.0  # A=1.0, B=1.0, C=0.0 の平均
    assert metrics.balanced_accuracy == 1.0
    assert metrics.confusion.shape == (3, 3)


def test_compute_classification_metrics_perfect_two_class():
    y_true = torch.tensor([0, 1, 0, 1])
    y_pred = torch.tensor([0, 1, 0, 1])
    metrics = compute_classification_metrics(y_true, y_pred, class_names=["A", "B"])

    assert metrics.macro_f1 == 1.0
    assert metrics.balanced_accuracy == 1.0


def test_compute_class_centroids_averages_within_class():
    embeddings = torch.tensor([[1.0, 0.0], [3.0, 0.0], [0.0, 2.0], [0.0, 4.0]])
    y = torch.tensor([0, 0, 1, 1])
    mask = torch.tensor([True, True, True, True])

    centroids = compute_class_centroids(embeddings, y, mask, num_classes=2)

    assert torch.allclose(centroids[0], torch.tensor([2.0, 0.0]))
    assert torch.allclose(centroids[1], torch.tensor([0.0, 3.0]))


def test_class_separation_orthogonal_centroids_have_zero_similarity():
    centroids = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    separation = compute_class_separation(centroids, class_names=["A", "B"])

    assert separation.similarity.shape == (2, 2)
    assert np.isclose(separation.similarity[0, 0], 1.0)
    assert np.isclose(separation.similarity[0, 1], 0.0)
    assert summarize_separation(separation) == 0.0


def test_class_separation_identical_centroids_have_max_similarity():
    centroids = torch.tensor([[1.0, 1.0], [2.0, 2.0]])  # 同一方向(スケール違い)
    separation = compute_class_separation(centroids, class_names=["A", "B"])

    assert np.isclose(summarize_separation(separation), 1.0)


def test_measure_seconds_returns_value_and_nonnegative_time():
    result, seconds = measure_seconds(lambda: 21 * 2)

    assert result == 42
    assert seconds >= 0


def test_measure_with_memory_on_cpu_returns_costrecord():
    result, record = measure_with_memory(lambda: sum(range(100)), device=torch.device("cpu"))

    assert result == 4950
    assert isinstance(record, CostRecord)
    assert record.seconds >= 0
    assert record.peak_gpu_memory_bytes is None  # CPUではGPUメモリは計測しない
