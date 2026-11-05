# データ

目録（[catalog/](../catalog/README.md)）のうち、再配布できる資料を共通の形（JSONL、1行1項目）に変えたもの。どのファイルも `scripts/` のスクリプトで配布元から作り直せる（手で直したデータは置かない）。

| ファイル | 資料（目録） | 版 | 件数 | ライセンス | 作り直す |
| -------- | ------------ | -- | ---: | ---------- | -------- |
| `jlt-standard-dict.jsonl` | [法令用語日英標準対訳辞書](../catalog/terms/jlt-standard-dict.md) | 19.0 | 3,869語（訳語 5,248） | PDL1.0 | `python3 scripts/ingest_jlt_standard_dict.py` |
| `jma-multilingual-dict.jsonl` | [気象庁 多言語辞書](../catalog/terms/jma-multilingual-dict.md) | 2026-03-26 | 7,279項目（14言語） | PDL1.0 | `python3 scripts/ingest_jma_multilingual_dict.py` |
| `plain-japanese-rewrites.jsonl` | [別冊「やさしい日本語書き換え例」](../catalog/plain-japanese/plain-japanese-rewrites.md) | 2020年8月 | 134語 | PDL1.0 | `python3 scripts/ingest_plain_japanese_rewrites.py`（pdftotext が必要） |
| `gakunen-kanji.jsonl` | [学年別漢字配当表](../catalog/kanji/gakunen-kanji.md) | 平成29年告示 | 1,026字 | 告示（著作権の対象外）・PDL1.0 | `python3 scripts/ingest_gakunen_kanji.py` |
| `joyo-kanji-hyo.jsonl` | [常用漢字表](../catalog/kanji/joyo-kanji-hyo.md) | 平成22年内閣告示第2号 | 本表 2,136字（音訓 4,388）・付表 116語 | 告示（著作権の対象外） | `python3 scripts/ingest_joyo_kanji_hyo.py`（pdftotext が必要） |
| `kanjidic2.jsonl` | [KANJIDIC2](../catalog/kanji/kanjidic2.md) | 2026-11-03 | 3,125字 | **CC BY-SA 4.0** | `python3 scripts/ingest_kanjidic2.py --refresh` |
| `isa-ichigen-soudan.jsonl` | [一元的相談窓口の一覧](../catalog/life-info/isa-ichigen-soudan.md) | 令和７年度末時点 | 348か所（290団体） | PDL1.0 | `python3 scripts/ingest_isa_ichigen_soudan.py` |
| `jps-nenkin-yougo.jsonl` | [年金用語集](../catalog/terms/jps-nenkin-yougo.md) | 用語ごとの更新日 | 116語 | 日本年金機構のサイトの条件（転載フリー） | `python3 scripts/ingest_jps_nenkin_yougo.py` |
| `mhlw-tagengo-yougo.jsonl` | [雇用管理に役立つ多言語用語集](../catalog/terms/mhlw-tagengo-yougo.md) | 2023-04-20 | 418語（14言語） | PDL1.0 | `python3 scripts/ingest_mhlw_tagengo_yougo.py` |
| `jps-foreign-residents.jsonl` | [日本年金機構 外国人向けの情報](../catalog/life-info/jps-foreign-residents.md)（やさしいにほんごのページ） | ページごとの更新日 | 27ページ | 日本年金機構のサイトの条件（転載フリー） | `python3 scripts/ingest_jps_foreign_residents.py` |
| `iryo-joho-net-opendata.jsonl` | [医療情報ネットのオープンデータ](../catalog/life-info/iryo-joho-net-opendata.md)（病院） | 2026-06-01 | 7,715病院 | PDL1.0 | `python3 scripts/ingest_iryo_joho_net_opendata.py` |
| `mext-shugaku-guidebook.jsonl` | [外国人児童生徒のための就学ガイドブック](../catalog/life-info/mext-shugaku-guidebook.md) | 2015年4月 | 160組（8言語×20） | PDL1.0 | `python3 scripts/ingest_mext_shugaku_guidebook.py`（pdftotext が必要） |
| `hellowork-foreign-language.jsonl` | [ハローワークの外国語の案内](../catalog/life-info/hellowork-foreign-language.md)（通訳がいるハローワーク） | 2026年8月 | 139か所（言語の行 360） | PDL1.0 | `python3 scripts/ingest_hellowork_foreign_language.py`（pdftotext が必要） |
| `mhlw-multilingual-medical-docs.jsonl` | [外国人向け多言語説明資料](../catalog/terms/mhlw-multilingual-medical-docs.md) | 言語ごと（2018年3月版ほか） | 53資料×13言語（単位 102,294。うち日本語と訳の組 62,188） | PDL1.0 | `python3 scripts/ingest_mhlw_multilingual_medical_docs.py`（LibreOffice が必要） |
| `seikatsu-cando.jsonl` | [「生活Can do」一覧](../catalog/levels/seikatsu-cando.md) | 2022-11-29 | Can do 785項目・生活・文化・社会的情報 145件 | PDL1.0（JF 番号の項目は国際交流基金の Can-do から採用） | `python3 scripts/ingest_seikatsu_cando.py`（pdftotext が必要） |

