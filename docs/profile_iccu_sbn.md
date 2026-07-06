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

### `http://id.loc.gov/ontologies/bibframe/Item`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://id.loc.gov/ontologies/bibframe/Item; http://id.loc.gov/ontologies/bibframe/Item; http://id.loc.gov/ontologies/bibframe/Item; http://id.loc.gov/ontologies/bibframe/Item; http://id.loc.gov/ontologies/bibframe/Item |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | Item of the library with ISIL IT-AN0009; Item of the library with ISIL IT-AV0004; Item of the library with ISIL IT-BA0129; Item of the library with ISIL IT-BN0010; Item of the library with ISIL IT-BR0029 |
| `http://id.loc.gov/ontologies/bibframe/heldBy` | 100% | no | uri:200 | http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-AN0009; http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-AV0004; http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-BA0129; http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-BN0010; http://dati.beniculturali.it/iccu/anagrafe/resource/Library/IT-BR0029 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/heldBy`（被覆率 100%）

### `http://id.loc.gov/ontologies/bibframe/Title`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://id.loc.gov/ontologies/bibframe/Title; http://id.loc.gov/ontologies/bibframe/Title; http://id.loc.gov/ontologies/bibframe/Title; http://id.loc.gov/ontologies/bibframe/Title; http://id.loc.gov/ontologies/bibframe/Title |
| `http://id.loc.gov/ontologies/bibframe/mainTitle` | 100% | no | literal:200 | Concorso per la realizzazione della statua di santa Caterina da Siena; Concorso per la realizzazione della statua di santa Caterina da Siena; Franco Angeli; Franco Angeli; Concorso per il ciborio della Chiesa del Corpus Domini in San Miniato di Siena |
| `http://id.loc.gov/ontologies/bflc/titleSortKey` | 70% | no | literal:141 | ; ; ; ;  |
| `http://id.loc.gov/ontologies/bibframe/subtitle` | 16% | yes | literal:38 | Siena-Città del Vaticano 2000; Siena-San Miniato 22 ottobre 2000; 6. Convegno degli artisti; Torrenieri-Montalcino dal 23 al 30 settembre 2000; semestrale di informazione del Comprensorio alpino di Morbegno |
| `http://id.loc.gov/ontologies/bflc/title40MarcKey` | 3% | no | literal:6 | 24010$aWicked.$3IT\ICCU\CFI\0514006$9Barnett, Jill; 24010$aWuthering heights$3IT\ICCU\CFI\0041944$9Brontë, Emily; 24010$aChild and adolescent clinical psychopharmacology.$3IT\ICCU\CFI\0514050$9Green, Wayne Hugo; 24010$aClinical gynecologic endocrinology and infertility. -$3IT\ICCU\CFI\0049392$9Speroff, Leon; 24010$aParole scomposte$3IT\ICCU\CAG\2143896$9Di Gennaro, Antonio <1975- ; Napoli > |
| `http://id.loc.gov/ontologies/bflc/title40MatchKey` | 3% | no | literal:6 | Wicked. Barnett, Jill; Wuthering heights Brontë, Emily; Child and adolescent clinical psychopharmacology. Green, Wayne Hugo; Clinical gynecologic endocrinology and infertility. - Speroff, Leon; Parole scomposte Di Gennaro, Antonio <1975- ; Napoli > |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://id.loc.gov/ontologies/bibframe/mainTitle`（被覆率 100%）
- `http://id.loc.gov/ontologies/bflc/titleSortKey`（被覆率 70%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/mainTitle`（被覆率 100%）
- `http://id.loc.gov/ontologies/bflc/titleSortKey`（被覆率 70%）

### `http://id.loc.gov/ontologies/bflc/AppliesTo`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://id.loc.gov/ontologies/bflc/AppliesTo; http://id.loc.gov/ontologies/bflc/AppliesTo; http://id.loc.gov/ontologies/bflc/AppliesTo; http://id.loc.gov/ontologies/bflc/AppliesTo; http://id.loc.gov/ontologies/bflc/AppliesTo |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | IT\ICCU\BVEC\174736; IT\ICCU\CFIC\120996; IT\ICCU\MILV\123126; IT\ICCU\BVEC\174626; IT\ICCU\CFIV\190337 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）

### `http://id.loc.gov/ontologies/bibframe/ProvisionActivity`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:399 | http://id.loc.gov/ontologies/bibframe/ProvisionActivity; http://id.loc.gov/ontologies/bibframe/Publication; http://id.loc.gov/ontologies/bibframe/ProvisionActivity; http://id.loc.gov/ontologies/bibframe/Publication; http://id.loc.gov/ontologies/bibframe/ProvisionActivity |
| `http://id.loc.gov/ontologies/bibframe/place` | 100% | yes | bnode:100, uri:101 | http://id.loc.gov/vocabulary/countries/; nodeID://b175136030; http://id.loc.gov/vocabulary/countries/; nodeID://b175136054; http://id.loc.gov/vocabulary/countries/ |
| `http://id.loc.gov/ontologies/bibframe/date` | 94% | no | literal:87, typed-literal:100 | 2000; 2000!; 2001; \2001!; 2000 |
| `http://id.loc.gov/ontologies/bibframe/agent` | 49% | yes | bnode:100 | nodeID://b175136031; nodeID://b175136055; nodeID://b175136099; nodeID://b175136125; nodeID://b175136147 |
| `http://id.loc.gov/ontologies/bibframe/note` | 8% | no | bnode:17 | nodeID://b175136216; nodeID://b175136465; nodeID://b175136515; nodeID://b175136645; nodeID://b175136776 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/place`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/date`（被覆率 94%）
- `http://id.loc.gov/ontologies/bibframe/agent`（被覆率 49%）

### `http://id.loc.gov/ontologies/bibframe/Publication`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | http://id.loc.gov/ontologies/bibframe/ProvisionActivity; http://id.loc.gov/ontologies/bibframe/Publication; http://id.loc.gov/ontologies/bibframe/ProvisionActivity; http://id.loc.gov/ontologies/bibframe/Publication; http://id.loc.gov/ontologies/bibframe/ProvisionActivity |
| `http://id.loc.gov/ontologies/bibframe/place` | 100% | yes | bnode:101, uri:100 | http://id.loc.gov/vocabulary/countries/; nodeID://b175136030; http://id.loc.gov/vocabulary/countries/; nodeID://b175136054; http://id.loc.gov/vocabulary/countries/ |
| `http://id.loc.gov/ontologies/bibframe/date` | 94% | no | literal:88, typed-literal:100 | 2000; 2000!; 2001; \2001!; 2000 |
| `http://id.loc.gov/ontologies/bibframe/agent` | 50% | yes | bnode:101 | nodeID://b175136031; nodeID://b175136055; nodeID://b175136099; nodeID://b175136125; nodeID://b175136147 |
| `http://id.loc.gov/ontologies/bibframe/note` | 8% | no | bnode:17 | nodeID://b175136216; nodeID://b175136465; nodeID://b175136515; nodeID://b175136645; nodeID://b175136776 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/place`（被覆率 100%）
- `http://id.loc.gov/ontologies/bibframe/date`（被覆率 94%）
- `http://id.loc.gov/ontologies/bibframe/agent`（被覆率 50%）

---
**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」はPhase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。
