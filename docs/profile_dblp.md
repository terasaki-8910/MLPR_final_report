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

### `http://purl.org/spar/cito/Citation`（全体 159037418 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://purl.org/spar/cito/hasCitationCreationDate` | 100% | no | literal:200 | 11 (6%) | 2025-08(43); 2025-05(37); 2025-05-04(32); 2025-04-29(31); 2025-05-05(27) |
| `http://purl.org/spar/cito/hasCitedEntity` | 100% | no | uri:200 | 200 (100%) | https://w3id.org/oc/meta/br/062402991015(1); https://w3id.org/oc/meta/br/06601731044(1); https://w3id.org/oc/meta/br/06603741616(1); https://w3id.org/oc/meta/br/06704279944(1); https://w3id.org/oc/meta/br/0690789407(1) |
| `http://purl.org/spar/cito/hasCitingEntity` | 100% | no | uri:200 | 18 (9%) | https://w3id.org/oc/meta/br/06010000349(37); https://w3id.org/oc/meta/br/06010000339(32); https://w3id.org/oc/meta/br/06010000327(31); https://w3id.org/oc/meta/br/06010000343(27); https://w3id.org/oc/meta/br/06010000344(16) |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:209 | 3 (2%) | http://purl.org/spar/cito/Citation(200); http://purl.org/spar/cito/AuthorSelfCitation(5); http://purl.org/spar/cito/JournalSelfCitation(4) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 200 (100%) | oci:0601000-062402991015(1); oci:0601000-06601731044(1); oci:0601000-06603741616(1); oci:0601000-06704279944(1); oci:0601000-0690789407(1) |
| `http://purl.org/spar/cito/hasCitationTimeSpan` | 90% | no | literal:179 | 133 (74%) | P4Y(5); P3Y(4); P1Y6M(4); P1Y11M(4); P6Y(3) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://purl.org/spar/cito/Citation`(200件); `http://purl.org/spar/cito/AuthorSelfCitation`(5件); `http://purl.org/spar/cito/JournalSelfCitation`(4件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 3/200 = 2%）
- `http://purl.org/spar/cito/hasCitationCreationDate`（被覆率 100%、異なり値数 11/200 = 6%）
- `http://purl.org/spar/cito/hasCitingEntity`（被覆率 100%、異なり値数 18/200 = 9%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://purl.org/spar/cito/hasCitationCreationDate`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitedEntity`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitingEntity`（被覆率 100%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/spar/cito/hasCitationTimeSpan`（被覆率 90%）

### `https://dblp.org/rdf/schema#Signature`（全体 29725147 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | 2 (1%) | https://dblp.org/rdf/schema#AuthorSignature(200); https://dblp.org/rdf/schema#Signature(200) |
| `https://dblp.org/rdf/schema#signatureCreator` | 100% | no | uri:200 | 165 (82%) | https://dblp.org/pid/85/5741(11); https://dblp.org/pid/02/7149(3); https://dblp.org/pid/45/4576(3); https://dblp.org/pid/19/1671(3); https://dblp.org/pid/21/829(2) |
| `https://dblp.org/rdf/schema#signatureDblpName` | 100% | no | literal:200 | 165 (82%) | Christodoulos A. Floudas(11); Marianthi G. Ierapetritou(3); Stacy L. Janak(3); Tapio Westerlund(3); Ernesto G. Birgin(2) |
| `https://dblp.org/rdf/schema#signatureOrdinal` | 100% | no | literal:200 | 4 (2%) | 1(135); 2(54); 3(9); 4(2) |
| `https://dblp.org/rdf/schema#signaturePublication` | 100% | no | uri:200 | 135 (68%) | https://dblp.org/rec/reference/opt/PistikopoulosFSR09(4); https://dblp.org/rec/reference/opt/KumarVJA09(4); https://dblp.org/rec/reference/opt/RajgariaMF09(3); https://dblp.org/rec/reference/opt/Ben-TalNZ09(3); https://dblp.org/rec/reference/opt/AlkayaVB09(3) |
| `https://dblp.org/rdf/schema#signatureOrcid` | 8% | no | uri:17 | 14 (82%) | https://orcid.org/0000-0002-7466-7663(2); https://orcid.org/0000-0001-9199-2110(2); https://orcid.org/0000-0002-7861-7380(2); https://orcid.org/0000-0003-3875-4441(1); https://orcid.org/0000-0003-3085-0084(1) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `https://dblp.org/rdf/schema#AuthorSignature`(200件); `https://dblp.org/rdf/schema#Signature`(200件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%、異なり値数 4/200 = 2%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureCreator`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureDblpName`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%）
- `https://dblp.org/rdf/schema#signaturePublication`（被覆率 100%）

