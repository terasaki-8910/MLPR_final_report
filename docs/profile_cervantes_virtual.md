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

### `http://rdaregistry.info/Elements/c/Item`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://rdaregistry.info/Elements/c/Item; http://rdaregistry.info/Elements/c/Item; http://rdaregistry.info/Elements/c/Item; http://rdaregistry.info/Elements/c/Item; http://rdaregistry.info/Elements/c/Item |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026 |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com |
| `http://rdaregistry.info/Elements/i/manifestationExemplified` | 100% | no | uri:200 | https://data.cervantesvirtual.com/manifestation/618261; https://data.cervantesvirtual.com/manifestation/618264; https://data.cervantesvirtual.com/manifestation/618267; https://data.cervantesvirtual.com/manifestation/618270; https://data.cervantesvirtual.com/manifestation/618273 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://purl.org/dc/terms/created`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 100%）
- `http://rdaregistry.info/Elements/i/manifestationExemplified`（被覆率 100%）

### `http://rdaregistry.info/Elements/c/Expression`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://rdaregistry.info/Elements/c/Expression; http://rdaregistry.info/Elements/c/Expression; http://rdaregistry.info/Elements/c/Expression; http://rdaregistry.info/Elements/c/Expression; http://rdaregistry.info/Elements/c/Expression |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026 |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | Psicología del niño y pedagogía experimental : problemas y métodos, desarrollo mental, fatiga intelectual; Los amantes desgraciados o El conde de Cominge : drama en tres actos : tercera parte; El caballero de buen gusto : comedia en prosa en tres actos; El contabilismo social (o Sistema para reemplazar la moneda); Moral universal o Deberes del hombre fundados en su naturaleza |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com |
| `http://rdvocab.info/Elements/#title` | 100% | no | literal:200 | Psicología del niño y pedagogía experimental : problemas y métodos, desarrollo mental, fatiga intelectual; Los amantes desgraciados o El conde de Cominge : drama en tres actos : tercera parte; El caballero de buen gusto : comedia en prosa en tres actos; El contabilismo social (o Sistema para reemplazar la moneda); Moral universal o Deberes del hombre fundados en su naturaleza |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 1059260; 1062782; 701638; 1063700; 1058915 |
| `http://rdaregistry.info/Elements/e/identifierForTheExpression` | 100% | no | literal:200 | 1059260; 1062782; 701638; 1063700; 1058915 |
| `http://rdaregistry.info/Elements/e/manifestationOfExpression` | 100% | no | uri:200 | https://data.cervantesvirtual.com/manifestation/1059261; https://data.cervantesvirtual.com/manifestation/1062783; https://data.cervantesvirtual.com/manifestation/701639; https://data.cervantesvirtual.com/manifestation/1063701; https://data.cervantesvirtual.com/manifestation/1058916 |
| `http://rdaregistry.info/Elements/e/workExpressed` | 100% | no | uri:200 | https://data.cervantesvirtual.com/work/1059259; https://data.cervantesvirtual.com/work/1062781; https://data.cervantesvirtual.com/work/701637; https://data.cervantesvirtual.com/work/1063699; https://data.cervantesvirtual.com/work/1058914 |
| `http://rdaregistry.info/Elements/e/languageOfExpression` | 96% | yes | uri:208 | https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/fr; https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/it; https://data.cervantesvirtual.com/language/es |
| `http://rdaregistry.info/Elements/e/contributor` | 50% | yes | uri:109 | https://data.cervantesvirtual.com/person/73130; https://data.cervantesvirtual.com/person/73132; https://data.cervantesvirtual.com/person/10168; https://data.cervantesvirtual.com/person/73273; https://data.cervantesvirtual.com/person/7750 |
| `http://rdaregistry.info/Elements/e/translator` | 37% | yes | uri:76 | https://data.cervantesvirtual.com/person/73021; https://data.cervantesvirtual.com/person/73005; https://data.cervantesvirtual.com/person/73005; https://data.cervantesvirtual.com/person/73061; https://data.cervantesvirtual.com/person/73083 |
| `http://rdaregistry.info/Elements/e/illustrator` | 14% | yes | uri:30 | https://data.cervantesvirtual.com/person/73105; https://data.cervantesvirtual.com/person/73116; https://data.cervantesvirtual.com/person/73150; https://data.cervantesvirtual.com/person/73217; https://data.cervantesvirtual.com/person/73218 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://rdvocab.info/Elements/#title`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）
- `http://rdaregistry.info/Elements/e/identifierForTheExpression`（被覆率 100%）

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

