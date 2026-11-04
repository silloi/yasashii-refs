# 目録

1つの資料につき1ファイル。前付け（YAML）の形式と、足すときの手順は [CLAUDE.md](../CLAUDE.md)。分野と言語の優先順位は [docs/priorities.md](../docs/priorities.md)。

`python3 scripts/check_catalog.py` で、前付けの書き漏れと、この一覧との食い違いを確かめられます。

## 一覧

扱い: `ingest` 取り込める／`link` リンクだけ／`outreach` 相談の候補／`exclude` 扱わない。使い道: 参考＝開発の参考、資源＝アプリの資源。

| 分類 | id | 資料 | 提供元 | 形式 | ライセンス | 商用 | 扱い | 使い道 |
| ---- | -- | ---- | ------ | ---- | ---------- | ---- | ---- | ------ |
| 用語 | [jlt-standard-dict](terms/jlt-standard-dict.md) | 法令用語日英標準対訳辞書 19.0 | 法務省 | PDF・XML・CSV | PDL1.0 | 可 | ingest | 参考・資源 |
| 用語 | [jma-multilingual-dict](terms/jma-multilingual-dict.md) | 気象庁 多言語辞書（防災の用語、14言語） | 気象庁 | XLSX | PDL1.0 | 可 | ingest | 参考・資源 |
| 用語 | [mhlw-multilingual-medical-docs](terms/mhlw-multilingual-medical-docs.md) | 外国人向け多言語説明資料（医療機関の書類、13言語・日本語併記） | 厚生労働省 | Word・PDF・Excel | PDL1.0 | 可 | ingest | 参考・資源 |
| 用語 | [jps-nenkin-yougo](terms/jps-nenkin-yougo.md) | 年金用語集（116語、取り込み済み） | 日本年金機構 | HTML | 独自（転載フリー） | 未確認 | ingest | 参考・資源 |
| 用語 | [mhlw-tagengo-yougo](terms/mhlw-tagengo-yougo.md) | 雇用管理に役立つ多言語用語集（418語、やさしい日本語＋14言語、取り込み済み） | 厚生労働省 | XLSX・HTML | PDL1.0 | 可 | ingest | 参考・資源 |
| やさしい日本語 | [plain-japanese-guideline](plain-japanese/plain-japanese-guideline.md) | 在留支援のためのやさしい日本語ガイドライン | 出入国在留管理庁・文化庁 | PDF | PDL1.0 | 可 | link | 参考 |
| やさしい日本語 | [plain-japanese-rewrites](plain-japanese/plain-japanese-rewrites.md) | 同 別冊「やさしい日本語書き換え例」 | 出入国在留管理庁・文化庁 | PDF | PDL1.0 | 可 | ingest | 参考・資源 |
| 生活情報 | [life-work-guidebook](life-info/life-work-guidebook.md) | 生活・就労ガイドブック 第8版（日本語・やさしい日本語＋18言語） | 出入国在留管理庁 | PDF | PDL1.0 | 可 | link | 参考・資源 |
| 生活情報 | [life-support-portal](life-info/life-support-portal.md) | 外国人生活支援ポータルサイト | 出入国在留管理庁 | HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [jma-multilingual-site](life-info/jma-multilingual-site.md) | 気象庁 多言語の防災気象情報（15言語） | 気象庁 | HTML | PDL1.0 | 可 | link | 参考・資源 |
| 生活情報 | [mlit-bousai-portal](life-info/mlit-bousai-portal.md) | 国土交通省 防災ポータル（8言語の版） | 国土交通省 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [bousai-apps-websites](life-info/bousai-apps-websites.md) | 災害時に便利なアプリとWEBサイト（15言語のチラシ） | 内閣府（防災庁のサイトに掲載） | PDF | 未確認 | 未確認 | link | 参考 |
| 生活情報 | [fdma-multilingual-119](life-info/fdma-multilingual-119.md) | 外国人からの119番・救急への対応（三者間同時通訳など） | 消防庁 | HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [iryo-joho-net-opendata](life-info/iryo-joho-net-opendata.md) | 医療情報ネットのオープンデータ（病院・診療所・薬局など） | 厚生労働省 | CSV | PDL1.0 | 可 | ingest | 参考・資源 |
| 生活情報 | [mhlw-foreign-patient-manual](life-info/mhlw-foreign-patient-manual.md) | 外国人患者の受入れのための医療機関向けマニュアル（第4.0版） | 厚生労働省（研究班） | PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [soumu-foreign-resident-register](life-info/soumu-foreign-resident-register.md) | 外国人住民に係る住民基本台帳制度（住所の届出・住民票、12言語） | 総務省 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [digital-mynumber](life-info/digital-mynumber.md) | マイナンバー制度・マイナンバーカード（日本語・英語） | デジタル庁 | HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [isa-ichigen-soudan](life-info/isa-ichigen-soudan.md) | 一元的相談窓口の現況と一覧（290団体、言語別の受付件数） | 出入国在留管理庁 | XLSX・PDF | PDL1.0 | 可 | ingest | 参考・資源 |
| 生活情報 | [jps-foreign-residents](life-info/jps-foreign-residents.md) | 外国人向けの情報（やさしいにほんご・英語・脱退一時金の請求書14言語） | 日本年金機構 | HTML・PDF・XLSX | 独自（転載フリー） | 未確認 | ingest | 参考・資源 |
| 生活情報 | [soumu-inhabitant-tax-foreigners](life-info/soumu-inhabitant-tax-foreigners.md) | 外国人の方の個人住民税について（チラシ5言語） | 総務省 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [nta-english](life-info/nta-english.md) | Information for Taxpayers（国税の英語の説明） | 国税庁 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [cfa-boshi-techou-multilingual](life-info/cfa-boshi-techou-multilingual.md) | 母子健康手帳 多言語版（10か国語）と外国人向けのリーフレット | こども家庭庁 | PDF・HTML | PDL1.0（一部に第三者の権利） | 未確認 | link | 参考 |
| 生活情報 | [mext-shugaku-guidebook](life-info/mext-shugaku-guidebook.md) | 外国人児童生徒のための就学ガイドブック（8言語、日本語併記） | 文部科学省 | PDF | PDL1.0 | 可 | ingest | 参考・資源 |
| 生活情報 | [casta-net](life-info/casta-net.md) | かすたねっと（多言語の学校の通知文書・教材・用語の検索） | 文部科学省 | HTML・PDF ほか | 独自（改変不可。文書は各公開主体） | 未確認 | link | 参考 |
| 生活情報 | [mext-koko-shugaku-shienkin](life-info/mext-koko-shugaku-shienkin.md) | 高等学校等就学支援金（新制度）のリーフレット（日本国籍以外の方用・英語） | 文部科学省 | PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [mhlw-foreign-worker-consultation](life-info/mhlw-foreign-worker-consultation.md) | 外国人労働者向けの相談機関（相談ダイヤル・ほっとライン13言語、相談コーナーの一覧） | 厚生労働省 | HTML | 独自（営利目的の再利用はしない） | 不可 | outreach | 参考・資源 |
| 生活情報 | [hellowork-foreign-language](life-info/hellowork-foreign-language.md) | ハローワークの外国語の案内（通訳がいるハローワークの一覧、外国語での電話10言語、利用チェックリスト） | 厚生労働省・ハローワーク | PDF | PDL1.0 | 可 | ingest | 参考・資源 |
| 生活情報 | [mhlw-model-labor-conditions-notice](life-info/mhlw-model-labor-conditions-notice.md) | 外国人労働者向けモデル労働条件通知書（13言語） | 厚生労働省 | PDF | PDL1.0 | 可 | link | 参考 |
| 漢字 | [joyo-kanji-hyo](kanji/joyo-kanji-hyo.md) | 常用漢字表（平成22年内閣告示） | 文化庁 | PDF | 告示 | 可 | ingest | 参考・資源 |
| 漢字 | [gakunen-kanji](kanji/gakunen-kanji.md) | 学年別漢字配当表（学習指導要領コード表） | 文部科学省 | CSV・PDF | 告示・PDL1.0 | 可 | ingest | 参考・資源 |
| 漢字 | [kanjidic2](kanji/kanjidic2.md) | KANJIDIC2 | EDRDG | XML | CC BY-SA 4.0 | 可（継承） | ingest | 参考・資源 |
| 漢字 | [onkun-warifuri](kanji/onkun-warifuri.md) | 音訓の小・中・高等学校段階別割り振り表（平成29年3月） | 文部科学省 | PDF | PDL1.0 | 可 | ingest | 参考・資源 |
| 漢字 | [bunka-kanji-frequency](kanji/bunka-kanji-frequency.md) | 漢字出現頻度表 順位対照表 Ver.1.3（書籍・新聞・ウェブでの順位） | 文化庁国語課 | PDF | PDL1.0 | 可 | ingest | 参考・資源 |
| 漢字 | [hyogai-jitaihyo](kanji/hyogai-jitaihyo.md) | 表外漢字字体表（平成12年答申、1,022字） | 国語審議会（文化庁） | PDF（データは Wikipedia の表） | PDL1.0（Wikipedia の表は CC BY-SA 4.0） | 可 | ingest | 参考 |
| 語彙 | [jmdict](vocabulary/jmdict.md) | JMdict | EDRDG | XML | CC BY-SA 4.0 | 可（継承） | ingest | 参考・資源 |
| 語彙 | [jmnedict](vocabulary/jmnedict.md) | JMnedict（固有名詞） | EDRDG | XML | CC BY-SA 4.0 | 可（継承） | ingest | 参考・資源 |
| 語彙 | [nihongo-kyoiku-goihyo](vocabulary/nihongo-kyoiku-goihyo.md) | 日本語教育語彙表 Ver1.1（17,908語、6段階の難易度） | 学習者辞書グループ（科研費） | Excel・Web | 独自（研究・教育に限る、二次配布不可） | 不可 | outreach | 参考 |
| レベル | [nihongo-sanshowaku](levels/nihongo-sanshowaku.md) | 日本語教育の参照枠（生活 Can do） | 文化審議会国語分科会 | PDF | PDL1.0 | 可 | link | 参考 |
| レベル | [seikatsusha-curriculum](levels/seikatsusha-curriculum.md) | 「生活者としての外国人」カリキュラム案（2022年の報告・生活 Can do 一覧） | 文化審議会国語分科会 | PDF・XLS | PDL1.0（教材例集の絵・写真は別） | 可 | link | 参考 |
| レベル | [jlpt](levels/jlpt.md) | 日本語能力試験の公開情報（出題基準は非公開） | 国際交流基金・日本国際教育支援協会 | HTML・PDF | 未確認 | 未確認 | link | 参考 |
| 公用文 | [kobun-sakusei](official-writing/kobun-sakusei.md) | 公用文作成の考え方（建議、2022年） | 文化審議会 | PDF | PDL1.0 | 可 | link | 参考 |
| 公用文 | [hinan-joho-guideline](official-writing/hinan-joho-guideline.md) | 避難情報に関するガイドライン（令和8年3月改定） | 内閣府（防災担当。防災庁のサイトに掲載） | PDF | 未確認 | 未確認 | link | 参考 |
| 統計 | [residents-stats](statistics/residents-stats.md) | 在留外国人数（令和8年6月末） | 出入国在留管理庁 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 統計 | [foreign-workers](statistics/foreign-workers.md) | 外国人雇用状況（令和7年10月末） | 厚生労働省 | HTML・PDF・XLSX | 未確認 | 未確認 | link | 参考 |
| 統計 | [international-students](statistics/international-students.md) | 外国人留学生在籍状況調査（令和7年度） | 日本学生支援機構 | HTML・PDF | 未確認 | 未確認 | link | 参考 |
| 統計 | [basic-survey](statistics/basic-survey.md) | 在留外国人に対する基礎調査（令和6年度） | 出入国在留管理庁 | PDF | PDL1.0 | 可 | link | 参考 |
| 道具 | [furifont](tools/furifont.md) | Furifont（ふりがなのフォント） | Anthony Fu | フォント・npm | MIT・OFL・CC BY-SA | 可 | link | 参考・資源 |
| 道具 | [dads](tools/dads.md) | デジタル庁デザインシステム | デジタル庁 | HTML・npm | MIT（トークン） | 可 | link | 参考・資源 |