### `https://dblp.org/rdf/schema#AuthorSignature`（全体 29557046 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | 2 (1%) | https://dblp.org/rdf/schema#AuthorSignature(200); https://dblp.org/rdf/schema#Signature(200) |
| `https://dblp.org/rdf/schema#signatureCreator` | 100% | no | uri:200 | 165 (82%) | https://dblp.org/pid/85/5741(11); https://dblp.org/pid/02/7149(3); https://dblp.org/pid/45/4576(3); https://dblp.org/pid/19/1671(3); https://dblp.org/pid/21/829(2) |
| `https://dblp.org/rdf/schema#signatureDblpName` | 100% | no | literal:200 | 165 (82%) | Christodoulos A. Floudas(11); Marianthi G. Ierapetritou(3); Stacy L. Janak(3); Tapio Westerlund(3); Ernesto G. Birgin(2) |
| `https://dblp.org/rdf/schema#signatureOrdinal` | 100% | no | literal:200 | 4 (2%) | 1(135); 2(54); 3(9); 4(2) |
| `https://dblp.org/rdf/schema#signaturePublication` | 100% | no | uri:200 | 135 (68%) | https://dblp.org/rec/reference/opt/PistikopoulosFSR09(4); https://dblp.org/rec/reference/opt/KumarVJA09(4); https://dblp.org/rec/reference/opt/RajgariaMF09(3); https://dblp.org/rec/reference/opt/Ben-TalNZ09(3); https://dblp.org/rec/reference/opt/AlkayaVB09(3) |
| `https://dblp.org/rdf/schema#signatureOrcid` | 8% | no | uri:17 | 14 (82%) | https://orcid.org/0000-0002-7466-7663(2); https://orcid.org/0000-0001-9199-2110(2); https://orcid.org/0000-0002-7861-7380(2); https://orcid.org/0000-0003-3875-4441(1); https://orcid.org/0000-0003-3085-0084(1) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `https://dblp.org/rdf/schema#AuthorSignature`(200件); `https://dblp.org/rdf/schema#Signature`(200件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%、異なり値数 4/200 = 2%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureCreator`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureDblpName`（被覆率 100%）
- `https://dblp.org/rdf/schema#signatureOrdinal`（被覆率 100%）
- `https://dblp.org/rdf/schema#signaturePublication`（被覆率 100%）

### `http://purl.org/spar/datacite/Identifier`（全体 28242960 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://purl.org/spar/datacite/usesIdentifierScheme` | 100% | no | uri:200 | 1 (0%) | http://purl.org/spar/datacite/omid(200) |
| `http://purl.org/spar/literal/hasLiteralValue` | 100% | no | literal:200 | 196 (98%) | br/06011086790(2); br/0609551616(2); br/06010965654(2); br/06012168173(2); br/0660866885(1) |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | 2 (1%) | http://purl.org/spar/datacite/Identifier(200); http://purl.org/spar/datacite/ResourceIdentifier(200) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://purl.org/spar/datacite/Identifier`(200件); `http://purl.org/spar/datacite/ResourceIdentifier`(200件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://purl.org/spar/datacite/usesIdentifierScheme`（被覆率 100%）
- `http://purl.org/spar/literal/hasLiteralValue`（被覆率 100%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）

### `http://purl.org/spar/datacite/ResourceIdentifier`（全体 22708597 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://purl.org/spar/datacite/usesIdentifierScheme` | 100% | no | uri:200 | 1 (0%) | http://purl.org/spar/datacite/omid(200) |
| `http://purl.org/spar/literal/hasLiteralValue` | 100% | no | literal:200 | 196 (98%) | br/06011086790(2); br/0609551616(2); br/06010965654(2); br/06012168173(2); br/0660866885(1) |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | 2 (1%) | http://purl.org/spar/datacite/Identifier(200); http://purl.org/spar/datacite/ResourceIdentifier(200) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://purl.org/spar/datacite/Identifier`(200件); `http://purl.org/spar/datacite/ResourceIdentifier`(200件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 2/200 = 1%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://purl.org/spar/datacite/usesIdentifierScheme`（被覆率 100%）
- `http://purl.org/spar/literal/hasLiteralValue`（被覆率 100%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）

