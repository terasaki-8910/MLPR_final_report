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

## 次のフェーズ

Phase 2完了。ユーザーによる`docs/profile_*.md`の目視確認・対象クラス候補の承認を待ってから
Phase 3（設定ファイルとラベル抽出）に進む。
