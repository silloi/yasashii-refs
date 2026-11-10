---
id: iryo-joho-net-opendata
name: 医療情報ネット（ナビイ）のオープンデータ
name_en: Medical Information Net (Navii) open data
publisher: 厚生労働省
publisher_en: Ministry of Health, Labour and Welfare (MHLW)
summary: 全国の病院・診療所・薬局などの情報を、CSV で配っているオープンデータ。
summary_en: Open data (CSV) on hospitals, clinics, pharmacies and other medical facilities across Japan.
url: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/newpage_43373.html
category: life-info
domains: [医療]
languages: [ja, en]
formats: [CSV]
version: 2026年6月1日時点（2024年8月1日時点の版から、何度か公表されている）
license: PDL-1.0
license_url: https://www.mhlw.go.jp/chosakuken/index.html
commercial: yes
redistribution: yes
attribution: 出典：厚生労働省「医療情報ネットのオープンデータ」（https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/newpage_43373.html）を加工して作成
handling: ingest
uses: [reference, resource]
checked: 2026-11-03
---

# 医療情報ネットのオープンデータ

全国の病院・診療所・歯科診療所・助産所・薬局の情報（医療機能情報提供制度で都道府県に報告されたもの）の一部を、CSV で配っているもの。

## 何が入っているか

- 8つのファイル（ZIP に入った CSV。病院の施設票は BOM 付きの UTF-8）:
  - 病院（施設票、診療科・診療時間票）
  - 診療所（施設票、診療科・診療時間票）
  - 歯科診療所（施設票、診療科・診療時間票）
  - 助産所
  - 薬局
- 病院の施設票（2026年6月1日時点）は7,715件、65列。
  - 正式名称とフリガナ、略称、英語表記（ローマ字表記）
  - 都道府県・市区町村のコード、所在地、緯度・経度
  - 案内用のホームページ
  - 休診日（曜日・週・祝日など）、病床数
- 2025年12月1日時点などの前の版も、同じページと e-Gov データポータル（https://data.e-gov.go.jp/data/dataset/iryou_teikyouseido_mhlw ）にある。
- 同じ制度のページに「用語解説（医療機関）」（令和7年12月版）がある。医療機関の情報に使う用語を、分かりやすく説明したもの。

## 開発の参考として

- 医療機関の名前・場所・診療科・診療時間を、公的なデータで引ける。病院の英語表記（ローマ字表記）があるので、多言語の画面でも名前を出せる。
- **外国語で受診できるかの項目は無い。** 医療情報ネットのサイトでは外国語で受診できる医療機関を探せるが、オープンデータには入っていない（2026年6月1日時点の病院の施設票で確認）。

## アプリの資源として（将来）

- 病院の施設票と診療科の名前を取り込んだ（`data/iryo-joho-net-opendata.jsonl`、7,715病院、2026年6月1日時点）。診療時間と、診療所・歯科診療所・助産所・薬局は、大きいので入れていない（使うときに地域を絞って配布元から取る）。
- 座標が 0 の病院（268）と、英語表記の無い病院（164）がある。

## 注意

- 利用規約: ページに「本データは、利用規約の条件の下、自由にご利用いただけます」とあり、厚生労働省のサイトの利用規約（PDL1.0 に準拠）に従う。データを使ったら、利用者アンケートへの協力が求められている。
- 医療機関から都道府県への報告をもとにしたデータなので、最新でない情報が含まれることがある。
