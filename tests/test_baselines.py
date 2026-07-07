import torch
from torch_geometric.data import Data

from rdf2graph.models import features_only_baseline, majority_baseline


def _synthetic_data() -> Data:
    torch.manual_seed(0)
    num_nodes = 20
    x = torch.randn(num_nodes, 4)
    y = torch.tensor([0] * 12 + [1] * 8, dtype=torch.long)
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:14] = True
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask[14:] = True

    data = Data(x=x, y=y)
    data.train_mask = train_mask
    data.test_mask = test_mask
    return data


def test_majority_baseline_predicts_most_frequent_train_class():
    data = _synthetic_data()  # train_mask(先頭14件)の内訳: クラス0が12件、クラス1が2件

    model = majority_baseline.fit(data)
    predictions = majority_baseline.predict(model, data)

    assert model.majority_class == 0
    assert (predictions == model.majority_class).all()
    assert predictions.shape == (data.num_nodes,)


def test_features_only_baseline_ignores_graph_structure_and_uses_features_only():
    data = _synthetic_data()

    model = features_only_baseline.fit(data)
    predictions = features_only_baseline.predict(model, data)

    assert predictions.shape == (data.num_nodes,)
    assert set(predictions.tolist()) <= {0, 1}
    # sklearnのLogisticRegressionはx以外(edge_index等)を一切参照しないため、
    # このData(edge_indexすら持たない)でもエラーなく動作することがそのまま
    # 「グラフ構造を使わない」ことの証拠になる。
