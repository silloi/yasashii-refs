---
id: joyo-kanji-hyo
name: 常用漢字表（平成22年内閣告示第2号）
publisher: 文化庁（内閣告示）
url: https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/
category: kanji
domains: [全般]
languages: [ja]
formats: [PDF]
version: 平成22年（2010年）11月30日 内閣告示第2号
license: 告示（著作権の対象外）
license_url: https://www.mext.go.jp/b_menu/1351168.htm
commercial: yes
redistribution: yes
attribution: 出典：「常用漢字表」（平成22年内閣告示第2号）
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# 常用漢字表

法令・公用文書・新聞・放送など、一般の社会生活で使う漢字の目安。2,136字と、その音訓。

## 何が入っているか

- 本表（字種・音訓・語例）、付表（「明日」「大人」などの熟字訓）、字体についての解説。文化庁のページで PDF を配布。
- 同じ日の内閣訓令第1号「公用文における漢字使用等について」で、公用文の漢字はこの表の本表と付表によると定めている。

## 開発の参考として

- 行政の文書がどの漢字を使うかの前提。常用漢字に無い字（表外字）は、行政の文書でも振り仮名や言い換えの対象になりやすい。
- 補足の文の漢字が常用漢字の範囲かを機械で確かめるときの基準。

## アプリの資源として（将来）

- 字種と音訓を JSONL にして、漢字のレベルを判定する（学年別漢字配当表・KANJIDIC2 と組み合わせる）。

## 注意

- 告示は著作権の対象ではない（著作権法第13条第2号）。配布している文化庁のサイトは「文部科学省ウェブサイト利用規約」（PDL1.0 に準拠）に従う。
- 機械で読める公式の版（CSV など）があるかは未確認。PDF から取り出すときは、KANJIDIC2 の常用漢字の印と突き合わせて確かめる。
