# ndl_authorities: ノード分類の結果

- 分類対象ノード数(target_class): 15000
- 総ノード数(1-hop隣接含む): 42545
- エッジ数(逆方向含む): 55112、リレーションタイプ数: 4
- 特徴量次元: 133（構造 5 + テキスト 128）
- クラス数: 5
- クラス名: personalNames, corporateNames, topicalTerms, geographicNames, uniformTitles

## モデル別 精度・コスト比較（test split）

| モデル | macro-F1 | balanced acc | 学習時間 | 推論時間 | ピークメモリ(学習時) |
|---|---|---|---|---|---|
| R-GCN | 0.7382 | 0.7490 | 1.77s | 0.012s | GPU 250 MB |
| Majority | 0.1655 | 0.2000 | 0.00s | 0.000s | GPU 19 MB |
| Features-only (LogReg) | 0.7881 | 0.7738 | 0.45s | 0.042s | GPU 19 MB |

多数派ベースラインと特徴量のみベースライン(グラフ構造を使わない)を併置することで、R-GCNの性能がグラフ構造由来なのか単にノード特徴由来なのかを切り分ける(CLAUDE.md決定事項#8)。

R-GCN学習: 最良val macro-F1はエポック49で得られた（全70エポック、早期終了込み）。

## R-GCN 混同行列（test split、行=正解 / 列=予測）

| 正解＼予測 | personalNames | corporateNames | topicalTerms | geographicNames | uniformTitles |
|---|---|---|---|---|---|
| personalNames | 1526 | 62 | 0 | 0 | 0 |
| corporateNames | 44 | 323 | 0 | 0 | 0 |
| topicalTerms | 1 | 0 | 224 | 5 | 0 |
| geographicNames | 0 | 0 | 4 | 53 | 0 |
| uniformTitles | 0 | 0 | 5 | 3 | 0 |

## クラス分離度（R-GCN埋め込みのクラスセントロイド間コサイン類似度）

- クラス間平均コサイン類似度（対角除く上三角の平均）: **0.3837**
- 値が低いほど、このエンドポイントのクラス群が埋め込み空間上でよく分離している（本プロジェクト唯一の独創性の根拠。CLAUDE.md 0.5節・決定事項#3）。
- ヒートマップ: `docs/class_separation_ndl_authorities.png`

