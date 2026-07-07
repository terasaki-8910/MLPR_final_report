# rdf2graph — 異種書誌LODへの汎用RDF→グラフ変換とR-GCNノード分類

大学院機械学習科目の最終レポート課題。図書館・書誌系の実在する公開SPARQLエンドポイントに対し、
**コード変更なく設定ファイル (`configs/*.yaml`) の差し替えだけで動く単一のRDF→グラフ変換
パイプライン**を適用し、**R-GCN (Relational Graph Convolutional Network) によるノード分類**を
行う。各エンドポイントは独立したグラフとして扱い（統合しない）、学習された埋め込み空間の
**クラス分離度（クラスセントロイド間コサイン類似度）**をエンドポイント横断で比較する。

## 背景と新規性の所在（正直な自己評価）

**R-GCN (Schlichtkrull et al., 2018) は RDF ナレッジグラフのノード分類における最も標準的な
手法であり、モデルとしての新規性は一切ない。** 原論文自体が AIFB・MUTAG・BGS・AM という
RDF ベンチマークで評価している。本プロジェクトはこれを隠さない。

本プロジェクトが主張する新規性は**モデル側ではなく評価・分析側**に限定される:

> スキーマ・言語・ドメインが大きく異なる実世界の書誌/典拠 LOD に対して、単一の RDF→グラフ
> 変換パイプラインを設定ファイルの差し替えだけで適用し、同一の R-GCN アーキテクチャで
> ノード分類を行い、学習された埋め込み空間のクラス分離度をエンドポイント横断で比較する。

地味だが具体的で検証可能な比較分析であり、「R-GCN を LOD に応用したのは初めて」といった
主張は一切しない。

## 対象エンドポイント

当初は書誌/典拠系の4エンドポイント（DBLP・NDL Web NDL Authorities・ICCU SBN・Cervantes
Virtual）を対象に計画したが、**提出期限の制約により、今回の提出は以下の2エンドポイントに
スコープを縮小した**（縮小の経緯と見送り理由は「既知の限界」節および `docs/progress.md`・
`CLAUDE.md` 決定事項#21 に明記）。

| キー | エンドポイント | 内容 | 分類対象クラス | ラベル |
|---|---|---|---|---|
| `ndl_authorities` | NDL Web NDL Authorities (`https://id.ndl.go.jp/auth/ndla/sparql`) | 日本語の主題・人物典拠データ | `skos:Concept`（典拠ノード自体） | `skos:inScheme`（典拠の種別: personalNames 等） |
| `dblp` | DBLP (`https://sparql.dblp.org/sparql`) | 計算機科学文献の書誌データ | `dblp:Publication` | `dblp:bibtexType`（Article / Inproceedings 等） |

**NDL は書誌ノードを持たない**ため分類対象が典拠ノード自体である点で、書誌レコードを分類する
DBLP とは概念が異なる。この非対称性はあえて残し、汎用パイプラインが異質なスキーマにも
設定変更のみで対応できることの実証に用いる。

対象クラス・ラベルプロパティのURIは決め打ちせず、スキーマ偵察（クラス発見）と述語プロファイル、
さらにGROUP BY全数集計によるラベル分布検証を経て確定した（`docs/profile_*.md`、`CLAUDE.md`
決定事項#16〜#20）。

## パイプラインの構成

```
configs/*.yaml
   │  (設定ファイル駆動: 80%自動 + 20%設定)
   ▼
[1] SPARQL 抽出   rdf2graph/sparql/     クラス発見・述語プロファイル・ラベル全数集計
   │                                    （キャッシュ・リトライ・ページング付き）
   ▼
[2] ラベル抽出    rdf2graph/convert/labels.py
   │   ラベル値ごとの真の件数比に max_nodes を按分する「層化抽出」
   │   （素朴な LIMIT 抽出が起こす格納順バイアスを回避。決定事項#19/#22）
   ▼
[3] グラフ変換    rdf2graph/convert/graph_builder.py
   │   edge_type 付き単一 Data（RGCNConv が直接消費、決定事項#15）
   │   ノード特徴 = 構造特徴（次数 + リレーション別隣接数）+ 浅いテキスト特徴（文字n-gram）
   │   label.property と rdf:type はエッジ/特徴から除外（ラベルリーク防止、決定事項#23）
   ▼
[4] 学習・評価    rdf2graph/models/  rdf2graph/eval/
       R-GCN + 多数派ベースライン + 特徴量のみベースライン
       macro-F1 / balanced accuracy / コスト / クラスセントロイド間コサイン類似度
```

### モデルとベースライン

- **R-GCN**: `torch_geometric.nn.RGCNConv` 2層 + 線形分類ヘッド1層。埋め込み（最終分類層直前
  の出力）を返し、クラス分離度の算出に用いる。
