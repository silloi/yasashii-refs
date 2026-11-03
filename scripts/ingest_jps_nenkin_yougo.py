#!/usr/bin/env python3
"""日本年金機構「年金用語集」（https://www.nenkin.go.jp/service/yougo/index.html ）を、
data/jps-nenkin-yougo.jsonl にする。

1行が1つの用語（用語集の1ページ）。
- 用語の一覧は、用語集のトップのページのリンクから取る（並び順もそのまま）。行（あ行など）の索引のページは除く。
- 各ページの見出し（h1。「か行　学生納付特例制度」）、ページID、更新日を読む。
- 本文は、更新日の枠（basic_info_wp）と「関連情報」の枠（kanren_wp）のあいだを読む。本文の枠（wysiwyg_wp）が
  いくつかに分かれ、あいだに表（2語）や計算式の画像（報酬比例部分）、小見出しが入るページがある。
  - 段落・箇条書きの項目・小見出し・表の行は、改行でつなぐ。表のセルはタブでつなぐ。
  - 画像は alt の文字で読む（「新規ウィンドウで開きます。」の印は除く）。
  - 本文の最初の段落は用語の名前のくり返しなので除く。小見出しの「関連リンク」は、リンクの見出しなので除く。
- 関連のリンク（p.innerLink、p.externalLink）は、本文のすぐ下のものと「関連情報」の枠の中のものを、出てくる順に読む。
- 本文が「〜の解説をご覧ください」だけの用語（カラ期間など）は、`see` に参照先の用語の id を入れる。
- 取得は1ページずつ、1秒の間を置く。取得したページは .cache/jps-nenkin-yougo/ に置く。
- 日本年金機構のサイトは原則として転載フリーだが、「転載の制限等の注記があるページは、この限りではありません」。
  本文に「転載」の語があるページが見つかったら止まる（目で確かめるため）。
用語の数が一覧のリンクの数と合わなければ止まる。

使い方: python3 scripts/ingest_jps_nenkin_yougo.py [--refresh]
"""

from __future__ import annotations

import html
import re
import sys
import time
import urllib.parse
from html.parser import HTMLParser

from common import CACHE, cached, opener, write_dataset

DATASET = "jps-nenkin-yougo"
BASE = "https://www.nenkin.go.jp"
INDEX = BASE + "/service/yougo/index.html"
TITLE = "年金用語集"
TERMS_URL = "https://www.nenkin.go.jp/info/aboutweb/aboutsite.html"
WAIT = 1.0  # 取得の間隔（秒）

TERM_LINK = re.compile(r"^/service/yougo/([a-z]+gyo)/([A-Za-z0-9_-]+)\.html$")
SEE = re.compile(r"の解説をご覧ください。?$")
BLOCKS = {"p", "li", "tr", "h2", "h3", "h4", "h5", "dt", "dd", "caption", "div"}
LINK_CLASSES = {"innerLink", "externalLink"}
SKIP_HEADINGS = {"関連リンク"}
START = '<div class="basic_info_wp">'
KANREN = '<div class="kanren_wp">'
YOUGO_NAV = '<div class="h2bg"><div><h2>年金用語集</h2></div></div>'