### `http://rdaregistry.info/Elements/c/Work`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://rdaregistry.info/Elements/c/Work; http://rdaregistry.info/Elements/c/Work; http://rdaregistry.info/Elements/c/Work; http://rdaregistry.info/Elements/c/Work; http://rdaregistry.info/Elements/c/Work |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026 |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | Rey decretado en el cielo y astucias de Luzifer : comedia famosa. Segunda parte; Carta de Marcelo Martínez Alcubilla a Rafael Altamira. Santander, 2 de septiembre de 1912; Tarjeta postal de Marcelo Martínez Alcubilla a Rafael Altamira. Santander, 24 de septiembre de 1913; Tarjeta postal de Marcelo Martínez Alcubilla a Rafael Altamira. Reinosa (Cantabria), 1913; Diccionario de la jurisprudencia penal de España o Repertorio alfabético de la jurisprudencia ... |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com |
| `http://rdaregistry.info/Elements/w/author` | 100% | no | uri:200 | https://data.cervantesvirtual.com/person/73001; https://data.cervantesvirtual.com/person/73004; https://data.cervantesvirtual.com/person/73004; https://data.cervantesvirtual.com/person/73004; https://data.cervantesvirtual.com/person/73004 |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 1020138; 1050983; 1051160; 1051163; 1058269 |
| `http://rdaregistry.info/Elements/w/expressionOfWork` | 100% | yes | uri:202 | https://data.cervantesvirtual.com/expression/1020139; https://data.cervantesvirtual.com/expression/1050984; https://data.cervantesvirtual.com/expression/1051161; https://data.cervantesvirtual.com/expression/1051164; https://data.cervantesvirtual.com/expression/1058270 |
| `http://rdaregistry.info/Elements/w/manifestationOfWork` | 100% | no | uri:200 | https://data.cervantesvirtual.com/manifestation/1020140; https://data.cervantesvirtual.com/manifestation/1050985; https://data.cervantesvirtual.com/manifestation/1051162; https://data.cervantesvirtual.com/manifestation/1051165; https://data.cervantesvirtual.com/manifestation/1058271 |
| `http://rdaregistry.info/Elements/w/titleOfTheWork` | 100% | no | literal:200 | Rey decretado en el cielo y astucias de Luzifer : comedia famosa. Segunda parte; Carta de Marcelo Martínez Alcubilla a Rafael Altamira. Santander, 2 de septiembre de 1912; Tarjeta postal de Marcelo Martínez Alcubilla a Rafael Altamira. Santander, 24 de septiembre de 1913; Tarjeta postal de Marcelo Martínez Alcubilla a Rafael Altamira. Reinosa (Cantabria), 1913; Diccionario de la jurisprudencia penal de España o Repertorio alfabético de la jurisprudencia ... |
| `http://purl.org/dc/elements/1.1/subject` | 38% | yes | literal:143, uri:32 | https://data.cervantesvirtual.com/person/73004; https://data.cervantesvirtual.com/person/73004; https://data.cervantesvirtual.com/person/73004; Derecho penal -- Historia -- Fuentes -- EMBUS; Derecho penal -- España -- Jurisprudencia -- Diccionarios -- EMBUS |
| `http://rdaregistry.info/Elements/w/formOfWork` | 8% | no | uri:16 | http://id.loc.gov/authorities/genreForms/gf2014026191; http://id.loc.gov/authorities/genreForms/gf2014026191; http://id.loc.gov/authorities/genreForms/gf2014026191; http://id.loc.gov/authorities/genreForms/gf2014026191; http://id.loc.gov/authorities/genreForms/gf2014026168 |
| `http://rdvocab.info/Elements/#titleProper` | 3% | no | literal:6 | [Constitución, 1807]; [Meditationes vitae Christi]; [Breve, 1254-07-08]; No cabe mas en amor, ni hay amor firme sin celos; El asombro de Jerez, Juana la Rabicortona. Segunda parte |
| `http://rdaregistry.info/Elements/w/P10055` | 2% | yes | uri:4 | https://data.cervantesvirtual.com/person/73066; https://data.cervantesvirtual.com/person/73066; https://data.cervantesvirtual.com/person/109754; https://data.cervantesvirtual.com/person/73135 |
| `http://rdaregistry.info/Elements/w/variantTitleForTheWork` | 2% | yes | literal:4 | Dido abandonada; Valiente Eneas, El; El Demoofonte :; Perla asombro del mar en la merced de su aurora, vida y muerte de Santa María de Cervellón y Socos, hija natural de la excelentísima ciudad de Barcelona |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://rdaregistry.info/Elements/w/titleOfTheWork`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）

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

