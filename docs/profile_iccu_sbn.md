# ICCU SBN スキーマ偵察結果

- エンドポイント: https://triplestore.iccu.sbn.it/sparql

## 主要クラス候補（インスタンス数上位）

| 順位 | クラスURI | インスタンス数(集計値) | 疑わしさ |
|---|---|---|---|
| 1 | `http://id.loc.gov/ontologies/bibframe/Item` | 29963760 | - |
| 2 | `http://id.loc.gov/ontologies/bibframe/Title` | 28436095 | - |
| 3 | `http://id.loc.gov/ontologies/bflc/AppliesTo` | 17101897 | - |
| 4 | `http://id.loc.gov/ontologies/bibframe/ProvisionActivity` | 15583290 | - |
| 5 | `http://id.loc.gov/ontologies/bibframe/Publication` | 15518029 | - |
| 6 | `http://id.loc.gov/ontologies/bibframe/Contribution` | 14247125 | - |
| 7 | `http://id.loc.gov/ontologies/bibframe/Instance` | 11213205 | - |
| 8 | `http://id.loc.gov/ontologies/bibframe/Agent` | 9616744 | - |
| 9 | `http://id.loc.gov/ontologies/bibframe/Local` | 9420045 | - |
| 10 | `http://id.loc.gov/ontologies/bibframe/GenerationProcess` | 9420045 | - |
| 11 | `http://id.loc.gov/ontologies/bibframe/AdminMetadata` | 9420045 | - |
| 12 | `http://id.loc.gov/ontologies/bibframe/Language` | 9417258 | - |
| 13 | `http://id.loc.gov/ontologies/bibframe/Work` | 8796317 | - |
| 14 | `http://id.loc.gov/ontologies/bflc/PrimaryContribution` | 8525531 | - |
| 15 | `http://id.loc.gov/ontologies/bibframe/Identifier` | 7800875 | - |
| 16 | `http://id.loc.gov/ontologies/bibframe/Note` | 7578078 | - |
| 17 | `http://www.loc.gov/mads/rdf/v1#Topic` | 6801540 | - |
| 18 | `http://id.loc.gov/ontologies/bibframe/Place` | 6344790 | - |
| 19 | `http://id.loc.gov/ontologies/bibframe/Extent` | 6200718 | - |
| 20 | `http://id.loc.gov/ontologies/bibframe/Print` | 4085749 | - |

## クラスごとの述語プロファイル

