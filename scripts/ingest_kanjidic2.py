#!/usr/bin/env python3
"""KANJIDIC2（EDRDG）から、学年（常用漢字・人名用漢字）・旧日本語能力試験の級・新聞の頻度順位のどれかがある字を取り出し、
data/kanjidic2.jsonl にする。

KANJIDIC2 は CC BY-SA 4.0。取り出したデータも CC BY-SA 4.0 で、EDRDG の謝辞を付けて配る。
EDRDG のライセンスは、データを使うアプリやサーバーに定期的な更新（ウェブの辞書なら月1回以上）を求めている。
アプリで使うときは --refresh で取り直す。

使い方: python3 scripts/ingest_kanjidic2.py [--refresh]
"""

from __future__ import annotations

import gzip
import io
import sys
import xml.etree.ElementTree as ET

from common import cached, opener, write_dataset

DATASET = "kanjidic2"
URL = "https://www.edrdg.org/kanjidic/kanjidic2.xml.gz"
PAGE = "https://www.edrdg.org/wiki/index.php/KANJIDIC_Project"
LICENCE = "https://www.edrdg.org/edrdg/licence.html"
# 日本語以外の読み（KANJIDIC2 の r_type → BCP 47）。朝鮮語の読みは Charles Muller 氏、ピンインは Christian Wittern 氏・Koichi Yasuoka 氏の提供
OTHER_READINGS = {"pinyin": "zh-Latn-pinyin", "korean_h": "ko", "vietnam": "vi"}
MEANING_LANGS = ("en", "es", "fr", "pt")


def texts(parent: ET.Element, path: str) -> list[str]:
    return [t for t in ((e.text or "").strip() for e in parent.iterfind(path)) if t]


def convert(raw: bytes) -> tuple[list[dict], dict]:
    header: dict[str, str] = {}
    records: list[dict] = []
    total = 0
    for _, el in ET.iterparse(io.BytesIO(gzip.decompress(raw)), events=("end",)):
        if el.tag == "header":
            header = {c.tag: (c.text or "").strip() for c in el}
            continue
        if el.tag != "character":
            continue
        total += 1
        grade, jlpt, freq = (el.findtext(f"misc/{k}") for k in ("grade", "jlpt", "freq"))
        if not (grade or jlpt or freq):
            el.clear()
            continue
        rec: dict = {"source": DATASET, "version": header["date_of_creation"], "kanji": el.findtext("literal")}
        if grade:
            rec["grade"] = int(grade)
        strokes = texts(el, "misc/stroke_count")
        if strokes:
            rec["strokes"] = int(strokes[0])  # 2つ目以降は、よくある数え違い
        if freq:
            rec["freq"] = int(freq)
        if jlpt:
            rec["jlpt_old"] = int(jlpt)  # 2010年より前の旧試験の級（1〜4）。N1〜N5 ではない
        on = texts(el, "reading_meaning/rmgroup/reading[@r_type='ja_on']")
        kun = texts(el, "reading_meaning/rmgroup/reading[@r_type='ja_kun']")
        if on:
            rec["on"] = on
        if kun:
            rec["kun"] = kun
        meanings: dict[str, list[str]] = {}
        for m in el.iterfind("reading_meaning/rmgroup/meaning"):
            lang = m.get("m_lang", "en")
            if lang in MEANING_LANGS and (m.text or "").strip():
                meanings.setdefault(lang, []).append(m.text.strip())
        if meanings:
            rec["meanings"] = {lang: meanings[lang] for lang in MEANING_LANGS if lang in meanings}
        other = {tag: texts(el, f"reading_meaning/rmgroup/reading[@r_type='{r_type}']") for r_type, tag in OTHER_READINGS.items()}
        other = {tag: v for tag, v in other.items() if v}
        if other:
            rec["readings_other"] = other
        records.append(rec)
        el.clear()
    if not header.get("date_of_creation"):
        raise RuntimeError("header の date_of_creation が無い")
    joyo = sum(1 for r in records if r.get("grade", 99) <= 8)
    if joyo != 2136:
        raise RuntimeError(f"常用漢字（学年 1〜8）が 2,136 字ではない: {joyo}")
    return records, {**header, "characters": total}


def main() -> int:
    raw = cached("kanjidic2.xml.gz", lambda: opener().open(URL, timeout=120).read())
    records, header = convert(raw)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": "KANJIDIC2",
        "version": header["date_of_creation"],
        "database_version": header.get("database_version"),
        "url": PAGE,
        "xml": URL,
        "selection": f"KANJIDIC2 の {header['characters']:,} 字のうち、学年・旧日本語能力試験の級・新聞の頻度順位のどれかがある字",
        "license": "CC-BY-SA-4.0",
        "license_url": LICENCE,
        "attribution": (
            f"出典：KANJIDIC2（Electronic Dictionary Research and Development Group、{PAGE}）を加工して作成。"
            "This data uses the KANJIDIC dictionary file. The file is the property of the Electronic Dictionary "
            f"Research and Development Group, and is used in conformance with the Group's licence ({LICENCE})."
        ),
    }, raw)
    print(f"{DATASET}: {len(records)} 字（全 {header['characters']} 字のうち）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
