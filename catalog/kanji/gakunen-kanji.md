---
id: gakunen-kanji
name: 学年別漢字配当表（小学校学習指導要領 平成29年告示 別表）
name_en: Table of Kanji by School Grade (appendix to the 2017 elementary school curriculum guidelines)
publisher: 文部科学省
publisher_en: Ministry of Education, Culture, Sports, Science and Technology (MEXT)
summary: 小学校の各学年で学ぶ漢字（1,026字）の一覧。
summary_en: The 1,026 kanji taught in each grade of elementary school.
url: https://www.mext.go.jp/content/20230901-mxt_syoto01-000013115_02.csv
category: kanji
domains: [全般]
languages: [ja]
formats: [CSV, PDF]
version: 小学校学習指導要領（平成29年告示）。学習指導要領コード表 Ver 1.0
license: 告示（著作権の対象外）。コード表は文部科学省ウェブサイト利用規約（PDL-1.0 に準拠）
license_en: Public notice (not subject to copyright). The code table follows the MEXT website terms of use (based on PDL 1.0).
license_url: https://www.mext.go.jp/b_menu/1351168.htm
commercial: yes
redistribution: yes
attribution: 出典：文部科学省「小学校学習指導要領（平成29年告示）コード表」を加工して作成
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# 学年別漢字配当表

小学校の各学年で学ぶ漢字（教育漢字）の一覧。小学校学習指導要領の国語の別表。

## 何が入っているか

- 第1学年 80字から第6学年まで（平成29年の改訂で、都道府県名に使う20字を第4学年に加えた）。
- 文部科学省の「学習指導要領コード表」（CSV、UTF-8）に、学習指導要領の本文と一緒に入っている。「別表 学年別漢字配当表」の行の下に「第一学年（80字）」、続けて1字ずつ1行（一、右、雨、円…）と、コードが並ぶ。
- 関連: 「音訓の小・中・高等学校段階別割り振り表」（平成29年3月、PDF）。常用漢字の音訓を、どの学校段階で学ぶかの表。

## 開発の参考として

- 「小学校の何年生で習う漢字か」は、日本語を学ぶ人にも、日本で育った子どもにも分かりやすい漢字の難しさの目安になる。

## アプリの資源として（将来）

- **取り込み済み:** [`data/gakunen-kanji.jsonl`](../../data/README.md)（1,026字。各学年の字数がコード表の見出しの字数と合うことを確かめている）。作り直すときは `python3 scripts/ingest_gakunen_kanji.py`。
- 漢字のレベル判定に使う。

## 注意

- `url` は CSV の直リンク。CSV を配布しているページ（学習指導要領コードの説明のページ）は未確認。
- 学習指導要領は告示で、著作権の対象ではない（著作権法第13条第2号）。コード表は文部科学省のサイトのコンテンツとして、出典を書けば加工・再配布できる。
- 学年は日本の子ども向けの順番で、日本語学習者が学ぶ順番とは違う。
