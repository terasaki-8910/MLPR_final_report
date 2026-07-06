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

## 次のフェーズ

Phase 2完了。configs確定状況: dblp/ndl_authorities=確定済み、iccu_sbn/cervantes_virtual=
全数集計で判明した問題（エイリアスURI・低被覆・空文字列）についてユーザーの判断待ち。
判断が出次第、残り2configを確定してPhase 3（ラベル抽出実装）に進む。
