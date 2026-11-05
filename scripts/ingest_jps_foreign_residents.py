#!/usr/bin/env python3
"""日本年金機構「やさしい日本語（にほんご）」のページ（https://www.nenkin.go.jp/international/simplejapanese/index.html ）を、
data/jps-foreign-residents.jsonl にする。

1行が1つのページ。目録の jps-foreign-residents のうち、やさしいにほんごのページだけを取り込む
（英語のページと、脱退一時金の請求書（PDF・Excel の様式）は入れない）。
- ページは、トップのページから、/international/simplejapanese/ の下の .html へのリンクをたどって集める。並びは URL の順。
- 見出し（h1）と、本文（main_inner の中。その節のページ一覧 lobgbox losubnavi より前）を読む。
  - 本文は、見出し（h2〜h5）・段落・箇条書きの項目・表の行などの単位（`blocks`）にする。表のセルはタブでつなぐ。
  - 画像は alt の文字で読む（「新規ウィンドウで開きます」の印は除く）。
  - 本文の中のリンク（各言語の PDF などを含む）は、`links` に文字と URL を入れる。
- ページID と更新日は、書いてあるページだけ。更新日の無いページの version は「更新日の記載なし」。
- 漢字のあとに読みを括弧で書いた日本語（「年金（ねんきん）」）と、語のあいだの空白（全角）は、そのまま入れる。
  元のページの誤り（読みの括弧の位置のずれなど）も直さない。開閉のボタンの文字（「詳細を開く」）は除く。
- 本文が無く、集めたほかのページへのリンクだけのページ（目次）は飛ばす（data/*.meta.json の skipped_menu_pages）。
- 日本年金機構のサイトは原則として転載フリーだが、「転載の制限等の注記があるページは、この限りではありません」。
  本文に「転載」の語があるページが見つかったら止まる（目で確かめるため）。
- 取得は1ページずつ、1秒の間を置く。取得したページは .cache/jps-foreign-residents/ に置く。

使い方: python3 scripts/ingest_jps_foreign_residents.py [--refresh]
"""

from __future__ import annotations

import html
import re
import sys
import time
import urllib.parse
from html.parser import HTMLParser

from common import CACHE, cached, opener, write_dataset

DATASET = "jps-foreign-residents"
PREFIX = "https://www.nenkin.go.jp/international/simplejapanese/"
INDEX = PREFIX + "index.html"
TITLE = "やさしい日本語（にほんご）"
TERMS_URL = "https://www.nenkin.go.jp/info/aboutweb/aboutsite.html"
WAIT = 1.0
START = '<div class="main_inner">'
ENDS = ('<div class="lobgbox losubnavi">', '<div class="foot_menu_shiraberu">')
BLOCKS = {"h2", "h3", "h4", "h5", "p", "li", "dt", "dd", "tr", "caption", "div"}
UI_TEXT = {"詳細を開く", "詳細を閉じる", "印刷"}  # 開閉のボタンなど、画面の操作の文字


def clean(s: str) -> str:
    s = html.unescape(s).replace(" ", " ")
    s = re.sub(r"[ \t\r\n]+", " ", s)
    return s.strip(" 　")