## 相談の候補（outreach）

使ってよい範囲が限られていて、そのままではデータとして取り込めないもの。商用のサービスや公開するデータに使うときは、権利者に相談して合意を交わす。

| 資料 | 限られている点 | 相談先 |
| ---- | -------------- | ------ |
| [日本語教育語彙表](vocabulary/nihongo-kyoiku-goihyo.md) | 研究・教育のための利用に限る。二次配布は控える | 学習者辞書グループ（サイトのメンバー欄） |
| [外国人労働者向けの相談機関](life-info/mhlw-foreign-worker-consultation.md)（外国人労働者相談コーナーの一覧） | 「確かめよう労働条件」のサイトの条件で、営利目的の複製・頒布等の再利用をしない | 厚生労働省（労働基準局） |
| [「生活者としての外国人」カリキュラム案](levels/seikatsusha-curriculum.md) の教材例集のイラスト・写真 | 日本語教育の教材を作るときに限る。営利目的なら各権利者に確認 | 文化庁国語課と、各イラスト・写真の権利者 |

## 扱わないもの

| 資料 | 理由 | 決めた日 |
| ---- | ---- | -------- |
| 10年以上前の、やさしい日本語の変換・判定ツール（YANSIS、やさにちチェッカー、チュウ太など） | このプロジェクト群は、こうした旧世代のツールを置き換えることを目指すため、参照しない（作り手の判断） | 2026-11-03 |
| Safety tips（観光庁監修の、外国人旅行者向けの災害時情報提供アプリ） | 民間の事業者が開発・運営するモバイルアプリが主で、API は有料（訪日旅行者向けのアプリでの利用を想定）。オープンなデータベースや文書として参照できない（作り手の判断） | 2026-11-03 |

