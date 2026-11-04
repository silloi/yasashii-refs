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
