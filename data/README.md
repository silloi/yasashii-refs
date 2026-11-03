# データ

目録（[catalog/](../catalog/README.md)）のうち、再配布できる資料を共通の形（JSONL、1行1項目）に変えたもの。どのファイルも `scripts/` のスクリプトで配布元から作り直せる（手で直したデータは置かない）。

| ファイル | 資料（目録） | 版 | 件数 | ライセンス | 作り直す |
| -------- | ------------ | -- | ---: | ---------- | -------- |
| `jlt-standard-dict.jsonl` | [法令用語日英標準対訳辞書](../catalog/terms/jlt-standard-dict.md) | 19.0 | 3,869語（訳語 5,248） | PDL1.0 | `python3 scripts/ingest_jlt_standard_dict.py` |
| `jma-multilingual-dict.jsonl` | [気象庁 多言語辞書](../catalog/terms/jma-multilingual-dict.md) | 2026-03-26 | 7,279項目（14言語） | PDL1.0 | `python3 scripts/ingest_jma_multilingual_dict.py` |
| `plain-japanese-rewrites.jsonl` | [別冊「やさしい日本語書き換え例」](../catalog/plain-japanese/plain-japanese-rewrites.md) | 2020年8月 | 134語 | PDL1.0 | `python3 scripts/ingest_plain_japanese_rewrites.py`（pdftotext が必要） |
| `gakunen-kanji.jsonl` | [学年別漢字配当表](../catalog/kanji/gakunen-kanji.md) | 平成29年告示 | 1,026字 | 告示（著作権の対象外）・PDL1.0 | `python3 scripts/ingest_gakunen_kanji.py` |

- 各行に `source`（目録の id）と `version` が入っている。出典の書き方・取得元の URL・件数・元ファイルのハッシュ・作った日は、同じ名前の `*.meta.json` にある。
- 使うときは `*.meta.json` の `attribution` を出典として書く（加工したことも含めて書いてある）。
- 元のファイルは `.cache/`（git 管理外）に置く。`--refresh` を付けると配布元から取り直す。
- 確かめるとき: `python3 -m unittest discover -s tests`

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
