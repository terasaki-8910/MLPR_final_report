---
description: rdf2tab プロジェクト（DBpedia汎用変換 + Tabular FM ノード分類）をフェーズ順に実装する
argument-hint: [phase番号 または "status" / "next"]
---

# /build-lod-project

このコマンドは、`CLAUDE.md`（ルート）に記載した意思決定に基づき、`rdf2tab` プロジェクトを実装するためのタスク仕様である。**`CLAUDE.md` を先に読んでいない場合はまずそれを読め。** ここに書く指示と `CLAUDE.md` が矛盾する場合、`CLAUDE.md` を優先する。

引数 `$ARGUMENTS` にフェーズ番号が渡された場合はそのフェーズから着手する。`status` の場合は現状の実装済みフェーズを `docs/progress.md`（無ければ作成）を見て報告する。引数なしの場合は未完了の最初のフェーズから着手する。

**フェーズを飛ばすな。** Phase 2 が終わっていない状態で Phase 5 のモデル比較に手を出すことを禁止する。理由: 変換の正しさを検証せずにモデル性能を語っても、性能差が変換バグに起因するのか本質的な差なのか切り分けられず、信頼性の評価軸で崩壊する。

各フェーズは「完了の定義（Definition of Done）」を満たすまで完了とみなさない。「動いた」は完了の定義ではない。

---

## Phase 0: 環境とスケルトン

- `requirements.txt` に固定バージョンで依存関係を書く。最低限: `rdflib`, `SPARQLWrapper`, `pandas`, `pyarrow`, `scikit-learn`, `torch`, `tabicl`, `tabpfn`, `openai`, `python-dotenv`, `pyyaml`, `pytest`, `pytest-mock`。Python 3.11 を前提とする。
- `setup.py` を最小構成で用意し、`pip install -e .` でパッケージとして import できるようにする。
- `temp_project_name/` を `rdf2tab/` にリネームし、`CLAUDE.md` のディレクトリ構成通りに空パッケージ（`__init__.py`）を作る。
- `.env.example` を作成し、`OPENAI_API_KEY=` を記載（値は空、コメントで「未設定でも `--offline` で全実験再現可能」と明記）。
- `.gitignore` を修正: `data/*` の全除外ルールに **例外を追加**し、`data/processed/llm_cache/` と `data/processed/*.parquet`（サイズが小さいもの）は Git 管理対象にする。生の SPARQL レスポンス（`data/raw/`）は引き続き除外する。

**完了の定義**: `pip install -e . && pytest` がエラーなく完走する（テストが0件でも良いがコマンドが壊れていないこと）。

---

## Phase 1: SPARQL クライアント（`rdf2tab/sparql/client.py`）

- `SPARQLClient(endpoint: str, cache_dir: Path, timeout: float, max_retries: int)` を実装する。
- クエリ文字列とその結果のハッシュベースキャッシュ（`data/raw/<hash>.json`）。同一クエリは2度エンドポイントを叩かない。
- 指数バックオフによるリトライ、タイムアウト処理。
- ページング用ヘルパー: `paginate(query_template: str, page_size: int, max_total: int) -> Iterator[list[dict]]`。`LIMIT`/`OFFSET` を自動挿入する。ここで**ユーザー入力を生文字列連結でクエリに埋め込むことを禁止**し、プレースホルダ方式にする。
- **テスト**: 本物のエンドポイントを叩かず、`requests`/`SPARQLWrapper` をモックしたテストで、キャッシュヒット時にネットワーク呼び出しが発生しないこと、リトライが動くこと、ページングが正しく `LIMIT`/`OFFSET` を積むことを検証する。

**完了の定義**: `tests/test_sparql_client.py` がネットワーク接続なしで全て pass する。

---

## Phase 2: 述語プロファイラ（`rdf2tab/sparql/profiler.py`）

目的: 「どのプロパティを特徴量にするか」をユーザーに丸投げしない。

- 指定した `target_class` のインスタンス集合（サンプル、既定 1000 件）に対して、出現する述語ごとに次を集計する: 出現率（インスタンス数に対する%）、値の型（URI / リテラルで文字列・数値・日付を判別）、多値かどうか。
- スコアリングして候補プロパティを順位付けし、`ProfileResult` として返す（人間可読な `to_markdown()` メソッドを持たせ、`docs/` に出力できるようにする＝了解性の担保）。
- `configs/*.yaml` の `features.auto_discover: true` のとき、このプロファイラの出力を使って特徴量候補を自動選定する（`min_coverage` 未満は除外、`max_properties` で上限）。

