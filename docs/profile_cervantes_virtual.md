# Cervantes Virtual スキーマ偵察結果

- エンドポイント: https://data.cervantesvirtual.com/sparql

## 主要クラス候補（インスタンス数上位）

| 順位 | クラスURI | インスタンス数(集計値) | 疑わしさ |
|---|---|---|---|
| 1 | `http://rdaregistry.info/Elements/c/Item` | 572749 | - |
| 2 | `http://rdaregistry.info/Elements/c/Expression` | 384975 | - |
| 3 | `http://rdaregistry.info/Elements/c/Work` | 384346 | - |
| 4 | `http://rdaregistry.info/Elements/c/Manifestation` | 372481 | - |
| 5 | `http://purl.org/dc/terms/bibliographicCitation` | 372480 | - |
| 6 | `http://rdaregistry.info/Elements/c/Person` | 115351 | - |
| 7 | `http://schema.org/Person` | 115351 | - |
| 8 | `http://rdaregistry.info/Elements/c/#C10007` | 26390 | - |
| 9 | `http://data.cervantesvirtual.com/publicationStatement/#publicationStatement` | 26388 | - |
| 10 | `http://isni.org/ontology#Resource` | 20846 | - |
| 11 | `http://rdaregistry.info/Elements/c/CorporateBody` | 6399 | - |
| 12 | `http://www.w3.org/2006/time#Instant` | 1569 | - |
| 13 | `http://www.w3.org/2006/time#DateTimeDescription` | 1569 | - |
| 14 | `http://xmlns.com/foaf/0.1/Document` | 825 | - |
| 15 | `http://www.geonames.org/ontology#Feature` | 703 | - |
| 16 | `http://purl.org/dc/dcmitype/Collection` | 627 | - |
| 17 | `http://schema.org/WebSite` | 627 | - |
| 18 | `http://www.w3.org/2004/02/skos/core#Concept` | 190 | - |
| 19 | `http://data.cervantesvirtual.com/publicationStatement/#Translation` | 153 | - |
| 20 | `http://xmlns.com/foaf/0.1/Organization` | 152 | - |

## クラスごとの述語プロファイル

### `http://rdaregistry.info/Elements/c/Item`（全体 572749 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://rdaregistry.info/Elements/c/Item(200) |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 1 (0%) | 02/02/2026(200) |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | 1 (0%) | http://www.cervantesvirtual.com(200) |
| `http://rdaregistry.info/Elements/i/manifestationExemplified` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/manifestation/618261(1); https://data.cervantesvirtual.com/manifestation/618264(1); https://data.cervantesvirtual.com/manifestation/618267(1); https://data.cervantesvirtual.com/manifestation/618270(1); https://data.cervantesvirtual.com/manifestation/618273(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 100%）
- `http://rdaregistry.info/Elements/i/manifestationExemplified`（被覆率 100%）

### `http://rdaregistry.info/Elements/c/Expression`（全体 384975 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://rdaregistry.info/Elements/c/Expression(200) |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 1 (0%) | 02/02/2026(200) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 199 (100%) | Cantar de Mío Cid(2); Psicología del niño y pedagogía experimental : problemas y métodos, desarrollo mental, fatiga intelectual(1); Los amantes desgraciados o El conde de Cominge : drama en tres actos : tercera parte(1); El caballero de buen gusto : comedia en prosa en tres actos(1); El contabilismo social (o Sistema para reemplazar la moneda)(1) |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | 1 (0%) | http://www.cervantesvirtual.com(200) |
| `http://rdvocab.info/Elements/#title` | 100% | no | literal:200 | 199 (100%) | Cantar de Mío Cid(2); Psicología del niño y pedagogía experimental : problemas y métodos, desarrollo mental, fatiga intelectual(1); Los amantes desgraciados o El conde de Cominge : drama en tres actos : tercera parte(1); El caballero de buen gusto : comedia en prosa en tres actos(1); El contabilismo social (o Sistema para reemplazar la moneda)(1) |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 200 (100%) | 1059260(1); 1062782(1); 701638(1); 1063700(1); 1058915(1) |
| `http://rdaregistry.info/Elements/e/identifierForTheExpression` | 100% | no | literal:200 | 200 (100%) | 1059260(1); 1062782(1); 701638(1); 1063700(1); 1058915(1) |
| `http://rdaregistry.info/Elements/e/manifestationOfExpression` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/manifestation/1059261(1); https://data.cervantesvirtual.com/manifestation/1062783(1); https://data.cervantesvirtual.com/manifestation/701639(1); https://data.cervantesvirtual.com/manifestation/1063701(1); https://data.cervantesvirtual.com/manifestation/1058916(1) |
| `http://rdaregistry.info/Elements/e/workExpressed` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/work/1059259(1); https://data.cervantesvirtual.com/work/1062781(1); https://data.cervantesvirtual.com/work/701637(1); https://data.cervantesvirtual.com/work/1063699(1); https://data.cervantesvirtual.com/work/1058914(1) |
| `http://rdaregistry.info/Elements/e/languageOfExpression` | 96% | yes | uri:208 | 10 (5%) | https://data.cervantesvirtual.com/language/es(179); https://data.cervantesvirtual.com/language/pt(9); https://data.cervantesvirtual.com/language/fr(5); https://data.cervantesvirtual.com/language/la(5); https://data.cervantesvirtual.com/language/it(4) |
| `http://rdaregistry.info/Elements/e/contributor` | 50% | yes | uri:109 | 45 (45%) | https://data.cervantesvirtual.com/person/7824(14); https://data.cervantesvirtual.com/person/74919(8); https://data.cervantesvirtual.com/person/8008(8); https://data.cervantesvirtual.com/person/76955(8); https://data.cervantesvirtual.com/person/73452(7) |
| `http://rdaregistry.info/Elements/e/translator` | 37% | yes | uri:76 | 61 (82%) | https://data.cervantesvirtual.com/person/8085(10); https://data.cervantesvirtual.com/person/73005(2); https://data.cervantesvirtual.com/person/73160(2); https://data.cervantesvirtual.com/person/73204(2); https://data.cervantesvirtual.com/person/74452(2) |
| `http://rdaregistry.info/Elements/e/illustrator` | 14% | yes | uri:30 | 26 (93%) | https://data.cervantesvirtual.com/person/73453(4); https://data.cervantesvirtual.com/person/74523(2); https://data.cervantesvirtual.com/person/73105(1); https://data.cervantesvirtual.com/person/73116(1); https://data.cervantesvirtual.com/person/73150(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://rdaregistry.info/Elements/e/languageOfExpression`（被覆率 96%、異なり値数 10/193 = 5%）
- `http://rdaregistry.info/Elements/e/contributor`（被覆率 50%、異なり値数 45/101 = 45%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 100%）
- `http://rdvocab.info/Elements/#title`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）
- `http://rdaregistry.info/Elements/e/identifierForTheExpression`（被覆率 100%）
- `http://rdaregistry.info/Elements/e/manifestationOfExpression`（被覆率 100%）
- `http://rdaregistry.info/Elements/e/workExpressed`（被覆率 100%）
- `http://rdaregistry.info/Elements/e/languageOfExpression`（被覆率 96%）
- `http://rdaregistry.info/Elements/e/contributor`（被覆率 50%）
- `http://rdaregistry.info/Elements/e/translator`（被覆率 37%）