- **多数派クラスベースライン**: 精度の下限。無条件で実装（`CLAUDE.md` 決定事項#8）。
- **特徴量のみベースライン**: グラフ構造を一切使わず、ノード特徴量だけでロジスティック回帰。
  **これが無いと「R-GCN の性能向上がグラフ構造由来なのか、単にノード特徴が強いだけか」を
  切り分けられない**ため無条件で実装（決定事項#8）。

## 実行方法（教員の再現手順）

外部API・課金サービスに一切依存しない。公開SPARQLエンドポイントとローカル環境のみで完結する
（GPUは任意。無い環境では自動でCPUにフォールバックする）。

```bash
# 1. 仮想環境の構築（GPUがある場合のCUDA版torch導入手順は下記「GPU環境」を参照）
python -m venv ml_env
# Linux/WSL:  source ml_env/bin/activate
# Windows:    ml_env\Scripts\activate
pip install -e .

# 2. テスト（ネットワーク不要でパスする）
pytest -m "not slow"

# 3. スキーマ偵察・ラベル分布検証（結果は data/raw/ にキャッシュされる。docs/profile_*.md を生成）
python scripts/run_profiler.py
python scripts/run_label_census.py

# 4. ラベル抽出とラベル分布の可視化（docs/label_distribution_*.png を生成）
python scripts/run_label_extraction.py

# 5. RDF→グラフ変換（data/processed/<key>/graph.pt を生成）
python scripts/run_graph_conversion.py

# 6. 学習・評価（docs/results_*.md, docs/class_separation_*.png,
#    docs/class_separation_summary.md を生成）
python scripts/run_training_eval.py
```

`configs/dblp.yaml` と `configs/ndl_authorities.yaml` は確定済みで、手順3〜6は**同じコードのまま
両エンドポイントに対して順に実行される**。エンドポイント固有の Python コードは存在しない
（`CLAUDE.md` アーキテクチャ原則#1）。

### GPU環境（任意）

開発機（RTX 5070 Ti / CUDA）では CUDA 版 torch を明示的に導入した:

```bash
pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cu128
pip install -e .
```

GPU が無い環境では `requirements.txt` の無指定 `torch` により PyPI 既定の CPU ビルドが入り、
学習・推論は自動で CPU にフォールバックする（`CLAUDE.md` 決定事項#7・#11）。`torch-scatter` /
`torch-sparse` / `pyg-lib` は意図的に含めていない（決定事項#12）。

## 成果物

- `docs/profile_*.md` — スキーマ偵察・述語プロファイル・ラベル全数集計の結果
- `docs/label_distribution_*.png` — 層化抽出後のクラス分布
- `docs/results_*.md` — モデル×指標の比較表・混同行列・コスト
- `docs/class_separation_*.png` — クラスセントロイド間コサイン類似度ヒートマップ
- `docs/class_separation_summary.md` — **エンドポイント横断のクラス分離度比較（本プロジェクトの
  主眼）**
- `docs/report.md` — 目的・方法・結果と考察のレポート
- `docs/progress.md` — フェーズごとの進捗と、正直な限界の記録

## 既知の限界（隠さない）

1. **対象を2エンドポイントに縮小した**: 提出期限の制約により、当初計画の4件のうち ICCU SBN・
   Cervantes Virtual は着手を見送った。両者は全数集計で追加のデータ品質問題（ICCU SBN: 件数が
   完全一致する異表記エイリアスTopic URIが多数・上位50値でもWork全体の5.1%しか被覆しない、
   Cervantes Virtual: 主題literalの最頻値が空文字列・低被覆率）が判明しており、残り時間で
   ラベル設計をやり直しつつ4件を完走させるのはリスクが高いと判断した（`CLAUDE.md` 決定事項
   #20・#21）。
2. **エンドポイント間でラベル空間を共有しない**: 各グラフは独立に構築・学習する。owl:sameAs
   解決等のエンティティリンクはスコープ外（決定事項#2）。そのため埋め込みベクトルそのものは
   比較できず、「クラス分離度という要約統計量」自体を比較する（決定事項#3）。
3. **層内サンプリング順序バイアスの残存**: ラベル層化抽出は層間（ラベル間）比率を全数集計の
   真の値に一致させるが、層内（同一ラベル値内）の抽出順序はサーバー既定順であり真の一様
   ランダムではない（決定事項#22）。
4. **評価軸から意図的に外したもの**: グラフ構造ロバスト性（エッジ削除・ノイズ耐性）、
   スケールアウト性、人為的クラス不均衡下での頑健性は時間制約により評価しない（決定事項#9）。

一次情報（設計判断・意思決定ログ）は [CLAUDE.md](./CLAUDE.md)、実装タスク仕様は
[.claude/commands/build-lod-project.md](./.claude/commands/build-lod-project.md) を参照。
