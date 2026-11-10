---
id: plain-japanese-rewrites
name: 在留支援のためのやさしい日本語ガイドライン 別冊「やさしい日本語書き換え例」
name_en: Easy Japanese rewriting examples (supplement to the Easy Japanese Guidelines)
publisher: 出入国在留管理庁・文化庁
publisher_en: Immigration Services Agency of Japan and Agency for Cultural Affairs
summary: 行政の用語や表現を、やさしい日本語に書き換えた例の一覧。
summary_en: Examples of administrative terms and phrases rewritten in Easy Japanese.
url: https://www.moj.go.jp/isa/support/portal/plainjapanese_guideline.html
category: plain-japanese
domains: [全般, 入国・在留手続, 市区町村での手続, 年金・福祉]
languages: [ja, ja-easy]
formats: [PDF]
version: 2020年8月（2021年4月20日に URL・QR コードを修正）
license: PDL-1.0
license_url: https://www.moj.go.jp/isa/copyright/index2.html
commercial: yes
redistribution: yes
attribution: 出典：出入国在留管理庁・文化庁「在留支援のためのやさしい日本語ガイドライン 別冊 やさしい日本語書き換え例」（出入国在留管理庁ホームページ）を加工して作成
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# 別冊「やさしい日本語書き換え例」

行政の用語や表現を、やさしい日本語に書き換えた例の一覧。

## 何が入っているか

- 「生活・仕事ガイドブック」（やさしい日本語版。いまの「生活・就労ガイドブック」）に出てくる用語 134語の、やさしい日本語での意味。「番号・語彙・意味」の表で、語にはふりがなが付いている。年金・保険・届出・学校など、手続きの用語が中心。
- 意味の中で、ほかの語を「(No.41)」のように参照している（55語）。
- 配布ページの PDF: `https://www.moj.go.jp/isa/content/930006077.pdf`（761KB）。

## 開発の参考として

- 行政の用語を「ことば」のレベルで言い換えるときの、公的な例。補足の言い換えが、この例と大きく食い違っていないかを見る。

## アプリの資源として（将来）

- **取り込み済み:** [`data/plain-japanese-rewrites.jsonl`](../../data/README.md)（134語。番号・語・読み・やさしい日本語での意味・参照）。作り直すときは `python3 scripts/ingest_plain_japanese_rewrites.py`（pdftotext が必要）。
- 「生活・就労ガイドブック」（多言語版）と同じ用語を使っているので、ガイドブックの各言語版と突き合わせれば、用語の多言語の対訳にもつなげられる可能性がある（未検証）。

## 注意

- 辞書に近い形だが、網羅的ではない（作り手の評価）。
- 書き換えは文脈によって変わるので、一つの正解として扱わない。
- 利用規約は [plain-japanese-guideline](plain-japanese-guideline.md) と同じ（PDL1.0）。取り出したデータには、加工したことを出典と別に書く。
