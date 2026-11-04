# 資料ごとの言語の対応

<!-- scripts/language_table.py が目録の前付けから作るファイル。手で直さない。 -->

目録の資料が、どの言語で読めるか（使えるか）の一覧。目録の前付けの `languages` から `python3 scripts/language_table.py` で作る。手で直さず、目録を直してから作り直す。

- 対象: 生活情報・用語・公用文・レベルの分類の資料のうち、外国語が1つ以上あるもの（37件）。外国語が無いもの（11件）は、最後の「外国語の版が無い資料」にまとめた。
- 分野: 前付けの `domains` の最初の分野の表に入れる（すべての分野にわたるものは「全般」）。分野の順は [priorities.md](priorities.md) の順位。
- 列の言語は、[priorities.md](priorities.md) の「併記する言語の順番（案）」の群の順。日本語の列は省いた。
  - ja-easy: やさしい日本語
  - 第1群: vi ベトナム語、zh-Hans 中国語（簡体字）、en 英語、tl フィリピノ語、ne ネパール語、id インドネシア語、pt ポルトガル語、ko 韓国語、my ミャンマー語
  - 第2群: es スペイン語、th タイ語、zh-Hant 中国語（繁体字）、km クメール語、mn モンゴル語
  - 第3群: si シンハラ語、bn ベンガル語、ur ウルドゥー語、ta タミル語
  - その他の列: hi ヒンディー語、tr トルコ語、uk ウクライナ語、ru ロシア語、fr フランス語、ar アラビア語、fa ペルシア語、de ドイツ語、it イタリア語、lo ラオ語、hr クロアチア語
- ○＝ある。＊＝中国語だが、簡体字・繁体字の区別が無い（話し言葉の対応など）。空欄＝無い。
- 資料の中の一部の文書だけにある言語も○にした（どの文書にあるかは各項目の本文）。言語は、各項目を確かめた日（前付けの `checked`）の時点。

## 分野ごとの表

