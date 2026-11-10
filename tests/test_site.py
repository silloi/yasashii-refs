"""閲覧用サイト（scripts/build_site.py）を一時ディレクトリに作って確かめる。

python3 -m unittest discover -s tests
"""

from __future__ import annotations

import collections
import html.parser
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_site  # noqa: E402


class Page(html.parser.HTMLParser):
    """カードの id・元のページへのリンク・ページ内の id を集める"""

    def __init__(self):
        super().__init__()
        self.ids: collections.Counter[str] = collections.Counter()
        self.cards: dict[str, dict[str, str]] = {}
        self.links: list[str] = []
        self._card: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids[a["id"]] += 1
        if tag == "li" and "card" in (a.get("class") or "").split():
            self._card = a["id"].removeprefix("r-")
            self.cards[self._card] = {"category": a["data-category"], "search": a["data-search"]}
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
            if self._card and a.get("class") == "primary":
                self.cards[self._card]["source"] = a["href"]


class BuildSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "dist"
        cls.entries = build_site.build(cls.out, site_url="https://example.pages.dev", updated="2026-11-10")
        cls.pages = {}
        for lang, path in (("ja", cls.out / "index.html"), ("en", cls.out / "en" / "index.html")):
            text = path.read_text(encoding="utf-8")
            parser = Page()
            parser.feed(text)
            cls.pages[lang] = (text, parser)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_entry_appears_in_both_languages_with_its_source_link(self):
        catalog = {p.stem for p in (ROOT / "catalog").glob("*/*.md")}
        self.assertEqual({e["id"] for e in self.entries}, catalog)
        for lang, (_, page) in self.pages.items():
            with self.subTest(lang=lang):
                self.assertEqual(set(page.cards), catalog)
                for entry in self.entries:
                    card = page.cards[entry["id"]]
                    self.assertEqual(card["source"], entry["url"])
                    self.assertEqual(card["category"], entry["category"])

    def test_text_comes_from_the_catalog(self):
        ja, en = self.pages["ja"][0], self.pages["en"][0]
        sample = next(e for e in self.entries if e["id"] == "seikatsu-cando")
        for key in ("name", "summary"):
            self.assertIn(build_site.esc(sample[key]), ja)
        for key in ("name_en", "summary_en", "publisher_en", "license_en"):
            self.assertIn(build_site.esc(sample[key]), en)
        self.assertIn("公共データ利用規約（PDL1.0）", ja)  # 説明の無い PDL-1.0 は読める名前にする
        self.assertIn("Public Data License 1.0 (PDL 1.0)", en)

    def test_states_purpose_and_what_mit_covers(self):
        ja, en = self.pages["ja"][0], self.pages["en"][0]
        self.assertIn("何のための目録か", ja)
        self.assertIn("載せている資料そのものには、MIT は当てはまりません", ja)
        self.assertIn("What the MIT License covers", en)
        self.assertIn("The MIT License does not cover the listed resources themselves", en)

    def test_does_not_host_the_data(self):
        files = [p.relative_to(self.out).as_posix() for p in self.out.rglob("*") if p.is_file()]
        self.assertFalse([f for f in files if f.endswith((".jsonl", ".json", ".csv", ".pdf", ".xlsx"))], files)
        for lang, (_, page) in self.pages.items():
            self.assertFalse([h for h in page.links if h.startswith("/data/") or h.endswith(".jsonl")], lang)

    def test_no_links_to_this_repository(self):
        # 一般公開のサイトには、GitHub（このリポジトリ・Issue・LICENSE）へのリンクを付けない。
        # 資料そのものの利用規約が GitHub にあるもの（デザイントークン・Furifont）は、元への案内なので残す
        pages = [self.out / "index.html", self.out / "en" / "index.html", self.out / "404.html"]
        for path in pages:
            text = path.read_text(encoding="utf-8")
            with self.subTest(page=path.name):
                self.assertNotIn("GitHub", text)
                self.assertNotIn("silloi", text)
        own_terms = {e["license_url"] for e in self.entries} | {e["url"] for e in self.entries}
        for lang, (_, page) in self.pages.items():
            self.assertFalse([h for h in page.links if "github" in h and h not in own_terms], lang)

    def test_contact_is_shown_without_a_plain_address(self):
        plain = f"{build_site.CONTACT_USER}@{build_site.CONTACT_DOMAIN}"
        self.assertIn(build_site.CONTACT_JA, self.pages["ja"][0])
        self.assertIn(build_site.CONTACT_EN, self.pages["en"][0])
        for path in self.out.rglob("*"):
            if path.is_file() and path.suffix in {".html", ".js", ".css", ".txt", ".xml", ""}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                with self.subTest(file=path.name):
                    self.assertNotIn(plain, text)
                    self.assertNotIn("mailto:", text)
        for source in [ROOT / "scripts" / "build_site.py", *(ROOT / "site" / "src").glob("*.*")]:
            self.assertNotIn(plain, source.read_text(encoding="utf-8", errors="ignore"), source.name)

    def test_html_ids_are_unique_and_links_are_absolute_or_site_paths(self):
        for lang, (_, page) in self.pages.items():
            with self.subTest(lang=lang):
                self.assertEqual([k for k, v in page.ids.items() if v > 1], [])
                for href in page.links:
                    self.assertRegex(href, r"^(https://|/|#)")

    def test_search_text_covers_both_languages(self):
        _, page = self.pages["en"]
        card = page.cards["mhlw-tagengo-yougo"]["search"]
        for term in ("雇用管理", "employment", "ベトナム語", "vietnamese", "雇用・労働", "employment and labor"):
            self.assertIn(term, card)

    def test_categories_and_assets(self):
        ja = self.pages["ja"][0]
        for category in {e["category"] for e in self.entries}:
            self.assertIn(f'data-category-chip="{category}"', ja)
        for name in build_site.ASSETS:
            self.assertTrue((self.out / "assets" / name).exists(), name)
        tokens = (self.out / "assets" / "dads-tokens.css").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2023 デジタル庁", tokens)  # MIT の表示を残す
        style = (self.out / "assets" / "style.css").read_text(encoding="utf-8")
        self.assertFalse(re.findall(r"#[0-9a-fA-F]{3,8}\b", style), "色はトークン（dads-tokens.css）から使う")
        self.assertIn("https://example.pages.dev/en/", ja)  # SITE_URL を canonical・hreflang に使う


if __name__ == "__main__":
    unittest.main()