- 各行に `source`（目録の id）と `version` が入っている。出典の書き方・取得元の URL・件数・元ファイルのハッシュ・作った日は、同じ名前の `*.meta.json` にある。
- 使うときは `*.meta.json` の `attribution` を出典として書く（加工したことも含めて書いてある）。
- 元のファイルは `.cache/`（git 管理外）に置く。`--refresh` を付けると配布元から取り直す。
- 確かめるとき: `python3 -m unittest discover -s tests`
- **`kanjidic2.jsonl` は CC BY-SA 4.0**（元の KANJIDIC2 のライセンスを継承）。これを使って作ったデータを配るときも CC BY-SA 4.0 にし、EDRDG の謝辞を付ける。リポジトリの MIT は、このファイルには当てはまらない。EDRDG のライセンスは、データを使うアプリやサーバーに定期的な更新（ウェブの辞書なら月1回以上）を求めているので、使う前に `--refresh` で取り直す。

## 形式

### jlt-standard-dict.jsonl

1行が1つの用語。訳語の候補は、元の CSV の順番のまま並べる。

```json
{"source":"jlt-standard-dict","version":"19.0","term":"相手方","reading":"あいてがた",
 "translations":[{"en":"opponent","no":1,"usage":"対審手続の場合",
   "example":{"ja":"…","en":"…","source":"刑事訴訟法第299条"}}, …]}
```

- `translations[].no` は訳語候補番号（候補が1つだけの用語には無い）。`usage` は使い分け基準。`notes` は注釈（元の CSV で付いていた候補に付けたまま）。
- 空の項目は書かない。

### jma-multilingual-dict.jsonl

1行が1項目。xlsx の「多言語辞書（本体）」のシートの1行。

```json
{"source":"jma-multilingual-dict","version":"2026-03-26","no":3,"kind":"用語","category":"特別警報・警報・注意報",
 "ja":"特別警報","tr":{"en":"Emergency Warning","zh-Hans":"特别警报","zh-Hant":"特別警報","ko":"특별 경보", …},
 "history":"2019/7/31追加"}
```

- `kind` は種別（用語・情報文・対応行動）、`category` は情報種別等（特別警報・警報・注意報、津波警報・注意報、市町村名など）。
- `tr` は訳。言語は BCP 47（en、zh-Hans、zh-Hant、ko、pt、es、id、vi、tl、th、ne、km、my、mn）。
- `note`（備考）、`code_table`・`code`（気象庁防災情報XMLのコード表とコード）、`history`（項目ごとの更新履歴）は、あるものだけ。
- `version` は「更新履歴」のシートの、いちばん新しい更新日。セルの文字は Excel のふりがな（フリガナ情報）を除いて読んでいる。
- 項目の多くは地名（市町村名 2,464、アメダス地点名 1,299 など）。用語だけを使うときは `category` で絞る。No.181 は日本語の欄が空（元のデータのまま）。

### plain-japanese-rewrites.jsonl