### 全般

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [つながるひろがる　にほんごでのくらし](../catalog/levels/tsunahiro.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  | uk・ru・fr | 19 |
| [生活・就労ガイドブック](../catalog/life-info/life-work-guidebook.md) | link | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  | hi・tr・uk・ru・fr | 18 |
| [日本語能力試験の公開情報](../catalog/levels/jlpt.md) | link |  |  |  | ○ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 |
| [法令用語日英標準対訳辞書](../catalog/terms/jlt-standard-dict.md) | ingest |  |  |  | ○ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 |

### 1. 入国・在留手続

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [特定技能総合支援サイトと外国人向け特定技能ガイドブック](../catalog/life-info/isa-ssw-support-site.md) | link | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  | ○ |  | ○ |  | ○ | ○ | ○ |  | ○ |  |  | 12 |

### 2. 緊急・災害

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [消防庁 外国人からの119番・救急への対応](../catalog/life-info/fdma-multilingual-119.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  |  |  | fr・it | 16 |
| [災害時に便利なアプリとWEBサイト](../catalog/life-info/bousai-apps-websites.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  |  |  |  | 14 |
| [多言語災害情報文例集・災害時多言語表示シート](../catalog/official-writing/clair-disaster-multilingual.md) | outreach | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  |  |  |  |  | ru・fr | 14 |
| [気象庁 多言語辞書](../catalog/terms/jma-multilingual-dict.md) | ingest |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  |  |  |  | 14 |
| [気象庁 多言語の防災気象情報](../catalog/life-info/jma-multilingual-site.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  |  |  |  | 14 |
| [国土交通省 防災ポータル](../catalog/life-info/mlit-bousai-portal.md) | link |  | ○ | ○ | ○ |  |  |  | ○ | ○ |  |  | ○ | ○ |  |  |  |  |  |  |  | 7 |

### 3. 医療

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [多言語医療問診票](../catalog/life-info/kif-medical-questionnaire.md) | outreach |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ |  |  | ○ | uk・ru・fr・ar・fa・de・lo・hr | 23 |
| [外国語版「予防接種と子どもの健康」と予診票](../catalog/life-info/yoboseshu-rc-foreign.md) | outreach |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  | ○ |  |  |  |  | uk・ru・fr・ar・de・it | 17 |
| [外国人向け多言語説明資料](../catalog/terms/mhlw-multilingual-medical-docs.md) | ingest |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  |  |  |  | hi・uk・ar | 13 |
| [医療情報ネットのオープンデータ](../catalog/life-info/iryo-joho-net-opendata.md) | ingest |  |  |  | ○ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 |

ほかの分野の表にある関連の資料: [消防庁 外国人からの119番・救急への対応](../catalog/life-info/fdma-multilingual-119.md)（緊急・災害）、[母子健康手帳 多言語版と外国人向けのリーフレット](../catalog/life-info/cfa-boshi-techou-multilingual.md)（出産・子育て）、[外国人労働者向け労災保険給付パンフレット](../catalog/life-info/mhlw-rousai-pamphlet.md)（雇用・労働）

### 4. 市区町村での手続

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [外国人住民に係る住民基本台帳制度](../catalog/life-info/soumu-foreign-resident-register.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ |  |  |  |  |  |  |  | 11 |
| [マイナンバーカード総合サイト](../catalog/life-info/jlis-mynumber-card.md) | link |  |  | ○ | ○ |  |  |  | ○ | ○ |  | ○ |  | ○ |  |  |  |  |  |  |  | 6 |
| [マイナンバー制度・マイナンバーカード](../catalog/life-info/digital-mynumber.md) | link |  |  |  | ○ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 |

### 5. 年金・福祉

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [日本年金機構 外国人向けの情報](../catalog/life-info/jps-foreign-residents.md) | ingest | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  | ru | 14 |

### 5. 税金

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [外国人の方の個人住民税について](../catalog/life-info/soumu-inhabitant-tax-foreigners.md) | link |  | ○ | ○ | ○ |  |  |  | ○ |  |  |  |  |  |  |  |  |  |  |  |  | 4 |
| [Information for Taxpayers](../catalog/life-info/nta-english.md) | link |  |  |  | ○ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 |

### 6. 出産・子育て

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [母子健康手帳 多言語版と外国人向けのリーフレット](../catalog/life-info/cfa-boshi-techou-multilingual.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  |  |  |  |  | 10 |

ほかの分野の表にある関連の資料: [外国語版「予防接種と子どもの健康」と予診票](../catalog/life-info/yoboseshu-rc-foreign.md)（医療）

### 6. 教育

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [外国人児童生徒のための就学ガイドブック](../catalog/life-info/mext-shugaku-guidebook.md) | ingest |  | ○ | ○ | ○ | ○ |  |  | ○ | ○ |  | ○ |  |  |  |  |  |  |  |  | uk | 8 |
| [かすたねっと](../catalog/life-info/casta-net.md) | link |  | ○ | ○ | ○ | ○ |  |  | ○ | ○ |  | ○ |  |  |  |  |  |  |  |  |  | 7 |
| [高等学校等就学支援金のリーフレット](../catalog/life-info/mext-koko-shugaku-shienkin.md) | link |  |  |  | ○ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 |

### 7. 雇用・労働

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [雇用管理に役立つ多言語用語集](../catalog/terms/mhlw-tagengo-yougo.md) | ingest | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  |  |  |  | 14 |
| [外国人労働者向けの相談機関](../catalog/life-info/mhlw-foreign-worker-consultation.md) | outreach | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  |  | 13 |
| [外国人労働者向けモデル労働条件通知書](../catalog/life-info/mhlw-model-labor-conditions-notice.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  |  | 13 |
| [外国人労働者向け労災保険給付パンフレット](../catalog/life-info/mhlw-rousai-pamphlet.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ |  |  |  |  |  | fa | 13 |
| [ハローワークの外国語の案内](../catalog/life-info/hellowork-foreign-language.md) | ingest | ○ | ○ | ＊ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |  |  |  |  |  |  | uk | 12 |
| [外国人技能実習機構 技能実習生向けの情報](../catalog/life-info/otit-trainee-support.md) | link | ○ | ○ | ○ | ○ | ○ |  | ○ |  |  | ○ |  | ○ |  | ○ | ○ |  |  |  |  |  | 9 |

ほかの分野の表にある関連の資料: [特定技能総合支援サイトと外国人向け特定技能ガイドブック](../catalog/life-info/isa-ssw-support-site.md)（入国・在留手続）

### 8. 住居

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [外国人の民間賃貸住宅入居円滑化ガイドライン](../catalog/life-info/mlit-chintai-guideline.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  |  | 13 |
| [部屋探しのガイドブック・外国人のための賃貸住宅入居の手引き・原状回復のポイント](../catalog/life-info/mlit-heya-sagashi.md) | link | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  |  | 13 |
| [UR 賃貸住宅の外国語の案内](../catalog/life-info/ur-nonjapanese.md) | link |  | ○ | ○ | ○ |  |  |  | ○ | ○ |  |  |  | ○ |  |  |  |  |  |  |  | 6 |

### 9. 交通

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [警察庁 外国人向けの交通ルールと運転免許の案内](../catalog/life-info/npa-traffic-foreign.md) | link |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ |  | hi・uk・ru・ar・fa | 21 |
| [自賠責保険・共済ポータルサイト](../catalog/life-info/mlit-jibaiseki-portal.md) | link |  | ○ | ○ | ○ |  |  |  | ○ | ○ |  |  |  | ○ |  |  |  |  |  |  |  | 6 |

### 9. 日常生活のルール・習慣

| 資料 | 扱い | ja-easy | vi | zh-Hans | en | tl | ne | id | pt | ko | my | es | th | zh-Hant | km | mn | si | bn | ur | ta | その他 | 外国語 |
| ---- | ---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | ---- | --: |
| [日本でくらすための銀行口座や送金のつかい方](../catalog/life-info/fsa-bank-account-guide.md) | link | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  |  |  |  | tr・uk | 15 |

## 言語ごとの数

表の37件のうち、その言語がある資料の数。3件以下のときは資料も挙げた。

| 群 | 言語 | 資料の数 |
| -- | ---- | -------- |
| — | やさしい日本語（ja-easy） | 10 |
| 第1群 | ベトナム語（vi） | 30 |
| 第1群 | 中国語（簡体字）（zh-Hans） | 30 |
| 第1群 | 英語（en） | 37 |
| 第1群 | フィリピノ語（tl） | 26 |
| 第1群 | ネパール語（ne） | 23 |
| 第1群 | インドネシア語（id） | 24 |
| 第1群 | ポルトガル語（pt） | 29 |
| 第1群 | 韓国語（ko） | 28 |
| 第1群 | ミャンマー語（my） | 20 |
| 第2群 | スペイン語（es） | 25 |
| 第2群 | タイ語（th） | 25 |
| 第2群 | 中国語（繁体字）（zh-Hant） | 13 |
| 第2群 | クメール語（km） | 18 |
| 第2群 | モンゴル語（mn） | 18 |
| 第3群 | シンハラ語（si） | 4 |
| 第3群 | ベンガル語（bn） | 1（[つながるひろがる　にほんごでのくらし](../catalog/levels/tsunahiro.md)） |
| 第3群 | ウルドゥー語（ur） | 2（[特定技能総合支援サイトと外国人向け特定技能ガイドブック](../catalog/life-info/isa-ssw-support-site.md)、[警察庁 外国人向けの交通ルールと運転免許の案内](../catalog/life-info/npa-traffic-foreign.md)） |
| 第3群 | タミル語（ta） | 1（[多言語医療問診票](../catalog/life-info/kif-medical-questionnaire.md)） |
| — | 中国語（字体の区別なし）（zh）＊ | 1（[ハローワークの外国語の案内](../catalog/life-info/hellowork-foreign-language.md)） |
| その他 | ウクライナ語（uk） | 9 |
| その他 | ロシア語（ru） | 7 |
| その他 | フランス語（fr） | 6 |
| その他 | アラビア語（ar） | 4 |
| その他 | ヒンディー語（hi） | 3（[生活・就労ガイドブック](../catalog/life-info/life-work-guidebook.md)、[警察庁 外国人向けの交通ルールと運転免許の案内](../catalog/life-info/npa-traffic-foreign.md)、[外国人向け多言語説明資料](../catalog/terms/mhlw-multilingual-medical-docs.md)） |
| その他 | ペルシア語（fa） | 3（[多言語医療問診票](../catalog/life-info/kif-medical-questionnaire.md)、[外国人労働者向け労災保険給付パンフレット](../catalog/life-info/mhlw-rousai-pamphlet.md)、[警察庁 外国人向けの交通ルールと運転免許の案内](../catalog/life-info/npa-traffic-foreign.md)） |
| その他 | トルコ語（tr） | 2（[日本でくらすための銀行口座や送金のつかい方](../catalog/life-info/fsa-bank-account-guide.md)、[生活・就労ガイドブック](../catalog/life-info/life-work-guidebook.md)） |
| その他 | ドイツ語（de） | 2（[多言語医療問診票](../catalog/life-info/kif-medical-questionnaire.md)、[外国語版「予防接種と子どもの健康」と予診票](../catalog/life-info/yoboseshu-rc-foreign.md)） |
| その他 | イタリア語（it） | 2（[消防庁 外国人からの119番・救急への対応](../catalog/life-info/fdma-multilingual-119.md)、[外国語版「予防接種と子どもの健康」と予診票](../catalog/life-info/yoboseshu-rc-foreign.md)） |
| その他 | ラオ語（lo） | 1（[多言語医療問診票](../catalog/life-info/kif-medical-questionnaire.md)） |
| その他 | クロアチア語（hr） | 1（[多言語医療問診票](../catalog/life-info/kif-medical-questionnaire.md)） |

## 第1群の言語が欠けている資料

第1群の9言語のうち、無いものがある資料（分野の順）。＊の中国語は、あるものとして数えた。

- [特定技能総合支援サイトと外国人向け特定技能ガイドブック](../catalog/life-info/isa-ssw-support-site.md)（入国・在留手続）: ポルトガル語、韓国語
- [国土交通省 防災ポータル](../catalog/life-info/mlit-bousai-portal.md)（緊急・災害）: フィリピノ語、ネパール語、インドネシア語、ミャンマー語
- [外国語版「予防接種と子どもの健康」と予診票](../catalog/life-info/yoboseshu-rc-foreign.md)（医療）: ミャンマー語
- [外国人向け多言語説明資料](../catalog/terms/mhlw-multilingual-medical-docs.md)（医療）: ミャンマー語
- [外国人住民に係る住民基本台帳制度](../catalog/life-info/soumu-foreign-resident-register.md)（市区町村での手続）: ミャンマー語
- [マイナンバーカード総合サイト](../catalog/life-info/jlis-mynumber-card.md)（市区町村での手続）: ベトナム語、フィリピノ語、ネパール語、インドネシア語、ミャンマー語
- [外国人の方の個人住民税について](../catalog/life-info/soumu-inhabitant-tax-foreigners.md)（税金）: フィリピノ語、ネパール語、インドネシア語、韓国語、ミャンマー語
- [母子健康手帳 多言語版と外国人向けのリーフレット](../catalog/life-info/cfa-boshi-techou-multilingual.md)（出産・子育て）: ミャンマー語
- [外国人児童生徒のための就学ガイドブック](../catalog/life-info/mext-shugaku-guidebook.md)（教育）: ネパール語、インドネシア語、ミャンマー語
- [かすたねっと](../catalog/life-info/casta-net.md)（教育）: ネパール語、インドネシア語、ミャンマー語
- [外国人技能実習機構 技能実習生向けの情報](../catalog/life-info/otit-trainee-support.md)（雇用・労働）: ネパール語、ポルトガル語、韓国語
- [UR 賃貸住宅の外国語の案内](../catalog/life-info/ur-nonjapanese.md)（住居）: フィリピノ語、ネパール語、インドネシア語、ミャンマー語
- [自賠責保険・共済ポータルサイト](../catalog/life-info/mlit-jibaiseki-portal.md)（交通）: フィリピノ語、ネパール語、インドネシア語、ミャンマー語
- 外国語が英語だけ: [日本語能力試験の公開情報](../catalog/levels/jlpt.md)（全般）、[法令用語日英標準対訳辞書](../catalog/terms/jlt-standard-dict.md)（全般）、[医療情報ネットのオープンデータ](../catalog/life-info/iryo-joho-net-opendata.md)（医療）、[マイナンバー制度・マイナンバーカード](../catalog/life-info/digital-mynumber.md)（市区町村での手続）、[Information for Taxpayers](../catalog/life-info/nta-english.md)（税金）、[高等学校等就学支援金のリーフレット](../catalog/life-info/mext-koko-shugaku-shienkin.md)（教育）

## 注記

- [ハローワークの外国語の案内](../catalog/life-info/hellowork-foreign-language.md): 前付けの `languages` は、案内している外国語の対応（通訳・電話）の言語。

## 外国語の版が無い資料

生活情報・用語・公用文・レベルの分類で、前付けの `languages` が日本語・やさしい日本語だけのもの。外国人に向けた資料とは限らない（自治体・医療機関・日本語教育の関係者に向けたものや、公用文の決まりを含む）。

- [法令における漢字使用等について](../catalog/official-writing/clb-horei-kanji.md)（全般）
- [公用文作成の考え方](../catalog/official-writing/kobun-sakusei.md)（全般）
- [外国人生活支援ポータルサイト](../catalog/life-info/life-support-portal.md)（全般）
- [日本語教育の参照枠](../catalog/levels/nihongo-sanshowaku.md)（全般）
- [「生活者としての外国人」に対する日本語教育の標準的なカリキュラム案](../catalog/levels/seikatsusha-curriculum.md)（全般）
- [避難情報に関するガイドライン](../catalog/official-writing/hinan-joho-guideline.md)（緊急・災害）
- [外国人患者の受入れのための医療機関向けマニュアル](../catalog/life-info/mhlw-foreign-patient-manual.md)（医療）
- [地方公共団体の一元的相談窓口の現況と一覧](../catalog/life-info/isa-ichigen-soudan.md)（市区町村での手続）
- [国際結婚、海外での出生等に関する戸籍Ｑ＆Ａ](../catalog/life-info/moj-koseki-international-qa.md)（市区町村での手続）
- [年金用語集](../catalog/terms/jps-nenkin-yougo.md)（年金・福祉）
- [セーフティネット住宅情報提供システム](../catalog/life-info/safetynet-jutaku.md)（住居）
