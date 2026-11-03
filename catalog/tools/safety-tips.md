---
id: safety-tips
name: Safety tips（外国人旅行者向けの災害時情報提供アプリ）
publisher: 観光庁（監修）
url: https://www.mlit.go.jp/kankocho/seisaku_seido/kihonkeikaku/jizoku_kankochi/anzenkakuho/inbound/tool.html
category: tools
domains: [緊急・災害]
languages: [ja, en, zh-Hans, zh-Hant, ko, es, pt, vi, th, id, tl, ne, km, my, mn]
formats: [アプリ（iOS・Android）, Web API]
version: 2014年10月から提供（2026-11-03 に確認）
license: 独自（アプリは無料。API は有料の契約）
license_url: https://www.mlit.go.jp/kankocho/content/810002937.pdf
commercial: 未確認
redistribution: no
attribution: 未確認（API を使うときは、契約の条件による）
handling: link
uses: [reference, resource]
checked: 2026-11-03
---

# Safety tips

観光庁が監修する、外国人旅行者向けの災害時情報提供アプリ。緊急地震速報などをプッシュ通知で知らせる。

## 何が入っているか

- 通知: 緊急地震速報、津波警報、気象特別警報、噴火速報、避難情報、熱中症情報、Jアラートなど（観光庁の「Safety tips の概要」）。
- ほかに、災害時の行動のフローチャート、周りの人に見せるコミュニケーションカード、情報を集めるためのリンク集。
- 言語: 15言語（日本語、英語、中国語（簡体字・繁体字）、韓国語、スペイン語、ポルトガル語、ベトナム語、タイ語、インドネシア語、タガログ語、ネパール語、クメール語、ビルマ語、モンゴル語）。アプリは無料。
- **Safety tips API**（事業者向けの案内 https://www.mlit.go.jp/kankocho/content/810002937.pdf ）:
  - ほかのアプリで、同じ災害情報を受け取れる（Web API の JSON と、FCM のプッシュ通知）。
  - 情報: 地震・津波・気象警報・噴火・熱中症・台風。オプションで天気予報と、発災前に対応行動を伝える「事前学習」。
  - 価格は端末の台数などで変わる（問い合わせ）。多言語対応の、訪日外国人旅行者向けのアプリで使うことを想定している。
  - 例: 日本政府観光局（JNTO）の「Japan Official Travel App」。

## 開発の参考として

- 旅行者向けだが、在留外国人にも勧められている（防災庁（旧内閣府）の冊子「[災害時に便利なアプリとWEBサイト](../life-info/bousai-apps-websites.md)」、出入国在留管理庁の「災害時に役立つ情報」）。アプリでは、まずこれを入れるよう案内できる。
- 自分のアプリで災害の通知を出したいときは、独自に作らず API を検討する。
  - 想定は訪日旅行者向けのアプリ。在留外国人向けのアプリで使えるかは、問い合わせが要る。

## 注意

- 開発・運営は民間の会社（アールシーソリューション株式会社。同社の報道発表による）。API の契約の条件は未確認。
- 気象庁の情報を伝えるアプリなので、独自の警報は出さない（[気象庁 多言語の防災気象情報](../life-info/jma-multilingual-site.md)の注意）。
