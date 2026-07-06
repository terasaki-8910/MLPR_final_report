# エンドポイント疎通確認結果

`scripts/check_endpoints.py` の実行結果。教員の実行環境ではネットワーク到達性が異なる可能性があるため、教員自身の環境でも再実行して確認することを推奨する。

**既知の未解決の限界（指摘#5）**: `SPARQLClient.paginate` のページング終了条件は「ページが`page_size`未満なら終了」であり、これは真の終端とサーバー側のresult cap（例: 一部トリプルストアが課す暗黙の上限）を区別できない。以下の`LIMIT 5000`検証は、この規模でサーバーが要求件数をそのまま返すかを実地確認するものであり、この限界自体を解消するものではない。`paginate`はページが短い場合にWARNINGログを出すのみの**緩和策であり、根本解決ではない**。

| エンドポイント | ASK | 応答時間 | LIMIT 5000検証 | 応答時間 |
|---|---|---|---|---|
| DBLP (https://sparql.dblp.org/sparql) | OK | 1.00s | LIMIT 5000 -> 5000行 (要求通り) | 2.57s |
| NDL Web NDL Authorities (https://id.ndl.go.jp/auth/ndla/sparql) | OK | 0.10s | LIMIT 5000 -> 1000行 (**要求件数と不一致 -- サーバー側capの可能性**) | 0.10s |
| ICCU SBN (https://triplestore.iccu.sbn.it/sparql) | OK | 1.43s | LIMIT 5000 -> 5000行 (要求通り) | 2.97s |
| Cervantes Virtual (https://data.cervantesvirtual.com/sparql) | OK | 1.11s | LIMIT 5000 -> 5000行 (要求通り) | 1.55s |

## 重要な発見: NDLは実際にサーバー側result capを持つ

上記の検証は仮説ではなく実際に踏んだ。**NDL Web NDL Authoritiesは`LIMIT 5000`を要求しても`1000`行しか返さない。** これは上記「既知の未解決の限界」で懸念していたサーバー側result capが、対象4エンドポイントのうち少なくとも1件（NDL）で実在することを意味する。

Phase 3でNDL用の`configs/ndl_authorities.yaml`の`sampling.page_size`を確定する際は、**1000を超える値を指定しても無言で1000件に切り詰められる**ことを前提にする（`page_size`は1000以下にするか、1000超を指定した場合にこの実測結果を踏まえて警告する運用にする）。他3エンドポイント（DBLP, ICCU SBN, Cervantes Virtual）はLIMIT 5000まで要求通り返すことを確認済みだが、`sampling.max_nodes`（最大15,000〜20,000）に至るまでの間にさらに小さいcapが存在しないことまでは保証されない。