**完了の定義**: `dbo:Book` と `dbo:Person` それぞれに対してプロファイラを実行し、出力markdownを `docs/profile_book.md` / `docs/profile_person.md` として保存する。この2つの出力が**プロパティ集合として大きく異なる**ことを目視確認する（同じであれば `dbo:Person` の選定が間違っている）。

---

## Phase 3: 設定スキーマとラベル抽出（`rdf2tab/convert/schema.py`, `rdf2tab/convert/labels.py`）

- `configs/dbo_book.yaml`, `configs/dbo_person.yaml` を作成する。スキーマは以下を骨格とする（`CLAUDE.md` 決定事項 #3, #6 に準拠）:

```yaml
endpoint: "https://dbpedia.org/sparql"
target_class: "dbo:Book"
sampling:
  max_instances: 5000
  page_size: 500
  seed: 42
label:
  property: "dct:subject"
  top_k: 20
  unmatched_policy: "drop"   # drop | other_class（既定drop、CLAUDE.md参照）
features:
  auto_discover: true
  min_coverage: 0.30
  max_properties: 25
  text_properties: ["dbo:abstract"]
  overrides:
    include: []
    exclude: ["dbo:wikiPageID", "dbo:wikiPageRevisionID", "dbo:wikiPageLength"]
split:
  train: 0.7
  val: 0.15
  test: 0.15
  stratify: true
```

- `dataclass` でこの YAML をロードするパーサを書く。未知キーはエラーにする（サイレントに無視しない）。
- ラベル抽出ロジック: 全インスタンスの `dct:subject` 値を集計 → 頻度上位 `top_k` のカテゴリ集合を確定 → 各インスタンスについて、上位カテゴリのうち頻度順で最初にマッチしたものを代表ラベルとする → どれにもマッチしないインスタンスは `unmatched_policy` に従う（既定 `drop`）。
- **テスト**: 人工的な triple 集合（10〜20件程度、モック）に対してラベル抽出が仕様通りに動くこと、`top_k` 境界条件、`drop` と `other_class` 両方の挙動を検証する。

**完了の定義**: `dbo:Book` の実データに対してラベル抽出を実行し、クラスごとのサンプル数分布（棒グラフ）を `docs/label_distribution_book.png` として出力する。極端な偏り（最大クラスが90%超など）があれば `top_k` かサンプル数を見直す。

---

## Phase 4: RDF→Tabular 変換エンジン（`rdf2tab/convert/tabular.py`）

- Phase 2 のプロファイラ出力と Phase 3 のラベルを統合し、`instance_uri, <features...>, label` の DataFrame を **ストリーミングで**構築する（全件を先にメモリに載せない。行ごとに生成して `pyarrow` で逐次書き込み）。
- 直接プロパティ（リテラル）は型に応じて数値正規化 / one-hot（カテゴリカル） / 生文字列保持（`text_properties` 指定分）に振り分ける。
- 1-hop object property は、対象 URI の `rdfs:label` を解決して文字列連結するか、出現数を集約する（多値属性の扱いは `CLAUDE.md` 通り、集約方法を明示的に選べるようにする。デフォルトの挙動をコード内コメントで説明する）。
- 出力は `data/processed/<target_class>/table.parquet` とし、`split` 設定に従って train/val/test を層化分割し、同じディレクトリに保存する。
- **テスト**: 小さな人工 RDF グラフ（rdflib の in-memory graph）に対して変換をかけ、出力 DataFrame の列・行数・型が期待通りであることを検証する。

**完了の定義**: `dbo:Book` と `dbo:Person` の両方で変換が通り、`data/processed/dbo_book/table.parquet` と `data/processed/dbo_person/table.parquet` が生成される。**この2つに対してコード変更が発生していないこと**（設定ファイルの差分のみで動いたこと）を `git diff` で確認し、`docs/progress.md` に記録する。

---

## Phase 5: Tabular Foundation Model 推論（`rdf2tab/models/tabular_fm.py`）

- `TabICLv2` を主モデルとしてラップする。`fit_predict(X_train, y_train, X_test) -> predictions, probabilities` のシンプルなインターフェースにする（学習ループを外部に露出させない。in-context learning モデルなので「学習」という概念がGBDTと違う点をdocstringで明記）。
- `TabPFNv2` も同一インターフェースで実装し、クロスチェックに使う。
- GPU (RTX 5070 Ti) 上での実行を前提にするが、GPU が無い環境でも CPU フォールバックで動くこと（教員の環境に GPU が無い可能性を考慮）。
- 推論時間・メモリを計測するデコレータ/コンテキストマネージャ（`rdf2tab/eval/cost.py` と共有）を用意し、1件推論とバッチ一括推論の両方を計測する。

