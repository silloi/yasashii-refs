# 目録

1つの資料につき1ファイル。前付け（YAML）の形式と、足すときの手順は [CLAUDE.md](../CLAUDE.md)。分野と言語の優先順位は [docs/priorities.md](../docs/priorities.md)。資料ごとの言語の対応は [docs/language-coverage.md](../docs/language-coverage.md)（前付けから作る一覧表）。

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
| 生活情報 | [life-work-guidebook](life-info/life-work-guidebook.md) | 生活・就労ガイドブック 第8版（日本語・やさしい日本語。外国語の18言語は第7版） | 出入国在留管理庁 | PDF | PDL1.0 | 可 | link | 参考・資源 |
| 生活情報 | [life-support-portal](life-info/life-support-portal.md) | 外国人生活支援ポータルサイト | 出入国在留管理庁 | HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [jma-multilingual-site](life-info/jma-multilingual-site.md) | 気象庁 多言語の防災気象情報（15言語） | 気象庁 | HTML | PDL1.0 | 可 | link | 参考・資源 |
| 生活情報 | [mlit-bousai-portal](life-info/mlit-bousai-portal.md) | 国土交通省 防災ポータル（8言語の版） | 国土交通省 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [bousai-apps-websites](life-info/bousai-apps-websites.md) | 災害時に便利なアプリとWEBサイト（15言語のチラシ） | 内閣府（防災庁のサイトに掲載） | PDF | 未確認 | 未確認 | link | 参考 |
| 生活情報 | [fdma-multilingual-119](life-info/fdma-multilingual-119.md) | 外国人からの119番・救急への対応（三者間同時通訳など） | 消防庁 | HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [iryo-joho-net-opendata](life-info/iryo-joho-net-opendata.md) | 医療情報ネットのオープンデータ（病院・診療所・薬局など） | 厚生労働省 | CSV | PDL1.0 | 可 | ingest | 参考・資源 |
| 生活情報 | [mhlw-foreign-patient-manual](life-info/mhlw-foreign-patient-manual.md) | 外国人患者の受入れのための医療機関向けマニュアル（第4.0版） | 厚生労働省（研究班） | PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [soumu-foreign-resident-register](life-info/soumu-foreign-resident-register.md) | 外国人住民に係る住民基本台帳制度（住所の届出・住民票、12言語） | 総務省 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [digital-mynumber](life-info/digital-mynumber.md) | マイナンバー制度・マイナンバーカード（日本語・英語） | デジタル庁 | HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [jlis-mynumber-card](life-info/jlis-mynumber-card.md) | マイナンバーカード総合サイト（日本語＋6言語） | 地方公共団体情報システム機構 | HTML | 未確認 | 未確認 | link | 参考 |
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
| 生活情報 | [mlit-heya-sagashi](life-info/mlit-heya-sagashi.md) | 部屋探しのガイドブック（14言語）・賃貸住宅入居の手引き（やさしい日本語）・原状回復のポイント（14言語） | 国土交通省 | PDF | PDL1.0（2言語は外部の団体の提供） | 未確認 | link | 参考 |
| 生活情報 | [mlit-chintai-guideline](life-info/mlit-chintai-guideline.md) | 外国人の民間賃貸住宅入居円滑化ガイドライン（契約書等の見本14言語） | 国土交通省 | PDF・Word | PDL1.0 | 可 | link | 参考・資源 |
| 生活情報 | [safetynet-jutaku](life-info/safetynet-jutaku.md) | セーフティネット住宅情報提供システム（入居対象者に「外国人」。日本語だけ） | すまいづくりまちづくりセンター連合会（国土交通省の制度） | HTML | 独自（自動の取得・複製・改変の禁止） | 不可 | link | 参考 |
| 生活情報 | [npa-traffic-foreign](life-info/npa-traffic-foreign.md) | 外国人向けの交通ルールと運転免許の案内（20言語。シンハラ語・ウルドゥー語を含む） | 警察庁 | PDF・HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [mlit-jibaiseki-portal](life-info/mlit-jibaiseki-portal.md) | 自賠責保険・共済ポータルサイト（6言語） | 国土交通省 | HTML | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [fsa-bank-account-guide](life-info/fsa-bank-account-guide.md) | 日本でくらすための銀行口座や送金のつかい方（やさしい日本語＋16言語） | 金融庁 | PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [kif-medical-questionnaire](life-info/kif-medical-questionnaire.md) | 多言語医療問診票（23言語、診療科別。シンハラ語・タミル語を含む） | NPO法人国際交流ハーティ港南台・かながわ国際交流財団 | PDF・HTML | 独自（営利目的の使用は禁止） | 不可 | outreach | 参考・資源 |
| 生活情報 | [yoboseshu-rc-foreign](life-info/yoboseshu-rc-foreign.md) | 外国語版「予防接種と子どもの健康」と予診票（10言語＋予診票のみ7言語） | 予防接種リサーチセンター | PDF | 独自（営利目的で利用しない、実績の報告） | 不可 | outreach | 参考 |
| 生活情報 | [mhlw-rousai-pamphlet](life-info/mhlw-rousai-pamphlet.md) | 外国人労働者向け労災保険給付パンフレット（14言語） | 厚生労働省 | PDF | PDL1.0 | 可 | link | 参考 |
| 生活情報 | [otit-trainee-support](life-info/otit-trainee-support.md) | 技能実習生手帳（9言語、第10版）・母国語相談・げんばのにほんご | 外国人技能実習機構 | PDF・HTML・アプリ | 独自（許諾なく複製・改変はできない） | 未確認 | link | 参考 |
| 生活情報 | [isa-ssw-support-site](life-info/isa-ssw-support-site.md) | 特定技能総合支援サイト（やさしい日本語＋13言語。シンハラ語・ウルドゥー語を含む）と特定技能ガイドブック | 出入国在留管理庁 | HTML・PDF | 独自（無断の複製・転用はできない） | 未確認 | link | 参考 |
| 生活情報 | [ur-nonjapanese](life-info/ur-nonjapanese.md) | UR 賃貸住宅の外国語の案内（5言語） | UR 都市機構 | HTML・PDF | 独自（無断の転載・改変はできない） | 未確認 | link | 参考 |
| 生活情報 | [moj-koseki-international-qa](life-info/moj-koseki-international-qa.md) | 国際結婚、海外での出生等に関する戸籍Ｑ＆Ａ（日本語） | 法務省 | HTML | PDL1.0 | 可 | link | 参考 |
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
| レベル | [tsunahiro](levels/tsunahiro.md) | つながるひろがる　にほんごでのくらし（生活の場面の日本語学習、A1〜B1。日本語と19言語の表示、シンハラ語・ベンガル語を含む） | 文部科学省 | HTML・動画 | 独自（私的使用以外の転載・複製は不可） | 未確認 | link | 参考 |
| レベル | [jlpt](levels/jlpt.md) | 日本語能力試験の公開情報（出題基準は非公開） | 国際交流基金・日本国際教育支援協会 | HTML・PDF | 独自（無断の複製・翻案はできない） | 未確認 | link | 参考 |
| 公用文 | [kobun-sakusei](official-writing/kobun-sakusei.md) | 公用文作成の考え方（建議、2022年） | 文化審議会 | PDF | PDL1.0 | 可 | link | 参考 |
| 公用文 | [hinan-joho-guideline](official-writing/hinan-joho-guideline.md) | 避難情報に関するガイドライン（令和8年3月改定） | 内閣府（防災担当。防災庁のサイトに掲載） | PDF | 未確認 | 未確認 | link | 参考 |
| 公用文 | [clair-disaster-multilingual](official-writing/clair-disaster-multilingual.md) | 多言語災害情報文例集（63文例、やさしい日本語＋14言語）・災害時多言語表示シート | 自治体国際化協会 | XLSX・Word・HTML | 独自（サイトは無断の複製・改変を禁止。文例集は「ご自由に」） | 未確認 | outreach | 参考・資源 |
| 公用文 | [clb-horei-kanji](official-writing/clb-horei-kanji.md) | 法令における漢字使用等について（内閣法制局長官決定、平成22年） | 内閣法制局 | PDF | PDL1.0 | 可 | link | 参考 |
| 統計 | [residents-stats](statistics/residents-stats.md) | 在留外国人数（令和8年6月末） | 出入国在留管理庁 | HTML・PDF | PDL1.0 | 可 | link | 参考 |
| 統計 | [foreign-workers](statistics/foreign-workers.md) | 外国人雇用状況（令和7年10月末） | 厚生労働省 | HTML・PDF・XLSX | PDL1.0 | 可 | link | 参考 |
| 統計 | [international-students](statistics/international-students.md) | 外国人留学生在籍状況調査（令和7年度） | 日本学生支援機構 | HTML・PDF | 独自（許諾の無い転用は禁止） | 未確認 | link | 参考 |
| 統計 | [basic-survey](statistics/basic-survey.md) | 在留外国人に対する基礎調査（令和6年度） | 出入国在留管理庁 | PDF | PDL1.0 | 可 | link | 参考 |
| 道具 | [furifont](tools/furifont.md) | Furifont（ふりがなのフォント） | Anthony Fu | フォント・npm | MIT・OFL・CC BY-SA | 可 | link | 参考・資源 |
| 道具 | [dads](tools/dads.md) | デジタル庁デザインシステム | デジタル庁 | HTML・npm | MIT（トークン） | 可 | link | 参考・資源 |

