---
id: jps-nenkin-yougo
name: 年金用語集（日本年金機構）
name_en: Pension glossary (Japan Pension Service)
publisher: 日本年金機構
publisher_en: Japan Pension Service
summary: 年金の制度で使う言葉を、1語ずつ説明している用語集。
summary_en: A glossary explaining the terms used in Japan's pension system, one term at a time.
url: https://www.nenkin.go.jp/service/yougo/index.html
category: terms
domains: [年金・福祉]
languages: [ja]
formats: [HTML]
version: 用語ごとに更新日がある（2012年9月6日〜2026年10月1日。2026-11-03 に確認）
license: 独自（原則リンクフリー・転載フリー）
license_en: Custom terms (linking and reproduction are generally free)
license_url: https://www.nenkin.go.jp/info/aboutweb/aboutsite.html
commercial: 未確認
redistribution: yes
attribution: 出典：日本年金機構ホームページ「年金用語集」（https://www.nenkin.go.jp/service/yougo/index.html）
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# 年金用語集

年金の制度で使う言葉を、日本年金機構が1語1ページで説明している用語集。

## 何が入っているか

- 116語（2026-11-03 に数えた）。か行32、さ行24、た行19、は行17、な行11、あ行5、ま行4、や行2、ら行2。わ行の索引のページはあるが、語は無い。
  - 例: 遺族基礎年金、学生納付特例制度、基礎年金番号、繰上げ受給、合算対象期間（カラ期間）、ねんきん定期便、マクロ経済スライド。
- 各語の定義と、関連するページへのリンク。
  - 5語（カラ期間、随時改定、定時決定、追納、障害年金等受給権者の特別一時金）は、ほかの語を見るように案内するだけ。
  - 表（加給年金額、定額部分）と、計算式の画像（報酬比例部分）を含む語がある。

## 開発の参考として

- 年金の言葉の、公的な定義。補足の「ことば」で言い換えるときの、元の正確な意味として使う。
- 外国人向けのやさしい説明は、[日本年金機構 外国人向けの情報](../life-info/jps-foreign-residents.md)にある。

## アプリの資源として（将来）

- **取り込み済み:** [`data/jps-nenkin-yougo.jsonl`](../../data/README.md)（116語）。作り直すときは `python3 scripts/ingest_jps_nenkin_yougo.py`（1ページずつ、1秒の間を置いて取得する）。
- 年金の言葉に、元の定義と日本年金機構のページへのリンクを添える材料。

## 注意

- **利用条件:** 「日本年金機構ホームページ（以下、当サイト）は、原則リンクフリー、転載フリーです。リンクや転載を行う際、ご連絡は不要です」（このサイトについて、2026年3月2日更新）。留意点は次の3つだけ。
  - 「リンクの制限、転載の制限等の注記があるページは、この限りではありません」。用語集のページに、その注記は無い（2026-11-03、取り込むスクリプトでも確かめている）。
  - 掲載情報を使って行うことに、日本年金機構は責任を負わない。
  - 内容・URL は予告なしに変わることがある。
- 出典の書き方の定めは無い。データには出典を付けている（`data/jps-nenkin-yougo.meta.json`）。
- 商用の利用と加工については書かれていない（制限する記述も無い）。そのため `commercial` は「未確認」のまま。
- 定義はふつうの日本語で、やさしい日本語ではない。
- 更新日が古い語がある（2012年・2013年が39語）。制度の改正に合っているかは、使うときに確かめる。