1行が1つの語。PDF の「番号・語彙・意味」の表から取り出したもの。

```json
{"source":"plain-japanese-rewrites","version":"2020年8月","no":2,"term":"育児休業給付金",
 "reading":"いくじきゅうぎょうきゅうふきん",
 "plain":"育児休業(No.1)をしているあいだに、雇用保険(No.41)からもらうことができるお金。",
 "see":[1,41],"section":"あ"}
```

- `reading` は語の上のふりがな。`plain` はやさしい日本語での意味（「生活・仕事ガイドブック（やさしい日本語版）」の説明。意味の上のふりがなは入れていない）。
- `plain` の中の「(No.41)」は元の表記のまま残し、参照先の番号を `see` に入れる。`section` は五十音の見出し。
- 取り出し方: `pdftotext -bbox-layout` で語ごとの位置と大きさを取り、文字の大きさで本文とふりがなを、位置で列を分ける。番号が 1〜134 で欠けずに続くことを確かめている。

### gakunen-kanji.jsonl

1行が1字。

```json
{"source":"gakunen-kanji","version":"平成29年告示","kanji":"一","grade":1,"code":"8210010110010000"}
```

- `grade` は学年（1〜6）。`code` は学習指導要領コード。

### joyo-kanji-hyo.jsonl

本表の字は1行が1字（`kind` が `本表`）、付表は1行が1語（`kind` が `付表`）。`no` は表の中の順番（本表・付表それぞれ1から）。

```json
{"source":"joyo-kanji-hyo","version":"平成22年内閣告示第2号","kind":"本表","no":1,"kanji":"亜","kyuji":["亞"],
 "readings":[{"reading":"ア","type":"on","examples":["亜流","亜麻","亜熱帯"]}]}
{"source":"joyo-kanji-hyo","version":"平成22年内閣告示第2号","kind":"本表","no":1215,"kanji":"遡","allowed_form":true,
 "readings":[{"reading":"ソ","type":"on","examples":["遡及","遡上"]},{"reading":"さかのぼる","type":"kun","examples":["遡る"]}],
 "notes":["［遡］＝許容字体，＊［（付）第２の１参照］"]}
{"source":"joyo-kanji-hyo","version":"平成22年内閣告示第2号","kind":"付表","no":29,"reading":"かわら","words":["河原","川原"]}
```

- `kyuji` は丸括弧で添えた康熙字典体（「弁」は3つ）。一部は CJK 互換漢字（U+F900〜）で入っているので、Unicode の正規化（NFC・NFKC）をかけない。
- `allowed_form` は、角括弧で添えた許容字体があること（しんにゅう・しょくへんの字形。文字コードは通用字体と同じ）。
- `readings` は表の順。`type` は `on`（音、片仮名）か `kun`（訓、平仮名）。`special` は1字下げの音訓（特別なもの・用法のごく狭いもの）。`examples` は例欄の語（「〔副〕」などの記号や「三羽（ば）」の読みも、そのまま）。例の無い音訓もある。
- `notes` は備考。字ごとにまとめてある（どの音訓の行にあったかは残していない）。
- 付表の `words` は語（2つ書き方があるものは2つ）、`notes` は読みの補足（「（「しはす」とも言う。）」）。
- 「亀」の康熙字典体（龜）は PDF から取り出せないので、スクリプトで補っている（`MISSING_KYUJI`）。

### kanjidic2.jsonl

1行が1字。KANJIDIC2 の 13,108字のうち、学年・旧日本語能力試験の級・新聞の頻度順位のどれかがある字（3,125字）。

```json
{"source":"kanjidic2","version":"2026-11-03","kanji":"亜","grade":8,"strokes":7,"freq":1509,"jlpt_old":1,
 "on":["ア"],"kun":["つ.ぐ"],
 "meanings":{"en":["Asia","rank next","come after","-ous"],"es":[…],"fr":[…],"pt":[…]},
 "readings_other":{"zh-Latn-pinyin":["ya4"],"ko":["아"],"vi":["A","Á"]}}
```