## これから確かめる候補

確かめるまでは目録に載せない（配布元・規約・形式を確かめてから、1ファイルずつ足す）。

- **語彙のレベル:** 日本語を読むための語彙データベース（VDRJ）
- **分野ごとの多言語・やさしい日本語の資料:** 優先順位（[docs/priorities.md](../docs/priorities.md)）の次は、住居、交通・日常
  - 「生活・就労ガイドブック」が各章で案内している国のページも手がかりになる（例: 住居の章の「部屋探しのガイドブック」、金融庁の銀行口座の案内）
- **雇用・労働の残り:**
  - 労災保険の外国語の案内（ガイドブックの第3章が案内する厚生労働省の労災補償のページ）
  - 外国人技能実習機構（技能実習生向けの多言語の資料）と、特定技能の外国人向けの情報（出入国在留管理庁）
  - 外国人雇用管理指針（平成19年告示第276号）。事業主向けの決まりで、告示の本文は https://www.mhlw.go.jp/content/000601382.pdf
- **出産・子育て・教育の残り:**
  - 児童手当の外国語の案内（こども家庭庁。ガイドブックの第4章は URL を挙げていない）
  - 文化庁・文部科学省の日本語学習のサイト（「つながるひろがる　にほんごでのくらし」、日本語能力自己評価ツール）。ガイドブックの第5章が案内している
  - 文部科学省「たのしくまなび隊」の「外国とつながりのある方向けコンテンツ」（外部の教材へのリンク集）
