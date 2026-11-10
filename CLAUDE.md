# yasashii-refs（エージェント向けの決まり）

外国人住民・日本語学習者のためのアプリを作るときに参照する資料の目録。概要は [README.md](README.md)。

## 目的

- いま重視しているのは**開発の参考**（何があるか・正式な出典はどれか・使ってよい条件・何が足りないか）。アプリが実行時に引くデータは将来の使い道。
- 網羅を目指さない。公的で、更新されていて、使ってよい条件がはっきりした資料を優先する。
- 載せるかどうかは、オープンなデータベースや文書として参照できるかで決める。国が勧めているかどうかは決め手にしない。民間の事業者のアプリやサービス（有料の API など）は、国が監修・推奨していても扱わない。

## 資料を目録に足す手順

1. **正式な配布元を探す。** 公的機関の公式ページ（PDF の直リンクではなく、配布ページ）を `url` にする。転載サイトやまとめサイトは出典にしない。
2. **規約を読む。** サイトの利用規約（「著作権について」「コンテンツの利用について」など）と、資料自体のライセンス表記の両方。
   - 根拠の URL を `license_url` に書き、本文に該当箇所を短く引用する。
   - 確かめた日を `checked` に書く。確かめていない項目は「未確認」と書き、推測で埋めない。
3. **扱いを決める**（`ingest` / `link` / `outreach` / `exclude`。意味は README）。
   - 商用で使えない（NC など）ものは `ingest` にしない。
   - 規約が分からないものは `link` にする。
4. **目録のファイルを作る。** `catalog/<分類>/<id>.md`。前付けの形式は下。本文には次を書く。
   - 何が入っているか
   - 開発の参考としての使い方
   - アプリの資源としての使い方（あれば）
   - 注意（版・誤り・偏り・足りないところ）
   - 閲覧用サイトに出す文（`summary`・`summary_en`・`name_en`・`publisher_en`、必要なら `license_en`）も前付けに書く。読む人は開発者だけでなく支援団体の担当者なので、専門の言葉を避けて書く。英語の名前は、提供元の英語名があればそれに合わせ、無ければ意味の分かる訳にする。
5. **一覧を更新する。** `catalog/README.md` の表に1行足す（同じ分類の中の並びは、閲覧用サイトの並びにもなる）。`python3 scripts/language_table.py` で、言語の対応表（`docs/language-coverage.md`）を作り直す。
6. **優先順位や足りないところに関わるなら、`docs/priorities.md` も更新する。**

## 目録の前付け（YAML）

```yaml
---
id: jlt-standard-dict              # ファイル名と同じ。英小文字とハイフン
name: 法令用語日英標準対訳辞書
name_en: Standard Japanese-English Dictionary of Legal Terms  # 閲覧用サイトの英語のページに出す名前
publisher: 法務省（日本法令外国語訳データベースシステム）
publisher_en: Ministry of Justice (Japanese Law Translation database)
summary: 法令の翻訳で使う用語の、日本語と英語の標準の対訳。  # 一言の説明（80字以内、「。」で終わる）。閲覧用サイトに出す
summary_en: Standard English equivalents for the terms used when translating Japanese laws.  # 200字以内
url: https://...                   # 正式な配布ページ
category: terms                    # catalog/ の下のフォルダ名
domains: [全般, 入国・在留手続, 市区町村での手続]  # docs/priorities.md の分野（ガイドブックの章）。分野を問わないものは [全般]
languages: [ja, en]                # ISO 639-1。中国語は字体を確かめて zh-Hans / zh-Hant（話し言葉の対応など、区別が無いときだけ zh）。やさしい日本語は ja-easy。新しい言語は scripts/check_catalog.py の LANGUAGES に足す
formats: [PDF, CSV, XML]
version: "19.0"                    # 分からなければ "未確認"
license: PDL-1.0                   # SPDX 風の短い名前。分からなければ 未確認
license_en: ...                    # license に説明を付けたとき（PDL-1.0・CC-BY-SA-4.0・告示（著作権の対象外）・未確認 のどれでもないとき）だけ。英語の利用条件
license_url: https://...
commercial: yes                    # yes / no / 未確認
redistribution: yes                # yes / no / 未確認（出典を書けば再配布できるか）
attribution: 出典：...             # 出典の書き方（規約に例があればそれに合わせる）
handling: ingest                   # ingest / link / outreach / exclude
uses: [reference, resource]        # reference: 開発の参考 / resource: アプリの資源
checked: 2026-11-03
---
```

