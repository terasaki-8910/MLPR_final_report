# 進捗記録

## Phase 0: 環境とスケルトン（2026-07-06 完了）

**完了の定義**: `pip install -e . && pytest` がエラーなく完走する。

根拠:
- `ml_env/`（完全独立venv、`--system-site-packages`不使用）を構築し、`torch==2.11.0` を
  `--index-url https://download.pytorch.org/whl/cu128` で導入（このマシンのRTX 5070 Ti /
  CUDA 13.1ドライバで動作確認済み）。教員環境での再現性を優先した経緯はCLAUDE.md決定事項#11参照。
- `pip install -e .` が成功（rdf2graph-0.1.0 および requirements.txt 全依存関係が導入された）。
- `pytest` 実行結果: **3 passed**（`test_package.py::test_import`,
  `test_rgcn_smoke.py::test_rgcn_forward_backward_cpu`,
  `test_rgcn_smoke.py::test_rgcn_forward_backward_cuda`）。
- `tests/test_rgcn_smoke.py`により、torch-scatter/torch-sparse/pyg-lib無しで`RGCNConv`が
  本プロジェクトの想定規模（ノード15,000/エッジ100,000/リレーション15種類）でforward/backward
  を実際に通せることをCPU・CUDA双方で検証済み（CLAUDE.md決定事項#12）。
- CLAUDE.md「7. デバッグ・失敗時の運用ルール」を追記（`git fetch`で他ワークツリーとの
  重複がないことを確認した上で実施）。

## Phase 1: SPARQLクライアント（2026-07-06 完了）

**完了の定義**: `tests/test_sparql_client.py`がネットワーク接続なしでpassし、4エンドポイント
それぞれに対して手動で1回疎通確認し、結果を`docs/endpoint_status.md`に記録する。

根拠:
- `rdf2graph/sparql/client.py`（`SPARQLClient`, `Binding`, 例外階層）、
  `rdf2graph/sparql/query_builder.py`（`iri`/`int_literal`/`string_literal`）を実装。
- `pytest tests/test_sparql_client.py -v` 実行結果: **10 passed**（ネットワーク接続なし）。
  キャッシュヒット、キャッシュ衝突/破損検知（WARNINGログ）、ページング終了条件のWARNINGログ、
  リトライ成功時のWARNINGログ、リトライ上限超過時の`SPARQLTimeoutError`、4xx時の
  `SPARQLQueryError`（リトライなし）、非JSON応答時と JSONデコード失敗時の
  `SPARQLResponseFormatError`、ASK応答のbool化を検証。
- `scripts/check_endpoints.py`を実装し、4エンドポイント全てに実機から疎通確認を実施
  （`docs/endpoint_status.md`に記録、2026-07-06実施）。全エンドポイントでASK成功。
  **重要な発見**: 大LIMIT（5000）検証で、DBLP・ICCU SBN・Cervantes Virtualは要求通り
  5000行返るが、**NDL Web NDL Authoritiesは1000行までしか返らないことを実証**した
  （サーバー側result capの実例。CLAUDE.md決定事項#14、詳細は`docs/endpoint_status.md`）。
- 実装中に発見・修正した不具合: `SPARQLWrapper`の`QueryResult.info()`が返す
  `KeyCaseInsensitiveDict`は`__getitem__`のみキーを小文字化し`.get()`はオーバーライドされて
  いないため、`.info().get("Content-Type", ...)`が実機4エンドポイント全てで空文字を返す
  （＝Content-Type検証が常に失敗する）不具合を`scripts/check_endpoints.py`の実行で発見し、
  ブラケットアクセスに切り替えて修正した（`rdf2graph/sparql/client.py`の`_content_type_of`）。
  ユニットテストのモックが実際の依存ライブラリの挙動を単純化しすぎていたために検出できな
  かった箇所であり、実エンドポイントに対する疎通確認を省略しないことの実例となった。

### 未解決・据え置き事項（隠さず明記）

- ページング終了条件（`page_size`未満のページ受信を終端とみなす判定）は、サーバー側の
  result capとの区別ができない。WARNINGログによる可視化のみの**緩和策であり、根本解決では
  ない**（レビューで承認済みの既知の限界。CLAUDE.md決定事項#14）。