## 相談の候補（outreach）

使ってよい範囲が限られていて、そのままではデータとして取り込めないもの。商用のサービスや公開するデータに使うときは、権利者に相談して合意を交わす。

| 資料 | 限られている点 | 相談先 |
| ---- | -------------- | ------ |
| [日本語教育語彙表](vocabulary/nihongo-kyoiku-goihyo.md) | 研究・教育のための利用に限る。二次配布は控える | 学習者辞書グループ（サイトのメンバー欄） |
| [外国人労働者向けの相談機関](life-info/mhlw-foreign-worker-consultation.md)（外国人労働者相談コーナーの一覧） | 「確かめよう労働条件」のサイトの条件で、営利目的の複製・頒布等の再利用をしない | 厚生労働省（労働基準局） |
| [多言語災害情報文例集](official-writing/clair-disaster-multilingual.md) | サイトポリシーは無断の複製・転用・改変を認めない。文例集のページは「ご自由にご活用ください」で、データの再配布や商用まで含むかは書かれていない | 自治体国際化協会 |
| [多言語医療問診票](life-info/kif-medical-questionnaire.md) | 営利目的の使用は禁止。インターネットでの利用は申請（リンク・制作者名の併記） | 多言語医療問診票事務局（かながわ国際交流財団） |
| [外国語版「予防接種と子どもの健康」と予診票](life-info/yoboseshu-rc-foreign.md) | 営利目的で利用しない。利用実績の報告が必要 | 予防接種リサーチセンター |
| [「生活者としての外国人」カリキュラム案](levels/seikatsusha-curriculum.md) の教材例集のイラスト・写真 | 日本語教育の教材を作るときに限る。営利目的なら各権利者に確認 | 文化庁国語課と、各イラスト・写真の権利者 |