### `http://rdaregistry.info/Elements/c/Work`（全体 384346 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://rdaregistry.info/Elements/c/Work(200) |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 1 (0%) | 02/02/2026(200) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 190 (95%) | Memoires pour servir a l'histoire des insectes(5); Rey decretado en el cielo y astucias de Luzifer : comedia famosa. Segunda parte(2); Historia civil de España, sucessos de la guerra y tratados de paz desde el año de mil setecientos hasta el de mil setecientos y treinta y tres : parte primera-[quarta] / escrita por ... fray Nicolas de Jesus Belando, Religioso Francisco Descalzo ...(2); La prudencia en la niñez : comedia famosa(2); Palingenesia Iuris civilis : iuris consultorum reliquiae quae iustiniani Digestis continentur ceteraque iurisprudentiae civilis fragmenta minora secundum auctores et libros(2) |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | 1 (0%) | http://www.cervantesvirtual.com(200) |
| `http://rdaregistry.info/Elements/w/author` | 100% | no | uri:200 | 135 (68%) | https://data.cervantesvirtual.com/person/7702(14); https://data.cervantesvirtual.com/person/73051(7); https://data.cervantesvirtual.com/person/73102(7); https://data.cervantesvirtual.com/person/73031(5); https://data.cervantesvirtual.com/person/73001(4) |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 200 (100%) | 1020138(1); 1050983(1); 1051160(1); 1051163(1); 1058269(1) |
| `http://rdaregistry.info/Elements/w/expressionOfWork` | 100% | yes | uri:202 | 202 (101%) | https://data.cervantesvirtual.com/expression/1020139(1); https://data.cervantesvirtual.com/expression/1050984(1); https://data.cervantesvirtual.com/expression/1051161(1); https://data.cervantesvirtual.com/expression/1051164(1); https://data.cervantesvirtual.com/expression/1058270(1) |
| `http://rdaregistry.info/Elements/w/manifestationOfWork` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/manifestation/1020140(1); https://data.cervantesvirtual.com/manifestation/1050985(1); https://data.cervantesvirtual.com/manifestation/1051162(1); https://data.cervantesvirtual.com/manifestation/1051165(1); https://data.cervantesvirtual.com/manifestation/1058271(1) |
| `http://rdaregistry.info/Elements/w/titleOfTheWork` | 100% | no | literal:200 | 190 (95%) | Memoires pour servir a l'histoire des insectes(5); Rey decretado en el cielo y astucias de Luzifer : comedia famosa. Segunda parte(2); Historia civil de España, sucessos de la guerra y tratados de paz desde el año de mil setecientos hasta el de mil setecientos y treinta y tres : parte primera-[quarta] / escrita por ... fray Nicolas de Jesus Belando, Religioso Francisco Descalzo ...(2); La prudencia en la niñez : comedia famosa(2); Palingenesia Iuris civilis : iuris consultorum reliquiae quae iustiniani Digestis continentur ceteraque iurisprudentiae civilis fragmenta minora secundum auctores et libros(2) |
| `http://purl.org/dc/elements/1.1/subject` | 38% | yes | literal:143, uri:32 | 126 (214%) | Economía política -- EMBUS(6); Historia(3); Teatro español -- Siglo 17º(3); Escuela Clásica de Economía Política -- EMBUS(2); Derecho romano -- EMBUS(2) |
| `http://rdaregistry.info/Elements/w/formOfWork` | 8% | no | uri:16 | 3 (19%) | http://id.loc.gov/authorities/genreForms/gf2014026168(6); http://id.loc.gov/authorities/genreForms/gf2011026337(6); http://id.loc.gov/authorities/genreForms/gf2014026191(4) |
| `http://rdvocab.info/Elements/#titleProper` | 3% | no | literal:6 | 5 (83%) | El asombro de Jerez, Juana la Rabicortona. Segunda parte(2); [Constitución, 1807](1); [Meditationes vitae Christi](1); [Breve, 1254-07-08](1); No cabe mas en amor, ni hay amor firme sin celos(1) |
| `http://rdaregistry.info/Elements/w/P10055` | 2% | yes | uri:4 | 3 (100%) | https://data.cervantesvirtual.com/person/73066(2); https://data.cervantesvirtual.com/person/109754(1); https://data.cervantesvirtual.com/person/73135(1) |
| `http://rdaregistry.info/Elements/w/variantTitleForTheWork` | 2% | yes | literal:4 | 4 (133%) | Dido abandonada(1); Valiente Eneas, El(1); El Demoofonte :(1); Perla asombro del mar en la merced de su aurora, vida y muerte de Santa María de Cervellón y Socos, hija natural de la excelentísima ciudad de Barcelona(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 100%）
- `http://rdaregistry.info/Elements/w/author`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）
- `http://rdaregistry.info/Elements/w/expressionOfWork`（被覆率 100%）
- `http://rdaregistry.info/Elements/w/manifestationOfWork`（被覆率 100%）
- `http://rdaregistry.info/Elements/w/titleOfTheWork`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/subject`（被覆率 38%）

### `http://rdaregistry.info/Elements/c/Manifestation`（全体 372481 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:406 | 4 (2%) | http://purl.org/dc/terms/bibliographicCitation(200); http://rdaregistry.info/Elements/c/Manifestation(200); http://purl.org/dc/dcmitype/Collection(3); http://schema.org/WebSite(3) |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 1 (0%) | 02/02/2026(200) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 197 (98%) | Funeral oratoria, que en las celebres honras, que consagro la religiosissima comunidad de Rmos. PP. Trinitarios Calzados de la ciudad de Granada, el dia 25, de septiembre de 1722 à la loable memorial de el venerable Fr. Feliciano de Sevilla... de PP. Capuchinos del S. P. S. Francisco / dixo el M. R. P. ... Fr. Vicente de Burgos, hijo de la... Trinitaria familia de la Observancia...; sacala a luz y la dedica... un devoto de este soberano mysterio...(2); Dictionnaire mathematique ou Idée generale des mathematiques : dans lequel l'on trouve outre les termes de cette science plusieurs termes des Arts et des autres sciences avec des raisonnemens qui conduisent peu à peu l'esprit à une connoissance universelle des mathematiques / par M. Ozanam ..(2); La gran victoria de España en los campos de Vitoria : comedia sin fama / su autor Don Antonio Valladares de Sotomayor(2); Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F(1); Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .(1) |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | 1 (0%) | http://www.cervantesvirtual.com(200) |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 200 (100%) | 1002915(1); 1004651(1); 1005770(1); 1006358(1); 1007072(1) |
| `http://purl.org/dc/terms/bibliographicCitation` | 100% | no | literal:200 | 200 (100%) | @Misc{BVMC:1002915,
author = {Massillon, Jean Baptiste, (C.O.), Obispo de Clermont },
title = {Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo},
url = {https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915}
}
(1); @Misc{BVMC:1004651,
title = {Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .},
url = {https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651}
}
(1); @Misc{BVMC:1005770,
title = {Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721},
url = {https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770}
}
(1); @Misc{BVMC:1006358,
author = {Cabello y Negrete, Francisco},
title = {Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ...},
url = {https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358}
}
(1); @Misc{BVMC:1007072,
author = {Mariotte, Edmé},
title = {Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets},
url = {https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072}
}
(1) |
| `http://rdaregistry.info/Elements/m/expressionManifested` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/expression/1002914(1); https://data.cervantesvirtual.com/expression/1004650(1); https://data.cervantesvirtual.com/expression/1005769(1); https://data.cervantesvirtual.com/expression/1006357(1); https://data.cervantesvirtual.com/expression/1007071(1) |
| `http://rdaregistry.info/Elements/m/title` | 100% | no | literal:200 | 197 (98%) | Funeral oratoria, que en las celebres honras, que consagro la religiosissima comunidad de Rmos. PP. Trinitarios Calzados de la ciudad de Granada, el dia 25, de septiembre de 1722 à la loable memorial de el venerable Fr. Feliciano de Sevilla... de PP. Capuchinos del S. P. S. Francisco / dixo el M. R. P. ... Fr. Vicente de Burgos, hijo de la... Trinitaria familia de la Observancia...; sacala a luz y la dedica... un devoto de este soberano mysterio...(2); Dictionnaire mathematique ou Idée generale des mathematiques : dans lequel l'on trouve outre les termes de cette science plusieurs termes des Arts et des autres sciences avec des raisonnemens qui conduisent peu à peu l'esprit à une connoissance universelle des mathematiques / par M. Ozanam ..(2); La gran victoria de España en los campos de Vitoria : comedia sin fama / su autor Don Antonio Valladares de Sotomayor(2); Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F(1); Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .(1) |
| `http://rdaregistry.info/Elements/m/uniformResourceLocator` | 100% | no | uri:200 | 200 (100%) | https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915(1); https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651(1); https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770(1); https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358(1); https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072(1) |
| `http://rdaregistry.info/Elements/m/workManifested` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/work/1002913(1); https://data.cervantesvirtual.com/work/1004649(1); https://data.cervantesvirtual.com/work/1005768(1); https://data.cervantesvirtual.com/work/1006356(1); https://data.cervantesvirtual.com/work/1007070(1) |
| `http://rdaregistry.info/Elements/m/insertedIn` | 100% | yes | uri:404 | 36 (18%) | https://data.cervantesvirtual.com/manifestation/266317(168); https://data.cervantesvirtual.com/manifestation/263038(150); https://data.cervantesvirtual.com/manifestation/281418(15); https://data.cervantesvirtual.com/manifestation/254825(14); https://data.cervantesvirtual.com/manifestation/230142(8) |
| `http://purl.org/dc/elements/1.1/language` | 96% | yes | uri:195 | 8 (4%) | https://data.cervantesvirtual.com/language/es(143); https://data.cervantesvirtual.com/language/la(27); https://data.cervantesvirtual.com/language/fr(16); https://data.cervantesvirtual.com/language/it(3); https://data.cervantesvirtual.com/language/ca(2) |
| `http://rdaregistry.info/Elements/m/noteOnEditionStatement` | 94% | no | literal:189 | 24 (13%) | Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla(150); Reproducción digital del original conservado en la Biblioteca de la Universidad de Granada(14); Reproducción digital del original conservado en la Biblioteca de la Universidad de Valladolid(3); Edición digital a partir de la 2ª edición con correcciones inéditas, Habana, Cultural, 1928 (Colección de libros cubanos ; 1-3). Localización: <a href="http://www.fundacionbarcenillas.org/">Fundación Barcenillas</a>. Colección Pérez Arauna(2); Edición digital a partir de Barcelona, por Matheo Barceló, Impresor, en la Puerta del Angel. Año 1779. Localización: Biblioteca de Menéndez Pelayo. Sig. 33.585(1) |
| `http://rdaregistry.info/Elements/m/placeOfProduction` | 88% | no | literal:175 | 170 (97%) | A Lyon :, Chez les Freres Duplain, ..., 1757 (3); A La Haye : chez Jean Neaulme, 1740(2); En Granada : en la imprenta de la S.S. Trinidad, ca. 1722(2); Madrid : Imprenta de Juan Antonio Garcia ; España: Madrid, 1860(2); Sevilla : : [editor no identificado] (Imp. y Taller de encuadernaciones de Juan Moyano), , 1852 (Imp. y Taller de encuadernaciones de Juan Moyano)(1) |
| `http://xmlns.com/foaf/0.1/homepage` | 86% | no | uri:173 | 173 (100%) | https://archive.org/details/A1140551(1); https://archive.org/details/A11202416(1); https://archive.org/details/A11303806(1); https://archive.org/details/A11311212(1); https://archive.org/details/A039a467468(1) |
| `http://rdaregistry.info/Elements/m/dateOfPublication` | 86% | no | literal:34, uri:137 | 31 (91%) | 1725?](2); ca. 1722(2); 2011-2014(2); , 1852(1); 1723?](1) |
| `http://purl.org/dc/terms/publisher` | 84% | no | uri:169 | 4 (2%) | https://data.cervantesvirtual.com/institution/9(150); https://data.cervantesvirtual.com/institution/6(14); https://data.cervantesvirtual.com/institution/57(3); https://data.cervantesvirtual.com/institution/75(2) |
| `http://rdaregistry.info/Elements/m/noteOnManifestation` | 74% | yes | literal:375 | 295 (199%) | Descr. física Texto a dos col.(15); Descr. física Port. con orla tip(9); Encuadernacion: Perg.(7); Nota Area Public. Marca tip. en port.(6); Descr. física Texto con apostillas marginales(5) |
| `http://rdaregistry.info/Elements/m/dimensions` | 71% | no | literal:142 | 45 (32%) | 4º(53); 8º(11); ; 4o(10); 21 cm(6); 4o(5) |
| `http://xmlns.com/foaf/0.1/depiction` | 64% | no | uri:127 | 127 (100%) | https://www.cervantesvirtual.com/portadas/069/0697961(1); https://www.cervantesvirtual.com/portadas/069/0697991(1); https://www.cervantesvirtual.com/portadas/069/0697997(1); https://www.cervantesvirtual.com/portadas/069/0698030(1); https://www.cervantesvirtual.com/portadas/069/0698081(1) |
| `http://rdaregistry.info/Elements/m/printer` | 45% | no | uri:90 | 58 (64%) | https://data.cervantesvirtual.com/corporatebody/72988(12); https://data.cervantesvirtual.com/person/73203(4); https://data.cervantesvirtual.com/person/73199(3); https://data.cervantesvirtual.com/person/73310(3); https://data.cervantesvirtual.com/person/72995(2) |
| `http://rdaregistry.info/Elements/m/otherPFCManifestation` | 34% | yes | uri:88 | 74 (110%) | https://data.cervantesvirtual.com/person/73058(5); https://data.cervantesvirtual.com/person/73584(3); https://data.cervantesvirtual.com/corporatebody/73643(3); https://data.cervantesvirtual.com/person/73063(2); https://data.cervantesvirtual.com/person/73079(2) |
| `http://rdaregistry.info/Elements/m/publisher` | 24% | yes | uri:54 | 41 (85%) | https://data.cervantesvirtual.com/person/73452(7); https://data.cervantesvirtual.com/person/73707(4); https://data.cervantesvirtual.com/person/73713(3); https://data.cervantesvirtual.com/person/73058(2); https://data.cervantesvirtual.com/person/73043(2) |
| `http://rdaregistry.info/Elements/m/publishersName` | 24% | yes | literal:54 | 41 (85%) | García, Mar(7); Travieso, Mercedes(4); García Márquez, Mariángeles(3); Tarascó y Lassa, Rafael(2); Razola, Casimiro(2) |
| `http://rdaregistry.info/Elements/u/publisher` | 22% | no | literal:44 | 6 (14%) | Fundación(29); ES-GrU(11); SIRSI(1); UkOxU(1); Gabinete de Antigüedades(1) |
| `http://rdaregistry.info/Elements/m/publicationStatement` | 16% | no | literal:31 | 8 (26%) | Alicante : Biblioteca Virtual Miguel de Cervantes, 2015(17); Alicante : Biblioteca Virtual Miguel de Cervantes, 2014(7); Alicante : Biblioteca Virtual Miguel de Cervantes, 2005(2); Santander : Ayuntamiento ; Alicante : Biblioteca Virtual Miguel de Cervantes, 2016(1); Alicante : Biblioteca Virtual Miguel de Cervantes, 2021(1) |
| `http://rdaregistry.info/Elements/m/exemplarOfManifestation` | 12% | no | uri:25 | 25 (100%) | https://data.cervantesvirtual.com/item/606066(1); https://data.cervantesvirtual.com/item/604497(1); https://data.cervantesvirtual.com/item/136667(1); https://data.cervantesvirtual.com/item/24233(1); https://data.cervantesvirtual.com/item/25763(1) |
| `http://rdaregistry.info/Elements/m/dateOfDistribution` | 12% | no | uri:23 | 6 (26%) | https://data.cervantesvirtual.com/date/2015(14); https://data.cervantesvirtual.com/date/2014(4); https://data.cervantesvirtual.com/date/2005(2); https://data.cervantesvirtual.com/date/2016(1); https://data.cervantesvirtual.com/date/2021(1) |
| `http://rdaregistry.info/Elements/m/carrierType` | 4% | no | uri:9 | 1 (11%) | http://rdaregistry.info/termList/RDACarrierType/1010(9) |
| `http://rdaregistry.info/Elements/m/mediaType` | 4% | no | uri:9 | 2 (22%) | http://rdaregistry.info/termList/RDAMediaType/1003(8); http://rdaregistry.info/termList/RDAMediaType/1008(1) |
| `http://rdaregistry.info/Elements/u/contentType` | 4% | no | uri:9 | 4 (44%) | http://rdaregistry.info/termList/RDAContentType/1020(4); http://rdaregistry.info/termList/RDAContentType/1007(3); http://rdaregistry.info/termList/RDAContentType/1004(1); http://rdaregistry.info/termList/RDAContentType/1009(1) |
| `http://schema.org/datePublished` | 2% | no | literal:3 | 3 (100%) | 201510302(1); 20180381(1); 202212349(1) |
| `http://schema.org/headline` | 2% | no | literal:3 | 3 (100%) | Fundación Pablo Iglesias(1); Sergio Ramírez(1); Alfonso de Cartagena(1) |
| `http://schema.org/isBasedOnUrl` | 2% | no | uri:3 | 3 (100%) | https://www.cervantesvirtual.com/portales/fundacion_pablo_iglesias/(1); https://www.cervantesvirtual.com/portales/sergio_ramirez/(1); https://www.cervantesvirtual.com/portales/alfonso_de_cartagena/(1) |
| `http://schema.org/isFamilyFriendly` | 2% | no | literal:3 | 1 (33%) | True(3) |
| `http://schema.org/thumbnailUrl` | 2% | no | uri:3 | 3 (100%) | https://www.cervantesvirtual.com/images/banners_portales/fundacion-pablo-iglesias.jpg(1); https://www.cervantesvirtual.com/images/banners_portales/sergio-ramirez.jpg(1); https://www.cervantesvirtual.com/images/banners_portales/alfonso-de-cartagena-707767.jpg(1) |
| `http://rdaregistry.info/Elements/u/concordance` | 1% | no | uri:2 | 2 (100%) | https://www.cervantesvirtual.com/concordancias/los-jardines-interiores--0(1); https://www.cervantesvirtual.com/concordancias/pico-de-la-mirndula-y-la-inquisicin-espaola-breve-indito-de-inocencio-viii-0(1) |
| `http://rdaregistry.info/Elements/m/frequency` | 1% | no | literal:2 | 2 (100%) | Semanal(1); Irregular(1) |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfFirstIssueOrPartOfSequence` | 1% | no | literal:2 | 2 (100%) | IV Época, núm. 2 (9 mayo 1945)(1); Núm. 1 (25 julio 1944)(1) |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfLastIssueOrPartOfSequence` | 1% | no | literal:2 | 2 (100%) | V Época, núm. 24 (diciemabre 1969)(1); Núm. 10 (28 julio 1945)(1) |
| `http://rdaregistry.info/Elements/m/noteOnTitle` | 0% | yes | literal:2 | 2 (200%) | Precede al título: "N. 15"(1); Inc.: Sale Juan Rana, y Gila. / Gil. ES hora de venir, marido á casa? / Què esto en el mundo passa! [...]. Exp.: para quando à la Rana / le crie pelo / FIN(1) |
| `http://rdaregistry.info/Elements/m/wholePartManifestationRelationship` | 0% | no | uri:1 | 1 (100%) | https://data.cervantesvirtual.com/manifestation/327300(1) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://purl.org/dc/terms/bibliographicCitation`(200件); `http://rdaregistry.info/Elements/c/Manifestation`(200件); `http://purl.org/dc/dcmitype/Collection`(3件); `http://schema.org/WebSite`(3件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 4/200 = 2%）
- `http://purl.org/dc/terms/publisher`（被覆率 84%、異なり値数 4/169 = 2%）
- `http://purl.org/dc/elements/1.1/language`（被覆率 96%、異なり値数 8/191 = 4%）
- `http://rdaregistry.info/Elements/m/noteOnEditionStatement`（被覆率 94%、異なり値数 24/189 = 13%）
- `http://rdaregistry.info/Elements/m/insertedIn`（被覆率 100%、異なり値数 36/199 = 18%）
- `http://rdaregistry.info/Elements/m/dimensions`（被覆率 71%、異なり値数 45/142 = 32%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）
- `http://purl.org/dc/terms/bibliographicCitation`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/expressionManifested`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/title`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/uniformResourceLocator`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/workManifested`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/insertedIn`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/language`（被覆率 96%）
- `http://rdaregistry.info/Elements/m/noteOnEditionStatement`（被覆率 94%）
- `http://rdaregistry.info/Elements/m/placeOfProduction`（被覆率 88%）
- `http://xmlns.com/foaf/0.1/homepage`（被覆率 86%）
- `http://rdaregistry.info/Elements/m/dateOfPublication`（被覆率 86%）
- `http://purl.org/dc/terms/publisher`（被覆率 84%）
- `http://rdaregistry.info/Elements/m/noteOnManifestation`（被覆率 74%）
- `http://rdaregistry.info/Elements/m/dimensions`（被覆率 71%）
- `http://xmlns.com/foaf/0.1/depiction`（被覆率 64%）
- `http://rdaregistry.info/Elements/m/printer`（被覆率 45%）
- `http://rdaregistry.info/Elements/m/otherPFCManifestation`（被覆率 34%）