### `http://rdaregistry.info/Elements/c/Manifestation`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:406 | http://purl.org/dc/terms/bibliographicCitation; http://rdaregistry.info/Elements/c/Manifestation; http://purl.org/dc/terms/bibliographicCitation; http://rdaregistry.info/Elements/c/Manifestation; http://purl.org/dc/terms/bibliographicCitation |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026 |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F; Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .; Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721; Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ... /  dixola ... Francisco Cabello y Negrete .; Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets /  revûes & corrigées de nouveau ; tome premier [-second] |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 1002915; 1004651; 1005770; 1006358; 1007072 |
| `http://purl.org/dc/terms/bibliographicCitation` | 100% | no | literal:200 | @Misc{BVMC:1002915,
author = {Massillon, Jean Baptiste, (C.O.), Obispo de Clermont },
title = {Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo},
url = {https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915}
}
; @Misc{BVMC:1004651,
title = {Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .},
url = {https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651}
}
; @Misc{BVMC:1005770,
title = {Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721},
url = {https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770}
}
; @Misc{BVMC:1006358,
author = {Cabello y Negrete, Francisco},
title = {Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ...},
url = {https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358}
}
; @Misc{BVMC:1007072,
author = {Mariotte, Edmé},
title = {Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets},
url = {https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072}
}
 |
| `http://rdaregistry.info/Elements/m/expressionManifested` | 100% | no | uri:200 | https://data.cervantesvirtual.com/expression/1002914; https://data.cervantesvirtual.com/expression/1004650; https://data.cervantesvirtual.com/expression/1005769; https://data.cervantesvirtual.com/expression/1006357; https://data.cervantesvirtual.com/expression/1007071 |
| `http://rdaregistry.info/Elements/m/title` | 100% | no | literal:200 | Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F; Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .; Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721; Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ... /  dixola ... Francisco Cabello y Negrete .; Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets /  revûes & corrigées de nouveau ; tome premier [-second] |
| `http://rdaregistry.info/Elements/m/uniformResourceLocator` | 100% | no | uri:200 | https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915; https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651; https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770; https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358; https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072 |
| `http://rdaregistry.info/Elements/m/workManifested` | 100% | no | uri:200 | https://data.cervantesvirtual.com/work/1002913; https://data.cervantesvirtual.com/work/1004649; https://data.cervantesvirtual.com/work/1005768; https://data.cervantesvirtual.com/work/1006356; https://data.cervantesvirtual.com/work/1007070 |
| `http://rdaregistry.info/Elements/m/insertedIn` | 100% | yes | uri:404 | https://data.cervantesvirtual.com/manifestation/266317; https://data.cervantesvirtual.com/manifestation/263038; https://data.cervantesvirtual.com/manifestation/266317; https://data.cervantesvirtual.com/manifestation/263038; https://data.cervantesvirtual.com/manifestation/266317 |
| `http://purl.org/dc/elements/1.1/language` | 96% | yes | uri:195 | https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/fr |
| `http://rdaregistry.info/Elements/m/noteOnEditionStatement` | 94% | no | literal:189 | Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla |
| `http://rdaregistry.info/Elements/m/placeOfProduction` | 88% | no | literal:175 | Sevilla : : [editor no identificado] (Imp. y Taller de encuadernaciones de Juan Moyano), , 1852 (Imp. y Taller de encuadernaciones de Juan Moyano); Impresso en Granada : en la imprenta de la SSma. Trinidad, 1723?]; [lugar no identificado] : en la Imprenta de la SS. Trinidad, 1721?]; Impresso en Granada : en la imprenta de la SS. Trinidad, 1725?]; A La Haye : chez Jean Neaulme, 1740 |
| `http://xmlns.com/foaf/0.1/homepage` | 86% | no | uri:173 | https://archive.org/details/A1140551; https://archive.org/details/A11202416; https://archive.org/details/A11303806; https://archive.org/details/A11311212; https://archive.org/details/A039a467468 |
| `http://rdaregistry.info/Elements/m/dateOfPublication` | 86% | no | literal:34, uri:137 | , 1852; 1723?]; 1721?]; 1725?]; https://data.cervantesvirtual.com/date/1740 |
| `http://purl.org/dc/terms/publisher` | 84% | no | uri:169 | https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9 |
| `http://rdaregistry.info/Elements/m/noteOnManifestation` | 74% | yes | literal:375 | Descr. física Sign.: A8; Descr. física Port. con orla tip; Descr. física Texto con orla tip; Nota Area Public. Datos de imp. tomados del final del texto; Nota Area Public. Año de imp. tomado del tít |
| `http://rdaregistry.info/Elements/m/dimensions` | 71% | no | literal:142 | ; 21 cm; 4º; ; 4o; ; 4o; ; 4o |
| `http://xmlns.com/foaf/0.1/depiction` | 64% | no | uri:127 | https://www.cervantesvirtual.com/portadas/069/0697961; https://www.cervantesvirtual.com/portadas/069/0697991; https://www.cervantesvirtual.com/portadas/069/0697997; https://www.cervantesvirtual.com/portadas/069/0698030; https://www.cervantesvirtual.com/portadas/069/0698081 |
| `http://rdaregistry.info/Elements/m/printer` | 45% | no | uri:90 | https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/person/72995; https://data.cervantesvirtual.com/corporatebody/72988 |
| `http://rdaregistry.info/Elements/m/otherPFCManifestation` | 34% | yes | uri:88 | https://data.cervantesvirtual.com/person/72975; https://data.cervantesvirtual.com/person/97172; https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/corporatebody/72982; https://data.cervantesvirtual.com/person/72995 |
| `http://rdaregistry.info/Elements/m/publisher` | 24% | yes | uri:54 | https://data.cervantesvirtual.com/person/73058; https://data.cervantesvirtual.com/corporatebody/100210; https://data.cervantesvirtual.com/person/73028; https://data.cervantesvirtual.com/person/73043; https://data.cervantesvirtual.com/person/73043 |
| `http://rdaregistry.info/Elements/m/publishersName` | 24% | yes | literal:54 | Tarascó y Lassa, Rafael; Imprenta y Librería Española y Extranjera (Sevilla); Alfonso y Padilla, Pedro José; Razola, Casimiro; Razola, Casimiro |
| `http://rdaregistry.info/Elements/u/publisher` | 22% | no | literal:44 | Fundación; ES-GrU; ES-GrU; ES-GrU; SIRSI |
| `http://rdaregistry.info/Elements/m/publicationStatement` | 16% | no | literal:31 | Santander : Ayuntamiento ; Alicante : Biblioteca Virtual Miguel de Cervantes, 2016; Alicante : Biblioteca Virtual Miguel de Cervantes, 2021; Alacant : Biblioteca Virtual Miguel de Cervantes, 2006; Alicante : Biblioteca Virtual Miguel de Cervantes, 2005; Alicante : Biblioteca Virtual Miguel de Cervantes, 2005 |
| `http://rdaregistry.info/Elements/m/exemplarOfManifestation` | 12% | no | uri:25 | https://data.cervantesvirtual.com/item/606066; https://data.cervantesvirtual.com/item/604497; https://data.cervantesvirtual.com/item/136667; https://data.cervantesvirtual.com/item/24233; https://data.cervantesvirtual.com/item/25763 |
| `http://rdaregistry.info/Elements/m/dateOfDistribution` | 12% | no | uri:23 | https://data.cervantesvirtual.com/date/2016; https://data.cervantesvirtual.com/date/2021; https://data.cervantesvirtual.com/date/2006; https://data.cervantesvirtual.com/date/2005; https://data.cervantesvirtual.com/date/2005 |
| `http://rdaregistry.info/Elements/m/carrierType` | 4% | no | uri:9 | http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010 |
| `http://rdaregistry.info/Elements/m/mediaType` | 4% | no | uri:9 | http://rdaregistry.info/termList/RDAMediaType/1003; http://rdaregistry.info/termList/RDAMediaType/1003; http://rdaregistry.info/termList/RDAMediaType/1003; http://rdaregistry.info/termList/RDAMediaType/1008; http://rdaregistry.info/termList/RDAMediaType/1003 |
| `http://rdaregistry.info/Elements/u/contentType` | 4% | no | uri:9 | http://rdaregistry.info/termList/RDAContentType/1020; http://rdaregistry.info/termList/RDAContentType/1020; http://rdaregistry.info/termList/RDAContentType/1004; http://rdaregistry.info/termList/RDAContentType/1009; http://rdaregistry.info/termList/RDAContentType/1007 |
| `http://schema.org/datePublished` | 2% | no | literal:3 | 201510302; 20180381; 202212349 |
| `http://schema.org/headline` | 2% | no | literal:3 | Fundación Pablo Iglesias; Sergio Ramírez; Alfonso de Cartagena |
| `http://schema.org/isBasedOnUrl` | 2% | no | uri:3 | https://www.cervantesvirtual.com/portales/fundacion_pablo_iglesias/; https://www.cervantesvirtual.com/portales/sergio_ramirez/; https://www.cervantesvirtual.com/portales/alfonso_de_cartagena/ |
| `http://schema.org/isFamilyFriendly` | 2% | no | literal:3 | True; True; True |
| `http://schema.org/thumbnailUrl` | 2% | no | uri:3 | https://www.cervantesvirtual.com/images/banners_portales/fundacion-pablo-iglesias.jpg; https://www.cervantesvirtual.com/images/banners_portales/sergio-ramirez.jpg; https://www.cervantesvirtual.com/images/banners_portales/alfonso-de-cartagena-707767.jpg |
| `http://rdaregistry.info/Elements/u/concordance` | 1% | no | uri:2 | https://www.cervantesvirtual.com/concordancias/los-jardines-interiores--0; https://www.cervantesvirtual.com/concordancias/pico-de-la-mirndula-y-la-inquisicin-espaola-breve-indito-de-inocencio-viii-0 |
| `http://rdaregistry.info/Elements/m/frequency` | 1% | no | literal:2 | Semanal; Irregular |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfFirstIssueOrPartOfSequence` | 1% | no | literal:2 | IV Época, núm. 2 (9 mayo 1945); Núm. 1 (25 julio 1944) |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfLastIssueOrPartOfSequence` | 1% | no | literal:2 | V Época, núm. 24 (diciemabre 1969); Núm. 10 (28 julio 1945) |
| `http://rdaregistry.info/Elements/m/noteOnTitle` | 0% | yes | literal:2 | Precede al título: "N. 15"; Inc.: Sale Juan Rana, y Gila. / Gil. ES hora de venir, marido á casa? / Què esto en el mundo passa! [...]. Exp.: para quando à la Rana / le crie pelo / FIN |
| `http://rdaregistry.info/Elements/m/wholePartManifestationRelationship` | 0% | no | uri:1 | https://data.cervantesvirtual.com/manifestation/327300 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/title`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）
- `http://purl.org/dc/terms/bibliographicCitation`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/noteOnEditionStatement`（被覆率 94%）
- `http://rdaregistry.info/Elements/m/placeOfProduction`（被覆率 88%）
- `http://rdaregistry.info/Elements/m/noteOnManifestation`（被覆率 74%）
- `http://rdaregistry.info/Elements/m/dimensions`（被覆率 71%）

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