## 扱わないもの

| 資料 | 理由 | 決めた日 |
| ---- | ---- | -------- |
| 10年以上前の、やさしい日本語の変換・判定ツール（YANSIS、やさにちチェッカー、チュウ太など） | このプロジェクト群は、こうした旧世代のツールを置き換えることを目指すため、参照しない（作り手の判断） | 2026-11-03 |
| Safety tips（観光庁監修の、外国人旅行者向けの災害時情報提供アプリ） | 民間の事業者が開発・運営するモバイルアプリが主で、API は有料（訪日旅行者向けのアプリでの利用を想定）。オープンなデータベースや文書として参照できない（作り手の判断） | 2026-11-03 |
| NHK WORLD-JAPAN の多言語の災害情報、VoiceTra（情報通信研究機構の音声翻訳アプリ） | 放送とアプリのサービスで、オープンなデータベースや文書として参照できない（CLAUDE.md の基準）。救急隊の救急ボイストラは [fdma-multilingual-119](life-info/fdma-multilingual-119.md) に書いた | 2026-11-04 |
| 医療通訳の育成の資料（厚生労働省の医療通訳育成カリキュラム基準など） | 医療通訳者を育てるための資料で、利用者向けの補足や訳語の基準には、厚生労働省の[外国人向け多言語説明資料](terms/mhlw-multilingual-medical-docs.md)と[多言語医療問診票](life-info/kif-medical-questionnaire.md)で足りる | 2026-11-04 |
| 文部科学省「たのしくまなび隊」の「外国とつながりのある方向けコンテンツ」 | 外部の教材へのリンク集で、資料そのものではない | 2026-11-04 |
| 外国人雇用管理指針（平成19年告示第276号） | 事業主が守る決まりで、利用者向けの補足には直接使わない。本文は https://www.mhlw.go.jp/content/000601382.pdf | 2026-11-04 |
| 電力・ガスの契約の相談窓口（電力・ガス取引監視等委員会） | 契約のトラブルの相談先で関連が低い。このリポジトリの取得では 403 | 2026-11-04 |
| 自治体の「やさしい日本語」の手引きと、自治体ごとの生活情報（ごみの出し方など） | 数が多く、地域ごとに違う。国の[在留支援のためのやさしい日本語ガイドライン](plain-japanese/plain-japanese-guideline.md)と、国の分野ごとの資料で足りる。地域の情報は、窓口の一覧（[isa-ichigen-soudan](life-info/isa-ichigen-soudan.md)）から自治体へ案内する | 2026-11-04 |
| 日本語を読むための語彙データベース（VDRJ） | 配布元のサイトが https に対応しておらず、この環境からもブラウザからも開きにくい。研究者が作った語彙表で、利用条件を確かめられない（確かめられるようになったら見直す） | 2026-11-04 |

