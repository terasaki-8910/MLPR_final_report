---
description: rdf2graph プロジェクト（4つの図書館系SPARQLエンドポイント × R-GCNノード分類）をフェーズ順に実装する
argument-hint: [phase番号 または "status" / "next"]
---

# /build-lod-project

このコマンドは `CLAUDE.md`（ルート）の意思決定に基づき `rdf2graph` プロジェクトを実装するためのタスク仕様である。**`CLAUDE.md` を先に読め。** 矛盾があれば `CLAUDE.md` が勝つ。

時間制約を踏まえてスコープを圧縮した8フェーズ構成にしている。「完了の定義を満たさずに次に進まない」という規律は緩めない。ここを緩めると時間を節約したはずが手戻りで余計に失う。

引数 `$ARGUMENTS` にフェーズ番号があればそこから着手。`status` なら `docs/progress.md` を見て報告。

---

## Phase 0: 環境とスケルトン

- プロジェクトのソースコードパッケージを `rdf2graph/` として作成する（既存スケルトンに仮ディレクトリがあれば `rdf2graph/` に置き換える）。
- `requirements.txt`: `rdflib`, `SPARQLWrapper`, `torch`, `torch-geometric`, `pandas`, `scikit-learn`, `pytest`, `pytest-mock`, `pyyaml`, `matplotlib`。外部API（LLM等）や商用Tabular Foundation Modelへの依存は一切持たない。公開SPARQLエンドポイントとローカルGPUのみで完結する構成にする。これは教員側の環境構築失敗リスクを下げる。
- `configs/` 配下に `dblp.yaml`, `ndl_authorities.yaml`, `iccu_sbn.yaml`, `cervantes_virtual.yaml` の空テンプレートを作る（中身は Phase 3）。

**完了の定義**: `pip install -e . && pytest` がエラーなく完走する。

---

## Phase 1: SPARQL クライアント（`rdf2graph/sparql/client.py`）

- `SPARQLClient(endpoint, cache_dir, timeout, max_retries)`。クエリ文字列ハッシュベースのディスクキャッシュ。指数バックオフリトライ。
- `paginate(query_template, page_size, max_total)` で `LIMIT`/`OFFSET` を自動管理。ユーザー入力を生文字列連結でクエリに埋め込むことを禁止（プレースホルダ方式）。
- **テスト**: モックレスポンスでキャッシュヒット時にネットワーク呼び出しが発生しないこと、ページングが正しいことを検証する。実エンドポイントに対する疎通テストは `tests/` ではなく `scripts/check_endpoints.py` のような別スクリプトに分離し、CI では実行しない。

**完了の定義**: `tests/test_sparql_client.py` がネットワーク接続なしで pass する。加えて、4エンドポイントそれぞれに対して手動で1回疎通確認し、結果を `docs/endpoint_status.md` に記録する（実装環境から再確認すること。サンドボックス経由の確認は教員のネットワーク環境と同一ではない）。

---

## Phase 2: スキーマ偵察 + 述語プロファイラ（`rdf2graph/sparql/profiler.py`）

対象4エンドポイントは正確なオントロジーURIが未調査であるため、`target_class` やラベルプロパティの決め打ちを禁止する（`CLAUDE.md` 決定事項 #4）。

- `discover_classes(endpoint) -> list[ClassCandidate]`: `SELECT ?class (COUNT(?s) AS ?count) WHERE { ?s a ?class } GROUP BY ?class ORDER BY DESC(?count) LIMIT 20` 相当のクエリでインスタンス数上位のクラスを発見する。
- 発見したクラス上位数件について述語プロファイラ（出現率・値型・多値判定）を実行し、`docs/profile_<endpoint>.md` に人間可読な形で出力する。
- **このプロファイル結果を人間（ユーザー）が目視確認してから Phase 3 に進む。** 自動探索の結果を鵜呑みにしてラベル・特徴量を確定させない。理由: NDL典拠データのように書誌ノードを持たないエンドポイントでは、機械的なスコアリングだけでは「意味のある分類対象」を見誤るリスクが高い。

**完了の定義**: 4エンドポイントすべてに対して `docs/profile_dblp.md`, `docs/profile_ndl_authorities.md`, `docs/profile_iccu_sbn.md`, `docs/profile_cervantes_virtual.md` が生成され、それぞれ「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」が記載されている。この4つのファイルの中身が互いに大きく異なる（同じテンプレ的結果になっていない）ことを目視確認する。

---

## Phase 3: 設定ファイルとラベル抽出（`rdf2graph/convert/schema.py`, `rdf2graph/convert/labels.py`）

- Phase 2 の出力を見ながら、4つの `configs/*.yaml` を人間が確定する（自動生成に任せない。ここは「20%の設定」の部分）。骨格:

```yaml
endpoint: "https://sparql.dblp.org/sparql"
target_class: "<Phase2で発見した実際のURI>"
sampling:
  max_nodes: 15000
  max_edges: 100000
  page_size: 500
  seed: 42
label:
  property: "<Phase2で発見した実際のURI>"
  top_k: 10
  unmatched_policy: "drop"
features:
  auto_discover: true
  min_coverage: 0.30
  max_properties: 20
  text_properties: ["<タイトル相当のプロパティ>"]
  text_vectorizer: "hashing"   # hashing | tfidf, 次元は128〜256程度
split:
  train: 0.7
  val: 0.15
  test: 0.15
  stratify: true
```

