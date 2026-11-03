---
id: dads
name: デジタル庁デザインシステム（DADS）
publisher: デジタル庁
url: https://design.digital.go.jp/dads/
category: tools
domains: [全般]
languages: [ja]
formats: [HTML, Figma, npm パッケージ]
version: β版 v2.18.2（サイトの表示。デザイントークンの npm パッケージは 2.1.0）
license: MIT（デザイントークン @digital-go-jp/design-tokens）
license_url: https://github.com/digital-go-jp/design-tokens
commercial: yes
redistribution: yes
attribution: 色の値は、デジタル庁デザインシステムのデザイントークン（@digital-go-jp/design-tokens、MIT License、© デジタル庁）による
handling: link
uses: [reference, resource]
checked: 2026-11-03
---

# デジタル庁デザインシステム

行政のウェブサービスのための、色・文字・部品・アクセシビリティの指針。

## 開発の参考として

- アクセシビリティや画面の設計で迷ったときの基準（作り手の方針）。とくに「カラー：アクセシビリティ」の次の点。
  - コントラスト比（文字は 4.5:1 以上、文字以外は 3:1 以上）
  - 色だけで情報を区別しない
  - カラーユニバーサルデザイン推奨配色セットを参考にする
- フォーカスの印（黄と黒の2重）。リンクの色（青と、訪問済みの紫を、色覚の多様性に配慮して明度差を付ける）。
- 「行間を読む」（`gyokan`）では、色をすべてこのデザイントークンから選び、テストで値とコントラスト比を確かめている。

## アプリの資源として

- デザイントークン（`@digital-go-jp/design-tokens`、MIT）は npm で配布されていて、そのまま使える。

## 注意

- 公的サイトの中には、同じデザイントークンの CSS 変数を使っているものがある。他のページの中に部品を差し込むアプリでは、変数名を自分の名前で付け直して、元のページの変数を上書きしない（「行間を読む」は `--gk-` に付け直している）。
