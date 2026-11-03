---
id: kanjidic2
name: KANJIDIC2
publisher: Electronic Dictionary Research and Development Group（EDRDG）
url: https://www.edrdg.org/wiki/index.php/KANJIDIC_Project
category: kanji
domains: [全般]
languages: [ja, en, fr, es, pt]
formats: [XML]
version: 随時更新
license: CC-BY-SA-4.0
license_url: https://www.edrdg.org/edrdg/licence.html
commercial: yes
redistribution: yes
attribution: EDRDG のライセンスに従った謝辞を付ける（例文は KANJIDIC Project のページにある。文面は未確認）
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# KANJIDIC2

漢字1字ごとの情報（読み・意味・画数・学年・頻度など）をまとめた、日本語学習者向けのオープンなデータ。

## 何が入っているか

- 学年（`grade`）: 1〜6 は小学校で学ぶ漢字（教育漢字）、8 はそれ以外の常用漢字、9・10 は人名用漢字。
- 日本語能力試験（`jlpt`）: **2010年より前の旧試験の級（1〜4）**。いまの N1〜N5 とは対応しない。
- 意味は英語のほか、フランス語・スペイン語・ポルトガル語など（言語は字によって違う）。

## 開発の参考として

- 学年・常用漢字かどうか・旧試験の級を、1つのデータで引ける。公式の表（常用漢字表・学年別漢字配当表）と突き合わせて使う。

## アプリの資源として（将来）

- 漢字のレベル判定の基礎データ。

## 注意

- ライセンスは CC BY-SA 4.0（EDRDG の辞書ファイル共通）。取り込んだデータのファイルも CC BY-SA 4.0 で配り、謝辞を付ける。アプリやウェブで語を表示するときの謝辞の付け方にも決まりがある（ライセンスのページ。謝辞の例文はプロジェクトのページにあると書かれている）。
- いまの N1〜N5 の漢字のリストは公式には無い（[jlpt](../levels/jlpt.md)）。`jlpt` を N の級に読み替えない。