### `http://purl.org/dc/terms/bibliographicCitation`（全体 372480 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:406 | 4 (2%) | http://purl.org/dc/terms/bibliographicCitation(200); http://rdaregistry.info/Elements/c/Manifestation(200); http://purl.org/dc/dcmitype/Collection(3); http://schema.org/WebSite(3) |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 1 (0%) | 02/02/2026(200) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | 197 (98%) | Funeral oratoria, que en las celebres honras, que consagro la religiosissima comunidad de Rmos. PP. Trinitarios Calzados de la ciudad de Granada, el dia 25, de septiembre de 1722 à la loable memorial de el venerable Fr. Feliciano de Sevilla... de PP. Capuchinos del S. P. S. Francisco / dixo el M. R. P. ... Fr. Vicente de Burgos, hijo de la... Trinitaria familia de la Observancia...; sacala a luz y la dedica... un devoto de este soberano mysterio...(2); Dictionnaire mathematique ou Idée generale des mathematiques : dans lequel l'on trouve outre les termes de cette science plusieurs termes des Arts et des autres sciences avec des raisonnemens qui conduisent peu à peu l'esprit à une connoissance universelle des mathematiques / par M. Ozanam ..(2); La gran victoria de España en los campos de Vitoria : comedia sin fama / su autor Don Antonio Valladares de Sotomayor(2); Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F(1); Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .(1) |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | 1 (0%) | http://www.cervantesvirtual.com(200) |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 200 (100%) | 1002915(1); 1004651(1); 1005770(1); 1006358(1); 1007072(1) |
| `http://purl.org/dc/terms/bibliographicCitation` | 100% | no | literal:200 | 200 (100%) | @Misc{BVMC:1002915,
author = {Massillon, Jean Baptiste, (C.O.), Obispo de Clermont },
title = {Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo},
url = {https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915}
}
(1); @Misc{BVMC:1004651,
title = {Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .},
url = {https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651}
}
(1); @Misc{BVMC:1005770,
title = {Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721},
url = {https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770}
}
(1); @Misc{BVMC:1006358,
author = {Cabello y Negrete, Francisco},
title = {Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ...},
url = {https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358}
}
(1); @Misc{BVMC:1007072,
author = {Mariotte, Edmé},
title = {Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets},
url = {https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072}
}
(1) |
| `http://rdaregistry.info/Elements/m/expressionManifested` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/expression/1002914(1); https://data.cervantesvirtual.com/expression/1004650(1); https://data.cervantesvirtual.com/expression/1005769(1); https://data.cervantesvirtual.com/expression/1006357(1); https://data.cervantesvirtual.com/expression/1007071(1) |
| `http://rdaregistry.info/Elements/m/title` | 100% | no | literal:200 | 197 (98%) | Funeral oratoria, que en las celebres honras, que consagro la religiosissima comunidad de Rmos. PP. Trinitarios Calzados de la ciudad de Granada, el dia 25, de septiembre de 1722 à la loable memorial de el venerable Fr. Feliciano de Sevilla... de PP. Capuchinos del S. P. S. Francisco / dixo el M. R. P. ... Fr. Vicente de Burgos, hijo de la... Trinitaria familia de la Observancia...; sacala a luz y la dedica... un devoto de este soberano mysterio...(2); Dictionnaire mathematique ou Idée generale des mathematiques : dans lequel l'on trouve outre les termes de cette science plusieurs termes des Arts et des autres sciences avec des raisonnemens qui conduisent peu à peu l'esprit à une connoissance universelle des mathematiques / par M. Ozanam ..(2); La gran victoria de España en los campos de Vitoria : comedia sin fama / su autor Don Antonio Valladares de Sotomayor(2); Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F(1); Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .(1) |
| `http://rdaregistry.info/Elements/m/uniformResourceLocator` | 100% | no | uri:200 | 200 (100%) | https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915(1); https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651(1); https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770(1); https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358(1); https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072(1) |
| `http://rdaregistry.info/Elements/m/workManifested` | 100% | no | uri:200 | 200 (100%) | https://data.cervantesvirtual.com/work/1002913(1); https://data.cervantesvirtual.com/work/1004649(1); https://data.cervantesvirtual.com/work/1005768(1); https://data.cervantesvirtual.com/work/1006356(1); https://data.cervantesvirtual.com/work/1007070(1) |
| `http://rdaregistry.info/Elements/m/insertedIn` | 100% | yes | uri:404 | 36 (18%) | https://data.cervantesvirtual.com/manifestation/266317(168); https://data.cervantesvirtual.com/manifestation/263038(150); https://data.cervantesvirtual.com/manifestation/281418(15); https://data.cervantesvirtual.com/manifestation/254825(14); https://data.cervantesvirtual.com/manifestation/230142(8) |
| `http://purl.org/dc/elements/1.1/language` | 96% | yes | uri:195 | 8 (4%) | https://data.cervantesvirtual.com/language/es(143); https://data.cervantesvirtual.com/language/la(27); https://data.cervantesvirtual.com/language/fr(16); https://data.cervantesvirtual.com/language/it(3); https://data.cervantesvirtual.com/language/ca(2) |
| `http://rdaregistry.info/Elements/m/noteOnEditionStatement` | 94% | no | literal:189 | 24 (13%) | Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla(150); Reproducción digital del original conservado en la Biblioteca de la Universidad de Granada(14); Reproducción digital del original conservado en la Biblioteca de la Universidad de Valladolid(3); Edición digital a partir de la 2ª edición con correcciones inéditas, Habana, Cultural, 1928 (Colección de libros cubanos ; 1-3). Localización: <a href="http://www.fundacionbarcenillas.org/">Fundación Barcenillas</a>. Colección Pérez Arauna(2); Edición digital a partir de Barcelona, por Matheo Barceló, Impresor, en la Puerta del Angel. Año 1779. Localización: Biblioteca de Menéndez Pelayo. Sig. 33.585(1) |
| `http://rdaregistry.info/Elements/m/placeOfProduction` | 88% | no | literal:175 | 170 (97%) | A Lyon :, Chez les Freres Duplain, ..., 1757 (3); A La Haye : chez Jean Neaulme, 1740(2); En Granada : en la imprenta de la S.S. Trinidad, ca. 1722(2); Madrid : Imprenta de Juan Antonio Garcia ; España: Madrid, 1860(2); Sevilla : : [editor no identificado] (Imp. y Taller de encuadernaciones de Juan Moyano), , 1852 (Imp. y Taller de encuadernaciones de Juan Moyano)(1) |
| `http://xmlns.com/foaf/0.1/homepage` | 86% | no | uri:173 | 173 (100%) | https://archive.org/details/A1140551(1); https://archive.org/details/A11202416(1); https://archive.org/details/A11303806(1); https://archive.org/details/A11311212(1); https://archive.org/details/A039a467468(1) |
| `http://rdaregistry.info/Elements/m/dateOfPublication` | 86% | no | literal:34, uri:137 | 31 (91%) | 1725?](2); ca. 1722(2); 2011-2014(2); , 1852(1); 1723?](1) |
| `http://purl.org/dc/terms/publisher` | 84% | no | uri:169 | 4 (2%) | https://data.cervantesvirtual.com/institution/9(150); https://data.cervantesvirtual.com/institution/6(14); https://data.cervantesvirtual.com/institution/57(3); https://data.cervantesvirtual.com/institution/75(2) |
| `http://rdaregistry.info/Elements/m/noteOnManifestation` | 74% | yes | literal:375 | 295 (199%) | Descr. física Texto a dos col.(15); Descr. física Port. con orla tip(9); Encuadernacion: Perg.(7); Nota Area Public. Marca tip. en port.(6); Descr. física Texto con apostillas marginales(5) |
| `http://rdaregistry.info/Elements/m/dimensions` | 71% | no | literal:142 | 45 (32%) | 4º(53); 8º(11); ; 4o(10); 21 cm(6); 4o(5) |
| `http://xmlns.com/foaf/0.1/depiction` | 64% | no | uri:127 | 127 (100%) | https://www.cervantesvirtual.com/portadas/069/0697961(1); https://www.cervantesvirtual.com/portadas/069/0697991(1); https://www.cervantesvirtual.com/portadas/069/0697997(1); https://www.cervantesvirtual.com/portadas/069/0698030(1); https://www.cervantesvirtual.com/portadas/069/0698081(1) |
| `http://rdaregistry.info/Elements/m/printer` | 45% | no | uri:90 | 58 (64%) | https://data.cervantesvirtual.com/corporatebody/72988(12); https://data.cervantesvirtual.com/person/73203(4); https://data.cervantesvirtual.com/person/73199(3); https://data.cervantesvirtual.com/person/73310(3); https://data.cervantesvirtual.com/person/72995(2) |
| `http://rdaregistry.info/Elements/m/otherPFCManifestation` | 34% | yes | uri:88 | 74 (110%) | https://data.cervantesvirtual.com/person/73058(5); https://data.cervantesvirtual.com/person/73584(3); https://data.cervantesvirtual.com/corporatebody/73643(3); https://data.cervantesvirtual.com/person/73063(2); https://data.cervantesvirtual.com/person/73079(2) |
| `http://rdaregistry.info/Elements/m/publisher` | 24% | yes | uri:54 | 41 (85%) | https://data.cervantesvirtual.com/person/73452(7); https://data.cervantesvirtual.com/person/73707(4); https://data.cervantesvirtual.com/person/73713(3); https://data.cervantesvirtual.com/person/73058(2); https://data.cervantesvirtual.com/person/73043(2) |
| `http://rdaregistry.info/Elements/m/publishersName` | 24% | yes | literal:54 | 41 (85%) | García, Mar(7); Travieso, Mercedes(4); García Márquez, Mariángeles(3); Tarascó y Lassa, Rafael(2); Razola, Casimiro(2) |
| `http://rdaregistry.info/Elements/u/publisher` | 22% | no | literal:44 | 6 (14%) | Fundación(29); ES-GrU(11); SIRSI(1); UkOxU(1); Gabinete de Antigüedades(1) |
| `http://rdaregistry.info/Elements/m/publicationStatement` | 16% | no | literal:31 | 8 (26%) | Alicante : Biblioteca Virtual Miguel de Cervantes, 2015(17); Alicante : Biblioteca Virtual Miguel de Cervantes, 2014(7); Alicante : Biblioteca Virtual Miguel de Cervantes, 2005(2); Santander : Ayuntamiento ; Alicante : Biblioteca Virtual Miguel de Cervantes, 2016(1); Alicante : Biblioteca Virtual Miguel de Cervantes, 2021(1) |
| `http://rdaregistry.info/Elements/m/exemplarOfManifestation` | 12% | no | uri:25 | 25 (100%) | https://data.cervantesvirtual.com/item/606066(1); https://data.cervantesvirtual.com/item/604497(1); https://data.cervantesvirtual.com/item/136667(1); https://data.cervantesvirtual.com/item/24233(1); https://data.cervantesvirtual.com/item/25763(1) |
| `http://rdaregistry.info/Elements/m/dateOfDistribution` | 12% | no | uri:23 | 6 (26%) | https://data.cervantesvirtual.com/date/2015(14); https://data.cervantesvirtual.com/date/2014(4); https://data.cervantesvirtual.com/date/2005(2); https://data.cervantesvirtual.com/date/2016(1); https://data.cervantesvirtual.com/date/2021(1) |
| `http://rdaregistry.info/Elements/m/carrierType` | 4% | no | uri:9 | 1 (11%) | http://rdaregistry.info/termList/RDACarrierType/1010(9) |
| `http://rdaregistry.info/Elements/m/mediaType` | 4% | no | uri:9 | 2 (22%) | http://rdaregistry.info/termList/RDAMediaType/1003(8); http://rdaregistry.info/termList/RDAMediaType/1008(1) |
| `http://rdaregistry.info/Elements/u/contentType` | 4% | no | uri:9 | 4 (44%) | http://rdaregistry.info/termList/RDAContentType/1020(4); http://rdaregistry.info/termList/RDAContentType/1007(3); http://rdaregistry.info/termList/RDAContentType/1004(1); http://rdaregistry.info/termList/RDAContentType/1009(1) |
| `http://schema.org/datePublished` | 2% | no | literal:3 | 3 (100%) | 201510302(1); 20180381(1); 202212349(1) |
| `http://schema.org/headline` | 2% | no | literal:3 | 3 (100%) | Fundación Pablo Iglesias(1); Sergio Ramírez(1); Alfonso de Cartagena(1) |
| `http://schema.org/isBasedOnUrl` | 2% | no | uri:3 | 3 (100%) | https://www.cervantesvirtual.com/portales/fundacion_pablo_iglesias/(1); https://www.cervantesvirtual.com/portales/sergio_ramirez/(1); https://www.cervantesvirtual.com/portales/alfonso_de_cartagena/(1) |
| `http://schema.org/isFamilyFriendly` | 2% | no | literal:3 | 1 (33%) | True(3) |
| `http://schema.org/thumbnailUrl` | 2% | no | uri:3 | 3 (100%) | https://www.cervantesvirtual.com/images/banners_portales/fundacion-pablo-iglesias.jpg(1); https://www.cervantesvirtual.com/images/banners_portales/sergio-ramirez.jpg(1); https://www.cervantesvirtual.com/images/banners_portales/alfonso-de-cartagena-707767.jpg(1) |
| `http://rdaregistry.info/Elements/u/concordance` | 1% | no | uri:2 | 2 (100%) | https://www.cervantesvirtual.com/concordancias/los-jardines-interiores--0(1); https://www.cervantesvirtual.com/concordancias/pico-de-la-mirndula-y-la-inquisicin-espaola-breve-indito-de-inocencio-viii-0(1) |
| `http://rdaregistry.info/Elements/m/frequency` | 1% | no | literal:2 | 2 (100%) | Semanal(1); Irregular(1) |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfFirstIssueOrPartOfSequence` | 1% | no | literal:2 | 2 (100%) | IV Época, núm. 2 (9 mayo 1945)(1); Núm. 1 (25 julio 1944)(1) |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfLastIssueOrPartOfSequence` | 1% | no | literal:2 | 2 (100%) | V Época, núm. 24 (diciemabre 1969)(1); Núm. 10 (28 julio 1945)(1) |
| `http://rdaregistry.info/Elements/m/noteOnTitle` | 0% | yes | literal:2 | 2 (200%) | Precede al título: "N. 15"(1); Inc.: Sale Juan Rana, y Gila. / Gil. ES hora de venir, marido á casa? / Què esto en el mundo passa! [...]. Exp.: para quando à la Rana / le crie pelo / FIN(1) |
| `http://rdaregistry.info/Elements/m/wholePartManifestationRelationship` | 0% | no | uri:1 | 1 (100%) | https://data.cervantesvirtual.com/manifestation/327300(1) |

