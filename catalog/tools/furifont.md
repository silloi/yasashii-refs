---
id: furifont
name: Furifont
name_en: Furifont
publisher: Anthony Fu（オープンソース）
publisher_en: Anthony Fu (open source)
summary: 文章に手を加えずに、漢字の上にふりがなを表示できるフォント。
summary_en: A font that shows furigana above kanji without changing the text.
url: https://furifont.antfu.me/
category: tools
domains: [全般]
languages: [ja]
formats: [フォント, npm パッケージ, ブックマークレット]
version: 未確認
license: MIT（コード）、OFL-1.1（フォント）、CC-BY-SA-4.0（辞書）
license_en: MIT (code), OFL 1.1 (font), CC BY-SA 4.0 (dictionary)
license_url: https://raw.githubusercontent.com/antfu/furifont/main/README.md
commercial: yes
redistribution: yes
attribution: フォントは SIL OFL 1.1、辞書は CC BY-SA 4.0 の表示に従う
handling: link
uses: [reference, resource]
checked: 2026-11-03
---

# Furifont

漢字の上にふりがなを表示するフォント。文章に手を加えず（ルビの指定なしで）、フォントを替えるだけでふりがなが出る。

## 仕組み

- Source Han Sans JP / Source Han Serif JP から作る。作るときに数千語の辞書を読み、ふりがな付きの字形を新しく描いて、語ごとに合字（リガチャ）で表示する。
- 文字そのものは変わらないので、コピーすれば元の漢字のまま。
- どのページにも Furifont を当てるブックマークレットとユーザースクリプトがある（送り仮名の読みの有無も選べる）。
- 自分でフォントを作り直せる（例: `npx furifont build --base "Source Han Serif JP Bold" --script hepburn --family "My Furigana"`）。パッケージ: `@furifont/core`、`@furifont/dictionary`、`@furifont/helper-web`。

## 開発の参考として

- 「行間を読む」では、ふりがなを自前で付けず、Furifont で付ける案がある（どの場面で使うかは検討中）。原文を変えない、という方針と合う。

## 注意

- 読みは語ごとに辞書で決めるので、文脈で読みが変わる語は間違えることがある（作者も、読みが誤っている場合があると注意している）。
- 辞書は JMdict・JMnedict・KANJIDIC2（EDRDG）、JmdictFurigana、yomitan-jlpt-vocab、Tatoeba（CC BY 2.0 FR）などに由来し、CC BY-SA 4.0。
- 一部のサイト（X、GitHub など）は外部のフォントの読み込みを止めているため、ブックマークレットが効かない。
