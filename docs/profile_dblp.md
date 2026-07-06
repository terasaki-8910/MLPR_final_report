# DBLP スキーマ偵察結果

- エンドポイント: https://sparql.dblp.org/sparql

## 主要クラス候補（インスタンス数上位）

| 順位 | クラスURI | インスタンス数(集計値) | 疑わしさ |
|---|---|---|---|
| 1 | `http://purl.org/spar/cito/Citation` | 159037418 | - |
| 2 | `https://dblp.org/rdf/schema#Signature` | 29725147 | - |
| 3 | `https://dblp.org/rdf/schema#AuthorSignature` | 29557046 | - |
| 4 | `http://purl.org/spar/datacite/Identifier` | 28242960 | - |
| 5 | `http://purl.org/spar/datacite/ResourceIdentifier` | 22708597 | - |
| 6 | `https://dblp.org/rdf/schema#Publication` | 8625948 | - |
| 7 | `http://purl.org/spar/cito/AuthorSelfCitation` | 4841829 | - |
| 8 | `http://purl.org/spar/cito/JournalSelfCitation` | 4817575 | - |
| 9 | `http://purl.org/spar/datacite/PersonalIdentifier` | 4497852 | - |
| 10 | `https://dblp.org/rdf/schema#Creator` | 4137866 | - |
| 11 | `https://dblp.org/rdf/schema#Person` | 4104016 | - |
| 12 | `https://dblp.org/rdf/schema#Inproceedings` | 3910938 | - |
| 13 | `https://dblp.org/rdf/schema#Article` | 3381776 | - |
| 14 | `https://dblp.org/rdf/schema#Informal` | 979612 | - |
| 15 | `https://dblp.org/rdf/schema#Book` | 175109 | - |
| 16 | `https://dblp.org/rdf/schema#EditorSignature` | 168101 | - |
| 17 | `https://dblp.org/rdf/schema#Editorship` | 67281 | - |
| 18 | `https://dblp.org/rdf/schema#Incollection` | 43741 | - |
| 19 | `https://dblp.org/rdf/schema#AmbiguousCreator` | 33316 | - |
| 20 | `https://dblp.org/rdf/schema#Reference` | 27366 | - |

## クラスごとの述語プロファイル

### `http://purl.org/spar/cito/Citation`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://purl.org/spar/cito/hasCitationCreationDate` | 100% | no | literal:200 | 2020; 2020; 2020; 2020; 2020 |
| `http://purl.org/spar/cito/hasCitedEntity` | 100% | no | uri:200 | https://w3id.org/oc/meta/br/062402991015; https://w3id.org/oc/meta/br/06601731044; https://w3id.org/oc/meta/br/06603741616; https://w3id.org/oc/meta/br/06704279944; https://w3id.org/oc/meta/br/0690789407 |
| `http://purl.org/spar/cito/hasCitingEntity` | 100% | no | uri:200 | https://w3id.org/oc/meta/br/0601000; https://w3id.org/oc/meta/br/0601000; https://w3id.org/oc/meta/br/0601000; https://w3id.org/oc/meta/br/0601000; https://w3id.org/oc/meta/br/0601000 |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:209 | http://purl.org/spar/cito/Citation; http://purl.org/spar/cito/Citation; http://purl.org/spar/cito/Citation; http://purl.org/spar/cito/Citation; http://purl.org/spar/cito/Citation |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | oci:0601000-062402991015; oci:0601000-06601731044; oci:0601000-06603741616; oci:0601000-06704279944; oci:0601000-0690789407 |
| `http://purl.org/spar/cito/hasCitationTimeSpan` | 90% | no | literal:179 | P9Y; P1Y; P15Y; P6Y; P8Y |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitationCreationDate`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitationTimeSpan`（被覆率 90%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://purl.org/spar/cito/hasCitationCreationDate`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitedEntity`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitingEntity`（被覆率 100%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitationTimeSpan`（被覆率 90%）

