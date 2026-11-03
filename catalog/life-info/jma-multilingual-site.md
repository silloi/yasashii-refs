---
id: jma-multilingual-site
name: 気象庁 多言語の防災気象情報（災害情報のページ）
publisher: 気象庁
url: https://www.data.jma.go.jp/multi/index.html?lang=jp
category: life-info
domains: [緊急・災害]
languages: [ja, en, zh-Hans, zh-Hant, ko, es, pt, vi, th, id, tl, ne, km, my, mn]
formats: [HTML]
version: 随時更新（2026-11-03 に確認）
license: PDL-1.0
license_url: https://www.jma.go.jp/jma/kishou/info/coment.html
commercial: yes
redistribution: yes
attribution: 出典：気象庁ホームページ（https://www.data.jma.go.jp/multi/index.html）
handling: link
uses: [reference, resource]
checked: 2026-11-03
---

# 気象庁 多言語の防災気象情報

気象庁が、警報・注意報や地震・津波などの情報を、15言語で出しているページ。

## 何が入っているか

- 言語: 日本語、英語、中国語（簡体字・繁体字）、韓国語、スペイン語、ポルトガル語、ベトナム語、タイ語、インドネシア語、タガログ語、ネパール語、クメール語、ビルマ語、モンゴル語。[多言語辞書](../terms/jma-multilingual-dict.md)の14言語と同じ。
- 主な内容（メニュー）: 警報・注意報、天気予報、台風、気象衛星、キキクル（土砂災害・浸水・洪水の危険度）、津波、地震、火山。

## 開発の参考として

- 多言語辞書の訳語が、実際の警報・注意報・地震などの画面でどう使われているかを見られる。内容は公共データ利用規約（PDL1.0）で使える。
- アプリで防災の情報を多言語で出すときの、公式の案内先。気象庁の発表を独自に訳したり言い換えたりせず、ここへ案内する。
- 訳語は多言語辞書と同じ。補足を付けるときも、辞書の訳語にそろえる。
- 2026年5月下旬から「新たな防災気象情報」の運用が始まり、警報・注意報の名前にレベルが付いた（例: 土砂災害警戒情報 → レベル４土砂災害危険警報）。古い資料の名前と取り違えない（[避難情報に関するガイドライン](../official-writing/hinan-joho-guideline.md)）。

## 注意

- 利用規約は気象庁のサイト共通（公共データ利用規約 第1.0版に準拠）。
- **気象業務法:** 気象庁以外の者が独自に予報や警報を出すことは制限されている（第17条・第23条）。アプリでは気象庁の発表を正しく伝える形にし、独自の警報を作らない。
- ページの中身は JavaScript で作られる。HTML を取得しただけでは文字が入っていない。データとして使うなら、気象庁防災情報XML などの開発者向けの提供を使う。