### `http://purl.org/dc/terms/bibliographicCitation`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | yes | uri:406 | http://purl.org/dc/terms/bibliographicCitation; http://rdaregistry.info/Elements/c/Manifestation; http://purl.org/dc/terms/bibliographicCitation; http://rdaregistry.info/Elements/c/Manifestation; http://purl.org/dc/terms/bibliographicCitation |
| `http://purl.org/dc/terms/created` | 100% | no | literal:200 | 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026; 02/02/2026 |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:200 | Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F; Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .; Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721; Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ... /  dixola ... Francisco Cabello y Negrete .; Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets /  revûes & corrigées de nouveau ; tome premier [-second] |
| `http://purl.org/dc/terms/creator` | 100% | no | uri:200 | http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com; http://www.cervantesvirtual.com |
| `http://purl.org/dc/elements/1.1/identifier` | 100% | no | literal:200 | 1002915; 1004651; 1005770; 1006358; 1007072 |
| `http://purl.org/dc/terms/bibliographicCitation` | 100% | no | literal:200 | @Misc{BVMC:1002915,
author = {Massillon, Jean Baptiste, (C.O.), Obispo de Clermont },
title = {Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo},
url = {https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915}
}
; @Misc{BVMC:1004651,
title = {Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .},
url = {https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651}
}
; @Misc{BVMC:1005770,
title = {Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721},
url = {https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770}
}
; @Misc{BVMC:1006358,
author = {Cabello y Negrete, Francisco},
title = {Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ...},
url = {https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358}
}
; @Misc{BVMC:1007072,
author = {Mariotte, Edmé},
title = {Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets},
url = {https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072}
}
 |