- `query()`の返り値が`list[dict[str, Binding]] | bool`とSELECT/ASKで型が割れている点は
  任意対応（`ask()`/`select()`への分離）として提示されたが、**未実施のまま据え置いた**。
- `tests/test_rgcn_smoke.py`は`@pytest.mark.slow`でマーキング済み（`pytest.ini`にマーカー
  登録）。デフォルトの`pytest`実行では引き続き実行される（Phase 0完了定義を満たすため）が、
  今後`pytest -m "not slow"`で高速反復時に除外できる。

## Phase 2: スキーマ偵察 + 述語プロファイラ（2026-07-06 完了）

**完了の定義**: 4エンドポイントすべてに対して`docs/profile_dblp.md`, `docs/profile_ndl_authorities.md`,
`docs/profile_iccu_sbn.md`, `docs/profile_cervantes_virtual.md`が生成され、それぞれ「主要クラス候補」
「ラベル候補プロパティ」「特徴量候補プロパティ」が記載されている。この4つのファイルの中身が互いに
大きく異なる（同じテンプレ的結果になっていない）ことを目視確認する。

根拠:
- `rdf2graph/sparql/profiler.py`（`discover_classes`, `profile_predicates`,
  `suggest_label_candidates`, `suggest_feature_candidates`, `render_profile_markdown`）を実装。
  すべて`SPARQLClient.query()`を経由し、`query_builder.py`の`iri`/`int_literal`を再利用（新しい
  HTTP呼び出し経路を追加していない）。
- `discover_classes`は`?s a ?class`のCOUNT/GROUP BYクエリで上位クラスを発見する。CLAUDE.md
  決定事項#14（NDLのLIMIT 5000→1000行の実証済みresult cap）を踏まえ、不自然に丸い数字の
  カウント（1000, 5000, 10000等の倍数）が出た場合は`ClassCandidate.suspicious=True`でマークし、
  素通ししない設計にした。
- `profile_predicates`はサブクエリで対象クラスのインスタンスを`sample_size`件（既定200）に
  固定してから`?s ?p ?o`と結合することで、主語の境目でLIMITが切れて統計が歪む問題を避けた。
  被覆率・多値判定・値の型分布・サンプル値を算出する。
- `tests/test_profiler.py`（9件、ネットワークなしで全pass）: クラス発見のパース、丸い数字の
  疑わしさ判定、被覆率/多値/値の型の計算、空サンプルの扱い、ラベル/特徴量候補の抽出ロジック、
  Markdownレンダリングの必須セクション有無を検証。
- `scripts/run_profiler.py`を実装し、4エンドポイント（DBLP, NDL Web NDL Authorities, ICCU SBN,
  Cervantes Virtual）に対して実機から実行。`data/raw/<key>/`にクエリ結果をキャッシュしつつ、
  `docs/profile_dblp.md`, `docs/profile_ndl_authorities.md`, `docs/profile_iccu_sbn.md`,
  `docs/profile_cervantes_virtual.md`を生成。4ファイルの内容を目視確認し、スキーマ・分布とも
  互いに大きく異なる（同じテンプレ的結果になっていない）ことを確認した。
- **重要な発見**（詳細はCLAUDE.md決定事項#16）: DBLPとICCU SBNでは、インスタンス数最上位の
  クラスが書誌レコードそのものではなく支援的・管理的なクラスだった（DBLP: 1位`cito:Citation`
  1.59億件 vs 書誌レコードに相当する`dblp:Publication`は6位8,625,948件。ICCU SBN: 1位
  `bibframe:Item`2,996万件 vs `bibframe:Work`は13位879万件）。NDLとCervantes Virtualでは
  上位クラスがそのまま自然な分類対象候補と一致した。この非対称性は決定事項#4（決め打ち禁止）
  の根拠を実地で裏付けるものであり、Phase 3では機械的な1位選択を採用しない。
