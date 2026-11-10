---
id: jmnedict
name: JMnedict（ENAMDICT。日本の固有名詞の辞書）
name_en: JMnedict (ENAMDICT, dictionary of Japanese proper names)
publisher: Electronic Dictionary Research and Development Group（EDRDG）
publisher_en: Electronic Dictionary Research and Development Group (EDRDG)
summary: 地名・人名・会社名など、日本の固有名詞の表記と読みを集めたオープンな辞書データ。
summary_en: An open dataset of Japanese proper names such as places, people and companies, with readings.
url: https://www.edrdg.org/enamdict/enamdict_doc.html
category: vocabulary
domains: [全般]
languages: [ja, en]
formats: [XML]
version: 随時更新
license: CC-BY-SA-4.0
license_url: https://www.edrdg.org/edrdg/licence.html
commercial: yes
redistribution: yes
attribution: This publication has included material from the JMnedict (ENAMDICT) dictionary files in accordance with the licence provisions of the Electronic Dictionaries Research Group. See https://www.edrdg.org/（EDRDG の謝辞の例を言い換えたもの）
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# JMnedict

日本の固有名詞（地名・姓・名・会社名など）の表記と読みを集めた、オープンな辞書データ。JMdict と同じ EDRDG が作っている。

## 何が入っているか

- 固有名詞の表記・読み・種類（地名・姓・名など）と、英語の訳やローマ字。XML（JMnedict.xml.gz）。
- 配布: https://www.edrdg.org/pub/Nihongo/JMnedict.xml.gz

## 開発の参考として

- 字が「名前に偏るか」を見る材料。漢字の級の推定で、常用外の字のうち人名・地名にばかり使う字を除くのに使っている（[docs/jlpt-kanji-levels.md](../../docs/jlpt-kanji-levels.md)）。

## アプリの資源として（将来）

- 地名・人名の読み。行政の文書に出る地名の読みを補うときの手がかりになる。

## 注意

- ライセンスは EDRDG の辞書ファイル共通（CC BY-SA 4.0）。謝辞・更新の義務は [KANJIDIC2](../kanji/kanjidic2.md) と同じ。
- `ftp.edrdg.org` の HTTPS は証明書が名前と合わない（2026-11-03）。`www.edrdg.org/pub/Nihongo/` から取る。
