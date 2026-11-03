---
id: jlt-standard-dict
name: 法令用語日英標準対訳辞書
publisher: 法務省（日本法令外国語訳データベースシステム）
url: https://www.japaneselawtranslation.go.jp/ja/dicts/download
category: terms
domains: [全般, 入国・在留手続, 市区町村での手続]
languages: [ja, en]
formats: [PDF, XML, CSV]
version: "19.0"
license: PDL-1.0
license_url: https://www.japaneselawtranslation.go.jp/ja/index/terms
commercial: yes
redistribution: yes
attribution: 出典：日本法令外国語訳データベースシステム（法務省）「法令用語日英標準対訳辞書」第19.0版
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# 法令用語日英標準対訳辞書

法令の翻訳で使う用語の、日本語と英語の標準の対訳。法務省の「日本法令外国語訳データベースシステム」で配布している。

## 何が入っているか

- 用語（見出し語）、読み、訳語番号、訳語、訳語の使い分け基準、用例（和文・英文）、用例の出典、注釈（派生語など）。
- 最新は 19.0。1.0 から 19.0 まで、過去の版もダウンロードできる（変更履歴のページあり）。
- 形式は PDF・XML・CSV（Shift-JIS と UTF-8）。
- サイトでは、辞書の検索と、法令の訳文の中での使われ方を探す「文脈検索」も使える。

## 開発の参考として

- 行政・法令の用語を英語にするときの、公的な基準の訳語。補足や併記の英訳が、この辞書と食い違っていないかの確認に使える。
- 「訳語の使い分け基準」は、同じ用語を場面によって訳し分ける根拠になる。
- 法令そのものの英訳（同じサイト）は、在留手続などの制度を英語で説明するときの参考になる。

## アプリの資源として（将来）

- **取り込み済み:** [`data/jlt-standard-dict.jsonl`](../../data/README.md)（19.0、3,869語・訳語 5,248）。作り直すときは `python3 scripts/ingest_jlt_standard_dict.py`。配布ページのフォーム（確認用のトークン付き）と同じ手順で CSV（UTF-8）を取る。
- ページに出てくる用語を引いて、標準の英訳を補足づくりの参考として渡す、などに使える。

## 注意

- 利用規約: サイトの内容には、権利表記が無い限り「公共データ利用規約（第1.0版）」（PDL1.0）が適用される。ロゴとキャラクターは対象外。
- 法令の翻訳は正文ではなく、法的な効力を持つのは日本語の法令だけ、と注記されている。
- 対象は法令用語で、生活の場面の言葉（窓口の言い回しなど）は少ない。