- `grade` は学年（1〜6 は教育漢字、8 はそれ以外の常用漢字、9・10 は人名用漢字）。`strokes` は画数、`freq` は新聞での頻度の順位（2,500位まで）。
- `jlpt_old` は **2010年より前の旧試験の級（1〜4）**。いまの N1〜N5 ではない。
- `on`・`kun` は KANJIDIC2 のすべての読み（常用漢字表の音訓より多い）。訓の「.」の後ろは送り仮名、「-」は接頭・接尾に使う形。常用の音訓は `joyo-kanji-hyo.jsonl` で引く。
- `meanings` は意味（英語・スペイン語・フランス語・ポルトガル語。字によって、ある言語が違う）。`readings_other` は日本語以外の読み（ピンイン、朝鮮語のハングル、ベトナム語の漢越音）。
- 取り込んでいない項目: 名乗り、部首、辞書の番号、SKIP コード（別のライセンス）など。

### isa-ichigen-soudan.jsonl

1行が1つの窓口の場所。出入国在留管理庁の「一元的相談窓口の現況」の Excel の「参考」のシートから取り出したもの。

```json
{"source":"isa-ichigen-soudan","version":"令和７年度末時点","no":1,"prefecture":"北海道","establisher":"北海道",
 "name":"北海道外国人相談センター","address":"札幌市中央区北3条西7丁目 道庁別館12階","phone":"011-200-9595",
 "days":["月","火","水","木","金"],"hours":"9:00～17:00"}
```

- `prefecture` は都道府県、`establisher` は設置者（交付金を受けた地方公共団体）。`name` は窓口の名前。
- `days` は開所日（月〜日と祝）。`hours` は開所時間、`notes` は備考（開所時間の補足など）。どちらも元の文のまま（空白の連続だけ1つにまとめた）。
- `joint` は、複数の団体が共同で運営している窓口（広島市と安芸郡の4町）。
- 同じ窓口に場所が複数あるときは、場所ごとに1行（豊田市の本庁舎と支所など）。元のシートでは縦に結合されているセルを、各行に配っている。
- 電話番号などの値が「－」だけのものは、値が無いとみなして書いていない。
- 半角のカタカナ（ﾋﾞﾙ など）は元のまま。対応する言語の項目は、元の一覧に無い。

### jps-nenkin-yougo.jsonl

1行が1つの用語（日本年金機構の年金用語集の1ページ）。並びは用語集のトップのページの順。

```json
{"source":"jps-nenkin-yougo","version":"2013-02-21","id":"kagyo/gakuseinofu","row":"か行","term":"学生納付特例制度",
 "definition":"大学や専修学校等の学生であって、国民年金の第1号被保険者である本人の前年所得が一定以下の人に対し、…",
 "related":[{"title":"学生納付特例制度","url":"https://www.nenkin.go.jp/service/kokunen/menjo/20150514.html"}, …],
 "page_id":"150010-866-661-344","url":"https://www.nenkin.go.jp/service/yougo/kagyo/gakuseinofu.html"}
```

- `version` はページの更新日（用語ごとに違う。2012-09-06〜2026-10-01）。`id` は URL の行と名前（`kagyo/gakuseinofu`）。`row` は「か行」など。
- `definition` は本文。段落・箇条書きの項目・小見出し・表の行は改行（`\n`）で、表のセルはタブ（`\t`）でつなぐ。計算式の画像（報酬比例部分）は、画像の alt の文字で読んでいる。最初の段落（用語の名前のくり返し）は除いた。
- `see` は、本文が「〜の解説をご覧ください」だけの用語（5語）の、参照先の用語の `id`。例: カラ期間 → `kagyo/gassantaisho`（合算対象期間）。
- `related` は、ページの関連のリンク（文字と URL）。年金用語集のほかの語へのリンクは、文字が「（年金用語集）」で始まる。
- `page_id` は日本年金機構のサイトのページID。
- 取り込むスクリプトは、本文に「転載」の語（転載の制限の注記）があると止まる。

### mhlw-tagengo-yougo.jsonl