### `http://id.loc.gov/ontologies/bibframe/Item`（全体 29963760 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://id.loc.gov/ontologies/bibframe/Item(200) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 157 (78%) | Item of the library with ISIL IT-FI0098(9); Item of the library with ISIL IT-RM0267(6); Item of the library with ISIL IT-RM0117(5); Item of the library with ISIL IT-FI0101(4); Item of the library with ISIL IT-PG0109(3) |
| `http://id.loc.gov/ontologies/bibframe/heldBy` | 100% | no | uri:200 | 157 (78%) | http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-FI0098(9); http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-RM0267(6); http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-RM0117(5); http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-FI0101(4); http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-PG0109(3) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/heldBy`（被覆率 100%）

### `http://id.loc.gov/ontologies/bibframe/Title`（全体 28436095 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://id.loc.gov/ontologies/bibframe/Title(200) |
| `http://id.loc.gov/ontologies/bibframe/mainTitle` | 100% | no | literal:200 | 82 (41%) | Inferno(12); Diario accidentale di un vivente(4); <<Una >>donna di ghiaccio(4); <<1: >>Per chi inizia(4); Cime tempestose(4) |
| `http://id.loc.gov/ontologies/bflc/titleSortKey` | 70% | no | literal:141 | 1 (1%) | (141) |
| `http://id.loc.gov/ontologies/bibframe/subtitle` | 16% | yes | literal:38 | 36 (116%) | poesie(2); Ricerca religiosa e rivelazione biblica, Gesù, il Salvatore(2); Siena-Città del Vaticano 2000(1); Siena-San Miniato 22 ottobre 2000(1); 6. Convegno degli artisti(1) |
| `http://id.loc.gov/ontologies/bflc/title40MarcKey` | 3% | no | literal:6 | 6 (100%) | 24010$aWicked.$3IT\ICCU\CFI\0514006$9Barnett, Jill(1); 24010$aWuthering heights$3IT\ICCU\CFI\0041944$9Brontë, Emily(1); 24010$aChild and adolescent clinical psychopharmacology.$3IT\ICCU\CFI\0514050$9Green, Wayne Hugo(1); 24010$aClinical gynecologic endocrinology and infertility. -$3IT\ICCU\CFI\0049392$9Speroff, Leon(1); 24010$aParole scomposte$3IT\ICCU\CAG\2143896$9Di Gennaro, Antonio <1975- ; Napoli >(1) |
| `http://id.loc.gov/ontologies/bflc/title40MatchKey` | 3% | no | literal:6 | 6 (100%) | Wicked. Barnett, Jill(1); Wuthering heights Brontë, Emily(1); Child and adolescent clinical psychopharmacology. Green, Wayne Hugo(1); Clinical gynecologic endocrinology and infertility. - Speroff, Leon(1); Parole scomposte Di Gennaro, Antonio <1975- ; Napoli >(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://id.loc.gov/ontologies/bibframe/mainTitle`（被覆率 100%、異なり値数 82/200 = 41%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/mainTitle`（被覆率 100%）
- `http://id.loc.gov/ontologies/bflc/titleSortKey`（被覆率 70%）

### `http://id.loc.gov/ontologies/bflc/AppliesTo`（全体 17101897 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://id.loc.gov/ontologies/bflc/AppliesTo(200) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 162 (81%) | IT\ICCU\BIAV\085351(4); IT\ICCU\CFIV\016951(4); IT\ICCU\CFIV\008732(3); IT\ICCU\CFIV\027146(3); IT\ICCU\CFIV\114090(3) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）

### `http://id.loc.gov/ontologies/bibframe/ProvisionActivity`（全体 15583290 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:399 | 2 (1%) | http://id.loc.gov/ontologies/bibframe/ProvisionActivity(200); http://id.loc.gov/ontologies/bibframe/Publication(199) |
| `http://id.loc.gov/ontologies/bibframe/place` | 100% | yes | bnode:100, uri:101 | 2 (2%) | http://id.loc.gov/vocabulary/countries/(100); http://id.loc.gov/vocabulary/countries/herausgegeben%20von%20Richard%20Muther(1) |
| `http://id.loc.gov/ontologies/bibframe/date` | 94% | no | literal:87, typed-literal:100 | 56 (30%) | 2000(26); 2001(21); 1996(11); 1998(10); 1997(8) |
| `http://id.loc.gov/ontologies/bibframe/agent` | 49% | yes | bnode:100 | - |  |
| `http://id.loc.gov/ontologies/bibframe/note` | 8% | no | bnode:17 | - |  |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://id.loc.gov/ontologies/bibframe/ProvisionActivity`(200件); `http://id.loc.gov/ontologies/bibframe/Publication`(199件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）
- `http://id.loc.gov/ontologies/bibframe/place`（被覆率 100%、異なり値数 2/200 = 2%）
- `http://id.loc.gov/ontologies/bibframe/date`（被覆率 94%、異なり値数 56/187 = 30%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/place`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/date`（被覆率 94%）
- `http://id.loc.gov/ontologies/bibframe/agent`（被覆率 49%）

### `http://id.loc.gov/ontologies/bibframe/Publication`（全体 15518029 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | 2 (1%) | http://id.loc.gov/ontologies/bibframe/ProvisionActivity(200); http://id.loc.gov/ontologies/bibframe/Publication(200) |
| `http://id.loc.gov/ontologies/bibframe/place` | 100% | yes | bnode:101, uri:100 | 1 (1%) | http://id.loc.gov/vocabulary/countries/(100) |
| `http://id.loc.gov/ontologies/bibframe/date` | 94% | no | literal:88, typed-literal:100 | 57 (30%) | 2000(26); 2001(21); 1996(11); 1998(10); 1997(8) |
| `http://id.loc.gov/ontologies/bibframe/agent` | 50% | yes | bnode:101 | - |  |
| `http://id.loc.gov/ontologies/bibframe/note` | 8% | no | bnode:17 | - |  |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://id.loc.gov/ontologies/bibframe/ProvisionActivity`(200件); `http://id.loc.gov/ontologies/bibframe/Publication`(200件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）
- `http://id.loc.gov/ontologies/bibframe/date`（被覆率 94%、異なり値数 57/188 = 30%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/place`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/date`（被覆率 94%）
- `http://id.loc.gov/ontologies/bibframe/agent`（被覆率 50%）

### `http://id.loc.gov/ontologies/bibframe/Work`（全体 8796317 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:349 | 2 (1%) | http://id.loc.gov/ontologies/bibframe/Work(200); http://id.loc.gov/ontologies/bibframe/Text(149) |
| `http://id.loc.gov/ontologies/bibframe/hasInstance` | 100% | no | uri:200 | 200 (100%) | http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514000#Instance(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514001#Instance(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514004#Instance(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514007#Instance(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514008#Instance(1) |
| `http://id.loc.gov/ontologies/bibframe/title` | 100% | yes | bnode:422 | - |  |
| `http://id.loc.gov/ontologies/bibframe/adminMetadata` | 79% | yes | bnode:316 | - |  |
| `http://id.loc.gov/ontologies/bibframe/language` | 76% | yes | bnode:326, uri:1 | 1 (100%) | http://id.loc.gov/vocabulary/languages/Sammlung%20illustrierter%20Monographien(1) |
| `http://id.loc.gov/ontologies/bibframe/content` | 74% | no | uri:149 | 1 (1%) | http://id.loc.gov/vocabulary/contentTypes/txt(149) |
| `http://id.loc.gov/ontologies/bibframe/contribution` | 70% | yes | bnode:342 | - |  |
| `http://id.loc.gov/ontologies/bibframe/subject` | 36% | yes | uri:221 | 170 (239%) | http://triplestore.iccu.sbn.it/resource/Topic/pubblicazioni-periodicheperiodici-(17); http://triplestore.iccu.sbn.it/resource/Topic/rivisteperiodici-(17); http://triplestore.iccu.sbn.it/resource/Topic/mostreesposizioni-(4); http://triplestore.iccu.sbn.it/resource/Topic/851-92poesia-italiana-2000-21-(3); http://triplestore.iccu.sbn.it/resource/Topic/arti-figurativearte-(2) |
| `http://id.loc.gov/ontologies/bibframe/notation` | 17% | no | uri:34 | 1 (3%) | http://id.loc.gov/vocabulary/mscript/b(34) |
| `http://id.loc.gov/ontologies/bibframe/hasSeries` | 14% | no | uri:27 | 27 (100%) | http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514004#Work760-10(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514055#Work760-10(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514064#Work760-11(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514065#Work760-11(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514070#Work760-11(1) |
| `http://id.loc.gov/ontologies/bibframe/note` | 10% | yes | bnode:42 | - |  |
| `http://id.loc.gov/ontologies/bibframe/expressionOf` | 8% | no | uri:17 | 17 (100%) | http://triplestore.iccu.sbn.it/resource/UniformTitle/IT-ICCU-CFI-0514006(1); http://triplestore.iccu.sbn.it/resource/UniformTitle/IT-ICCU-CAG-2143896(1); http://triplestore.iccu.sbn.it/resource/UniformTitle/IT-ICCU-CAG-2143899(1); http://triplestore.iccu.sbn.it/resource/UniformTitle/IT-ICCU-CFI-0514105(1); http://triplestore.iccu.sbn.it/resource/UniformTitle/IT-ICCU-IEI-0110821(1) |
| `http://id.loc.gov/ontologies/bibframe/partOf` | 7% | no | uri:14 | 10 (71%) | http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFIV-008732#Work(3); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFIV-114090#Work(2); http://triplestore.iccu.sbn.it/resource/IT-ICCU-SBLV-075217#Work(2); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFIV-190344#Work(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-BIAV-085351#Work(1) |
| `http://id.loc.gov/ontologies/bibframe/identifiedBy` | 2% | yes | bnode:12 | - |  |
| `http://id.loc.gov/ontologies/bflc/appliesTo` | 2% | yes | bnode:6 | - |  |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://id.loc.gov/ontologies/bibframe/Work`(200件); `http://id.loc.gov/ontologies/bibframe/Text`(149件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/hasInstance`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/title`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/adminMetadata`（被覆率 79%）
- `http://id.loc.gov/ontologies/bibframe/language`（被覆率 76%）
- `http://id.loc.gov/ontologies/bibframe/content`（被覆率 74%）
- `http://id.loc.gov/ontologies/bibframe/contribution`（被覆率 70%）
- `http://id.loc.gov/ontologies/bibframe/subject`（被覆率 36%）

### `http://id.loc.gov/ontologies/bibframe/Instance`（全体 11213205 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:344 | 2 (1%) | http://id.loc.gov/ontologies/bibframe/Instance(200); http://id.loc.gov/ontologies/bibframe/Print(144) |
| `http://id.loc.gov/ontologies/bibframe/instanceOf` | 100% | no | uri:200 | 200 (100%) | http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514002#Work(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514003#Work(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514005#Work(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514010#Work(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514019#Work(1) |
| `http://id.loc.gov/ontologies/bibframe/title` | 100% | yes | bnode:400 | - |  |
| `http://id.loc.gov/ontologies/bibframe/provisionActivity` | 78% | yes | bnode:618 | - |  |
| `http://id.loc.gov/ontologies/bibframe/issuance` | 78% | no | uri:155 | 2 (1%) | http://id.loc.gov/vocabulary/issuance/mono(117); http://id.loc.gov/vocabulary/issuance/serl(38) |
| `http://id.loc.gov/ontologies/bibframe/extent` | 74% | yes | bnode:294 | - |  |
| `http://id.loc.gov/ontologies/bibframe/hasItem` | 74% | yes | uri:1098 | 1098 (747%) | http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514002/Item/FI0098(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514002/Item/PG0109(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514002/Item/RM0117(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514002/Item/RM0267(1); http://triplestore.iccu.sbn.it/resource/IT-ICCU-CFI-0514003/Item/FI0098(1) |
| `http://id.loc.gov/ontologies/bibframe/dimensions` | 73% | no | literal:146 | 41 (28%) | 30 cm(13); 24 cm.(12); 21 cm.(11); 24 cm(10); 26 cm.(8) |
| `http://id.loc.gov/ontologies/bibframe/carrier` | 72% | no | uri:144 | 1 (1%) | http://id.loc.gov/vocabulary/carriers/nc(144) |
| `http://id.loc.gov/ontologies/bibframe/media` | 57% | no | uri:114 | 1 (1%) | http://id.loc.gov/vocabulary/mediaTypes/n(114) |
| `http://id.loc.gov/ontologies/bibframe/responsibilityStatement` | 55% | no | literal:110 | 101 (92%) | E. Beniamino Stumpo, M. Teresa Tonelli(3); Dante Alighieri(3); Marcello Sensini(3); Ettore Quaglia, Fausto Mazza(2); Giuseppe Cionchi(2) |
| `http://id.loc.gov/ontologies/bibframe/note` | 46% | yes | bnode:332 | - |  |
| `http://id.loc.gov/ontologies/bibframe/identifiedBy` | 26% | yes | bnode:106 | - |  |
| `http://id.loc.gov/ontologies/bflc/appliesTo` | 1% | yes | bnode:4 | - |  |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://id.loc.gov/ontologies/bibframe/Instance`(200件); `http://id.loc.gov/ontologies/bibframe/Print`(144件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）
- `http://id.loc.gov/ontologies/bibframe/issuance`（被覆率 78%、異なり値数 2/155 = 1%）
- `http://id.loc.gov/ontologies/bibframe/dimensions`（被覆率 73%、異なり値数 41/146 = 28%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/instanceOf`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/title`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/provisionActivity`（被覆率 78%）
- `http://id.loc.gov/ontologies/bibframe/issuance`（被覆率 78%）
- `http://id.loc.gov/ontologies/bibframe/extent`（被覆率 74%）
- `http://id.loc.gov/ontologies/bibframe/hasItem`（被覆率 74%）
- `http://id.loc.gov/ontologies/bibframe/dimensions`（被覆率 73%）
- `http://id.loc.gov/ontologies/bibframe/carrier`（被覆率 72%）
- `http://id.loc.gov/ontologies/bibframe/media`（被覆率 57%）
- `http://id.loc.gov/ontologies/bibframe/responsibilityStatement`（被覆率 55%）
- `http://id.loc.gov/ontologies/bibframe/note`（被覆率 46%）

---
**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」はPhase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。