- NDLは要求した上位20件に対し発見されたクラスが5件のみだった。丸い数字のカウントは検出されな
  かったため`suspicious`フラグは立たなかったが、`render_profile_markdown`は要求件数を下回った
  場合に警告文を出力する設計にしており、`docs/profile_ndl_authorities.md`にもその注記がある。

### 未完了・保留事項（隠さず明記）

- ICCU SBNで`bibframe:Local`/`bibframe:GenerationProcess`/`bibframe:AdminMetadata`の3クラスが
  完全に同一のインスタンス数（9,420,045件）を示した。丸い数字ではないため`discover_classes`の
  疑わしさ判定には引っかからないが、構造的な1:1生成（`bibframe:Instance`ごとに機械的に付与される
  管理用メタデータ）である可能性が高いと判断した。これらはPhase 3の`target_class`候補から
  除外する前提だが、確証はない（教員への報告時に限界として明記する）。
- **ユーザー（人間）による目視確認・承認がPhase 3着手の前提条件**（build-lod-project.md Phase 2
  完了の定義、CLAUDE.md決定事項#4）。本コミット時点ではまだユーザー確認前。

### Phase 2 追補（2026-07-06 レビュー指摘への対応）

ユーザーレビューで2点の欠陥を指摘され、修正・再実行した（詳細はCLAUDE.md決定事項#17〜#19）。

1. **述語プロファイラの対象範囲が上位5クラスに限定されていた**: 決定事項#16で発見した
   「インスタンス数1位は支援クラスであることが多い」という教訓が、対象クラス選定自体には
   活かされていなかった。`scripts/run_profiler.py`に`EXTRA_CLASSES_OF_INTEREST`を追加し、
   DBLPの`dblp:Publication`、ICCU SBNの`bibframe:Work`/`bibframe:Instance`を追加でプロファイル
   した。`profile_predicates`に`total_instance_count`引数を追加し、Markdown上で「全体X件中Y件
   サンプリング」を表示できるようにした。
2. **`suggest_label_candidates`のスコアリングが被覆率のみに依存し、カーディナリティを見て
   いなかった**: URI型というだけで無条件除外する不具合と、自由テキスト/タイムスタンプを
   誤って最上位提案する不具合の2つがあった。「値の異なり数(カーディナリティ)が値を持つ
   主語数に対して十分小さいか」を主基準にする設計に再実装し、literal/uri混在述語は
   literal側のみを判定対象にする処理も追加した。加えて、修正後の実データ確認で新たに
   「異なり値数1（実質定数値）の述語が誤って最上位に来る」不具合を発見し、
   `min_distinct_values=2`で除外するよう追加修正した。
   `tests/test_profiler.py`を全面的に書き直し（31件、ネットワークなしで全pass）。

再実行結果（`data/raw/`のキャッシュヒットにより高速）:
- NDLの`skos:Concept`で`skos:inScheme`（被覆率99%、異なり値3/104=3%）がラベル候補として
  正しく提案されるようになった（旧版はURI型というだけで無条件除外していた）。
- DBLPの`dblp:Publication`で`rdf:type`が多値（`Publication`+サブタイプ1種を同時に持つ）
  であることが確認され、`bibtexType`（異なり値2種）等の閉じた集合述語がラベル候補として
  浮上した。
- Cervantes Virtualの`Item`クラスで`dc:terms:created`（全200件が"02/02/2026"固定値、収穫日時
  スタンプと推定）が誤って最上位候補になっていたが、`min_distinct_values`修正後は除外され、
  「機械的な提案なし」に正しく変わった。

### 未解決の重要な懸念（Phase 3着手前にユーザーに判断を仰ぐ）

DBLPの`dblp:Publication`（全体8,625,948件）を200件サンプリングした結果、`rdf:type`の内訳が
`Incollection`188件（94%）に偏り、`Inproceedings`（全体の約45%相当）や`Article`（約39%相当）
が1件も現れなかった。`discover_classes`から分かる各サブタイプの全体比率と大きく乖離しており、
`profile_predicates`が使う「サブクエリ+LIMIT」方式のサンプリングが、エンドポイント側の
物理的な格納順・挿入順に相関した非ランダムな結果を返している可能性が高い。これは
Phase 2の全ての「カーディナリティに基づくラベル候補提案」の信頼性に影響しうる懸念であり、
ランダムサンプリングの導入（Phase 3設定確定時、またはPhase 4のノード抽出時）を検討するか
どうかは、ユーザーに判断を仰ぐ（詳細はCLAUDE.md決定事項#19）。

