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

## 次のフェーズ

Phase 2（スキーマ偵察 + 述語プロファイラ）に進む。`query_builder.py`を再利用し、対象クラス・
ラベルプロパティのURIをここで初めて実地探索・確定する（決め打ち禁止、CLAUDE.md決定事項#4）。