⚠️ このクラスのインスタンスは複数の`rdf:type`を同時に持つ場合がある（内訳: `http://purl.org/dc/terms/bibliographicCitation`(200件); `http://rdaregistry.info/Elements/c/Manifestation`(200件); `http://purl.org/dc/dcmitype/Collection`(3件); `http://schema.org/WebSite`(3件)）。追加の述語取得なしに使えるサブタイプ由来のラベル候補になりうるため検討する価値がある。

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%、異なり値数 4/200 = 2%）
- `http://purl.org/dc/terms/publisher`（被覆率 84%、異なり値数 4/169 = 2%）
- `http://purl.org/dc/elements/1.1/language`（被覆率 96%、異なり値数 8/191 = 4%）
- `http://rdaregistry.info/Elements/m/noteOnEditionStatement`（被覆率 94%、異なり値数 24/189 = 13%）
- `http://rdaregistry.info/Elements/m/insertedIn`（被覆率 100%、異なり値数 36/199 = 18%）
- `http://rdaregistry.info/Elements/m/dimensions`（被覆率 71%、異なり値数 45/142 = 32%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）
- `http://purl.org/dc/terms/bibliographicCitation`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/expressionManifested`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/title`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/uniformResourceLocator`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/workManifested`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/insertedIn`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/language`（被覆率 96%）
- `http://rdaregistry.info/Elements/m/noteOnEditionStatement`（被覆率 94%）
- `http://rdaregistry.info/Elements/m/placeOfProduction`（被覆率 88%）
- `http://xmlns.com/foaf/0.1/homepage`（被覆率 86%）
- `http://rdaregistry.info/Elements/m/dateOfPublication`（被覆率 86%）
- `http://purl.org/dc/terms/publisher`（被覆率 84%）
- `http://rdaregistry.info/Elements/m/noteOnManifestation`（被覆率 74%）
- `http://rdaregistry.info/Elements/m/dimensions`（被覆率 71%）
- `http://xmlns.com/foaf/0.1/depiction`（被覆率 64%）
- `http://rdaregistry.info/Elements/m/printer`（被覆率 45%）
- `http://rdaregistry.info/Elements/m/otherPFCManifestation`（被覆率 34%）

---
**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」はPhase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。