1行が1つの用語。厚生労働省の「雇用管理に役立つ多言語用語集」の Excel 版（15シート）を、用語ごとに1行にまとめたもの。並びと項番は「やさしい日本語」のシートのもの。

```json
{"source":"mhlw-tagengo-yougo","version":"2023-04-20","no":255,"web_id":"c06_07","category":"6.安全衛生・災害補償",
 "term":"安全衛生","reading":"あんぜんえいせい",
 "ja_easy":{"term":"安全衛生（あんぜんえいせい）","definition":"安全（あんぜん）に健康（けんこう）に働（はたら）くことができること。","example":"…"},
 "tr":{"en":{"term":"Safety and health education","definition":"To be able to work safely and healthily.","example":"…"},
       "zh-Hans":{"term":"安全卫生", …}, …}}
```

- `no` は項番（1〜418）。`web_id` は、ウェブ版の各言語のページの行の id（`…/tagengoyougosyu/index.html#c06_07`）。`category` はカテゴリー（11）。
- `ja_easy` は、やさしい日本語の用語・定義・例文。読みは元のとおり括弧書き（「働（はたら）く」）。
- `term` は用語から読みの括弧を除いたもの、`reading` は読み（括弧の直前の漢字を、括弧の中の読みに置き換えたもの。片仮名と数字はそのまま。例: シフト表 → シフトひょう）。
- `tr` は14言語の訳（BCP 47: en、zh-Hans、zh-Hant、ko、es、pt、tl、vi、ne、id、th、my、mn、km）。どれも `term`・`definition`・`example` がある。
- ポルトガル語とタガログ語のシートは、項番の振り方と並びがほかと違う。どのシートも、日本語の列（カテゴリー・用語・定義・例文）で突き合わせている。
- セルの文字は、ふりがな（フリガナ情報）を除いて読んでいる。セルの中の改行は空白1つにした。ゼロ幅スペース（U+200B）は元のまま（カンボジア語に多い）。

### jps-foreign-residents.jsonl

1行が1つのページ。日本年金機構の「やさしい日本語（にほんご）」のページ（/international/simplejapanese/ の下）を、トップのページからリンクをたどって集めたもの。並びは URL の順。英語のページと、脱退一時金の請求書（様式）は入れていない。

```json
{"source":"jps-foreign-residents","version":"2026-03-02",
 "url":"https://www.nenkin.go.jp/international/simplejapanese/japanese-system/benefit/withdrawalpayment.html",
 "title":"日本（にほん）を　はなれるときに　もらうことが　できる　お金（かね）／脱退一時金（だったいいちじきん）",
 "page_id":"170010010-998-458-222",
 "blocks":[{"type":"p","text":"外国人（がいこくじん）が　日本（にほん）で　短（みじか）い　間（あいだ）、…"}, …],
 "links":[{"text":"英語（えいご）（PDF）","url":"https://www.nenkin.go.jp/shinsei/jukyu/sonota-kyufu/20150406.files/A.pdf"}, …]}
```

- `version` はページの更新日。更新日の書いていないページ（16ページ）は「更新日の記載なし」。`page_id` は書いてあるページだけ。
- `blocks` は本文の単位。`type` は見出し（`h2`〜`h5`）・段落（`p`）・箇条書きの項目（`li`）・表の行（`tr`。セルはタブでつなぐ）など。最初の見出しのくり返しと、開閉のボタンの文字（「詳細を開く」）は除いた。
- 漢字のあとの読みの括弧（「年金（ねんきん）」）と、語のあいだの全角の空白は元のまま。元のページの誤り（「社会保障協定は（しゃかいほしょうきょうてい）」のような括弧の位置のずれ）も直していない。
- `links` は本文の中のリンク（各言語の PDF など）。
- 本文が無く、ほかのページへのリンクだけのページ（目次、2ページ）は入れていない（`*.meta.json` の `skipped_menu_pages`）。
- 取り込むスクリプトは、本文に「転載」の語（転載の制限の注記）があると止まる。

### iryo-joho-net-opendata.jsonl