### Phase 2 追補2（2026-07-06 ラベル候補の全数集計検証）

決定事項#19のサンプリングバイアス懸念への対応として、ユーザー指示によりラベル候補述語の
値分布をGROUP BY全数集計で直接検証した（`rdf2graph/sparql/profiler.py`の`count_label_values`、
`scripts/run_label_census.py`。行単位サンプリングを一切経由しない）。結果は各
`docs/profile_*.md`の「全数集計によるラベル候補検証」節に追記（既存の200件サンプル節は
温存、決定事項#19の注記も維持）。テスト6件追加（計37件、ネットワークなしで全pass）。

主要な発見（詳細はCLAUDE.md決定事項#20）:
- **決定事項#19のサンプリングバイアスが実証に変わった**: DBLPの`bibtexType`真の分布は
  Article 50.7%+Inproceedings 45.4%で96%だが、200件サンプルにはこの2値が1件も現れず
  Incollectionが94%を占めていた。サンプル統計は分布推定に使えない。
- DBLP（8値の閉じた集合・被覆100%）とNDL（10値の閉じた集合・被覆100%）はラベルとして
  健全であることを確認し、`configs/dblp.yaml`・`configs/ndl_authorities.yaml`を確定した。
- **ICCU SBN: エイリアスTopic URI問題を発見・実証**。件数が完全一致するTopicペアは
  同一Work集合に機械的に両方付与される異表記エイリアスであることを共起カウントで確認
  （例: `convegnicongressi-`と`congressi-e-convegnicongressi-`の共起=20,539件で各件数と
  完全一致）。また上位50値合計でもWork全体の5.1%しか被覆せず、drop方式の抽出母数想定
  （2.5〜3倍）が成立しない（〜50倍必要）。
- **Cervantes Virtual: 最頻literal値が空文字列**（3,816件）。`;`連結の複合主題も多く、
  上位50値合計の被覆はWork全体の15%（〜16倍の母数が必要）。
- ICCU SBN・Cervantes Virtualの2件は「分布が想定より歪んでいた場合はconfig確定前に報告」
  というユーザーのゲート指示に該当するため、config確定を保留して報告した。

## スコープ縮小（2026-07-07、提出期限の制約により確定・ユーザー承認済み）

提出期限が数時間後に迫ったため、今回の提出は **NDL Web NDL Authorities と DBLP の2エンドポイント
のみ** で完成させる方針に変更した（CLAUDE.md決定事項#21）。ICCU SBN・Cervantes Virtualは
config確定作業も含めて着手しない。この2件は決定事項#20で判明した追加のデータ品質問題
（ICCU SBNのエイリアスTopic URI、Cervantes Virtualの空文字列最頻値・低被覆率）への対応が
Phase 3着手前にまだ残っており、残り時間で4エンドポイント全てを完走させるリスクを避けた。
これは意図的なスコープ縮小であり、限界節にそのまま明記する（隠さない）。

対象2エンドポイントの`configs/dblp.yaml`・`configs/ndl_authorities.yaml`は既に確定済み
（Phase 2追補2、決定事項#20）であり変更不要。

## Phase 3〜6: 運用モード変更（この期間限定、緊急対応）

提出期限の制約により、フェーズごとのユーザー承認待ちを省略し、Phase 3→4→5→6を自律的に連続実行する
運用に切り替えた（ユーザー承認済み）。停止条件は (a) 同一バグで3回以上連続して修正に失敗した場合、
(b) configの上限値（max_nodes/max_edges）を超える必要が生じた場合、(c) 不可逆な分岐で誤ると
致命的な場合、の3つのみ。まずNDLで通しパイプラインを完成させ、動作確認後にDBLPへconfig差し替え
だけで展開する。詳細な各フェーズの完了根拠は以降に追記する。

### Phase 3/4 設計判断の要約（詳細はCLAUDE.md決定事項#22〜#24）

