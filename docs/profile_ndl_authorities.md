# NDL Web NDL Authorities スキーマ偵察結果

- エンドポイント: https://id.ndl.go.jp/auth/ndla/sparql

## 主要クラス候補（インスタンス数上位）

⚠️ 要求した上位20件に対し、実際に発見されたクラスは5件のみだった。スキーマが元々小さい可能性もあるが、GROUP BY集計自体が打ち切られている可能性も排除できない（素通しせず目視確認すること）。

| 順位 | クラスURI | インスタンス数(集計値) | 疑わしさ |
|---|---|---|---|
| 1 | `http://www.w3.org/2004/02/skos/core#Concept` | 1490689 | - |
| 2 | `http://xmlns.com/foaf/0.1/Person` | 1048223 | - |
| 3 | `http://xmlns.com/foaf/0.1/Organization` | 242412 | - |
| 4 | `http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family` | 3018 | - |
| 5 | `http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work` | 1100 | - |

## クラスごとの述語プロファイル

### `http://www.w3.org/2004/02/skos/core#Concept`（全体 1490689 件中 105 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:105 | 1 (1%) | http://www.w3.org/2004/02/skos/core#Concept(105) |
| `http://purl.org/dc/terms/created` | 100% | no | literal:105 | 9 (9%) | 2013-11-20(74); 2013-11-21(15); 2011-07-20(10); 2012-05-18(1); 1992-04-24(1) |
| `http://purl.org/dc/terms/modified` | 100% | no | literal:105 | 101 (96%) | 2017-03-28T18:56:56(5); 2017-03-28T18:56:51(1); 2014-04-08T11:15:05(1); 2013-11-20T11:49:44(1); 2013-11-27T14:52:37(1) |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:105 | 105 (100%) | ミッキー・カーチス, 1938-(1); 日本曳家協会(1); 椎葉, 乙虫, 1942-(1); 川路, 美樹, 1938-(1); 片山, 淳子(1) |
| `http://xmlns.com/foaf/0.1/primaryTopic` | 99% | no | uri:104 | 104 (100%) | http://id.ndl.go.jp/auth/entity/001103148(1); http://id.ndl.go.jp/auth/entity/001152848(1); http://id.ndl.go.jp/auth/entity/001152849(1); http://id.ndl.go.jp/auth/entity/001152850(1); http://id.ndl.go.jp/auth/entity/001152851(1) |
| `http://www.w3.org/2008/05/skos-xl#prefLabel` | 99% | no | bnode:104 | - |  |
| `http://www.w3.org/2004/02/skos/core#exactMatch` | 99% | yes | uri:114 | 114 (110%) | http://viaf.org/viaf/sourceID/NDL%7C001103148#skos:Concept(1); http://viaf.org/viaf/sourceID/NDL%7C001152848#skos:Concept(1); http://viaf.org/viaf/sourceID/NDL%7C001152849#skos:Concept(1); http://viaf.org/viaf/sourceID/NDL%7C001152850#skos:Concept(1); http://viaf.org/viaf/sourceID/NDL%7C001152851#skos:Concept(1) |
| `http://www.w3.org/2004/02/skos/core#inScheme` | 99% | no | uri:104 | 3 (3%) | http://id.ndl.go.jp/auth#personalNames(70); http://id.ndl.go.jp/auth#corporateNames(33); http://id.ndl.go.jp/auth#geographicNames(1) |
| `http://purl.org/dc/terms/source` | 64% | yes | literal:84 | 74 (110%) | 推量読み(3); ア・テクニック・オブ・アドバンスド・ラテン・アメリカン・フィガーズ, 2013.10(3); 稲むらの火浜口梧陵のはなし, 2013.5(3); 茶の機能, 2013.11(2); 八重山タイムス(2) |
| `http://www.w3.org/2008/05/skos-xl#altLabel` | 32% | yes | bnode:51 | - |  |
| `http://www.w3.org/2004/02/skos/core#note` | 8% | no | literal:8 | 8 (100%) | 別名: 川路, 美樹, 1938-(1); 別名: ミッキー・カーチス, 1938-(1); 別名: 漣, 健児, 1931-2005(1); 本名: 岡村, 浩, 1964-(1); 別名: 新田, 宣夫.(1) |
| `http://www.w3.org/2004/02/skos/core#historyNote` | 4% | no | literal:4 | 4 (100%) | 生年追加 (20190626)(1); 生年追加 (20140804)(1); 没年追加 (20150408)(1); 多摩総合精神保健福祉センター (東京都立)→東京都立多摩総合精神保健福祉センター (20050224)(1) |
| `http://ndl.go.jp/dcndl/terms/laterName` | 3% | no | uri:3 | 3 (100%) | http://id.ndl.go.jp/auth/ndlna/00558619(1); http://id.ndl.go.jp/auth/ndlna/001152908(1); http://id.ndl.go.jp/auth/ndlna/001152870(1) |
| `http://ndl.go.jp/dcndl/terms/previousName` | 3% | no | uri:3 | 3 (100%) | http://id.ndl.go.jp/auth/ndlna/00272948(1); http://id.ndl.go.jp/auth/ndlna/001152918(1); http://id.ndl.go.jp/auth/ndlna/001152871(1) |
| `http://ndl.go.jp/dcndl/terms/realName` | 1% | no | uri:1 | 1 (100%) | http://id.ndl.go.jp/auth/ndlna/00668070(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- `http://www.w3.org/2004/02/skos/core#inScheme`（被覆率 99%、異なり値数 3/104 = 3%）
- `http://purl.org/dc/terms/created`（被覆率 100%、異なり値数 9/105 = 9%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/terms/modified`（被覆率 100%）
- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://xmlns.com/foaf/0.1/primaryTopic`（被覆率 99%）
- `http://www.w3.org/2008/05/skos-xl#prefLabel`（被覆率 99%）
- `http://www.w3.org/2004/02/skos/core#exactMatch`（被覆率 99%）
- `http://www.w3.org/2004/02/skos/core#inScheme`（被覆率 99%）
- `http://purl.org/dc/terms/source`（被覆率 64%）
- `http://www.w3.org/2008/05/skos-xl#altLabel`（被覆率 32%）