## リンク切れと版の維持

- 配布元のページや PDF の URL は、予告なく変わることがある（日本年金機構のサイトの利用条件などにも書かれている）。見つけたリンク切れと移った先は、各目録の「注意」に書く。
- 「生活・就労ガイドブック」（第8版）が案内している URL のうち、古くなっていたもの（2026-11-03〜04 に確認）:
  - 第3章「外国人雇用のルールに関するパンフレット」: 404（[hellowork-foreign-language](life-info/hellowork-foreign-language.md)）
  - 第5章 高等学校等就学支援金制度: 404。「高校生等への修学支援」のページに移った（[mext-koko-shugaku-shienkin](life-info/mext-koko-shugaku-shienkin.md)）
  - 第8章 総務省の個人住民税: ページが見つからない。移った先は目録に書いた（[soumu-inhabitant-tax-foreigners](life-info/soumu-inhabitant-tax-foreigners.md)）
- **確かめ方:** `python3 scripts/check_links.py`（数分かかる）。前付けの `url`・`license_url` と、本文・docs・取り込み元の URL（2026-11-04 には137件）を1つずつ取得して、`catalog/link-state.json` に記録し、前回から変わったところを出す。
  - 配布ページは、ページの中のファイル（PDF・Excel など）へのリンクの一覧を記録する。新しい版は、たいていファイルの番号の変化として出る。
  - 利用条件のページは、本文のハッシュを記録する（条件が書き換わったら分かる）。ファイルは、大きさと更新日時を記録する。
  - `catalog/link-state.json` の差分（git diff）が、そのまま変化の記録になる。変わったものは、目録の「注意」・`version`・`checked` を直し、記録と一緒にコミットする。
  - 続けて2回回したとき、変わったのは一時的な接続の失敗の1件だけだった（2026-11-04）。接続の失敗や 5xx は、5秒待って1回だけやり直す。
- **確かめられないもの:**
  - ボット対策で止まるサイト（マイナンバーカード総合サイト）は、ステータス（403）を記録するだけにする。中身はブラウザで確かめる。
  - このクラウドの環境では、github.com もプロキシが 403 を返す（セッションに足したリポジトリしか開けない）。
  - 同じ名前のまま中身が替わったファイルは、配布ページのリンクの一覧だけでは分からない。
- 最初の確認（2026-11-04）で見つけたリンク切れ: 文化庁のカリキュラム案のページが案内する「生活Can do」一覧の PDF（404）。文部科学省のページが案内する新しい PDF に直した（[seikatsusha-curriculum](levels/seikatsusha-curriculum.md)、[nihongo-sanshowaku](levels/nihongo-sanshowaku.md)）。
- 定期的に回すしくみ（いつ・どこで回すか）は、まだ決めていない。

## これから確かめる候補

確かめるまでは目録に載せない（配布元・規約・形式を確かめてから、1ファイルずつ足す）。

- **分野ごとの多言語・やさしい日本語の資料:** 優先順位（[docs/priorities.md](../docs/priorities.md)）の9分野と、その「残り」は確かめた（2026-11-04）。残っているのは下のものだけ
- **ブラウザで確かめるもの**（このリポジトリの取得では中身が読めない。自動の操作では取り出さない）:
  - マイナンバーカード総合サイト（地方公共団体情報システム機構）の利用条件（言語は確かめた）。「リンク・著作権」https://www.kojinbango-card.go.jp/link_copy/ と「サイト利用規約」https://www.kojinbango-card.go.jp/tos/
- **防災の残り:**
  - 防災庁のサイトのコンテンツの利用条件（2026-11-04 もまだ書かれていない。時間をおいて確かめる）