**完了の定義**: `dbo:Book` の test split に対して TabICLv2 / TabPFNv2 双方で推論が通り、macro-F1 が `eval/metrics.py` 経由で算出できる。

---

## Phase 6: LLM API ベースライン（`rdf2tab/models/llm_baseline.py`）

**`CLAUDE.md` 決定事項 #5 を厳守すること。ここが最も事故りやすい。**

- OpenAI API（既定モデル `gpt-4o-mini`、`configs/*.yaml` または CLI 引数で変更可能）でゼロショット/フューショット分類を行う。
- プロンプトはインスタンスの特徴量（Phase 4 の表形式データの行）をテキスト化して構築する。ラベル候補（top_k カテゴリ名）を選択肢としてプロンプトに含め、モデルには選択肢の中から選ばせる（自由記述させて事後マッチングする方式は評価がブレるため禁止）。
- **すべてのリクエスト/レスポンスを `data/processed/llm_cache/<config_hash>.jsonl` にキャッシュする。** 同一 (プロンプト, モデル名) の組に対しては絶対に2度課金しない。
- `OPENAI_API_KEY` が環境変数/`.env` に無い場合、自動的に `--offline` 相当の挙動になり、キャッシュのみを使う。キャッシュにも無ければ明示的なエラー（サイレントにダミー値を返さない）。
- 呼び出しごとに prompt/completion トークン数と概算コスト（$）を記録し、`rdf2tab/eval/cost.py` に渡して集計できるようにする。

**完了の定義**: 一度だけ実際に API キーを使って `dbo:Book` test split 全件の推論を行い、結果を `data/processed/llm_cache/` にコミットする。その後 `.env` を削除した状態で再実行し、**ネットワークエラーが出ずキャッシュから同じ結果が再現される**ことを確認する（これが「教員が追加コストなしで再現できる」の実地証明になる）。

---

## Phase 7: 多数派クラスベースライン（`rdf2tab/models/majority_baseline.py`）

- train split の最頻クラスを常に予測するだけの実装（数行）。議論の対象にしない、無条件で実装する（`CLAUDE.md` 決定事項 #6 参照）。

**完了の定義**: 他モデルと同じ評価ハーネスに接続され、レポート用の比較表に自動的に1行として現れる。

---

## Phase 8: 評価ハーネス（`rdf2tab/eval/metrics.py`, `rdf2tab/eval/cost.py`）

- 指標: macro-F1, balanced accuracy, per-class confusion matrix。
- 頑健性評価: 自然なクラス分布と、意図的にダウンサンプリングして偏らせた分布（例: 最大クラスを50%まで間引く）の両方で上記指標を算出し、劣化度合いを比較する。
- コスト評価: GPU 系（TabICL/TabPFN）は推論時間・`torch.cuda.max_memory_allocated`、LLM 系は実測レイテンシ・トークン数・概算コスト（$）。両者を同じ表で比較できるように統一フォーマット（例: "1推論あたりコスト" を GPU は電力/時間換算しない、素直に時間とメモリ、LLMは時間と$として併記し、単位が異なることを表のキャプションで明記する。**無理に同一単位に揃えて誤魔化さない**）。
- 変換時間のスケーリング測定: `sampling.max_instances` を 500/1000/2000/5000 と振って Phase 4 の変換を再実行し、SPARQL抽出時間と純変換時間を分離して記録、`docs/conversion_time_scaling.png` に曲線としてプロットする。

**完了の定義**: `docs/results_dbo_book.md` と `docs/results_dbo_person.md` に、モデル×指標の比較表と頑健性曲線・変換時間曲線が出力される。

---

## Phase 9: README とレポート下地

- `README.md` を、`CLAUDE.md` の内容を踏まえて次の章立てで書き直す: 背景（先行研究との差別化を含む）/ データとラベル定義 / 変換パイプライン / モデルとベースライン / 実行方法（`pip install` から結果再現までの具体コマンド）/ 既知の限界（GBDT非採用、LLM APIコスト依存の2点を明記）。
- `docs/report.md` に、課題PDFが要求する「目的・方法・結果と考察」の3節構成でドラフトを作る（本文は実験結果が出てから学生が最終的に書くが、骨子と図表の挿入位置はここで用意する）。

**完了の定義**: 新規に `git clone` した状態を想定し、README記載のコマンドだけを上から順に実行して `docs/results_*.md` まで到達できること（教員視点でのドライラン）。

---

## 進捗記録

各フェーズ完了時に `docs/progress.md` に日付・フェーズ番号・完了の定義を満たしたことの根拠（テスト結果、生成ファイルパス）を追記する。次回セッションはここを読んで再開位置を判断する。