### `http://xmlns.com/foaf/0.1/Person`（全体 1048223 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://xmlns.com/foaf/0.1/Person(200) |
| `http://xmlns.com/foaf/0.1/name` | 100% | no | literal:200 | 200 (100%) | 椎葉乙虫(1); 川路美樹(1); 片山淳子(1); 一恋ちえ(1); 加藤明彦(1) |
| `http://RDVocab.info/ElementsGr2/dateOfBirth` | 38% | no | literal:77 | 47 (61%) | 1959(5); 1946(4); 1938(3); 1947(3); 1978(3) |
| `http://RDVocab.info/ElementsGr2/biographicalInformation` | 26% | no | literal:52 | 44 (85%) | 大学教員(7); 漫画家(2); 大学教員, カルチャーシンク経営(2); 静岡県文学連盟会員(1); 作曲家, 作詞家(1) |
| `http://RDVocab.info/ElementsGr2/fieldOfActivityOfThePerson` | 4% | no | literal:7 | 7 (100%) | 応用生物化学(1); 生物系薬学(1); 日本語文法 (談話レベル)(1); 形而上学(1); 生化学(1) |
| `http://RDVocab.info/ElementsGr2/dateOfDeath` | 2% | no | literal:5 | 5 (100%) | 2015(1); 1712(1); 1683(1); 1966(1); (1) |
| `http://RDVocab.info/ElementsGr2/professionOrOccupation` | 2% | no | literal:3 | 3 (100%) | 児童文学作家(1); ロケット科学者, 大学教員(1); 精神科医(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）
- `http://RDVocab.info/ElementsGr2/dateOfBirth`（被覆率 38%）

### `http://xmlns.com/foaf/0.1/Organization`（全体 242412 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://xmlns.com/foaf/0.1/Organization(200) |
| `http://xmlns.com/foaf/0.1/name` | 100% | no | literal:200 | 200 (100%) | 日本曳家協会(1); チャイルドケモハウス(1); 熊本県立第二高等学校(1); 実地指導対策研究会(1); 総合女性史学会(1) |
| `http://RDVocab.info/ElementsGr2/dateOfEstablishment` | 40% | no | literal:81 | 41 (51%) | 2012(6); 2009(6); 2013(4); 2006(3); 1991(3) |
| `http://RDVocab.info/ElementsGr2/corporateHistory` | 35% | yes | literal:79 | 56 (80%) | 株式会社(9); 特定非営利活動法人(5); 一般社団法人(4); 名称変更(3); 財団法人(3) |
| `http://RDVocab.info/ElementsGr2/dateOfTermination` | 8% | no | literal:16 | 12 (75%) | 2013(3); 1995(2); 2012(2); 1985(1); 1976(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）
- `http://RDVocab.info/ElementsGr2/dateOfEstablishment`（被覆率 40%）
- `http://RDVocab.info/ElementsGr2/corporateHistory`（被覆率 35%）

### `http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family`（全体 3018 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family(200) |
| `http://xmlns.com/foaf/0.1/name` | 100% | no | literal:200 | 165 (82%) | 中村(12); 池田(4); 長谷川(4); 中山(3); 清水(2) |
| `http://RDVocab.info/ElementsGr2/familyHistory` | 4% | no | literal:8 | 7 (88%) | 旗本(2); 古代の豪族, 皇別氏族.(1); 付家老(1); 本多忠勝家の家老(1); 公家(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）

### `http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work`（全体 1100 件中 200 件をサンプリング）

| 述語URI | 被覆率 | 多値 | 値の型 | 異なり値数(対象主語数比) | 頻出値(上位) |
|---|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | 1 (0%) | http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work(200) |
| `http://purl.org/dc/terms/title` | 100% | no | literal:200 | 200 (100%) | 古画備考(1); ソクラテスの弁明(1); 東方見聞録(1); 大和物語(1); 竹取物語(1) |
| `http://purl.org/dc/terms/creator` | 92% | yes | uri:197 | 173 (95%) | http://id.ndl.go.jp/auth/entity/00456207(7); http://id.ndl.go.jp/auth/entity/00447571(4); http://id.ndl.go.jp/auth/entity/00430838(3); http://id.ndl.go.jp/auth/entity/00431922(3); http://id.ndl.go.jp/auth/entity/00432315(3) |
| `http://purl.org/dc/terms/created` | 2% | no | literal:3 | 3 (100%) | 1966年(1); 1885年(1); 1814年(1) |

**ラベル候補プロパティ**（被覆率が高く、値の異なり数が対象主語数に対して小さい＝閉じた集合とみなせる述語。確定ではない）:

- (機械的な提案なし。人間による個別調査が必要)

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/title`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 92%）

---
**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」はPhase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。
