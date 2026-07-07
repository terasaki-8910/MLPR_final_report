import torch
from torch_geometric.data import Data

from rdf2graph.models.rgcn import RGCNClassifier, fit, predict


def _synthetic_data(seed: int = 0) -> Data:
    generator = torch.Generator().manual_seed(seed)
    num_nodes = 30
    num_target = 20
    in_channels = 5
    num_forward_relations = 2
    num_relations = num_forward_relations * 2
    num_edges = 60

    x = torch.randn(num_nodes, in_channels, generator=generator)
    edge_index = torch.randint(0, num_nodes, (2, num_edges), generator=generator)
    edge_type = torch.randint(0, num_relations, (num_edges,), generator=generator)

    y = torch.full((num_nodes,), -1, dtype=torch.long)
    y[:num_target] = torch.randint(0, 2, (num_target,), generator=generator)

    target_mask = torch.zeros(num_nodes, dtype=torch.bool)
    target_mask[:num_target] = True
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:14] = True
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask[14:17] = True
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask[17:20] = True

    data = Data(x=x, edge_index=edge_index, edge_type=edge_type, y=y)
    data.num_relations = num_relations
    data.num_classes = 2
    data.class_names = ["A", "B"]
    data.target_mask = target_mask
    data.train_mask = train_mask
    data.val_mask = val_mask
    data.test_mask = test_mask
    return data


def test_rgcn_fit_predict_smoke_cpu():
    data = _synthetic_data()

    model, history = fit(data, hidden_channels=8, max_epochs=5, patience=5, device=torch.device("cpu"))
    predictions, embeddings = predict(model, data, device=torch.device("cpu"))

    assert predictions.shape == (data.num_nodes,)
    assert embeddings.shape == (data.num_nodes, 8)
    assert torch.isfinite(embeddings).all()
    assert len(history.train_losses) > 0
    assert len(history.val_macro_f1) == len(history.train_losses)
    assert history.best_epoch >= 0


def test_rgcn_num_bases_does_not_exceed_num_relations():
    # NDLのように関係数が非常に少ないエンドポイントでもnum_bases>num_relationsにならない
    # ことを確認する(RGCNConvはnum_bases>num_relationsだとエラーになる)。
    model = RGCNClassifier(in_channels=5, hidden_channels=4, num_relations=1, num_classes=2)

    assert model.conv1.num_bases <= 1
