#!/usr/bin/env python3
"""目録（catalog/）から、閲覧用の静的サイトを作る。日本語（/）と英語（/en/）の2ページ。

- 読むだけのサイト。資料のデータは置かない。資料ごとに、名前・出している団体・一言の説明・元のページへのリンク・
  利用条件（ライセンス・商用利用・再配布・確認日）を載せ、元のページへ案内する。
- 分類で絞り込み、キーワードで検索できる（site/src/app.js。JavaScript が無くても一覧は読める）。
- 見た目は、デジタル庁デザインシステムのデザイントークン（site/src/dads-tokens.css）を使う（site/src/style.css）。
- 文面は目録の前付けから作る（summary・summary_en・name_en・publisher_en・license_en。scripts/check_catalog.py で必須）。
  前付けに無い値（分類・言語・分野・形式の名前）は、この中の表で日本語と英語にする。表に無い値があれば止まる。
- Cloudflare Pages が main への push ごとに実行する（ビルドコマンド `python3 scripts/build_site.py`、出力先 `site/dist`）。
- 一般公開のサイトなので、GitHub（このリポジトリ・Issue・LICENSE）へのリンクは付けない。
- 連絡先のメールアドレスは、ボットに拾われないよう、@ を置き換えた形で載せる（mailto にしない）。
  そのままの形は、このファイルにもサイトにも書かない（CONTACT_USER と CONTACT_DOMAIN に分けて持つ）。
- 標準ライブラリだけで動く。

使い方: python3 scripts/build_site.py [出力先]（既定は site/dist。中身は作り直す）
環境変数 SITE_URL: サイトの URL（canonical・OGP・サイトマップに使う。既定は DEFAULT_SITE_URL）
"""

from __future__ import annotations

import datetime
import html
import json
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_catalog import LANGUAGES, parse_front_matter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
SRC = ROOT / "site" / "src"
DIST = ROOT / "site" / "dist"
DEFAULT_SITE_URL = "https://yasashii-refs.pages.dev"
# 連絡先（資料の権利者からの知らせなど）。サイトには「@」を置き換えた形（CONTACT_JA・CONTACT_EN）で出す
CONTACT_USER = "contact"
CONTACT_DOMAIN = "12taio.jp"
CONTACT_JA = f"{CONTACT_USER}（アットマーク）{CONTACT_DOMAIN}"
CONTACT_EN = f"{CONTACT_USER} [at] {CONTACT_DOMAIN}"
ASSETS = ["dads-tokens.css", "style.css", "app.js"]  # site/src から /assets/ に写す
ROOT_FILES = ["favicon.svg", "og.png"]  # site/src からサイトの直下に写す（あるものだけ）

# 分類（catalog/ のフォルダ）: 日本語・英語の名前。並びは画面での順番
CATEGORIES = {
    "life-info": ("多言語の生活情報", "Multilingual living information"),
    "plain-japanese": ("やさしい日本語", "Easy Japanese"),
    "terms": ("行政用語・用語集", "Administrative terms and glossaries"),
    "official-writing": ("公用文", "Official writing"),
    "levels": ("日本語のレベル", "Japanese proficiency levels"),
    "kanji": ("漢字", "Kanji"),
    "vocabulary": ("語彙・辞書", "Vocabulary and dictionaries"),
    "statistics": ("統計", "Statistics"),
    "tools": ("道具", "Tools"),
}
LANGUAGES_EN = {
    "ja": "Japanese", "ja-easy": "Easy Japanese", "vi": "Vietnamese", "zh-Hans": "Chinese (Simplified)",
    "en": "English", "tl": "Filipino", "ne": "Nepali", "id": "Indonesian", "pt": "Portuguese", "ko": "Korean",
    "my": "Burmese", "es": "Spanish", "th": "Thai", "zh-Hant": "Chinese (Traditional)", "km": "Khmer",
    "mn": "Mongolian", "si": "Sinhala", "bn": "Bengali", "ur": "Urdu", "ta": "Tamil", "zh": "Chinese",
    "hi": "Hindi", "tr": "Turkish", "uk": "Ukrainian", "ru": "Russian", "fr": "French", "ar": "Arabic",
    "fa": "Persian", "de": "German", "it": "Italian", "lo": "Lao", "hr": "Croatian",
}
DOMAINS_EN = {
    "全般": "General", "入国・在留手続": "Immigration and residence", "市区町村での手続": "Municipal procedures",
    "雇用・労働": "Employment and labor", "出産・子育て": "Pregnancy and childcare", "教育": "Education",
    "医療": "Medical care", "年金・福祉": "Pensions and welfare", "税金": "Taxes", "交通": "Transportation",
    "緊急・災害": "Emergencies and disasters", "住居": "Housing", "日常生活のルール・習慣": "Everyday rules and customs",
}
FORMATS_EN = {
    "動画": "Video", "npm パッケージ": "npm package", "ブックマークレット": "Bookmarklet", "フォント": "Font",
    "アプリ": "App", "Web 検索": "Web search", "Google スプレッドシート（閲覧のみ）": "Google Sheets (view only)",
}
# 説明の付いていない license の値の、日本語・英語の書き方
LICENSE_LABELS = {
    "PDL-1.0": ("公共データ利用規約（PDL1.0）", "Public Data License 1.0 (PDL 1.0)"),
    "CC-BY-SA-4.0": ("CC BY-SA 4.0", "CC BY-SA 4.0"),
    "告示（著作権の対象外）": ("告示（著作権の対象外）", "Public notice (not subject to copyright)"),
    "未確認": ("未確認", "Not yet confirmed"),
}
FLAGS = {  # commercial・redistribution の値: (日本語, 英語, CSS の印)
    "yes": ("可", "Allowed", "yes"),
    "no": ("不可", "Not allowed", "no"),
    "未確認": ("未確認", "Unconfirmed", "unknown"),
}