class Blocks(HTMLParser):
    """本文の範囲の HTML から、単位（種類と文字）と、リンクを読む"""

    def __init__(self, base: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base = base
        self.blocks: list[dict] = []
        self.links: list[dict] = []
        self._buf = ""
        self._kind = "p"
        self._skip = 0       # basic_info_wp の中（深さ）
        self._table = 0
        self._cell = False
        self._href: str | None = None
        self._a_text = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        if self._skip:
            if tag == "div":
                self._skip += 1
            return
        if tag == "div" and "basic_info_wp" in cls:
            self._skip = 1
            return
        if tag == "a" and a.get("href") and not a["href"].startswith(("#", "javascript:")):
            self._href, self._a_text = urllib.parse.urljoin(self.base, html.unescape(a["href"])), ""
        if tag == "table":
            self._flush()
            self._table += 1
            return
        if self._table:
            if tag == "tr":
                self._flush()
                self._kind = "tr"
            elif tag in ("td", "th"):
                if self._cell:
                    self._buf += "\t"
                self._cell = True
            elif tag in ("br", "p", "li", "div"):
                self._buf += " "
            elif tag == "caption":
                self._flush()
                self._kind = "caption"
            return
        if tag in BLOCKS:
            self._flush()
            self._kind = "p" if tag == "div" else tag
        elif tag == "br":
            self._buf += "\n"
        elif tag == "img" and a.get("alt") and "新規ウィンドウ" not in a["alt"]:
            self._buf += a["alt"]

    def handle_endtag(self, tag):
        if self._skip:
            if tag == "div":
                self._skip -= 1
            return
        if tag == "a" and self._href is not None:
            text = clean(self._a_text)
            if text and not any(x["url"] == self._href and x["text"] == text for x in self.links):
                self.links.append({"text": text, "url": self._href})
            self._href = None
        if tag == "table":
            self._table -= 1
            self._flush()
            return
        if self._table:
            if tag in ("tr", "caption"):
                self._flush()
            return
        if tag in BLOCKS:
            self._flush()

    def handle_data(self, data):
        if self._skip:
            return
        data = re.sub(r"[\t\r\n]", " ", data)
        self._buf += data
        if self._href is not None:
            self._a_text += data

    def close(self):
        super().close()
        self._flush()

    def _flush(self):
        for line in self._buf.split("\n"):
            text = "\t".join(c for c in (clean(x) for x in line.split("\t")) if c)
            if text:
                self.blocks.append({"type": self._kind, "text": text})
        self._buf = ""
        self._cell = False
        self._kind = "p" if not self._table else "tr"


def page_links(page: str, url: str) -> list[str]:
    out = []
    for href in re.findall(r'href="([^"#]+)"', page):
        u = urllib.parse.urljoin(url, html.unescape(href)).split("#")[0]
        if u.startswith(PREFIX) and u.endswith(".html"):
            out.append(u)
    return out


def parse_date(s: str) -> str:
    m = re.fullmatch(r"(\d{4})年(\d{1,2})月(\d{1,2})日", s)
    if not m:
        raise ValueError(f"更新日が読めない: {s!r}")
    return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"


def parse_page(page: str, url: str) -> dict:
    h1 = re.search(r"<h1>(.*?)</h1>", page, re.S)
    start = page.find(START)
    ends = [i for i in (page.find(e, start) for e in ENDS) if i >= 0]
    if not h1 or start < 0 or not ends:
        raise ValueError(f"{url}: ページの形が想定と違う")
    body = Blocks(url)
    body.feed(page[start:min(ends)])
    body.close()
    blocks = [b for b in body.blocks if b["text"] not in UI_TEXT]
    title = clean(re.sub(r"<[^>]+>", "", h1.group(1)))
    if blocks and blocks[0]["text"] == title:
        blocks = blocks[1:]
    text = "\n".join(b["text"] for b in blocks)
    if "転載" in text:
        raise ValueError(f"{url}: 「転載」の語がある。利用の条件を確かめる")
    rec = {"title": title, "blocks": blocks, "links": body.links}
    page_id = re.search(r'<p class="page_number">ページID：(.*?)</p>', page)
    updated = re.search(r'<p class="update">更新日：(.*?)</p>', page)
    if page_id:
        rec["page_id"] = clean(page_id.group(1))
    rec["updated"] = parse_date(clean(updated.group(1))) if updated else None
    return rec


def cache_name(url: str) -> str:
    return DATASET + "/" + url[len(PREFIX):].replace("/", "__")


def fetcher(url: str):
    def fetch() -> bytes:
        time.sleep(WAIT)
        return opener().open(url, timeout=60).read()
    return fetch


def crawl() -> dict[str, bytes]:
    """トップのページから、/international/simplejapanese/ の下のページをたどる。URL → HTML"""
    (CACHE / DATASET).mkdir(parents=True, exist_ok=True)
    pages: dict[str, bytes] = {}
    queue = [INDEX]
    while queue:
        url = queue.pop(0)
        if url in pages:
            continue
        pages[url] = cached(cache_name(url), fetcher(url))
        queue += [u for u in page_links(pages[url].decode("utf-8"), url) if u not in pages and u not in queue]
    return pages


def convert(pages: dict[str, bytes], skipped: list[str] | None = None) -> list[dict]:
    """本文が無く、集めたほかのページへのリンクだけのページ（目次）は飛ばす（skipped に URL を入れる）"""
    records = []
    for url in sorted(pages):
        p = parse_page(pages[url].decode("utf-8"), url)
        if not p["blocks"]:
            if p["links"] and all(x["url"].split("#")[0] in pages for x in p["links"]):
                if skipped is not None:
                    skipped.append(url)
                continue
            raise ValueError(f"{url}: 本文が無い")
        rec = {"source": DATASET, "version": p["updated"] or "更新日の記載なし", "url": url, "title": p["title"]}
        if "page_id" in p:
            rec["page_id"] = p["page_id"]
        rec["blocks"] = p["blocks"]
        if p["links"]:
            rec["links"] = p["links"]
        records.append(rec)
    return records


def main() -> int:
    pages = crawl()
    skipped: list[str] = []
    records = convert(pages, skipped)
    dated = [r["version"] for r in records if r["version"][:1].isdigit()]
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": f"日本年金機構「{TITLE}」",
        "version": f"ページごと（各行の version はページの更新日。いちばん新しいものは {max(dated)}）",
        "url": INDEX,
        "license": "日本年金機構ホームページの利用条件（原則リンクフリー・転載フリー）",
        "license_url": TERMS_URL,
        "attribution": f"出典：日本年金機構ホームページ「{TITLE}」（{INDEX}）を加工して作成",
        "skipped_menu_pages": skipped,
        "source_sha256_of": "各ページを、URL の順につないだもの",
    }, b"".join(pages[u] for u in sorted(pages)))
    print(f"{DATASET}: {len(records)} ページ・単位 {sum(len(r['blocks']) for r in records)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
