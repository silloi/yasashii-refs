# データ

目録（[catalog/](../catalog/README.md)）のうち、再配布できる資料を共通の形（JSONL、1行1項目）に変えたもの。どのファイルも `scripts/` のスクリプトで配布元から作り直せる（手で直したデータは置かない）。

| ファイル | 資料（目録） | 版 | 件数 | ライセンス | 作り直す |
| -------- | ------------ | -- | ---: | ---------- | -------- |
| `jlt-standard-dict.jsonl` | [法令用語日英標準対訳辞書](../catalog/terms/jlt-standard-dict.md) | 19.0 | 3,869語（訳語 5,248） | PDL1.0 | `python3 scripts/ingest_jlt_standard_dict.py` |
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

### gakunen-kanji.jsonl

1行が1字。

```json
{"source":"gakunen-kanji","version":"平成29年告示","kanji":"一","grade":1,"code":"8210010110010000"}
```

- `grade` は学年（1〜6）。`code` は学習指導要領コード。
