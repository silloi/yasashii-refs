---
id: jps-foreign-residents
name: 日本年金機構 外国人向けの情報（やさしいにほんご・英語・脱退一時金の請求書）
publisher: 日本年金機構
url: https://www.nenkin.go.jp/international/index.html
category: life-info
domains: [年金・福祉]
languages: [ja-easy, en, zh-Hans, ko, pt, es, id, tl, th, vi, my, km, ru, ne, mn]
formats: [HTML, PDF, XLSX]
version: 2026-11-03 に確認
license: 独自（原則リンクフリー・転載フリー）
license_url: https://www.nenkin.go.jp/info/aboutweb/aboutsite.html
commercial: 未確認
redistribution: yes
attribution: 出典：日本年金機構ホームページ（https://www.nenkin.go.jp/international/index.html）
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# 日本年金機構 外国人向けの情報

日本年金機構のサイトの、外国人向けの「やさしいにほんご」と英語のページ、短期在留外国人の脱退一時金の請求書（14言語）。

## 何が入っているか

- **やさしいにほんご**（https://www.nenkin.go.jp/international/simplejapanese/index.html ）: 漢字のあとに読みを括弧で書いた日本語（「年金（ねんきん）」）。
  - 日本の社会保険、社会保障協定、相談できる場所
  - 「したいこと」から: 年金に入る、保険料を払う、年金をもらう、年金をもらっている人の手続き
  - 「場面」から: 日本に来た、日本をはなれる、仕事をはじめる／やめる
  - 動画とパンフレット
- **英語**: Japanese Social Insurance Systems、International Social Security Agreement、Where to consult。
- **短期在留外国人の脱退一時金の請求書**（https://www.nenkin.go.jp/shinsei/jukyu/sonota-kyufu/20150406.html ）:
  - 14言語: 英語、中国語（簡体字）、韓国語、ポルトガル語、スペイン語、インドネシア語、フィリピノ（タガログ）語、タイ語、ベトナム語、ミャンマー語、カンボジア（クメール）語、ロシア語、ネパール語、モンゴル語
  - それぞれ PDF・Excel と記入例。
  - 「生活・就労ガイドブック」の第7章が、脱退一時金の確認先として案内している。

## 開発の参考として

- 年金の説明を、国の機関がやさしい日本語で書いた見本。読みを括弧で添える書き方（ルビを使わない）の例でもある。
- 脱退一時金（日本を離れたあとに、払った保険料の一部を受け取る手続）は短期在留外国人に特有の手続で、補足に書く価値が高い。
- 年金の言葉の定義は、同じ日本年金機構の[年金用語集](../terms/jps-nenkin-yougo.md)にある（取り込み済み）。

## アプリの資源として（将来）

- やさしいにほんごのページを取り込んだ（`data/jps-foreign-residents.jsonl`、27ページ。見出し・段落・項目の単位と、各言語の PDF へのリンク）。年金の手続を場面ごとに説明した文の見本になる。英語のページと請求書（様式）は入れていない。
- 脱退一時金の請求書（14言語）は、記入の案内に添える材料になる。

## 注意

- **利用条件:** 「日本年金機構ホームページ（以下、当サイト）は、原則リンクフリー、転載フリーです。リンクや転載を行う際、ご連絡は不要です」（このサイトについて、2026年3月2日更新）。ただし「リンクの制限、転載の制限等の注記があるページは、この限りではありません」。取り込むときは、ページごとにこの注記が無いことを確かめる（取り込みのスクリプトは、本文に「転載」の語があると止まる。2026-11-05 の27ページには無かった）。
- 出典の書き方の定めは無い。商用の利用と加工については書かれていない（制限する記述も無い）ので、`commercial` は「未確認」のまま。
