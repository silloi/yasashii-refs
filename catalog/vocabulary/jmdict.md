---
id: jmdict
name: JMdict（Japanese-Multilingual Dictionary）
name_en: JMdict (Japanese-Multilingual Dictionary)
publisher: Electronic Dictionary Research and Development Group（EDRDG）
publisher_en: Electronic Dictionary Research and Development Group (EDRDG)
summary: 日本語の語の読みと、外国語の訳をまとめたオープンな辞書データ。
summary_en: An open dictionary dataset of Japanese words with readings and translations.
url: https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project
category: vocabulary
domains: [全般]
languages: [ja, en]
formats: [XML]
version: 随時更新
license: CC-BY-SA-4.0
license_url: https://www.edrdg.org/edrdg/licence.html
commercial: yes
redistribution: yes
attribution: This publication has included material from the JMdict (EDICT, etc.) dictionary files in accordance with the licence provisions of the Electronic Dictionaries Research Group. See https://www.edrdg.org/（EDRDG の謝辞の例 https://www.edrdg.org/edrdg/sample.html ）
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# JMdict

日本語の語の読みと、外国語の訳をまとめたオープンな辞書データ。

## 何が入っているか

- 見出し語（漢字・かなの表記）、読み、品詞、英語の訳。英語以外の言語の訳もある（どの言語がどれだけあるかは未確認）。

## 開発の参考として

- 語の読みを引く基礎データ。読みの自動付与（ふりがな）は、このデータを元にした実装が多い（例: [Furifont](../tools/furifont.md) の辞書）。

## アプリの資源として（将来）

- 補足に出てくる語の読み、英語の訳の候補。

## 注意

- ライセンスは CC BY-SA 4.0（[KANJIDIC2](../kanji/kanjidic2.md) と同じ）。
- 一般の語の辞書で、行政の用語や言い回しの「本当の意味」までは載っていない。行政の用語は [法令用語日英標準対訳辞書](../terms/jlt-standard-dict.md) を優先する。
- 語彙の難しさ（レベル）の情報は無い。