1行が1つの病院。厚生労働省の「医療情報ネットのオープンデータ」の、病院の施設票（2026年6月1日時点）と、診療科・診療時間票の診療科の名前。

```json
{"source":"iryo-joho-net-opendata","version":"2026-06-01","id":"0111010000010","name":"札幌医科大学附属病院",
 "name_kana":"サッポロイカダイガクフゾクビョウイン","short_name":"札医大","short_name_kana":"サツイダイ",
 "name_en":"Sapporo Medical University Hospital","pref_code":"01","city_code":"101",
 "address":"北海道札幌市中央区南１条西１６丁目２９１番地","url":"https://web.sapmed.ac.jp/hospital/",
 "lat":43.055405,"lng":141.333497,"weekly":"1111100","weeks":["1111111", …],"holiday":"0",
 "closed_other":"01月01日，01月02日，…","beds":{"general":812,"psychiatric":32,"total":844},
 "departments":["内科","感染症内科", …]}
```

- 休診日は、定義書の値（**0：休診、1：診療**）を曜日の順（月火水木金土日）の7文字にまとめた。空欄は `-`。`weekly` は毎週決まった曜日、`weeks` は第1〜第5週の曜日、`holiday` は祝日。`closed_other` はその他の休診日（元の文のまま）。
- `beds` は病床数（一般・療養・精神・結核・感染症・合計など。空欄でないものだけ）。
- `departments` は診療科目名（診療科・診療時間票に出てくる順。重ねない）。**診療時間は入れていない**（票が大きいため。病院だけで25万行・44MB）。
- 緯度・経度がどちらも 0 の病院（座標が無いもの、268病院）は、`lat`・`lng` を入れていない。英語表記が無い病院もある（164病院）。
- **診療所・歯科診療所・助産所・薬局は入れていない**（件数が多く、ファイルが大きくなるため）。使うときは配布元から取る。
- 外国語で受診できるかの項目は、オープンデータに無い。

### mext-shugaku-guidebook.jsonl

1行が、1つの言語の、日本語のページとその訳のページの組。文部科学省の「外国人児童生徒のための就学ガイドブック」の PDF（8言語）。

```json
{"source":"mext-shugaku-guidebook","version":"2015年4月","lang":"pt","pages":[8,9],
 "ja":"●高等教育について\n高等教育は、主として大学と短期大学で行われています。…",
 "tr":"●Sobre o ensino superior\nO ensino superior é realizado principalmente …",
 "sections":[{"ja":"●高等教育について\n…","tr":"●Sobre o ensino superior\n…"},{"ja":"(２） 教育内容","tr":"(2) Conteúdo educacional"}, …]}
```

- `lang` は訳の言語（en、ko、vi、tl、zh-Hans、pt、es、uk）。`pages` は PDF のページ（日本語、訳）。どの言語も 2〜41ページの20組。
- `ja`・`tr` は、ページの文字を段落ごとに改行でつないだもの（日本語と中国語は行をそのままつなぎ、ほかの言語は空白でつないだ）。ページ番号は除いた。
- `sections` は、見出しの印（●・■・①・(1) など）で区切った組。日本語と訳で見出しの数が同じページ（160組のうち85組）だけにある。数が違うページは、ページ単位で使う。
- 図のページ（学校系統図など）は文字の並びがくずれる。本文は2015年4月の版で、その後の制度の変更は入っていない。

### hellowork-foreign-language.jsonl

1行が1つのハローワーク（出張所・外国人雇用サービスセンターなどを含む）。厚生労働省の「通訳がいるハローワークのご紹介」（PDF、2026年8月）の表。外国語で電話ができるハローワークのチラシと、利用チェックリストは入れていない。

```json
{"source":"hellowork-foreign-language","version":"2026-08","pref_code":"01","pref_en":"Hokkaido","pref":"北海道",
 "office":"ハローワーク札幌","tel":"011-200-9923","office_en":"Sapporo Office","pdf_page":3,
 "languages":[{"lang":"en","name":"英語","name_en":"English",
   "schedule":[{"day":"火","text":"13:00～17:00\n※第 1､2､4 のみ\nOnly 1st,2nd,4th","times":["13:00～17:00"],
                "note":"※第 1､2､4 のみ","note_en":"Only 1st,2nd,4th"},{"day":"木", …}]}, …]}
```

