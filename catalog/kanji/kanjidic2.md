---
id: kanjidic2
name: KANJIDIC2
publisher: Electronic Dictionary Research and Development Group（EDRDG）
url: https://www.edrdg.org/wiki/index.php/KANJIDIC_Project
category: kanji
domains: [全般]
languages: [ja, en, es, fr, pt, zh, ko, vi]
formats: [XML]
version: 毎日更新（取り込んだのは 2026-11-03 版。database_version 2026-307）
license: CC-BY-SA-4.0
license_url: https://www.edrdg.org/edrdg/licence.html
commercial: yes
redistribution: yes
attribution: This package uses the KANJIDIC dictionary files. These files are the property of the Electronic Dictionary Research and Development Group, and are used in conformance with the Group's licence.（EDRDG の謝辞の例 https://www.edrdg.org/edrdg/sample.html 。適当に言い換えてよい）
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# KANJIDIC2

漢字1字ごとの情報（読み・意味・画数・学年・頻度など）をまとめた、日本語学習者向けのオープンなデータ。

## 何が入っているか

- 13,108字（JIS X 0208・0212・0213 の漢字）。毎日更新される。
- 学年（`grade`）: 1〜6 は小学校で学ぶ漢字（教育漢字）、8 はそれ以外の常用漢字、9・10 は人名用漢字（10 は常用漢字の異体字）。
- 日本語能力試験（`jlpt`）: **2010年より前の旧試験の級（1〜4）**。いまの N1〜N5 とは対応しない。ファイルの説明（DTD）には「新しい級の公式の漢字リストは無い。旧2級が N2 と N3 に分かれたほかは、旧級に近いとされる」とある。
- 新聞での頻度の順位（`freq`、2,500位まで）。新聞の記事に偏る。
- 読み: 音読み・訓読み（訓は「.」の後ろが送り仮名、「-」は接頭・接尾に使う形）・名乗り。ほかに中国語のピンイン、朝鮮語の読み（ハングル・ローマ字）、ベトナム語の漢越音。
- 意味: 英語のほか、スペイン語・フランス語・ポルトガル語（字によって、ある言語が違う）。

## 開発の参考として

- 学年・常用漢字かどうか・旧試験の級を、1つのデータで引ける。学年は[学年別漢字配当表](gakunen-kanji.md)と、常用漢字（学年 1〜8）は[常用漢字表](joyo-kanji-hyo.md)と、1字も違わないことを確かめた（`tests/test_data.py`）。
- ベトナム語の漢越音や朝鮮語の読みは、漢字圏の学習者の手がかりになる（ベトナムは在留外国人・外国人労働者の上位。[docs/priorities.md](../../docs/priorities.md)）。
- 旧試験の級の字数（このデータ）: 4級 103字、3級 181字、2級 739字、1級 1,207字（累計 103・284・1,023・2,230字）。
  - 1級には人名用漢字が251字（阿・葵・茜など）入っている。すべて常用外。旧試験の『出題基準』の1級と同じかは未確認。
  - 常用漢字のうち157字（挨・宛・闇など）には級が無い。どれも2010年の改定で加わった字（[docs/jlpt-kanji-levels.md](../../docs/jlpt-kanji-levels.md)）。
  - N5〜N1 相当の級の推定は、ここから旧級を取っている（[docs/jlpt-kanji-levels.md](../../docs/jlpt-kanji-levels.md)）。

## アプリの資源として（将来）

- **取り込み済み:** [`data/kanjidic2.jsonl`](../../data/README.md)（3,125字。学年・旧試験の級・頻度の順位のどれかがある字）。作り直すときは `python3 scripts/ingest_kanjidic2.py --refresh`。
- 漢字のレベル判定の基礎データ。

## 注意

- **ライセンス:** CC BY-SA 4.0（EDRDG の辞書ファイル共通）。取り込んだデータも CC BY-SA 4.0 で配る。データの著作権を自分のものと主張してはいけない。商用でも使える（収益が出るなら寄付が勧められている）。
- **謝辞の付け方（ライセンスのページ）:**
  - 大きく抜き出して公開するとき（語彙のリストなど）は、このファイルを使ったことを明記する。
  - ソフトウェア・ウェブ・アプリで使うときは、説明書やサイトに出典を書き、ライセンスへのリンクを置く。
  - ウェブで辞書として語を表示するときは、画面ごとに謝辞を出す。ほかの資料と混ぜて表示するなら、まとめた謝辞でよい。
  - スマートフォンのアプリでは、メニューから開く画面（「出典」など）に出す。起動画面だけでは足りない。
- **更新の義務:** データを使うソフトウェア・サーバー・アプリは、新しい版に定期的に更新する手順を持つこと。ウェブの辞書は少なくとも月1回。更新しないとライセンス違反になる。
- SKIP コード（Jack Halpern 氏）は別のライセンスなので、取り込んでいない。ピンイン（Christian Wittern 氏・Koichi Yasuoka 氏）と朝鮮語の読み（Charles Muller 氏）は提供者が著作権を持ち、同じ条件で配られている。
- いまの N1〜N5 の漢字のリストは公式には無い（[jlpt](../levels/jlpt.md)）。取り込んだデータでは、旧試験の級を `jlpt_old` という名前にしている。N の級に読み替えない。
