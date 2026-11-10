---
id: mhlw-tagengo-yougo
name: 雇用管理に役立つ多言語用語集（厚生労働省、やさしい日本語＋14言語）
name_en: Multilingual Glossary for Employment Management
publisher: 厚生労働省（職業安定局外国人雇用対策課）
publisher_en: Foreign Workers Affairs Division, Employment Security Bureau, Ministry of Health, Labour and Welfare (MHLW)
summary: 人事・労務でよく使う労働と社会保険の用語418語の、やさしい日本語の説明と多言語の訳。
summary_en: 418 labor and social insurance terms with Easy Japanese definitions and translations.
url: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/jigyounushi/tagengoyougosyu.html
category: terms
domains: [雇用・労働]
languages: [ja-easy, en, zh-Hans, zh-Hant, ko, es, pt, tl, vi, ne, id, th, my, mn, km]
formats: [XLSX, HTML]
version: "2023-04-20"
license: PDL-1.0
license_url: https://www.mhlw.go.jp/chosakuken/index.html
commercial: yes
redistribution: yes
attribution: 出典：厚生労働省「雇用管理に役立つ多言語用語集」（https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/jigyounushi/tagengoyougosyu.html）
handling: ingest
uses: [reference, resource]
checked: 2026-11-04
---

# 雇用管理に役立つ多言語用語集

人事・労務の場面でよく使う、労働と社会保険の用語418語の用語集。それぞれの語に、やさしい日本語の定義と例文（読みは括弧書き）と、14言語の訳（用語・定義・例文）がある。「生活・就労ガイドブック」の第3章が、労働や社会保険の言葉が分からないときの確認先として案内している。

## 何が入っているか

- 418語、11のカテゴリー: 1.採用（14）、2.賃金・社会保険料・税・給付金（104）、3.労働時間（39）、4.休日・休暇（37）、5.異動・退職・休職・解雇（54）、6.安全衛生・災害補償（35）、7.ハラスメント（10）、8.在留資格等（28）、9.有期雇用・派遣（16）、10.労働に関する基礎用語（37）、11.その他（44）。
- 言語: やさしい日本語、英語、中国語（簡体字・繁体字）、韓国語、スペイン語、ポルトガル語、タガログ語、ベトナム語、ネパール語、インドネシア語、タイ語、ミャンマー語、モンゴル語、カンボジア語（クメール語）。
- 形式:
  - Excel 版（15シート。やさしい日本語と14言語）。文書の更新日は2023年4月20日。
  - ウェブ版（やさしい日本語と9言語。カテゴリーと五十音で探せる）。インドネシア語・タイ語・ミャンマー語・モンゴル語・カンボジア語は、Excel 版にだけある。
- 令和2年度の「雇用管理に役立つ多言語用語集及び翻訳データの作成・普及事業」の成果物（委託先は民間の会社）。同じ事業の、あと2つの道具:
  - 「外国人社員と働く職場の労務管理に使えるポイント・例文集」（令和3年3月、PDF・Word）。場面ごとの、やさしい日本語の説明の例文。
  - 「モデル就業規則やさしい日本語版」（Word）。

## 開発の参考として

- 労働・社会保険の言葉の、国が作った多言語の対訳。補足で言い換えるときの訳語の基準になる。
- やさしい日本語の定義と例文が、言い換えの見本になる（例:「安全衛生」→「安全（あんぜん）に健康（けんこう）に働（はたら）くことができること。」）。
- ミャンマー語・インドネシア語・ネパール語を含む。ほかの分野の公的な資料で抜けていることが多い言語（[docs/priorities.md](../../docs/priorities.md)）。

## アプリの資源として（将来）

- **取り込み済み:** [`data/mhlw-tagengo-yougo.jsonl`](../../data/README.md)（418語、14言語）。作り直すときは `python3 scripts/ingest_mhlw_tagengo_yougo.py`。
- 雇用・労働の文に出てくる言葉に、やさしい日本語の定義と、利用者の言語の訳を添える材料。

## 注意

- 利用規約: 「当ホームページで公開している情報…は、特記されていない限り厚生労働省に帰属し、権利表記の記載がない限り「公共データ利用規約（第1.0版）」（PDL1.0）に準拠した利用条件の下で、利用することができます」。用語集のページと Excel に、別の権利表記は無い（2026-11-04）。
- **ポルトガル語とタガログ語のシートは、項番の振り方と並びがほかのシートと違う**（同じ項番が別の用語を指す）。項番で突き合わせると訳がずれる。取り込みでは、日本語の列（カテゴリー・用語・定義・例文）で突き合わせた。
- 元のままにしたもの:
  - 「月平均所定外労働時間」の読みが、Excel 版では「つきへんいきん…」になっている（ウェブ版は「つきへいきん…」）。
  - 英語の「安全衛生」の訳が「Safety and health education」で、「安全衛生教育」の訳と同じ。
  - カンボジア語などに、ゼロ幅スペース（U+200B）がある。
- Excel のセルには、ふりがな（フリガナ情報）が入っている。取り込むときは除く。
- 用語は事業主・人事担当者の目線で選ばれている（就業規則・労働条件の説明に使う語が中心）。