### `https://dblp.org/rdf/schema#Signature`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | https://dblp.org/rdf/schema#AuthorSignature; https://dblp.org/rdf/schema#Signature; https://dblp.org/rdf/schema#AuthorSignature; https://dblp.org/rdf/schema#Signature; https://dblp.org/rdf/schema#AuthorSignature |
| `https://dblp.org/rdf/schema#signatureCreator` | 100% | no | uri:200 | https://dblp.org/pid/21/829; https://dblp.org/pid/10/5696; https://dblp.org/pid/29/5566; https://dblp.org/pid/83/6470; https://dblp.org/pid/13/3413 |
| `https://dblp.org/rdf/schema#signatureDblpName` | 100% | no | literal:200 | Ernesto G. Birgin; José Mario Martínez; Yannis Marinakis; Dukwon Kim; Magdalene Marinaki |
| `https://dblp.org/rdf/schema#signatureOrdinal` | 100% | no | literal:200 | 1; 2; 1; 1; 1 |
| `https://dblp.org/rdf/schema#signaturePublication` | 100% | no | uri:200 | https://dblp.org/rec/reference/opt/BirginM09; https://dblp.org/rec/reference/opt/BirginM09; https://dblp.org/rec/reference/opt/Marinakis09a; https://dblp.org/rec/reference/opt/Kim09; https://dblp.org/rec/reference/opt/Marinaki09 |
| `https://dblp.org/rdf/schema#signatureOrcid` | 8% | no | uri:17 | https://orcid.org/0000-0002-7466-7663; https://orcid.org/0000-0003-3875-4441; https://orcid.org/0000-0002-7466-7663; https://orcid.org/0000-0003-3085-0084; https://orcid.org/0000-0003-4522-5804 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `https://dblp.org/rdf/schema#signatureDblpName`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureCreator`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureDblpName`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%）
- `https://dblp.org/rdf/schema#signaturePublication`（被覆率 100%）

### `https://dblp.org/rdf/schema#AuthorSignature`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | https://dblp.org/rdf/schema#AuthorSignature; https://dblp.org/rdf/schema#Signature; https://dblp.org/rdf/schema#AuthorSignature; https://dblp.org/rdf/schema#Signature; https://dblp.org/rdf/schema#AuthorSignature |
| `https://dblp.org/rdf/schema#signatureCreator` | 100% | no | uri:200 | https://dblp.org/pid/21/829; https://dblp.org/pid/10/5696; https://dblp.org/pid/29/5566; https://dblp.org/pid/83/6470; https://dblp.org/pid/13/3413 |
| `https://dblp.org/rdf/schema#signatureDblpName` | 100% | no | literal:200 | Ernesto G. Birgin; José Mario Martínez; Yannis Marinakis; Dukwon Kim; Magdalene Marinaki |
| `https://dblp.org/rdf/schema#signatureOrdinal` | 100% | no | literal:200 | 1; 2; 1; 1; 1 |
| `https://dblp.org/rdf/schema#signaturePublication` | 100% | no | uri:200 | https://dblp.org/rec/reference/opt/BirginM09; https://dblp.org/rec/reference/opt/BirginM09; https://dblp.org/rec/reference/opt/Marinakis09a; https://dblp.org/rec/reference/opt/Kim09; https://dblp.org/rec/reference/opt/Marinaki09 |
| `https://dblp.org/rdf/schema#signatureOrcid` | 8% | no | uri:17 | https://orcid.org/0000-0002-7466-7663; https://orcid.org/0000-0003-3875-4441; https://orcid.org/0000-0002-7466-7663; https://orcid.org/0000-0003-3085-0084; https://orcid.org/0000-0003-4522-5804 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `https://dblp.org/rdf/schema#signatureDblpName`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureCreator`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureDblpName`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%）
- `https://dblp.org/rdf/schema#signaturePublication`（被覆率 100%）

### `http://purl.org/spar/datacite/Identifier`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://purl.org/spar/datacite/usesIdentifierScheme` | 100% | no | uri:200 | http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid |
| `http://purl.org/spar/literal/hasLiteralValue` | 100% | no | literal:200 | br/0660866885; br/06603776706; br/06170444432; br/061803984117; br/06603785366 |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | http://purl.org/spar/datacite/Identifier; http://purl.org/spar/datacite/ResourceIdentifier; http://purl.org/spar/datacite/Identifier; http://purl.org/spar/datacite/ResourceIdentifier; http://purl.org/spar/datacite/Identifier |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://purl.org/spar/literal/hasLiteralValue`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://purl.org/spar/datacite/usesIdentifierScheme`（被覆率 100%）
- `http://purl.org/spar/literal/hasLiteralValue`（被覆率 100%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）

### `http://purl.org/spar/datacite/ResourceIdentifier`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://purl.org/spar/datacite/usesIdentifierScheme` | 100% | no | uri:200 | http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid; http://purl.org/spar/datacite/omid |
| `http://purl.org/spar/literal/hasLiteralValue` | 100% | no | literal:200 | br/0660866885; br/06603776706; br/06170444432; br/061803984117; br/06603785366 |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | http://purl.org/spar/datacite/Identifier; http://purl.org/spar/datacite/ResourceIdentifier; http://purl.org/spar/datacite/Identifier; http://purl.org/spar/datacite/ResourceIdentifier; http://purl.org/spar/datacite/Identifier |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://purl.org/spar/literal/hasLiteralValue`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://purl.org/spar/datacite/usesIdentifierScheme`（被覆率 100%）
- `http://purl.org/spar/literal/hasLiteralValue`（被覆率 100%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）

---
**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」はPhase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。
