# dblp: ノード分類の結果

- 分類対象ノード数(target_class): 15000
- 総ノード数(1-hop隣接含む): 47149
- エッジ数(逆方向含む): 100000、リレーションタイプ数: 20
- 特徴量次元: 149（構造 21 + テキスト 128）
- クラス数: 5
- クラス名: Article, Inproceedings, Phdthesis, Incollection, Proceedings

## モデル別 精度・コスト比較（test split）

| モデル | macro-F1 | balanced acc | 学習時間 | 推論時間 | ピークメモリ(学習時) |
|---|---|---|---|---|---|
| R-GCN | 0.5231 | 0.5214 | 3.56s | 0.020s | GPU 948 MB |
| Majority | 0.1351 | 0.2000 | 0.00s | 0.000s | GPU 20 MB |
| Features-only (LogReg) | 0.5821 | 0.5548 | 2.20s | 0.059s | GPU 20 MB |

多数派ベースラインと特徴量のみベースライン(グラフ構造を使わない)を併置することで、R-GCNの性能がグラフ構造由来なのか単にノード特徴由来なのかを切り分ける(CLAUDE.md決定事項#8)。

R-GCN学習: 最良val macro-F1はエポック80で得られた（全101エポック、早期終了込み）。

## R-GCN 混同行列（test split、行=正解 / 列=予測）

| 正解＼予測 | Article | Inproceedings | Phdthesis | Incollection | Proceedings |
|---|---|---|---|---|---|
| Article | 1007 | 140 | 0 | 0 | 0 |
| Inproceedings | 218 | 809 | 0 | 0 | 0 |
| Phdthesis | 36 | 5 | 0 | 0 | 0 |
| Incollection | 9 | 9 | 0 | 0 | 0 |
| Proceedings | 1 | 0 | 0 | 0 | 16 |

## クラス分離度（R-GCN埋め込みのクラスセントロイド間コサイン類似度）

- クラス間平均コサイン類似度（対角除く上三角の平均）: **0.4566**
- 値が低いほど、このエンドポイントのクラス群が埋め込み空間上でよく分離している（本プロジェクト唯一の独創性の根拠。CLAUDE.md 0.5節・決定事項#3）。
- ヒートマップ: `docs/class_separation_dblp.png`