| `http://rdaregistry.info/Elements/m/expressionManifested` | 100% | no | uri:200 | https://data.cervantesvirtual.com/expression/1002914; https://data.cervantesvirtual.com/expression/1004650; https://data.cervantesvirtual.com/expression/1005769; https://data.cervantesvirtual.com/expression/1006357; https://data.cervantesvirtual.com/expression/1007071 |
| `http://rdaregistry.info/Elements/m/title` | 100% | no | literal:200 | Escritos inéditos de Monseñor Juan Bautista Massillon y apuntes biográficos acerca del mismo /  traducidos y ordenados por el Doctor D.C.F; Metrico manifiesto de la celebre, y magnifica festiuidad, que el illustre, y venerable Orden Tercero dedicò con rendido afecto a Maria SSpma.s del Carmen su patrona, y madre esclarecida, en su propio dia diez y seis de iulio de este año de mil setecientes y veinte y tres .; Letras que se han de cantar en la Capilla del glorioso Obispo, y martyr Señor San Blas, en la Santa Iglesia Metropolitana, y Apostolica de Granada, este año de 1721; Oracion funebre, en las honras reales, que à la tierna memoria de el Rey nuestro señor D. Luis RIR de Castilla, consagraron en la santa iglesia colegial de Antequera ... /  dixola ... Francisco Cabello y Negrete .; Oeuvres de M. Mariotte ... : comprenant tous les traitez de cet auteur ... : imprimees sur les exemplaires les plus exacts et les plus complets /  revûes & corrigées de nouveau ; tome premier [-second] |
| `http://rdaregistry.info/Elements/m/uniformResourceLocator` | 100% | no | uri:200 | https://www.cervantesvirtual.com/obra/escritos-ineditos-de-monsenor-juan-bautista-massillon-y-apuntes-biograficos-acerca-del-mismo-1002915; https://www.cervantesvirtual.com/obra/metrico-manifiesto-de-la-celebre-y-magnifica-festiuidad-que-el-illustre-y-venerable-orden-tercero-dedico-con-rendido-afecto-a-maria-sspmas-del-carmen-su-patrona-y-madre-esclarecida-1004651; https://www.cervantesvirtual.com/obra/letras-que-se-han-de-cantar-en-la-capilla-del-glorioso-obispo-y-martyr-senor-san-blas-en-la-santa-iglesia-metropolitana-y-apostolica-de-granada-este-ano-de-1721-1005770; https://www.cervantesvirtual.com/obra/oracion-funebre-en-las-honras-reales-que-a-la-tierna-memoria-de-el-rey-nuestro-senor-d-luis-rir-de-castilla-consagraron-en-la-santa-iglesia-colegial-de-antequera-1006358; https://www.cervantesvirtual.com/obra/oeuvres-de-m-mariotte--comprenant-tous-les-traitez-de-cet-auteur--imprimees-sur-les-exemplaires-les-plus-exacts-et-les-plus-complets-1007072 |
| `http://rdaregistry.info/Elements/m/workManifested` | 100% | no | uri:200 | https://data.cervantesvirtual.com/work/1002913; https://data.cervantesvirtual.com/work/1004649; https://data.cervantesvirtual.com/work/1005768; https://data.cervantesvirtual.com/work/1006356; https://data.cervantesvirtual.com/work/1007070 |
| `http://rdaregistry.info/Elements/m/insertedIn` | 100% | yes | uri:404 | https://data.cervantesvirtual.com/manifestation/266317; https://data.cervantesvirtual.com/manifestation/263038; https://data.cervantesvirtual.com/manifestation/266317; https://data.cervantesvirtual.com/manifestation/263038; https://data.cervantesvirtual.com/manifestation/266317 |
| `http://purl.org/dc/elements/1.1/language` | 96% | yes | uri:195 | https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/es; https://data.cervantesvirtual.com/language/fr |
| `http://rdaregistry.info/Elements/m/noteOnEditionStatement` | 94% | no | literal:189 | Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla; Reproducción digital del original conservado en la Biblioteca de la Universidad de Sevilla |
| `http://rdaregistry.info/Elements/m/placeOfProduction` | 88% | no | literal:175 | Sevilla : : [editor no identificado] (Imp. y Taller de encuadernaciones de Juan Moyano), , 1852 (Imp. y Taller de encuadernaciones de Juan Moyano); Impresso en Granada : en la imprenta de la SSma. Trinidad, 1723?]; [lugar no identificado] : en la Imprenta de la SS. Trinidad, 1721?]; Impresso en Granada : en la imprenta de la SS. Trinidad, 1725?]; A La Haye : chez Jean Neaulme, 1740 |
| `http://xmlns.com/foaf/0.1/homepage` | 86% | no | uri:173 | https://archive.org/details/A1140551; https://archive.org/details/A11202416; https://archive.org/details/A11303806; https://archive.org/details/A11311212; https://archive.org/details/A039a467468 |
| `http://rdaregistry.info/Elements/m/dateOfPublication` | 86% | no | literal:34, uri:137 | , 1852; 1723?]; 1721?]; 1725?]; https://data.cervantesvirtual.com/date/1740 |
| `http://purl.org/dc/terms/publisher` | 84% | no | uri:169 | https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9; https://data.cervantesvirtual.com/institution/9 |
| `http://rdaregistry.info/Elements/m/noteOnManifestation` | 74% | yes | literal:375 | Descr. física Sign.: A8; Descr. física Port. con orla tip; Descr. física Texto con orla tip; Nota Area Public. Datos de imp. tomados del final del texto; Nota Area Public. Año de imp. tomado del tít |
| `http://rdaregistry.info/Elements/m/dimensions` | 71% | no | literal:142 | ; 21 cm; 4º; ; 4o; ; 4o; ; 4o |
| `http://xmlns.com/foaf/0.1/depiction` | 64% | no | uri:127 | https://www.cervantesvirtual.com/portadas/069/0697961; https://www.cervantesvirtual.com/portadas/069/0697991; https://www.cervantesvirtual.com/portadas/069/0697997; https://www.cervantesvirtual.com/portadas/069/0698030; https://www.cervantesvirtual.com/portadas/069/0698081 |
| `http://rdaregistry.info/Elements/m/printer` | 45% | no | uri:90 | https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/person/72995; https://data.cervantesvirtual.com/corporatebody/72988 |
| `http://rdaregistry.info/Elements/m/otherPFCManifestation` | 34% | yes | uri:88 | https://data.cervantesvirtual.com/person/72975; https://data.cervantesvirtual.com/person/97172; https://data.cervantesvirtual.com/corporatebody/72988; https://data.cervantesvirtual.com/corporatebody/72982; https://data.cervantesvirtual.com/person/72995 |
| `http://rdaregistry.info/Elements/m/publisher` | 24% | yes | uri:54 | https://data.cervantesvirtual.com/person/73058; https://data.cervantesvirtual.com/corporatebody/100210; https://data.cervantesvirtual.com/person/73028; https://data.cervantesvirtual.com/person/73043; https://data.cervantesvirtual.com/person/73043 |
| `http://rdaregistry.info/Elements/m/publishersName` | 24% | yes | literal:54 | Tarascó y Lassa, Rafael; Imprenta y Librería Española y Extranjera (Sevilla); Alfonso y Padilla, Pedro José; Razola, Casimiro; Razola, Casimiro |
| `http://rdaregistry.info/Elements/u/publisher` | 22% | no | literal:44 | Fundación; ES-GrU; ES-GrU; ES-GrU; SIRSI |
| `http://rdaregistry.info/Elements/m/publicationStatement` | 16% | no | literal:31 | Santander : Ayuntamiento ; Alicante : Biblioteca Virtual Miguel de Cervantes, 2016; Alicante : Biblioteca Virtual Miguel de Cervantes, 2021; Alacant : Biblioteca Virtual Miguel de Cervantes, 2006; Alicante : Biblioteca Virtual Miguel de Cervantes, 2005; Alicante : Biblioteca Virtual Miguel de Cervantes, 2005 |
| `http://rdaregistry.info/Elements/m/exemplarOfManifestation` | 12% | no | uri:25 | https://data.cervantesvirtual.com/item/606066; https://data.cervantesvirtual.com/item/604497; https://data.cervantesvirtual.com/item/136667; https://data.cervantesvirtual.com/item/24233; https://data.cervantesvirtual.com/item/25763 |
| `http://rdaregistry.info/Elements/m/dateOfDistribution` | 12% | no | uri:23 | https://data.cervantesvirtual.com/date/2016; https://data.cervantesvirtual.com/date/2021; https://data.cervantesvirtual.com/date/2006; https://data.cervantesvirtual.com/date/2005; https://data.cervantesvirtual.com/date/2005 |
| `http://rdaregistry.info/Elements/m/carrierType` | 4% | no | uri:9 | http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010; http://rdaregistry.info/termList/RDACarrierType/1010 |
| `http://rdaregistry.info/Elements/m/mediaType` | 4% | no | uri:9 | http://rdaregistry.info/termList/RDAMediaType/1003; http://rdaregistry.info/termList/RDAMediaType/1003; http://rdaregistry.info/termList/RDAMediaType/1003; http://rdaregistry.info/termList/RDAMediaType/1008; http://rdaregistry.info/termList/RDAMediaType/1003 |
| `http://rdaregistry.info/Elements/u/contentType` | 4% | no | uri:9 | http://rdaregistry.info/termList/RDAContentType/1020; http://rdaregistry.info/termList/RDAContentType/1020; http://rdaregistry.info/termList/RDAContentType/1004; http://rdaregistry.info/termList/RDAContentType/1009; http://rdaregistry.info/termList/RDAContentType/1007 |
| `http://schema.org/datePublished` | 2% | no | literal:3 | 201510302; 20180381; 202212349 |
| `http://schema.org/headline` | 2% | no | literal:3 | Fundación Pablo Iglesias; Sergio Ramírez; Alfonso de Cartagena |
| `http://schema.org/isBasedOnUrl` | 2% | no | uri:3 | https://www.cervantesvirtual.com/portales/fundacion_pablo_iglesias/; https://www.cervantesvirtual.com/portales/sergio_ramirez/; https://www.cervantesvirtual.com/portales/alfonso_de_cartagena/ |
| `http://schema.org/isFamilyFriendly` | 2% | no | literal:3 | True; True; True |
| `http://schema.org/thumbnailUrl` | 2% | no | uri:3 | https://www.cervantesvirtual.com/images/banners_portales/fundacion-pablo-iglesias.jpg; https://www.cervantesvirtual.com/images/banners_portales/sergio-ramirez.jpg; https://www.cervantesvirtual.com/images/banners_portales/alfonso-de-cartagena-707767.jpg |
| `http://rdaregistry.info/Elements/u/concordance` | 1% | no | uri:2 | https://www.cervantesvirtual.com/concordancias/los-jardines-interiores--0; https://www.cervantesvirtual.com/concordancias/pico-de-la-mirndula-y-la-inquisicin-espaola-breve-indito-de-inocencio-viii-0 |
| `http://rdaregistry.info/Elements/m/frequency` | 1% | no | literal:2 | Semanal; Irregular |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfFirstIssueOrPartOfSequence` | 1% | no | literal:2 | IV Época, núm. 2 (9 mayo 1945); Núm. 1 (25 julio 1944) |
| `http://rdaregistry.info/Elements/m/chronologicalDesignationOfLastIssueOrPartOfSequence` | 1% | no | literal:2 | V Época, núm. 24 (diciemabre 1969); Núm. 10 (28 julio 1945) |
| `http://rdaregistry.info/Elements/m/noteOnTitle` | 0% | yes | literal:2 | Precede al título: "N. 15"; Inc.: Sale Juan Rana, y Gila. / Gil. ES hora de venir, marido á casa? / Què esto en el mundo passa! [...]. Exp.: para quando à la Rana / le crie pelo / FIN |
| `http://rdaregistry.info/Elements/m/wholePartManifestationRelationship` | 0% | no | uri:1 | https://data.cervantesvirtual.com/manifestation/327300 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/title`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/elements/1.1/identifier`（被覆率 100%）
- `http://purl.org/dc/terms/bibliographicCitation`（被覆率 100%）
- `http://rdaregistry.info/Elements/m/noteOnEditionStatement`（被覆率 94%）
- `http://rdaregistry.info/Elements/m/placeOfProduction`（被覆率 88%）
- `http://rdaregistry.info/Elements/m/noteOnManifestation`（被覆率 74%）
- `http://rdaregistry.info/Elements/m/dimensions`（被覆率 71%）

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
