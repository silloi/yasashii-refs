# 目録

1つの資料につき1ファイル。前付け（YAML）の形式と、足すときの手順は [CLAUDE.md](../CLAUDE.md)。分野と言語の優先順位は [docs/priorities.md](../docs/priorities.md)。

`python3 scripts/check_catalog.py` で、前付けの書き漏れと、この一覧との食い違いを確かめられます。

## 一覧

扱い: `ingest` 取り込める／`link` リンクだけ／`outreach` 相談の候補／`exclude` 扱わない。使い道: 参考＝開発の参考、資源＝アプリの資源。

| 分類 | id | 資料 | 提供元 | 形式 | ライセンス | 商用 | 扱い | 使い道 |
| ---- | -- | ---- | ------ | ---- | ---------- | ---- | ---- | ------ |
| 用語 | [jlt-standard-dict](terms/jlt-standard-dict.md) | 法令用語日英標準対訳辞書 19.0 | 法務省 | PDF・XML・CSV | PDL1.0 | 可 | ingest | 参考・資源 |
| やさしい日本語 | [plain-japanese-guideline](plain-japanese/plain-japanese-guideline.md) | 在留支援のためのやさしい日本語ガイドライン | 出入国在留管理庁・文化庁 | PDF | PDL1.0 | 可 | link | 参考 |
| やさしい日本語 | [plain-japanese-rewrites](plain-japanese/plain-japanese-rewrites.md) | 同 別冊「やさしい日本語書き換え例」 | 出入国在留管理庁・文化庁 | PDF | PDL1.0 | 可 | ingest | 参考・資源 |
| 生活情報 | [life-work-guidebook](life-info/life-work-guidebook.md) | 生活・就労ガイドブック 第8版（日本語・やさしい日本語＋18言語） | 出入国在留管理庁 | PDF | PDL1.0 | 可 | link | 参考・資源 |
| 生活情報 | [life-support-portal](life-info/life-support-portal.md) | 外国人生活支援ポータルサイト | 出入国在留管理庁 | HTML | PDL1.0 | 可 | link | 参考 |
| 漢字 | [joyo-kanji-hyo](kanji/joyo-kanji-hyo.md) | 常用漢字表（平成22年内閣告示） | 文化庁 | PDF | 告示 | 可 | ingest | 参考・資源 |
| 漢字 | [gakunen-kanji](kanji/gakunen-kanji.md) | 学年別漢字配当表（学習指導要領コード表） | 文部科学省 | CSV・PDF | 告示・PDL1.0 | 可 | ingest | 参考・資源 |
| 漢字 | [kanjidic2](kanji/kanjidic2.md) | KANJIDIC2 | EDRDG | XML | CC BY-SA 4.0 | 可（継承） | ingest | 参考・資源 |
| 語彙 | [jmdict](vocabulary/jmdict.md) | JMdict | EDRDG | XML | CC BY-SA 4.0 | 可（継承） | ingest | 参考・資源 |
| レベル | [nihongo-sanshowaku](levels/nihongo-sanshowaku.md) | 日本語教育の参照枠（生活 Can do） | 文化審議会国語分科会 | PDF | PDL1.0 | 可 | link | 参考 |
| レベル | [jlpt](levels/jlpt.md) | 日本語能力試験の公開情報（出題基準は非公開） | 国際交流基金・日本国際教育支援協会 | HTML・PDF | 未確認 | 未確認 | link | 参考 |
| 統計 | [residents-stats](statistics/residents-stats.md) | 在留外国人数（令和8年6月末） | 出入国在留管理庁 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 統計 | [foreign-workers](statistics/foreign-workers.md) | 外国人雇用状況（令和7年10月末） | 厚生労働省 | HTML・PDF・XLSX | 未確認 | 未確認 | link | 参考 |
| 統計 | [international-students](statistics/international-students.md) | 外国人留学生在籍状況調査（令和7年度） | 日本学生支援機構 | HTML・PDF | 未確認 | 未確認 | link | 参考 |
| 統計 | [basic-survey](statistics/basic-survey.md) | 在留外国人に対する基礎調査（令和6年度） | 出入国在留管理庁 | PDF | PDL1.0 | 可 | link | 参考 |
| 道具 | [furifont](tools/furifont.md) | Furifont（ふりがなのフォント） | Anthony Fu | フォント・npm | MIT・OFL・CC BY-SA | 可 | link | 参考・資源 |
| 道具 | [dads](tools/dads.md) | デジタル庁デザインシステム | デジタル庁 | HTML・npm | MIT（トークン） | 可 | link | 参考・資源 |

## 扱わないもの

| 資料 | 理由 | 決めた日 |
| ---- | ---- | -------- |
| 10年以上前の、やさしい日本語の変換・判定ツール（YANSIS、やさにちチェッカー、チュウ太など） | このプロジェクト群は、こうした旧世代のツールを置き換えることを目指すため、参照しない（作り手の判断） | 2026-11-03 |

## これから確かめる候補

確かめるまでは目録に載せない（配布元・規約・形式を確かめてから、1ファイルずつ足す）。

- **語彙のレベル:** 日本語教育語彙表（統合型の語彙データベース J-CLID などで参照できる。配布元と規約が未確認）、日本語を読むための語彙データベース（VDRJ）
- **生活の場面の分類:** 文化庁「『生活者としての外国人』に対する日本語教育の標準的なカリキュラム案」
- **公用文の書き方:** 文化審議会「公用文作成の考え方」（建議、2022年）
- **分野ごとの多言語・やさしい日本語の資料:** 外国人生活支援ポータルサイトのリンク集から、医療（多言語の問診票など）、教育（外国人の子どもの就学のガイドブック）、年金・税、防災を、優先順位（[docs/priorities.md](../docs/priorities.md)）の順に
- **自治体の「やさしい日本語」の手引き:** 数が多いので網羅しない。少数を選んで載せるか、扱わない
- **確認の残り:** 「生活・就労ガイドブック」の中国語版が簡体字か繁体字か、各言語版の版（第8版か）、厚生労働省・日本学生支援機構・日本語能力試験のサイトの利用規約
