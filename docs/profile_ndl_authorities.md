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

### `http://www.w3.org/2004/02/skos/core#Concept`（サンプルインスタンス数: 105）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:105 | http://www.w3.org/2004/02/skos/core#Concept; http://www.w3.org/2004/02/skos/core#Concept; http://www.w3.org/2004/02/skos/core#Concept; http://www.w3.org/2004/02/skos/core#Concept; http://www.w3.org/2004/02/skos/core#Concept |
| `http://purl.org/dc/terms/created` | 100% | no | literal:105 | 2012-05-18; 2013-11-20; 2013-11-20; 2013-11-20; 2013-11-20 |
| `http://purl.org/dc/terms/modified` | 100% | no | literal:105 | 2017-03-28T18:56:51; 2014-04-08T11:15:05; 2013-11-20T11:49:44; 2013-11-27T14:52:37; 2013-11-20T11:52:05 |
| `http://www.w3.org/2000/01/rdf-schema#label` | 100% | no | literal:105 | ミッキー・カーチス, 1938-; 日本曳家協会; 椎葉, 乙虫, 1942-; 川路, 美樹, 1938-; 片山, 淳子 |
| `http://xmlns.com/foaf/0.1/primaryTopic` | 99% | no | uri:104 | http://id.ndl.go.jp/auth/entity/001103148; http://id.ndl.go.jp/auth/entity/001152848; http://id.ndl.go.jp/auth/entity/001152849; http://id.ndl.go.jp/auth/entity/001152850; http://id.ndl.go.jp/auth/entity/001152851 |
| `http://www.w3.org/2008/05/skos-xl#prefLabel` | 99% | no | bnode:104 | nodeID://b1246795179; nodeID://b1246855228; nodeID://b1246855230; nodeID://b1246855233; nodeID://b1246855234 |
| `http://www.w3.org/2004/02/skos/core#exactMatch` | 99% | yes | uri:114 | http://viaf.org/viaf/sourceID/NDL%7C001103148#skos:Concept; http://viaf.org/viaf/sourceID/NDL%7C001152848#skos:Concept; http://viaf.org/viaf/sourceID/NDL%7C001152849#skos:Concept; http://viaf.org/viaf/sourceID/NDL%7C001152850#skos:Concept; http://viaf.org/viaf/sourceID/NDL%7C001152851#skos:Concept |
| `http://www.w3.org/2004/02/skos/core#inScheme` | 99% | no | uri:104 | http://id.ndl.go.jp/auth#personalNames; http://id.ndl.go.jp/auth#corporateNames; http://id.ndl.go.jp/auth#personalNames; http://id.ndl.go.jp/auth#personalNames; http://id.ndl.go.jp/auth#personalNames |
| `http://purl.org/dc/terms/source` | 64% | yes | literal:84 | おれと戦争と音楽と, 2012.1; 家が動く!曳家の仕事, 2013.10; 冬隣, 2013.11; おれと戦争と音楽と, 2012.1: 本文 (読み), (生年); ユーアーマイデスティニー, c1958 |
| `http://www.w3.org/2008/05/skos-xl#altLabel` | 32% | yes | bnode:51 | nodeID://b1246795180; nodeID://b1246795181; nodeID://b1246795182; nodeID://b1246855229; nodeID://b1246855238 |
| `http://www.w3.org/2004/02/skos/core#note` | 8% | no | literal:8 | 別名: 川路, 美樹, 1938-; 別名: ミッキー・カーチス, 1938-; 別名: 漣, 健児, 1931-2005; 本名: 岡村, 浩, 1964-; 別名: 新田, 宣夫. |
| `http://www.w3.org/2004/02/skos/core#historyNote` | 4% | no | literal:4 | 生年追加 (20190626); 生年追加 (20140804); 没年追加 (20150408); 多摩総合精神保健福祉センター (東京都立)→東京都立多摩総合精神保健福祉センター (20050224) |
| `http://ndl.go.jp/dcndl/terms/laterName` | 3% | no | uri:3 | http://id.ndl.go.jp/auth/ndlna/00558619; http://id.ndl.go.jp/auth/ndlna/001152908; http://id.ndl.go.jp/auth/ndlna/001152870 |
| `http://ndl.go.jp/dcndl/terms/previousName` | 3% | no | uri:3 | http://id.ndl.go.jp/auth/ndlna/00272948; http://id.ndl.go.jp/auth/ndlna/001152918; http://id.ndl.go.jp/auth/ndlna/001152871 |
| `http://ndl.go.jp/dcndl/terms/realName` | 1% | no | uri:1 | http://id.ndl.go.jp/auth/ndlna/00668070 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://www.w3.org/2000/01/rdf-schema#label`（被覆率 100%）
- `http://purl.org/dc/terms/created`（被覆率 100%）
- `http://purl.org/dc/terms/modified`（被覆率 100%）
- `http://purl.org/dc/terms/source`（被覆率 64%）

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