- `languages` は表の言語の行。`lang` は言語（en、zh、pt、es、tl、vi、ko、ne、uk、th、id、my。中国語は表に字体の区別が無いので `zh`）。`name`・`name_en` は表の日本語・英語の名前（元のまま。「ベトナム」「スペイン」のように「語」の無いもの、片方が無いもの（松戸のポルトガル語の英語名）もある）。
- `schedule` は対応する曜日（月〜金。「―」の曜日は入れない）。`text` はマスの文字（元のまま。行は改行でつなぐ）。`times` は時間、`note` は「※」の注記、`note_en` は英語の注記（`text` から分けたもの。数字と記号だけの日付の並びは、直前の注記につなげた）。
- `check` がある事業所（一宮）は、表が込み入っていて、マスの読み分けがくずれているところがある。元の PDF（`pdf_page`）で確かめる。
- 表は PDF の文字の位置で読んでいる。曜日の列をまたぐ長い注記は、まとまりの中心の曜日に入れた。

### mhlw-multilingual-medical-docs.jsonl

1行が、1つの資料の1つの言語。厚生労働省の「外国人向け多言語説明資料」（医療機関の申込書・問診票・同意書など53資料、13言語）の、編集用の Word・Excel のファイルから取り出したもの（PDF は同じ内容なので使っていない）。

```json
{"source":"mhlw-multilingual-medical-docs","version":"2024年4月（言語を追加）","no":1,"title":"診療申込書",
 "category":["受付","外来"],"lang":"id","format":"docx","url":"https://www.mhlw.go.jp/content/10800000/1_001077183.docx",
 "units":[{"tr":"Formulir Pendaftaran Pasien","en":"Patient Registration Form","ja":"診療申込書"},
          {"tr":"Nama","en":"Name","ja":"氏名（カナ）"},
          {"text":"Tanggal Lahir (Tahun/Bulan/Tanggal)/Date of birth (YYYY/MM/DD)/生年月日"}, …]}
```

- `no`・`title`・`category` は、配布ページの表の番号（1〜53）・資料名・分類（受付／外来 など）。`lang` は言語（en、zh-Hans、ko、pt、es、uk、hi、id、ne、tl、th、vi、ar）。
- `version` は言語ごとの版（配布ページの注記による）: 英語・中国語・韓国語・ポルトガル語・スペイン語は「2018年3月版」、ウクライナ語は2022年7月、ヒンディー語・インドネシア語・ネパール語・タガログ語・タイ語・ベトナム語は2024年4月、アラビア語は2025年8月に追加。(53) は2025年2月に追加。
- `units` は文字の単位（Word は段落、Excel はセル）。資料は各言語の文を「/」でつないでいる。
  - 並びは、英語の資料は「英語/日本語」、中国語・韓国語・ポルトガル語・スペイン語は「訳/日本語」、ほかの8言語は「訳/英語/日本語」。
  - 「/」で区切った部分の文字の種類がこの並びに合う区切り方が1つだけのとき、`ja`（日本語）・`en`（英語）・`tr`（訳）に分けた。全体の約6割。
  - 区切り方が決まらない単位（日付の「YYYY/MM/DD」のように文の中に「/」がある、言語が1つだけ、など）は、`text` に元の文字のまま入れた。
- 古い形式（.doc・.xls）は、LibreOffice で .docx・.xlsx に変えてから読んでいる。
- 資料は「日本国内の医療機関を対象に提供」され、「各医療機関の責任においてご使用ください」とある。言語ごとに作った時期が違い、古い資料の制度の説明がいまの制度と合っているかは確かめていない。

### seikatsu-cando.jsonl

文化審議会国語分科会「『日本語教育の参照枠』に基づく『生活Can do』一覧」（PDF、令和4年11月29日）の2つの表。`kind` で分ける（`joyo-kanji-hyo.jsonl` の本表・付表と同じ形）。`no` は、それぞれの表の中の順番。