- **市区町村の手続の残り:**
  - 婚姻・離婚・死亡などの戸籍の届出の、外国人向けの国の情報（法務省民事局。ガイドブックは市区町村と大使館への問い合わせを案内しているだけ）
  - J-LIS の「マイナンバーカード総合サイト」の言語と利用条件（このリポジトリの取得では 403 になるので、ブラウザで確かめる）
- **医療の残り:**
  - 多言語の医療問診票（かながわ国際交流財団など。公的機関ではないので規約を確かめる）
  - 予防接種の多言語の資料（「予防接種と子どもの健康」の外国語版など。配布元と規約）。母子健康手帳の多言語版は [cfa-boshi-techou-multilingual](life-info/cfa-boshi-techou-multilingual.md)
  - 医療通訳の資料（厚生労働省の「医療通訳育成カリキュラム基準」など）
- **防災の残り:**
  - 消防庁の多言語の「救急車利用ガイド」（いまの配布ページ）
  - 自治体国際化協会（CLAIR）の「災害時多言語表示シート」などの災害時の多言語の支援の道具（規約）
  - NHK WORLD-JAPAN の多言語の災害情報、VoiceTra（NICT）の利用条件
  - 防災庁のサイトのコンテンツの利用条件（設置されたばかりで、まだ書かれていない）
- **公文書を書く側の資料:** 内閣法制局「法令における漢字使用等について」など、公用文作成の考え方の周辺
- **自治体の「やさしい日本語」の手引き:** 数が多いので網羅しない。少数を選んで載せるか、扱わない
- **確認の残り:** 「生活・就労ガイドブック」の中国語版が簡体字か繁体字か、各言語版の版（第8版か）、厚生労働省・日本学生支援機構・日本語能力試験のサイトの利用規約