- **ラベル抽出は層化サンプリング**: `count_label_values`で得たtop-kラベル値ごとの真の比率で
  `max_nodes`を按分し、値ごとに個別クエリで抽出する。素朴なLIMIT抽出は決定事項#19の
  サンプリングバイアス（DBLPで94% Incollectionに偏った実例）を再現してしまうため採用しない。
- **ラベルリーク防止**: `label.property`と`rdf:type`をPhase 4のエッジ/特徴量自動発見から
  無条件除外する（R-GCN原論文のAIFB/MUTAG前処理と同じ慣行）。

## Phase 3 完了（2026-07-07）

**完了の定義**: 2つの`configs/*.yaml`でラベル抽出を実行し、クラス分布を
`docs/label_distribution_<endpoint>.png`に出力。極端な偏り(最大クラス90%超)があればtop_k調整。

根拠:
- `rdf2graph/convert/schema.py`（`load_config`, 型付き`EndpointConfig`、値検証）+ 
  `tests/test_schema.py`（8件）。
- `rdf2graph/convert/labels.py`（`extract_labeled_nodes`, 層化抽出、`assign_label`頻度優先、
  `_allocate_per_class`按分）+ `tests/test_labels.py`（8件）。
- `scripts/run_label_extraction.py`で両エンドポイント実行。NDL・DBLPとも15,000ノード抽出成功。
  最大クラス share は NDL 70.5%（personalNames）、DBLP 51.0%（Article）で、いずれも90%未満の
  ため top_k=5 のまま確定（調整不要）。
- **実装中に発見・修正した不具合（隠さず記録）**: 初版の層化抽出は各層を単発の`LIMIT n`
  クエリで取得していたが、決定事項#14で実証済みのNDLサーバー側result cap（1応答=最大1000行）
  により、要求15,000件に対し3,438件しか取れず上位3クラスが1,000件で頭打ちになる不具合が
  実行時に発覚した。各層の取得を`client.paginate()`（OFFSETを進めて要求件数まで取得）に
  切り替えて修正し、15,000件フル取得を確認した。ユニットテストのモックがページングを
  経由しない単発クエリを想定していたため検出できなかった箇所であり、実エンドポイントでの
  実行が省略できないことの再度の実例。

## Phase 4 完了（2026-07-07）

**完了の定義**: 両エンドポイントで変換が通り`data/processed/<endpoint>/graph.pt`が生成される。
**コード変更なしで設定ファイルの差し替えだけで動いたこと**をgit diffで確認し記録する。

根拠:
- `rdf2graph/convert/graph_builder.py`（`build_graph`: VALUES句バッチでの1-hopプロパティ取得、
  `label.property`/`rdf:type`除外、object property限定エッジ、逆方向リレーション追加、
  構造特徴+文字n-gramテキスト特徴、max_edges seed固定間引き、層化train/val/test mask、
  `save_graph`/`load_graph`は`weights_only=False`明示）+ `tests/test_graph_builder.py`（4件、
  ラベルリーク除外・被覆率フィルタ・エッジ間引き・save/loadを検証）。
- `SPARQLClient`に後方互換な`method`引数（既定GET）を追加 + テスト3件追加。
- `scripts/run_graph_conversion.py`で両エンドポイント変換。**同一スクリプト・同一コードで
  ENDPOINTSのconfig差し替えのみにより両者が変換できた**（アーキテクチャ原則#1の実地証明）。
  - NDL: 総42,545ノード / 55,112エッジ / リレーション4種 / 特徴133次元 / 5クラス（抽出57.8s）。
  - DBLP: 総47,149ノード / 100,000エッジ（224,846候補から上限で間引き）/ リレーション20種 /
    特徴149次元 / 5クラス（抽出1,035.7s＝約17分、DBLPは述語数が多く低速）。
- **実装中に発見・修正した不具合（隠さず記録）**: 当初1-hopプロパティ取得を200件/バッチの
  POSTで送る設計にしたが、NDLがSPARQLWrapper経由のPOSTを`HTTP 403 Forbidden`で拒否した
  （生curlのPOST/GETは200なので、SPARQLWrapperのPOST送出形式がNDL側WAFに弾かれたと判断）。
  確実に動くGET経路に切り替え、URL長上限に収まるよう`PROPERTY_FETCH_BATCH_SIZE=60`にした
  （決定事項#23に追記）。

