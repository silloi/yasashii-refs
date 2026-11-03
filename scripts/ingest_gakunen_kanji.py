#!/usr/bin/env python3
"""学年別漢字配当表（小学校学習指導要領 平成29年告示 別表）を、文部科学省の学習指導要領コード表（CSV）から取り出し、
data/gakunen-kanji.jsonl にする。

コード表では「別表　学年別漢字配当表」の行の下に「第一学年（80字）」のような学年の行が続き、その下に1字ずつ1行で並ぶ。
学年の行に書かれた字数と、実際に並んでいる字数が合うかも確かめる。

使い方: python3 scripts/ingest_gakunen_kanji.py [--refresh]
"""

from __future__ import annotations

import csv
import io
import re
import sys

from common import cached, opener, write_dataset

DATASET = "gakunen-kanji"
CSV_URL = "https://www.mext.go.jp/content/20230901-mxt_syoto01-000013115_02.csv"
VERSION = "平成29年告示"
SOURCE_VERSION = "小学校学習指導要領（平成29年告示）コード表 Ver 1.0"
GRADES = {"第一学年": 1, "第二学年": 2, "第三学年": 3, "第四学年": 4, "第五学年": 5, "第六学年": 6}


def convert(raw: bytes) -> list[dict]:
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))
    start = next(i for i, r in enumerate(rows) if len(r) >= 3 and r[0] == "国語" and re.fullmatch(r"別表\s*学年別漢字配当表", r[2].strip()))
    records: list[dict] = []
    expected: dict[int, int] = {}
    grade = None
    for r in rows[start + 1:]:
        if len(r) < 4 or r[0] != "国語":
            break
        text, code = r[2].strip(), r[3].strip()
        m = re.fullmatch(r"(第.学年)（(\d+)字）", text)
        if m and m.group(1) in GRADES:
            grade = GRADES[m.group(1)]
            expected[grade] = int(m.group(2))
            continue
        if grade is None or len(text) != 1:
            break  # 別表が終わった
        records.append({"source": DATASET, "version": VERSION, "kanji": text, "grade": grade, "code": code})
    for g, n in expected.items():
        got = sum(1 for rec in records if rec["grade"] == g)
        if got != n:
            raise RuntimeError(f"第{g}学年: 表には {n} 字とあるが、{got} 字しか取り出せなかった")
    if sorted(expected) != [1, 2, 3, 4, 5, 6]:
        raise RuntimeError(f"学年がそろっていない: {sorted(expected)}")
    return records


def main() -> int:
    raw = cached("gakunen-kanji-coderev.csv", lambda: opener().open(CSV_URL, timeout=120).read())
    records = convert(raw)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": "学年別漢字配当表（小学校学習指導要領 平成29年告示 別表）",
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "url": CSV_URL,
        "license": "告示（著作権の対象外）。コード表は文部科学省ウェブサイト利用規約（PDL-1.0 に準拠）",
        "attribution": f"出典：文部科学省「小学校学習指導要領（平成29年告示）コード表」（{CSV_URL}）を加工して作成",
    }, raw)
    print(f"{DATASET}: {len(records)} 字", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