TEXT = {
    "ja": {
        "html_lang": "ja",
        "path": "/",
        "title": "yasashii-refs｜外国人住民・日本語学習者のための資料の目録",
        "description": "やさしい日本語、行政の用語、多言語の生活情報、漢字や語彙のレベルなど、外国人住民や日本語学習者のための"
                       "アプリ・サービスを作るときに参照できる公的な資料の目録。出している団体と、使ってよい条件を載せています。",
        "skip": "資料の一覧へ移動",
        "switch_label": "English",
        "switch_lang": "en",
        "switch_path": "/en/",
        "h1": "外国人住民・日本語学習者のための資料の目録",
        "lead": "やさしい日本語、行政の用語、多言語の生活情報、漢字や語彙のレベルなど、外国人住民や日本語学習者のためのアプリや"
                "サービスを作るときに参照できる公的な資料を、{count}件集めました。資料ごとに、出している団体と、使ってよい条件を"
                "載せています。",
        "purpose_h": "何のための目録か",
        "purpose": [
            "外国人住民や日本語学習者に向けたアプリを作る人や、支援団体の担当者が、「どんな公的な資料があるか」"
            "「どれが正式な出典か」「どんな条件で使えるか」を一度に確かめるための目録です。",
            "公的で、更新されていて、使ってよい条件がはっきりした資料を優先して載せています。網羅はめざしていません。",
            "このサイトは資料そのものを置かず、元のページへ案内します。使う前に、元のページと利用規約を確かめてください。",
        ],
        "license_h": "ライセンスの範囲",
        "license": [
            "この目録の説明文とプログラムは、MIT ライセンスで公開しています。自由に使い、直し、配ることができます。",
            "載せている資料そのものには、MIT は当てはまりません。それぞれの資料の利用条件（提供元の利用規約）に従ってください。",
        ],
        "notes_summary": "利用条件の見方と注意",
        "notes": [
            "<strong>利用条件</strong>は、提供元の利用規約の要点です。「公共データ利用規約（PDL1.0）」は国の多くのサイトが使う"
            "規約で、出典を書けば商用を含めて使えます（ロゴや第三者の権利があるものなどは除く）。",
            "<strong>商用利用・再配布</strong>は、利用規約を読んだうえでの目録の判断です。再配布の「可」は、出典を書けば配り直せる"
            "という意味です。「未確認」は、規約に書かれていないか、まだ確かめていないものです。",
            "<strong>確認日</strong>に、元のページと利用規約を確かめました。その後に変わっていることがあります。",
            "個人がまとめた目録で、公的機関の公式の資料ではありません。資料の権利者の方で、掲載に問題があれば、"
            "<span class=\"contact\">{contact}</span> までお知らせください（「（アットマーク）」を「@」に変えて送ってください）。",
        ],
        "finder_h": "資料を探す",
        "search_label": "キーワードで探す",
        "search_hint": "名前・団体・説明・言語・分野から探します。例: 年金、医療、ベトナム語、PDL",
        "categories_legend": "分類で絞り込む",
        "all": "すべて",
        "count": "{shown}件を表示（全{total}件）",
        "empty": "見つかりませんでした。キーワードを短くするか、分類を「すべて」にしてください。",
        "domains": "分野",
        "languages": "言語",
        "formats": "形式",
        "license_term": "利用条件",
        "commercial": "商用利用",
        "redistribution": "再配布",
        "checked": "確認日",
        "open": "元のページを開く",
        "terms": "利用規約",
        "sep": "、",  # 分野の名前に「・」があるので、並べるときは「、」で区切る
        "footer": [
            "yasashii-refs は、個人がまとめた目録です。公的機関の公式の資料ではありません。",
            "連絡先: <span class=\"contact\">{contact}</span>（「（アットマーク）」を「@」に変えて送ってください）",
            "配色と文字の設定に、<a href=\"https://design.digital.go.jp/\">デジタル庁デザインシステム</a>のデザイントークン"
            "（MIT License、© 2023 デジタル庁）を使っています。",
        ],
        "updated": "最終更新",
        "not_found_title": "ページが見つかりません｜yasashii-refs",
        "not_found": "ページが見つかりません。",
        "back": "目録のトップへ",
    },
    "en": {
        "html_lang": "en",
        "path": "/en/",
        "title": "yasashii-refs | Catalog of public resources for foreign residents and Japanese learners",
        "description": "A catalog of public resources, such as Easy Japanese, administrative terms, multilingual living "
                       "information and kanji and vocabulary levels, for people building apps and services for foreign "
                       "residents and learners of Japanese in Japan. Each entry lists the publisher and the terms of use.",
        "skip": "Skip to the list of resources",
        "switch_label": "日本語",
        "switch_lang": "ja",
        "switch_path": "/",
        "h1": "Catalog of public resources for foreign residents and Japanese learners",
        "lead": "{count} public resources you can refer to when building apps and services for foreign residents and "
                "learners of Japanese in Japan, such as Easy Japanese, administrative terms, multilingual living "
                "information and kanji and vocabulary levels. Each entry shows who publishes it and the terms of use.",
        "purpose_h": "What this catalog is for",
        "purpose": [
            "It helps app developers and staff of support organizations check, in one place, which public resources "
            "exist, which source is the official one, and on what terms each can be used.",
            "It favors resources that are public, kept up to date and clear about their terms of use. It does not try "
            "to list everything.",
            "This site does not host the resources themselves; it points you to the original pages. Check the original "
            "page and its terms before using a resource.",
        ],
        "license_h": "What the MIT License covers",
        "license": [
            "The descriptions and programs of this catalog are published under the MIT License. You may use, modify "
            "and share them freely.",
            "The MIT License does not cover the listed resources themselves. Follow each resource's terms of use set "
            "by its publisher.",
        ],
        "notes_summary": "How to read the terms, and notes",
        "notes": [
            "<strong>Terms of use</strong> summarize the publisher's terms. The Public Data License 1.0 (PDL 1.0) is "
            "used by many Japanese government websites and allows use, including commercial use, with attribution "
            "(except for logos, third-party rights and the like).",
            "<strong>Commercial use and redistribution</strong> are this catalog's reading of the terms. "
            "Redistribution marked Allowed means it may be shared again with attribution. Unconfirmed means the "
            "terms do not say, or we have not confirmed it yet.",
            "We checked the original page and its terms on the <strong>Checked</strong> date. They may have changed "
            "since.",
            "English titles and descriptions are our translations for reference; the Japanese titles are the "
            "original ones.",
            "This catalog is compiled by an individual and is not an official publication of any public body. If you "
            "hold rights to a listed resource and see a problem, please email <span class=\"contact\">{contact}</span> "
            "(replace [at] with @).",
        ],
        "finder_h": "Find resources",
        "search_label": "Search by keyword",
        "search_hint": "Searches names, publishers, descriptions, languages and topics. "
                       "Examples: pension, medical, Vietnamese, PDL",
        "categories_legend": "Filter by category",
        "all": "All",
        "count": "Showing {shown} of {total}",
        "empty": "Nothing found. Try a shorter keyword or choose All categories.",
        "domains": "Topics",
        "languages": "Languages",
        "formats": "Formats",
        "license_term": "Terms of use",
        "commercial": "Commercial use",
        "redistribution": "Redistribution",
        "checked": "Checked",
        "open": "Open the original page",
        "terms": "Terms of use",
        "sep": ", ",
        "footer": [
            "yasashii-refs is a catalog compiled by an individual. It is not an official publication of any public "
            "body.",
            "Contact: <span class=\"contact\">{contact}</span> (replace [at] with @)",
            "Colors and typography use the design tokens of the <a href=\"https://design.digital.go.jp/\">Digital "
            "Agency Design System</a> (MIT License, © 2023 Digital Agency, Japan).",
        ],
        "updated": "Last updated",
        "not_found_title": "Page not found | yasashii-refs",
        "not_found": "Page not found.",
        "back": "Back to the catalog",
    },
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def norm(text: str) -> str:
    """検索に使う形（NFKC・小文字）。app.js も同じようにそろえる"""
    return unicodedata.normalize("NFKC", text).lower()


def readme_order() -> dict[str, int]:
    """catalog/README.md の一覧の表に出てくる id の順番（同じ分類の中は、この順に並べる）"""
    index = (CATALOG / "README.md").read_text(encoding="utf-8")
    ids = re.findall(r"\[([a-z0-9-]+)\]\([a-z-]+/[a-z0-9-]+\.md\)", index)
    return {entry_id: i for i, entry_id in reversed(list(enumerate(ids)))}


def load_entries() -> list[dict]:
    """目録の全件。分類の順番、同じ分類の中は catalog/README.md の一覧の順"""
    entries = []
    for path in sorted(CATALOG.glob("*/*.md")):
        fm = parse_front_matter(path.read_text(encoding="utf-8"))
        if fm is None:
            raise SystemExit(f"{path}: 前付けが無い")
        for key in ("summary", "summary_en", "name_en", "publisher_en"):
            if not fm.get(key):
                raise SystemExit(f"{path}: {key} が無い（scripts/check_catalog.py で確かめる）")
        if fm["category"] not in CATEGORIES:
            raise SystemExit(f"{path}: 分類 {fm['category']} の名前が CATEGORIES に無い")
        for lang in fm["languages"]:
            if lang not in LANGUAGES_EN:
                raise SystemExit(f"{path}: 言語 {lang} の英語の名前が LANGUAGES_EN に無い")
        for domain in fm["domains"]:
            if domain not in DOMAINS_EN:
                raise SystemExit(f"{path}: 分野 {domain} の英語の名前が DOMAINS_EN に無い")
        for fmt in fm["formats"]:
            if not fmt.isascii() and fmt not in FORMATS_EN:
                raise SystemExit(f"{path}: 形式 {fmt} の英語の名前が FORMATS_EN に無い")
        if fm["license"] not in LICENSE_LABELS and not fm.get("license_en"):
            raise SystemExit(f"{path}: license_en が無い")
        entries.append(fm)
    order, listed = list(CATEGORIES), readme_order()
    entries.sort(key=lambda e: (order.index(e["category"]), listed.get(e["id"], len(listed)), e["id"]))
    return entries


def license_label(entry: dict, lang: str) -> str:
    if entry["license"] in LICENSE_LABELS:
        return LICENSE_LABELS[entry["license"]][0 if lang == "ja" else 1]
    return entry["license"] if lang == "ja" else entry["license_en"]


def search_text(entry: dict) -> str:
    """どちらの言語のページでも、日本語と英語の両方で引けるようにする"""
    parts = [
        entry["id"], entry["name"], entry["name_en"], entry["publisher"], entry["publisher_en"],
        entry["summary"], entry["summary_en"], *CATEGORIES[entry["category"]],
        entry["license"], entry.get("license_en", ""), *LICENSE_LABELS.get(entry["license"], ()),
    ]
    for lang in entry["languages"]:
        parts += [lang, LANGUAGES[lang], LANGUAGES_EN[lang]]
    for domain in entry["domains"]:
        parts += [domain, DOMAINS_EN[domain]]
    for fmt in entry["formats"]:
        parts += [fmt, FORMATS_EN.get(fmt, "")]
    return norm(" ".join(p for p in parts if p))


def render_card(entry: dict, lang: str) -> str:
    t = TEXT[lang]
    ja = lang == "ja"
    name = entry["name"] if ja else entry["name_en"]
    langs = t["sep"].join(LANGUAGES[c] if ja else LANGUAGES_EN[c] for c in entry["languages"])
    domains = t["sep"].join(d if ja else DOMAINS_EN[d] for d in entry["domains"])
    formats = t["sep"].join(f if ja else FORMATS_EN.get(f, f) for f in entry["formats"])

    def flag(key: str) -> str:
        label_ja, label_en, css = FLAGS[entry[key]]
        return f'<span class="flag flag-{css}">{esc(label_ja if ja else label_en)}</span>'

    original = "" if ja else f'\n  <p class="card-original" lang="ja">{esc(entry["name"])}</p>'
    facts = [
        (t["domains"], esc(domains)),
        (t["languages"], esc(langs)),
        (t["formats"], esc(formats)),
        (t["license_term"], esc(license_label(entry, lang))),
        (t["commercial"], flag("commercial")),
        (t["redistribution"], flag("redistribution")),
        (t["checked"], f'<time datetime="{esc(entry["checked"])}">{esc(entry["checked"])}</time>'),
    ]
    facts_html = "\n".join(f"    <div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in facts)
    return f"""<li class="card" id="r-{esc(entry["id"])}" data-category="{esc(entry["category"])}" data-search="{esc(search_text(entry))}">
  <p class="card-category">{esc(CATEGORIES[entry["category"]][0 if ja else 1])}</p>
  <h3 class="card-title">{esc(name)}</h3>{original}
  <p class="card-publisher">{esc(entry["publisher"] if ja else entry["publisher_en"])}</p>
  <p class="card-summary">{esc(entry["summary"] if ja else entry["summary_en"])}</p>
  <dl class="card-facts">
{facts_html}
  </dl>
  <ul class="card-links">
    <li><a class="primary" href="{esc(entry["url"])}">{esc(t["open"])}<span class="visually-hidden">: {esc(name)}</span></a></li>
    <li><a href="{esc(entry["license_url"])}">{esc(t["terms"])}<span class="visually-hidden">: {esc(name)}</span></a></li>
  </ul>
</li>"""


def head(lang: str, site_url: str, title: str, description: str, path: str) -> str:
    t = TEXT[lang]
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="{site_url}{TEXT[code]["path"]}">' for code in ("ja", "en")
    )
    return f"""<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{site_url}{path}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{site_url}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="yasashii-refs">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{site_url}{path}">
<meta property="og:image" content="{site_url}/og.png">
<meta property="og:locale" content="{"ja_JP" if lang == "ja" else "en_US"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/dads-tokens.css">
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/app.js" defer></script>
</head>"""


def header(lang: str) -> str:
    t = TEXT[lang]
    return f"""<header class="site-header">
  <div class="wrap">
    <p class="site-name"><a href="{t["path"]}">yasashii-refs</a></p>
    <p class="lang-switch"><a href="{t["switch_path"]}" hreflang="{t["switch_lang"]}" lang="{t["switch_lang"]}" data-lang-link>{esc(t["switch_label"])}</a></p>
  </div>
</header>"""


def footer(lang: str, updated: str) -> str:
    t = TEXT[lang]
    contact = esc(CONTACT_JA if lang == "ja" else CONTACT_EN)
    lines = "\n".join(f"    <p>{p.format(contact=contact)}</p>" for p in t["footer"])
    return f"""<footer class="site-footer">
  <div class="wrap">
{lines}
    <p>{esc(t["updated"])}: <time datetime="{updated}">{updated}</time>　© 2026 Yudai Nishiyama（MIT License）</p>
  </div>
</footer>"""


def render_page(entries: list[dict], lang: str, site_url: str, updated: str) -> str:
    t = TEXT[lang]
    total = len(entries)
    counts = {c: sum(e["category"] == c for e in entries) for c in CATEGORIES}
    chips = [f'<button type="button" class="chip" data-category-chip="" aria-pressed="true">{esc(t["all"])}'
             f'<span class="n">{total}</span></button>']
    for cat, labels in CATEGORIES.items():
        if counts[cat]:
            chips.append(f'<button type="button" class="chip" data-category-chip="{cat}" aria-pressed="false">'
                         f'{esc(labels[0 if lang == "ja" else 1])}<span class="n">{counts[cat]}</span></button>')
    chips_html = "\n          ".join(chips)
    purpose = "\n        ".join(f"<p>{esc(p)}</p>" for p in t["purpose"])
    license_html = "\n        ".join(f"<p>{p}</p>" for p in t["license"])
    contact = esc(CONTACT_JA if lang == "ja" else CONTACT_EN)
    notes = "\n      ".join(f"<li>{p.format(contact=contact)}</li>" for p in t["notes"])
    cards = "\n".join(render_card(e, lang) for e in entries)
    messages = esc(json.dumps({"count": t["count"]}, ensure_ascii=False))
    return f"""{head(lang, site_url, t["title"], t["description"], t["path"])}
<body>
<a class="skip" href="#list">{esc(t["skip"])}</a>
{header(lang)}
<main>
  <div class="intro wrap">
    <h1>{esc(t["h1"])}</h1>
    <p class="lead">{esc(t["lead"].format(count=total))}</p>
    <div class="about">
      <section aria-labelledby="purpose-h">
        <h2 id="purpose-h">{esc(t["purpose_h"])}</h2>
        {purpose}
      </section>
      <section aria-labelledby="license-h">
        <h2 id="license-h">{esc(t["license_h"])}</h2>
        {license_html}
      </section>
    </div>
    <details class="notes">
      <summary>{esc(t["notes_summary"])}</summary>
      <ul>
      {notes}
      </ul>
    </details>
  </div>
  <section class="finder" aria-labelledby="finder-h" data-finder data-total="{total}" data-messages="{messages}">
    <div class="wrap">
      <h2 id="finder-h">{esc(t["finder_h"])}</h2>
      <div class="controls" data-controls hidden>
        <div class="search" role="search">
          <label for="q">{esc(t["search_label"])}</label>
          <p class="hint" id="q-hint">{esc(t["search_hint"])}</p>
          <input id="q" type="search" autocomplete="off" aria-describedby="q-hint">
        </div>
        <fieldset class="chips">
          <legend>{esc(t["categories_legend"])}</legend>
          <div class="chip-list">
          {chips_html}
          </div>
        </fieldset>
        <p class="count" role="status" data-count></p>
      </div>
      <ol class="cards" id="list">
{cards}
      </ol>
      <p class="empty" data-empty hidden>{esc(t["empty"])}</p>
    </div>
  </section>
</main>
{footer(lang, updated)}
</body>
</html>
"""


def render_not_found(site_url: str) -> str:
    t, en = TEXT["ja"], TEXT["en"]
    return f"""{head("ja", site_url, t["not_found_title"], t["description"], "/404.html")}
<body>
{header("ja")}
<main class="wrap not-found">
  <h1>{esc(t["not_found"])} <span lang="en">{esc(en["not_found"])}</span></h1>
  <p><a href="/">{esc(t["back"])}</a>　<a href="/en/" lang="en">{esc(en["back"])}</a></p>
</main>
</body>
</html>
"""


def build(out: Path = DIST, site_url: str | None = None, updated: str | None = None) -> list[dict]:
    """サイトを out に作り直す。載せた資料（目録の前付け）を返す"""
    site_url = (site_url or os.environ.get("SITE_URL") or DEFAULT_SITE_URL).rstrip("/")
    if not re.match(r"^https://[a-z0-9.-]+$", site_url):
        raise SystemExit(f"SITE_URL は https://ホスト名 の形にする: {site_url}")
    updated = updated or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    entries = load_entries()
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    (out / "en").mkdir()
    for name in ASSETS:
        shutil.copyfile(SRC / name, out / "assets" / name)
    for name in ROOT_FILES:
        if (SRC / name).exists():
            shutil.copyfile(SRC / name, out / name)
    (out / "index.html").write_text(render_page(entries, "ja", site_url, updated), encoding="utf-8")
    (out / "en" / "index.html").write_text(render_page(entries, "en", site_url, updated), encoding="utf-8")
    (out / "404.html").write_text(render_not_found(site_url), encoding="utf-8")
    (out / "_headers").write_text(
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: DENY\n"
        "  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
        "base-uri 'none'; form-action 'none'; frame-ancestors 'none'; object-src 'none'\n"
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n",
        encoding="utf-8",
    )
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n", encoding="utf-8")
    urls = "\n".join(f"  <url><loc>{site_url}{TEXT[c]['path']}</loc><lastmod>{updated}</lastmod></url>" for c in TEXT)
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8",
    )
    return entries


def main() -> int:
    out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DIST
    entries = build(out)
    print(f"{len(entries)}件の資料で、{out} にサイトを作った", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