class Content(HTMLParser):
    """本文の範囲の HTML から、文字の行と、関連のリンクを読む"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.links: list[tuple[str, str]] = []   # (href, 文字)
        self._buf = ""
        self._skip = 0          # basic_info_wp の中（深さ）
        self._link_p = False    # p.innerLink / p.externalLink の中
        self._href = None
        self._a_text = ""
        self._cell = False
        self._table = 0         # 表の中（深さ）。セルの中の段落や改行は、行を分けずに空白にする

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
        if tag == "p" and cls & LINK_CLASSES:
            self._flush()
            self._link_p = True
            return
        if self._link_p:
            if tag == "a" and a.get("href"):
                self._href, self._a_text = a["href"], ""
            return
        if tag == "table":
            self._flush()
            self._table += 1
            return
        if self._table and tag not in ("tr", "caption"):
            if tag in ("td", "th"):
                if self._cell:
                    self._buf += "\t"
                self._cell = True
            elif tag in ("br", "p", "li", "div"):
                self._buf += " "
            return
        if tag in BLOCKS:
            self._flush()
        elif tag == "br":
            self._buf += "\n"
        elif tag == "img" and "img-guidance" not in cls and a.get("alt"):
            self._flush()
            self._buf = a["alt"]
            self._flush()

    def handle_endtag(self, tag):
        if self._skip:
            if tag == "div":
                self._skip -= 1
            return
        if self._link_p:
            if tag == "a" and self._href is not None:
                self.links.append((self._href, clean(self._a_text)))
                self._href = None
            if tag == "p":
                self._link_p = False
            return
        if tag == "table":
            self._table -= 1
            self._flush()
            return
        if self._table and tag not in ("tr", "caption"):
            return
        if tag in BLOCKS:
            self._flush()

    def handle_data(self, data):
        if self._skip:
            return
        if self._link_p:
            if self._href is not None:
                self._a_text += data
            return
        # HTML のソースの改行・タブは空白として読む（行とセルの区切りは、br・ブロック・セルの印だけで作る）
        self._buf += re.sub(r"[\t\r\n]", " ", data)

    def close(self):
        super().close()
        self._flush()

    def _flush(self):
        for line in self._buf.split("\n"):
            cells = [clean(c) for c in line.split("\t")]
            text = "\t".join(c for c in cells if c)
            if text:
                self.lines.append(text)
        self._buf = ""
        self._cell = False


def clean(s: str) -> str:
    s = html.unescape(s).replace(" ", " ")
    s = re.sub(r"[ \r\n]+", " ", s)
    return s.strip(" 　")


def parse_date(s: str) -> str:
    m = re.fullmatch(r"(\d{4})年(\d{1,2})月(\d{1,2})日", s)
    if not m:
        raise ValueError(f"更新日が読めない: {s!r}")
    return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"


def absolute(href: str) -> str:
    return urllib.parse.urljoin(BASE + "/service/yougo/", href)


def term_list(index_html: str) -> list[tuple[str, str]]:
    """トップのページの、用語のページへのリンク（行, slug）を、出てくる順に返す"""
    out, seen = [], set()
    for href in re.findall(r'href="([^"]+)"', index_html):
        m = TERM_LINK.match(html.unescape(href))
        if not m or m.group(2) == "index" or m.groups() in seen:
            continue
        seen.add(m.groups())
        out.append(m.groups())
    return out


def parse_page(page: str, url: str) -> dict:
    h1 = re.search(r"<h1>(.*?)</h1>", page, re.S)
    page_id = re.search(r'<p class="page_number">ページID：(.*?)</p>', page)
    updated = re.search(r'<p class="update">更新日：(.*?)</p>', page)
    start, kanren = page.find(START), page.find(KANREN)
    nav = page.find(YOUGO_NAV, kanren)
    if not (h1 and page_id and updated) or min(start, kanren, nav) < 0:
        raise ValueError(f"{url}: ページの形が想定と違う")
    m = re.fullmatch(r"(.行)[　 ]+(.+)", clean(re.sub(r"<[^>]+>", "", h1.group(1))))
    if not m:
        raise ValueError(f"{url}: 見出しが読めない: {h1.group(1)!r}")
    body = Content()
    body.feed(page[start:kanren])
    body.close()
    rel = Content()
    rel.feed(page[kanren:nav])
    rel.close()
    return {
        "row": m.group(1),
        "term": m.group(2),
        "lines": body.lines,
        "links": body.links + rel.links,
        "page_id": clean(page_id.group(1)),
        "updated": parse_date(clean(updated.group(1))),
    }


def fetcher(url: str):
    def fetch() -> bytes:
        time.sleep(WAIT)
        return opener().open(url, timeout=60).read()
    return fetch


def convert(index_raw: bytes, pages: dict[tuple[str, str], bytes]) -> list[dict]:
    terms = term_list(index_raw.decode("utf-8"))
    ids = {f"{row}/{slug}" for row, slug in terms}
    records = []
    for row, slug in terms:
        url = f"{BASE}/service/yougo/{row}/{slug}.html"
        p = parse_page(pages[(row, slug)].decode("utf-8"), url)
        lines = [x for x in p["lines"] if x not in SKIP_HEADINGS]
        if lines and lines[0] == p["term"]:
            lines = lines[1:]
        if not lines:
            raise ValueError(f"{url}: 本文が無い")
        text = "\n".join(lines)
        if "転載" in text:
            raise ValueError(f"{url}: 「転載」の語がある。利用の条件を確かめる")
        rec = {
            "source": DATASET,
            "version": p["updated"],
            "id": f"{row}/{slug}",
            "row": p["row"],
            "term": p["term"],
            "definition": text,
        }
        if len(lines) == 1 and SEE.search(lines[0]):
            targets = set()
            for href, _ in p["links"]:
                t = TERM_LINK.match(urllib.parse.urlparse(absolute(href)).path)
                if t and f"{t.group(1)}/{t.group(2)}" in ids:
                    targets.add(f"{t.group(1)}/{t.group(2)}")
            if len(targets) != 1:
                raise ValueError(f"{url}: 参照先の用語が分からない: {p['links']}")
            rec["see"] = targets.pop()
        links = [{"title": t, "url": absolute(h)} for h, t in p["links"] if t]
        if links:
            rec["related"] = links
        rec["page_id"] = p["page_id"]
        rec["url"] = url
        records.append(rec)
    if len(records) != len(terms):
        raise ValueError(f"用語の数が合わない: {len(records)} / {len(terms)}")
    return records


def main() -> int:
    (CACHE / DATASET).mkdir(parents=True, exist_ok=True)
    index_raw = cached(f"{DATASET}/index.html", fetcher(INDEX))
    terms = term_list(index_raw.decode("utf-8"))
    pages = {}
    for row, slug in terms:
        url = f"{BASE}/service/yougo/{row}/{slug}.html"
        pages[(row, slug)] = cached(f"{DATASET}/{row}_{slug}.html", fetcher(url))
    records = convert(index_raw, pages)
    latest = max(r["version"] for r in records)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": f"日本年金機構「{TITLE}」",
        "version": f"用語ごと（各行の version はページの更新日。いちばん新しいものは {latest}）",
        "url": INDEX,
        "license": "日本年金機構ホームページの利用条件（原則リンクフリー・転載フリー）",
        "license_url": TERMS_URL,
        "attribution": f"出典：日本年金機構ホームページ「{TITLE}」（{INDEX}）を加工して作成",
        "source_sha256_of": "トップのページと各用語のページを、並び順につないだもの",
    }, index_raw + b"".join(pages[t] for t in terms))
    print(f"{DATASET}: {len(records)} 語（参照だけの語 {sum('see' in r for r in records)}）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