## データを取り込むとき（`data/`、`scripts/`）

- 配布元から取得して変換するスクリプトを `scripts/` に置き、だれが実行しても同じ結果になるようにする（手作業で直したデータを置かない）。
- 形式は JSONL（1行1項目）。各項目に `source`（目録の id）と `version` を付ける。出典の書き方・取得元・件数・元ファイルのハッシュは `data/<id>.meta.json` に書く（`scripts/common.py` の `write_dataset`）。
- テストを `tests/` に足す（件数・形式・見本の値）。`python3 -m unittest discover -s tests` と `python3 scripts/check_catalog.py` が通ること。
- 取得するときは「yasashii-refs」と名乗り、ブラウザに偽装しない（`scripts/common.py` の `USER_AGENT`）。
- 元の資料のライセンスが継承（SA）を求めるものは、そのデータのファイルに同じライセンスを明記する。
- 元のファイル（PDF など）は、大きいものや再配布できないものはリポジトリに入れない（取得のスクリプトだけ置く）。

## 閲覧用サイト（`site/`）

- 目録から作る、読むだけの静的サイト（日本語 `/` と英語 `/en/`）。`python3 scripts/build_site.py` が `site/src/` と目録の前付けから `site/dist/`（git 管理外）に作る。
- Cloudflare Pages（アカウント `ni-hongo`、プロジェクト `yasashii-refs`）が、`main` への push のたびに作り直す（ビルドコマンド `python3 scripts/build_site.py`、出力先 `site/dist`）。手で上げない。
- 資料のデータは置かない。名前・提供元・一言の説明・元のページへのリンク・利用条件だけを載せ、元へ案内する。
- 一般公開のサイトなので、GitHub（このリポジトリ・Issue・LICENSE）へのリンクも、GitHub という言葉も載せない（`tests/test_site.py` で確かめる）。資料そのものの利用規約が GitHub にあるもの（デザイントークン・Furifont）は、元への案内なので載せてよい。
- 連絡先のメールアドレスは、ボットに拾われないよう「@」を置き換えた形（`contact（アットマーク）…`）で載せる。mailto のリンクにせず、そのままの形のアドレスはリポジトリにもサイトにも書かない（`scripts/build_site.py` の `CONTACT_USER`・`CONTACT_DOMAIN`。テストで確かめる）。
- 見た目は、デジタル庁デザインシステムのデザイントークン（`site/src/dads-tokens.css`。パッケージのファイルを変えずに写したもの。MIT の表示を消さない）だけを使う。`site/src/style.css` に色を直接書かない（`tests/test_site.py` で確かめる）。
- 共有の画像（`site/src/og.png`）は `site/src/og.html` から作る（作り方はファイルの頭に書いてある）。

## 入手のしかた

- 配布元が用意した入手方法に従う。閲覧のみで公開されているもの（ダウンロードを止めてあるシートなど）を、ブラウザの自動操作などで抜き出さない。
- 利用の申請（名前・所属などの個人情報の入力）は、作り手が自分で行う。エージェントは代わりに入力しない。
- 再配布できない資料を入手したときは、リポジトリに入れない。git 管理外の `local/` に置き、目録には入手方法と規約だけを書く。
- 申請で得たダウンロード先・ID・パスワードなどは、目録にもコードにも書かない。申請した人の名前・所属などの個人の情報も書かない。

## リンクと版を確かめるとき

- `python3 scripts/check_links.py` で目録の URL を確かめる（数分かかる）。前回からの変化は、出力と `catalog/link-state.json` の差分に出る。
- 変わったものは、目録の「注意」・`version`・`checked` を直す（取り込んだ資料の新しい版なら、取り込みのスクリプトも回し直す）。リンク切れは移った先を探して直し、見つからなければ「注意」に書く。直したら記録と一緒にコミットする。
- ボット対策で止まるサイトに、自動の取得を重ねない（中身はブラウザで確かめる）。

## 書き方

- 日本語で、短く書く。数値には調査名・時点・出典の URL を付ける。
- 扱わないと決めたものは、`catalog/README.md` の「扱わないもの」に理由と一緒に書く（同じ提案を繰り返さないため）。