- `kind` が `生活Can do`: 1行が1つの Can do。「４ 生活 Can do 一覧」の表（`no` は通番 1〜785）。
- `kind` が `生活・文化・社会的情報`: 1行が1つの情報。「５ 生活・文化・社会的情報の整理」の表（145件）。小分類ごとに、日本語学習と合わせて知っておくと役に立つ情報の例。`minor_no` で Can do とつながる。

```json
{"source":"seikatsu-cando","version":"2022-11-29","kind":"生活Can do","no":6,"activity":"やり取り","category":"製品やサービスを得るための取引","level":"A2",
 "cando":"電話で病院や歯医者の予約をするとき、ゆっくりとはっきりと話されれば、名前や電話番号、日時、診察理由など病院のスタッフの質問に答えることができる。",
 "major_no":"Ⅰ","major":"健康・安全に暮らす","middle_no":"01","middle":"健康を保つ",
 "minor_no":"01","minor":"医療機関で治療を受ける","essential":true,
 "case1_no":"0101","case1":"適切な医療機関の選択をする","case2_no":"0101090","case2":"予約を申し込む","pdf_page":11}
{"source":"seikatsu-cando","version":"2022-11-29","kind":"生活・文化・社会的情報","no":3,
 "major_no":"Ⅰ","major":"健康・安全に暮らす","minor_no":"01","minor":"医療機関で治療を受ける","essential":true,
 "text":"初診の場合の受診の仕方について","must_know":false,"pdf_page":91}
```

Can do の行:

- `activity` は言語活動（聞くこと・読むこと・やり取り・発表・書くこと）、`category` はそのカテゴリー、`level` はレベル（A1・A2・B1・B2）。
- 生活上の行為の事例: `major`（大分類、`major_no` は Ⅰ〜Ⅹ）・`middle`（中分類）・`minor`（小分類）・`case1`（事例１、上位項目）・`case2`（事例２、下位項目）。番号は元の表の文字のまま（先頭の 0 を残す）。
- `essential` は小分類の●（来日間もない外国人の生活の基盤に欠かせない、または安全にかかわり緊急性がある小分類）。
- `case1_status`・`case2_status` は、事例の名前の後の「（修正）」「（新規）」（既存の事例を直したもの・新しく足したもの）。名前からは外してある。
- `jf` は JF 番号（`JF362`、`JF生115` など）。国際交流基金の JF Can-do・JF 生活日本語 Can-do から採用した Can do（文言を一部変えたものを含む）。
- `representative` は、令和4年度の量的検証で、そのレベルの代表項目と認められた項目。`pdf_page` は PDF のページ（1始まり。印刷されたページ番号とは違う）。
- 表は PDF の文字の位置で読んでいる。マスの中の改行は、空白を入れずにつないだ。
- 元の PDF の食い違いは直していない: 小分類「（12）徒歩で移動する」の中分類は、分類一覧では「08 自力で移動する」、表では「07 公共交通機関を利用する」（データは表のまま）。事例２の番号の先頭4桁が事例１の番号と違う行がある（通番 23・24・279・769・770）。事例１「0403」の名前は「防犯に対処する」と「犯罪に対処する」の2つ。新しく足した事例２は、関係する元の事例２の番号を使っているので、`case2_no` だけでは項目が決まらない。

生活・文化・社会的情報の行:

- `text` は情報（頭の「☆」「・」は外した）。`must_know` は「☆」（来日間もないかどうかを問わず、情報として知っておく必要があるもの）。
- 大分類・小分類の名前と●は、この表に書いてあるまま。（47）だけ、分類一覧の令和3年度の改定前の名前（「電話・ファクシミリを利用する」。改定後は「電話等を利用する」）のまま。
- 「特に無し」の小分類（11・28・29・40）は、行が無い。
- 小分類の名前は、情報の並びの上下の中央にあるとは限らない（上にそろえた行もある）。表の行の境目（行の間の広いところ）で情報をまとめ、小分類の名前の位置で組んでいる。長い情報の折り返しは、前の行につないだ。
