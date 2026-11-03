#!/usr/bin/env python3
"""法令用語日英標準対訳辞書（法務省）の CSV（UTF-8）を取得し、data/jlt-standard-dict.jsonl にする。

1行 = 1つの用語。CSV では訳語の候補ごとに1行なので、同じ用語（用語＋読み）の行を、元の順番のまままとめる。
注釈は、元の CSV で付いていた訳語の候補に付けたままにする（解釈して付け替えない）。

使い方: python3 scripts/ingest_jlt_standard_dict.py [--version 19.0] [--refresh]
"""

from __future__ import annotations

import csv
import io
import re
import sys
import urllib.parse
import urllib.request

from common import cached, opener, write_dataset

DATASET = "jlt-standard-dict"
PAGE = "https://www.japaneselawtranslation.go.jp/ja/dicts/download"
FTYPE_CSV_UTF8 = "4"
HEADER = ["用語", "読み", "訳語候補番号", "訳語候補", "使い分け基準", "用例(和文)", "用例(英文)", "用例出典", "注釈1", "注釈2"]


def download(version: str) -> bytes:
    """配布ページのフォームと同じ手順で取る（ページを開いて確認用のトークンを受け取り、版と形式を送る）"""
    op = opener()
    page = op.open(PAGE, timeout=60).read().decode("utf-8")
    m = re.search(r'name="_csrfToken"[^>]*value="([^"]+)"', page)
    if not m:
        raise RuntimeError("配布ページの形が変わった（_csrfToken が見つからない）")
    body = urllib.parse.urlencode({"_csrfToken": m.group(1), "version": version, "ftype": FTYPE_CSV_UTF8}).encode()
    req = urllib.request.Request(PAGE, data=body, headers={"Referer": PAGE, "Content-Type": "application/x-www-form-urlencoded"})
    resp = op.open(req, timeout=180)
    if "text/csv" not in (resp.headers.get("Content-Type") or ""):
        raise RuntimeError(f"CSV が返ってこなかった: {resp.headers.get('Content-Type')}")
    return resp.read()


def convert(raw: bytes, version: str) -> list[dict]:
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))
    if rows[0] != HEADER:
        raise RuntimeError(f"列が想定と違う: {rows[0]}")
    terms: dict[tuple[str, str], dict] = {}
    for r in rows[1:]:
        term, reading, no, en, usage, ex_ja, ex_en, ex_src, note1, note2 = (c.strip() for c in r)
        rec = terms.setdefault((term, reading), {
            "source": DATASET,
            "version": version,
            "term": term,
            "reading": reading,
            "translations": [],
        })
        tr: dict = {"en": en}
        if no:
            tr["no"] = int(no)
        if usage:
            tr["usage"] = usage
        example = {k: v for k, v in (("ja", ex_ja), ("en", ex_en), ("source", ex_src)) if v}
        if example:
            tr["example"] = example
        notes = [n for n in (note1, note2) if n]
        if notes:
            tr["notes"] = notes
        rec["translations"].append(tr)
    return list(terms.values())


def main() -> int:
    version = sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else "19.0"
    raw = cached(f"jlt-standard-dict-{version}.csv", lambda: download(version))
    records = convert(raw, version)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": "法令用語日英標準対訳辞書",
        "version": version,
        "url": PAGE,
        "license": "PDL-1.0",
        "attribution": f"出典：日本法令外国語訳データベースシステム（法務省）「法令用語日英標準対訳辞書」第{version}版（{PAGE}）を加工して作成",
    }, raw)
    print(f"{DATASET}: {len(records)} 語", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