### `http://xmlns.com/foaf/0.1/Person`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://xmlns.com/foaf/0.1/Person; http://xmlns.com/foaf/0.1/Person; http://xmlns.com/foaf/0.1/Person; http://xmlns.com/foaf/0.1/Person; http://xmlns.com/foaf/0.1/Person |
| `http://xmlns.com/foaf/0.1/name` | 100% | no | literal:200 | 椎葉乙虫; 川路美樹; 片山淳子; 一恋ちえ; 加藤明彦 |
| `http://RDVocab.info/ElementsGr2/dateOfBirth` | 38% | no | literal:77 | 1942; 1938; 1987; 1947; 1955 |
| `http://RDVocab.info/ElementsGr2/biographicalInformation` | 26% | no | literal:52 | 静岡県文学連盟会員; 作曲家, 作詞家; 女優; 主任介護支援専門員; (有) 元気デザイン総合研究所代表取締役 |
| `http://RDVocab.info/ElementsGr2/fieldOfActivityOfThePerson` | 4% | no | literal:7 | 応用生物化学; 生物系薬学; 日本語文法 (談話レベル); 形而上学; 生化学 |
| `http://RDVocab.info/ElementsGr2/dateOfDeath` | 2% | no | literal:5 | 2015; 1712; 1683; 1966;  |
| `http://RDVocab.info/ElementsGr2/professionOrOccupation` | 2% | no | literal:3 | 児童文学作家; ロケット科学者, 大学教員; 精神科医 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）
- `http://RDVocab.info/ElementsGr2/dateOfBirth`（被覆率 38%）

### `http://xmlns.com/foaf/0.1/Organization`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://xmlns.com/foaf/0.1/Organization; http://xmlns.com/foaf/0.1/Organization; http://xmlns.com/foaf/0.1/Organization; http://xmlns.com/foaf/0.1/Organization; http://xmlns.com/foaf/0.1/Organization |
| `http://xmlns.com/foaf/0.1/name` | 100% | no | literal:200 | 日本曳家協会; チャイルドケモハウス; 熊本県立第二高等学校; 実地指導対策研究会; 総合女性史学会 |
| `http://RDVocab.info/ElementsGr2/dateOfEstablishment` | 40% | no | literal:81 | 1997; 2006; 2013; 1992; 1991 |
| `http://RDVocab.info/ElementsGr2/corporateHistory` | 35% | yes | literal:79 | 2008年12月社団法人化 ; 2013年現在一般社団法人; NPO法人; 2013年3月名称変更; 1995年7月名称変更; 一般社団法人 |
| `http://RDVocab.info/ElementsGr2/dateOfTermination` | 8% | no | literal:16 | 1995; 1985; 1976; 2024; 1995 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）
- `http://RDVocab.info/ElementsGr2/dateOfEstablishment`（被覆率 40%）
- `http://RDVocab.info/ElementsGr2/corporateHistory`（被覆率 35%）

### `http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Family |
| `http://xmlns.com/foaf/0.1/name` | 100% | no | literal:200 | 染谷; 阿倍; 宇宿; 小寺; 小坂田 |
| `http://RDVocab.info/ElementsGr2/familyHistory` | 4% | no | literal:8 | 古代の豪族, 皇別氏族.; 付家老; 旗本; 旗本; 本多忠勝家の家老 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://xmlns.com/foaf/0.1/name`（被覆率 100%）

### `http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work`（サンプルインスタンス数: 200）

| 述語URI | 被覆率 | 多値 | 値の型 | サンプル値 |
|---|---|---|---|---|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 100% | no | uri:200 | http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work; http://RDVocab.info/uri/schema/FRBRentitiesRDA/Work |
| `http://purl.org/dc/terms/title` | 100% | no | literal:200 | 古画備考; ソクラテスの弁明; 東方見聞録; 大和物語; 竹取物語 |
| `http://purl.org/dc/terms/creator` | 92% | yes | uri:197 | http://id.ndl.go.jp/auth/entity/00269261; http://id.ndl.go.jp/auth/entity/00452937; http://id.ndl.go.jp/auth/entity/00453065; http://id.ndl.go.jp/auth/entity/00269155; http://id.ndl.go.jp/auth/entity/00456207 |
| `http://purl.org/dc/terms/created` | 2% | no | literal:3 | 1966年; 1885年; 1814年 |

**ラベル候補プロパティ**（被覆率・値の型からの機械的な提案。確定ではない）:

- `http://purl.org/dc/terms/title`（被覆率 100%）

**特徴量候補プロパティ**（被覆率 >= 30% の述語。確定ではない）:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`（被覆率 100%）
- `http://purl.org/dc/terms/title`（被覆率 100%）
- `http://purl.org/dc/terms/creator`（被覆率 92%）

---
**注意**: このファイルは自動探索の結果である。CLAUDE.md 決定事項#4に基づき、上記の「主要クラス候補」「ラベル候補プロパティ」「特徴量候補プロパティ」はPhase 3で人間が目視確認・修正してから`configs/*.yaml`に反映すること。鵜呑みにしない。