- ラベル抽出ロジック: 全インスタンスの `label.property` 値を集計 → 頻度上位 `top_k` のカテゴリ集合を確定 → 各インスタンスについて頻度順で最初にマッチしたものを代表ラベルとする → どれにもマッチしないインスタンスは `unmatched_policy` に従う（既定 `drop`）。
- NDL典拠データについては「ラベル対象ノード＝典拠ノード自体」であることをコード上のコメントで明記し、他3エンドポイント（書誌ノードが分類対象）と概念が違うことが読んだ人に伝わるようにする。
- **テスト**: 人工triple集合でのラベル抽出ロジックのユニットテスト。

**完了の定義**: 4つの `configs/*.yaml` が確定し、それぞれでラベル抽出を実行した際のクラス分布を `docs/label_distribution_<endpoint>.png` として出力する。極端な偏り（最大クラスが90%超）があれば `top_k` を調整する。

---

## Phase 4: RDF→グラフ変換エンジン（`rdf2graph/convert/graph_builder.py`）

- rdflib で取得した triple 集合から、`torch_geometric.data.Data`（または異種エッジタイプが多い場合は `HeteroData`）を構築する。
  - ノード: `target_class` のインスタンス + それらと1-hopで繋がる周辺エンティティ（著者・主題等）。
  - エッジ: object property をリレーションタイプとして保持する（R-GCNの `edge_type` に対応）。
  - ノード特徴量: 構造特徴（次数、リレーションタイプ別隣接数）+ テキスト特徴（`text_properties` を hashing/TF-IDF ベクトル化、`CLAUDE.md` 決定事項 #5 の通りエンドポイントごとに独立学習）。
- メモリディシプリン: `sampling.max_nodes`/`max_edges` で上限を厳格に守る。上限超過時はランダムサブサンプリング（seed固定）で切る。
- **テスト**: 小さな人工RDFグラフ（rdflibのin-memory graph、数十triple）に対して変換をかけ、出力 `Data` オブジェクトのノード数・エッジ数・特徴次元が期待通りであることを検証する。

**完了の定義**: 4エンドポイントすべてで変換が通り、`data/processed/<endpoint>/graph.pt` が生成される。**コード変更なしで4エンドポイント分の設定ファイルの差し替えだけで動いたこと**を `git diff` で確認し `docs/progress.md` に記録する（ここが「汎用パイプライン」の主張の実地証明）。

---

## Phase 5: R-GCN とベースライン（`rdf2graph/models/rgcn.py`, `majority_baseline.py`, `features_only_baseline.py`）

- R-GCN（`torch_geometric.nn.RGCNConv` を使用、2〜3層）。`fit(data) -> model`, `predict(model, data) -> predictions, embeddings` のインターフェースにする。**埋め込み（最終層直前の出力）を返せるようにすること。Phase 6 のコサイン類似度計算で必須。**
- 多数派クラスベースライン（数行、無条件で実装、議論しない）。
- 特徴量のみベースライン（グラフ構造を使わず、Phase 4で作ったノード特徴量だけでロジスティック回帰またはMLP。**これも無条件で実装する**。理由: `CLAUDE.md` 決定事項#8。これがないと「R-GCNの性能向上はグラフ構造由来か、ノード特徴が強いだけか」を切り分けられない）。
- GPU (RTX 5070 Ti) 実行を前提としつつ、GPU無し環境でもCPUフォールバックで動作すること。

**完了の定義**: 4エンドポイントそれぞれで R-GCN・多数派・特徴量のみの3モデルが動き、macro-F1が算出できる。

---

## Phase 6: 評価ハーネス（`rdf2graph/eval/metrics.py`, `cost.py`, `embedding_similarity.py`）

- 精度: macro-F1, balanced accuracy, 混同行列。
- コスト: 学習時間・推論時間（GPU: `torch.cuda.max_memory_allocated`）。SPARQL抽出時間とグラフ構築時間を分離して記録し、`sampling.max_nodes` を振ってスケーリング傾向を`docs/conversion_time_scaling.png`に出す。
- **クラス分離度診断**（`embedding_similarity.py`）: R-GCNの埋め込みからラベルごとの平均ベクトル（セントロイド）を計算し、エンドポイント内の全クラスペアに対してコサイン類似度を算出、ヒートマップとして `docs/class_separation_<endpoint>.png` に出力する。4エンドポイント分をまとめた比較表（例: 「クラスペア間コサイン類似度の平均値」を1つの要約統計量にして4エンドポイントを並べる）を `docs/class_separation_summary.md` に作る。
- **意図的に実装しないもの**（`CLAUDE.md` 決定事項#9）: グラフ構造ロバスト性（エッジ削除耐性）、スケールアウト性、人為的クラス不均衡実験。これらを「今後の課題」として `docs/results_*.md` に明記する。

**完了の定義**: `docs/results_<endpoint>.md`（4本）にモデル×指標の比較表、コサイン類似度ヒートマップ、変換時間曲線が出力され、`docs/class_separation_summary.md` に4エンドポイント横断の要約が出る。

---

## Phase 7: README と報告書下地

- `README.md` を次の章立てで書く: 背景（新規性の主張が「比較分析」にある理由を明記）/ 対象エンドポイント4件の紹介 / 変換パイプライン / R-GCNとベースライン / 実行方法（教員が `pip install` から `docs/results_*.md` 再現まで到達できる具体コマンド）/ 既知の限界（グラフ構造ロバスト性・スケールアウト性の非評価、クラス不均衡実験の非実施、エンドポイント間ラベル空間非共有の3点を明記）。
- `docs/report.md` に「目的・方法・結果と考察」の3節構成のドラフトを作る。

**完了の定義**: 新規に `git clone` した状態から README のコマンドだけを順に実行して `docs/results_*.md` と `docs/class_separation_summary.md` まで到達できること。

---

## 進捗記録

各フェーズ完了時に `docs/progress.md` に日付・フェーズ番号・完了の定義を満たした根拠を追記する。