## Phase 5 完了（2026-07-07）

**完了の定義**: 両エンドポイントでR-GCN・多数派・特徴量のみの3モデルが動き、macro-F1が算出できる。

根拠:
- `rdf2graph/models/rgcn.py`（`RGCNClassifier` RGCNConv2層+線形ヘッド、`fit`早期終了付き、
  `predict`が予測と埋め込みを返す、GPU優先CPUフォールバック）、`majority_baseline.py`、
  `features_only_baseline.py`（ロジスティック回帰、グラフ構造不使用）+ テスト（`test_rgcn_model.py`
  2件、`test_baselines.py` 2件）。
- `rdf2graph/utils/device.py`（`select_device`、GPU優先CPUフォールバックを一元化）。

## Phase 6 完了（2026-07-07）

**完了の定義**: `docs/results_<endpoint>.md`（2本）にモデル×指標比較表・混同行列・コサイン類似度、
`docs/class_separation_summary.md`に2エンドポイント横断要約が出る。

根拠:
- `rdf2graph/eval/metrics.py`（macro-F1/balanced acc/混同行列、欠損クラスもmacroに算入）、
  `cost.py`（時間・GPU/CPUメモリ、resource非対応環境ではNone）、`embedding_similarity.py`
  （クラスセントロイド間コサイン類似度、要約統計量）+ `tests/test_eval.py`（7件）。
- `scripts/run_training_eval.py`で両エンドポイント学習・評価。`docs/results_*.md`（2本）・
  `docs/class_separation_*.png`（2枚）・`docs/class_separation_summary.md`を生成。

### 最終結果と最も重要な正直な所見

| エンドポイント | R-GCN macro-F1 | 多数派 | 特徴量のみ | クラス間平均cos類似度 |
|---|---|---|---|---|
| NDL | 0.7382 | 0.1655 | **0.7881** | 0.3837 |
| DBLP | 0.5231 | 0.1351 | **0.5821** | 0.4566 |

- **両エンドポイントで特徴量のみベースラインがR-GCNを上回った**。グラフ構造は精度に寄与せず、
  識別信号はノード自身のテキスト（ラベル/タイトルの文字n-gram）にほぼ尽きていた。これは
  決定事項#8（特徴量のみベースラインを無条件で置く）が機能して切り分けられた正直な所見であり、
  R-GCNを勝たせるためのモデル調整は意図的に行っていない（考察は`docs/report.md` 4.1節）。
- クラス分離度は NDL(0.384) < DBLP(0.457) で、NDLの方がクラスがよく分離。これはNDLの方が
  R-GCN macro-F1が高い（0.738 > 0.523）ことと整合し、この要約統計量が「クラスの分離しやすさ」
  の横断比較指標として機能することを支持する（本プロジェクトの主眼、決定事項#3）。

### 完走状況と簡略化した点（隠さない）

- **完走**: NDL・DBLPの2エンドポイントとも Phase 3→6 を通しで完走。全テスト68件pass
  （`pytest -m "not slow"`、ネットワーク不要）。
- **見送り**: ICCU SBN・Cervantes Virtual（決定事項#21、時間制約）。
- **簡略化**: (1) 変換時間スケーリング曲線（`max_nodes`を振る測定、`docs/conversion_time_scaling.png`）
  は未実施。固定規模での抽出/構築時間の内訳のみ記録した。(2) 層内サンプリング順序バイアスは
  残存（決定事項#22）。(3) グラフ構造ロバスト性・スケールアウト性・人為的不均衡下の頑健性は
  評価軸から意図的に除外（決定事項#9）。

## Phase 7 完了（2026-07-07）

- `README.md`（背景・新規性の所在・対象2件・パイプライン・実行手順・既知の限界）を全面刷新。
- `docs/report.md`（目的・関連研究・方法・結果と考察・限界の5節、最終数値反映済み）を作成。