### `https://dblp.org/rdf/schema#Publication`（全体 8625948 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://purl.org/spar/datacite/hasIdentifier` | 100% | yes | bnode:597 | - |  |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:400 | 4 (2%) | https://dblp.org/rdf/schema#Publication(200); https://dblp.org/rdf/schema#Incollection(188); https://dblp.org/rdf/schema#Editorship(9); https://dblp.org/rdf/schema#Book(3) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 199 (100%) | Preface. (2022)(2); Marc Rettig: The no-nonsense guide to computing careers. (1992)(1); Philip R. Cohen and Sharon L. Oviatt: Multimodal speech and pen interfaces. (2017)(1); Euan Freeman et al.: Multimodal feedback in HCI: haptics, non-speech audio, and their applications. (2017)(1); Ken Hinckley: A background perspective on touch as a multimodal (and multisensor) construct. (2017)(1) |
| `http://www.w3.org/2002/07/owl#sameAs` | 100% | yes | uri:448 | 448 (224%) | urn:isbn:0897914635(1); http://dx.doi.org/10.1145/3015783.3015795(1); https://doi.org/10.1145/3015783.3015795(1); http://dx.doi.org/10.1145/3015783.3015792(1); http://www.wikidata.org/entity/Q59589875(1) |
| `https://dblp.org/rdf/schema#bibtexType` | 100% | no | uri:200 | 2 (1%) | http://purl.org/net/nknouf/ns/bibtex#Incollection(188); http://purl.org/net/nknouf/ns/bibtex#Book(12) |
| `https://dblp.org/rdf/schema#numberOfCreators` | 100% | no | literal:200 | 8 (4%) | 1(85); 2(38); 3(29); 0(24); 4(8) |
| `https://dblp.org/rdf/schema#title` | 100% | no | literal:200 | 197 (98%) | Preface.(4); The no-nonsense guide to computing careers.(1); Multimodal speech and pen interfaces.(1); Multimodal feedback in HCI: haptics, non-speech audio, and their applications.(1); A background perspective on touch as a multimodal (and multisensor) construct.(1) |
| `https://dblp.org/rdf/schema#yearOfPublication` | 100% | no | literal:200 | 6 (3%) | 2022(100); 2019(64); 2018(15); 2017(14); 2023(6) |
| `https://dblp.org/rdf/schema#documentPage` | 100% | no | uri:199 | 199 (100%) | https://doi.org/10.1145/3015783.3015795(1); https://doi.org/10.1145/3015783.3015792(1); https://doi.org/10.1145/3015783.3015789(1); https://doi.org/10.1145/3015783.3015798(1); https://doi.org/10.1145/3015783.3015790(1) |
| `https://dblp.org/rdf/schema#doi` | 100% | no | uri:199 | 199 (100%) | https://doi.org/10.1145/3015783.3015795(1); https://doi.org/10.1145/3015783.3015792(1); https://doi.org/10.1145/3015783.3015789(1); https://doi.org/10.1145/3015783.3015798(1); https://doi.org/10.1145/3015783.3015790(1) |
| `https://dblp.org/rdf/schema#primaryDocumentPage` | 100% | no | uri:199 | 199 (100%) | https://doi.org/10.1145/3015783.3015795(1); https://doi.org/10.1145/3015783.3015792(1); https://doi.org/10.1145/3015783.3015789(1); https://doi.org/10.1145/3015783.3015798(1); https://doi.org/10.1145/3015783.3015790(1) |
| `https://dblp.org/rdf/schema#listedOnTocPage` | 98% | no | uri:197 | 11 (6%) | https://dblp.org/db/books/collections/GDH2022(47); https://dblp.org/db/books/collections/Go2019(29); https://dblp.org/db/books/collections/S2022(19); https://dblp.org/db/books/collections/Ma2019(18); https://dblp.org/db/books/collections/OSCSPK2019(17) |
| `https://dblp.org/rdf/schema#publishedIn` | 97% | no | literal:194 | 13 (7%) | Probabilistic and Causal Inference(46); Providing Sound Foundations for Cryptography(28); Democratizing Cryptography(18); Concurrency: the Works of Leslie Lamport(17); The Handbook of Multimodal-Multisensor Interfaces, Volume 3 (3)(16) |
| `https://dblp.org/rdf/schema#publishedAsPartOf` | 94% | no | uri:188 | 11 (6%) | https://dblp.org/rec/books/acm/22/GDH2022(46); https://dblp.org/rec/books/acm/19/Go2019(28); https://dblp.org/rec/books/acm/22/S2022(18); https://dblp.org/rec/books/acm/19/2019M(17); https://dblp.org/rec/books/acm/19/OSCSPK2019(16) |
| `https://dblp.org/rdf/schema#publishedInBook` | 94% | no | literal:188 | 11 (6%) | Probabilistic and Causal Inference(46); Providing Sound Foundations for Cryptography(28); Democratizing Cryptography(18); Concurrency: the Works of Leslie Lamport(17); The Handbook of Multimodal-Multisensor Interfaces, Volume 3 (3)(16) |
| `https://dblp.org/rdf/schema#createdBy` | 88% | yes | uri:373 | 268 (152%) | https://dblp.org/pid/p/JudeaPearl(22); https://dblp.org/pid/g/OdedGoldreich(8); https://dblp.org/pid/49/5661(8); https://dblp.org/pid/l/LeslieLamport(8); https://dblp.org/pid/o/SharonLOviatt(7) |
| `https://dblp.org/rdf/schema#hasSignature` | 88% | yes | bnode:373 | - |  |
| `https://dblp.org/rdf/schema#authoredBy` | 84% | yes | uri:345 | 263 (157%) | https://dblp.org/pid/p/JudeaPearl(22); https://dblp.org/pid/49/5661(8); https://dblp.org/pid/l/LeslieLamport(8); https://dblp.org/pid/g/OdedGoldreich(7); https://dblp.org/pid/g/ShafiGoldwasser(6) |
| `https://dblp.org/rdf/schema#pagination` | 83% | no | literal:166 | 164 (99%) | 277-317(2); 203-226(2); 403-447(1); 143-199(1); 547-570(1) |
| `https://dblp.org/rdf/schema#omid` | 74% | no | uri:148 | 148 (100%) | https://w3id.org/oc/meta/br/062402453300(1); https://w3id.org/oc/meta/br/062402453485(1); https://w3id.org/oc/meta/br/062402453401(1); https://w3id.org/oc/meta/br/062402453555(1); https://w3id.org/oc/meta/br/062402453250(1) |
| `https://dblp.org/rdf/schema#publishedInStream` | 53% | no | uri:106 | 2 (2%) | https://dblp.org/streams/series/acmb(105); https://dblp.org/streams/series/acmtb(1) |
| `https://dblp.org/rdf/schema#wikidata` | 20% | no | uri:39 | 39 (100%) | http://www.wikidata.org/entity/Q59589875(1); http://www.wikidata.org/entity/Q130973210(1); http://www.wikidata.org/entity/Q130990457(1); http://www.wikidata.org/entity/Q130841488(1); http://www.wikidata.org/entity/Q130844286(1) |
| `https://dblp.org/rdf/schema#publishedBy` | 6% | no | literal:12 | 2 (17%) | ACM(10); Association for Computing Machinery(2) |
| `https://dblp.org/rdf/schema#isbn` | 6% | no | uri:11 | 11 (100%) | urn:isbn:0897914635(1); urn:isbn:9781970001679(1); urn:isbn:9781970001716(1); urn:isbn:9781450372701(1); urn:isbn:9781450372664(1) |
| `https://dblp.org/rdf/schema#editedBy` | 4% | yes | uri:28 | 16 (178%) | https://dblp.org/pid/54/4934(3); https://dblp.org/pid/69/1786(3); https://dblp.org/pid/78/2516(3); https://dblp.org/pid/83/5858(3); https://dblp.org/pid/k/AntonioKruger(3) |
| `https://dblp.org/rdf/schema#publishedInSeries` | 3% | no | literal:6 | 2 (33%) | ACM Books(5); ACM TechBrief(1) |
| `https://dblp.org/rdf/schema#publishedInSeriesVolume` | 3% | no | literal:6 | 6 (100%) | 5(1); 36(1); 46(1); 50(1); 49(1) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `https://dblp.org/rdf/schema#Publication`(200件); `https://dblp.org/rdf/schema#Incollection`(188件); `https://dblp.org/rdf/schema#Editorship`(9件); `https://dblp.org/rdf/schema#Book`(3件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `https://dblp.org/rdf/schema#bibtexType`（被覆率 100%、異なり値数 2/200 = 1%）
- `https://dblp.org/rdf/schema#publishedInStream`（被覆率 53%、異なり値数 2/106 = 2%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 4/200 = 2%）
- `https://dblp.org/rdf/schema#yearOfPublication`（被覆率 100%、異なり値数 6/200 = 3%）
- `https://dblp.org/rdf/schema#numberOfCreators`（被覆率 100%、異なり値数 8/200 = 4%）
- `https://dblp.org/rdf/schema#listedOnTocPage`（被覆率 98%、異なり値数 11/197 = 6%）
- `https://dblp.org/rdf/schema#publishedAsPartOf`（被覆率 94%、異なり値数 11/188 = 6%）
- `https://dblp.org/rdf/schema#publishedInBook`（被覆率 94%、異なり値数 11/188 = 6%）
- `https://dblp.org/rdf/schema#publishedIn`（被覆率 97%、異なり値数 13/194 = 7%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://purl.org/spar/datacite/hasIdentifier`（被覆率 100%）
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://www.w3.org/2002/07/owl#sameAs`（被覆率 100%）
- `https://dblp.org/rdf/schema#bibtexType`（被覆率 100%）
- `https://dblp.org/rdf/schema#numberOfCreators`（被覆率 100%）
- `https://dblp.org/rdf/schema#title`（被覆率 100%）
- `https://dblp.org/rdf/schema#yearOfPublication`（被覆率 100%）
- `https://dblp.org/rdf/schema#documentPage`（被覆率 100%）
- `https://dblp.org/rdf/schema#doi`（被覆率 100%）
- `https://dblp.org/rdf/schema#primaryDocumentPage`（被覆率 100%）
- `https://dblp.org/rdf/schema#listedOnTocPage`（被覆率 98%）
- `https://dblp.org/rdf/schema#publishedIn`（被覆率 97%）
- `https://dblp.org/rdf/schema#publishedAsPartOf`（被覆率 94%）
- `https://dblp.org/rdf/schema#publishedInBook`（被覆率 94%）
- `https://dblp.org/rdf/schema#createdBy`（被覆率 88%）
- `https://dblp.org/rdf/schema#hasSignature`（被覆率 88%）
- `https://dblp.org/rdf/schema#authoredBy`（被覆率 84%）
- `https://dblp.org/rdf/schema#pagination`（被覆率 83%）
- `https://dblp.org/rdf/schema#omid`（被覆率 74%）
- `https://dblp.org/rdf/schema#publishedInStream`（被覆率 53%）

---
**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」はPhase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。

## 全数集計によるラベル候補検証

- 対象クラス: `https://dblp.org/rdf/schema#Publication`（全体 8625948 件）
- ラベル候補述語: `https://dblp.org/rdf/schema#bibtexType`
- 集計方法: `GROUP BY ?v` による全数集計（上位50件まで取得）。200件サンプルの述語プロファイル（決定事項#19のサンプリングバイアス懸念あり）を経由しない。

| 順位 | 値 | 件数 | 対クラス全体比 |
|---|---|---|---|
| 1 | `http://purl.org/net/nknouf/ns/bibtex#Article` | 4371169 | 50.7% |
| 2 | `http://purl.org/net/nknouf/ns/bibtex#Inproceedings` | 3916756 | 45.4% |
| 3 | `http://purl.org/net/nknouf/ns/bibtex#Phdthesis` | 156031 | 1.8% |
| 4 | `http://purl.org/net/nknouf/ns/bibtex#Incollection` | 71110 | 0.8% |
| 5 | `http://purl.org/net/nknouf/ns/bibtex#Proceedings` | 64784 | 0.8% |
| 6 | `http://purl.org/net/nknouf/ns/bibtex#Misc` | 24555 | 0.3% |
| 7 | `http://purl.org/net/nknouf/ns/bibtex#Book` | 21516 | 0.2% |
| 8 | `http://purl.org/net/nknouf/ns/bibtex#Mastersthesis` | 27 | 0.0% |

取得8値の合計は 8625948 件（クラス全体の 100.0%。多値述語では100%を超えうる）。最頻値はラベル付き集合の 50.7% を占める。

