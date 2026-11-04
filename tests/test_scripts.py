"""scripts/ の、ネットワークを使わない部分を確かめる。

python3 -m unittest discover -s tests
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_links  # noqa: E402
import language_table  # noqa: E402


class FileLinks(unittest.TestCase):
    PAGE = """
    <a href="/common/001.pdf">PDF</a>
    <a href='files/a.XLSX#top'>Excel</a>
    <a href="https://other.example.jp/b.pdf">他のホスト</a>
    <a href="/relays/download/1/?file=/files/libs/2.pdf&amp;file_name=x">中継</a>
    <a href="/page.html">ページ</a>
    """

    def test_same_host_document_links(self):
        links = check_links.file_links(self.PAGE, "https://www.example.go.jp/dir/index.html")
        self.assertEqual(links, [
            "https://www.example.go.jp/common/001.pdf",
            "https://www.example.go.jp/dir/files/a.XLSX",
            "https://www.example.go.jp/relays/download/1/?file=/files/libs/2.pdf&file_name=x",
        ])


class TextHash(unittest.TestCase):
    def test_ignores_scripts_comments_and_spacing(self):
        a = "<p>利用規約</p><script>var t = 1;</script><!-- 1 -->"
        b = "<p>\n  利用規約 </p><script>var t = 2;</script><!-- 2 -->"
        self.assertEqual(check_links.text_hash(a), check_links.text_hash(b))
        self.assertNotEqual(check_links.text_hash(a), check_links.text_hash("<p>利用規約（改定）</p>"))


class Changes(unittest.TestCase):
    def test_reports_status_files_and_text(self):
        old = {
            "https://a.jp/": {"refs": ["x"], "status": 200, "files": ["https://a.jp/1.pdf"]},
            "https://a.jp/terms": {"refs": ["x"], "status": 200, "text": "aaa"},
            "https://a.jp/same": {"refs": ["y"], "status": 200},
        }
        new = {
            "https://a.jp/": {"refs": ["x"], "status": 200, "files": ["https://a.jp/2.pdf"]},
            "https://a.jp/terms": {"refs": ["x"], "status": 404},
            "https://a.jp/same": {"refs": ["y"], "status": 200},
            "https://a.jp/new": {"refs": ["z"], "status": 200},
        }
        out = check_links.changes(old, new)
        self.assertIn("- [x] https://a.jp/: ファイルのリンク +1 −1", out)
        self.assertIn("    + https://a.jp/2.pdf", out)
        self.assertIn("    − https://a.jp/1.pdf", out)
        self.assertIn("- [x] https://a.jp/terms: 状態 200 → 404", out)
        self.assertFalse(any("same" in line or "new" in line for line in out))


class CollectUrls(unittest.TestCase):
    def test_front_matter_body_docs_and_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "catalog" / "terms").mkdir(parents=True)
            (root / "catalog" / "terms" / "foo.md").write_text(
                "---\nid: foo\nurl: https://a.jp/page.html\nlicense_url: 未確認\n---\n\n"
                "本文（https://a.jp/x.pdf ）。https://b.jp/y.html。[リンク](https://c.jp/z)\n",
                encoding="utf-8",
            )
            (root / "catalog" / "README.md").write_text("https://a.jp/page.html\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "notes.md").write_text("出典（https://d.jp/stat.html ）\n", encoding="utf-8")
            (root / "data").mkdir()
            (root / "data" / "foo.meta.json").write_text(json.dumps({"source": "foo", "url": "https://a.jp/dl.html"}))
            found = check_links.collect_urls(root)
        self.assertEqual(sorted(found), [
            "https://a.jp/dl.html", "https://a.jp/page.html", "https://a.jp/x.pdf",
            "https://b.jp/y.html", "https://c.jp/z", "https://d.jp/stat.html",
        ])
        self.assertEqual(found["https://a.jp/page.html"]["refs"], {"foo", "catalog/README.md"})
        self.assertEqual(found["https://a.jp/page.html"]["roles"], {"page", "link"})
        self.assertEqual(found["https://d.jp/stat.html"]["refs"], {"docs/notes.md"})


class ShortName(unittest.TestCase):
    def test_drops_parentheses_and_subtitles(self):
        self.assertEqual(
            language_table.short_name("マイナンバー（個人番号）制度・マイナンバーカード（デジタル庁のページ）"),
            "マイナンバー制度・マイナンバーカード",
        )
        self.assertEqual(language_table.short_name("つなひろ—日本語学習サイト"), "つなひろ")


if __name__ == "__main__":
    unittest.main()
