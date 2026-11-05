#!/usr/bin/env python3
"""厚生労働省「外国人向け多言語説明資料」（医療機関の書類、13言語・日本語併記）を、
data/mhlw-multilingual-medical-docs.jsonl にする。

1行が1つの資料の1つの言語（資料の番号・名前・分類・言語・ファイルと、文字の単位の並び）。
- 資料の一覧は、配布ページの表から読む（分類1・分類2・資料名「（１）診療申込書」と、Word・Excel のファイルへのリンク）。
  PDF は同じ内容なので使わない。
- Word（.doc・.docx）と Excel（.xls・.xlsx）を読む。古い形式（.doc・.xls）は、LibreOffice（soffice）で
  .docx・.xlsx に変えてから読む。取得したファイルと変えたファイルは .cache/mhlw-multilingual-medical-docs/ に置く。
- 文字の単位: Word は段落（表のマスの中の段落も）、Excel はセル。資料は、各言語の文を「/」でつないで並べている
  （「Nama/Name/氏名（カナ）」。次の段落の頭に「/」を置いて続けることもある）。
  - 「/」で始まる段落は、前の段落に続ける。
  - 言語の並びは、英語は「英語/日本語」、中国語・韓国語・ポルトガル語・スペイン語は「訳/日本語」、
    ほかの8言語は「訳/英語/日本語」。
  - 「/」で区切った部分の文字の種類（日本語は最後で、仮名か漢字がある。英語はラテン文字、訳はその言語の文字）が、
    この並びに合う区切り方が1つだけのときに、`ja`・`en`・`tr` に分ける。合わないとき（日付の「YYYY/MM/DD」のように
    文の中に「/」があって区切り方が決まらない、など）は、`text` に元の文字のまま入れる。
- 取得は1つずつ、1秒の間を置く。
- 第三者の権利の表記（「©」「Copyright」「無断転載」など）がある資料が見つかったら止まる（目で確かめるため）。

使い方: python3 scripts/ingest_mhlw_multilingual_medical_docs.py [--refresh]
"""

from __future__ import annotations

import html
import itertools
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from common import CACHE, cached, opener, write_dataset

DATASET = "mhlw-multilingual-medical-docs"
PAGE = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/kokusai/setsumei-ml.html"
TITLE = "外国人向け多言語説明資料"
TERMS_URL = "https://www.mhlw.go.jp/chosakuken/index.html"
WAIT = 1.0
DIR = CACHE / DATASET

LANGS = {
    "英語": "en", "中国語": "zh-Hans", "韓国語": "ko", "ポルトガル語": "pt", "スペイン語": "es",
    "ウクライナ語": "uk", "ヒンディー語": "hi", "インドネシア語": "id", "ネパール語": "ne",
    "タガログ語": "tl", "タイ語": "th", "ベトナム語": "vi", "アラビア語": "ar",
}
# 言語ごとの並び（最後が日本語）
ORDER = {"en": ["en", "ja"], **{k: ["tr", "ja"] for k in ("zh-Hans", "ko", "pt", "es")}}
for _k in ("uk", "hi", "id", "ne", "tl", "th", "vi", "ar"):
    ORDER[_k] = ["tr", "en", "ja"]
# 言語ごとの版（配布ページの注記による）
VERSIONS = {"en": "2018年3月版", "zh-Hans": "2018年3月版", "ko": "2018年3月版", "pt": "2018年3月版", "es": "2018年3月版",
            "uk": "2022年7月（ウクライナ語を追加）", "ar": "2025年8月（アラビア語を追加）"}
for _k in ("hi", "id", "ne", "tl", "th", "vi"):
    VERSIONS[_k] = "2024年4月（言語を追加）"
EDITABLE = re.compile(r"\.(docx?|xlsx?)$", re.I)
TITLE_CELL = re.compile(r"^[（(]\s*([0-9０-９]+)\s*[）)]\s*(.+)$")
THIRD_PARTY = re.compile(r"©|Copyright|無断転載|無断複製|All rights reserved", re.I)
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

KANA = re.compile(r"[぀-ヿｦ-ﾟ]")
HAN = re.compile(r"[㐀-鿿豈-﫿]")
LATIN = re.compile(r"[A-Za-zÀ-ɏḀ-ỿ]")
SCRIPTS = {
    "ko": re.compile(r"[가-힯ᄀ-ᇿ]"),
    "th": re.compile(r"[฀-๿]"),
    "hi": re.compile(r"[ऀ-ॿ]"),
    "ne": re.compile(r"[ऀ-ॿ]"),
    "ar": re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]"),
    "uk": re.compile(r"[Ѐ-ӿ]"),
}


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def documents(page: str) -> list[dict]:
    """配布ページの表から、資料（番号・名前・分類）ごとの、Word・Excel のファイル（言語・URL）を読む"""
    docs: list[dict] = []
    cat1 = cat2 = ""
    for m in re.finditer(r"(?is)<td([^>]*)>(.*?)</td>", page):
        attrs, inner = m.group(1), m.group(2)
        links = re.findall(r'(?is)<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', inner)
        files = [(urllib.parse.urljoin(PAGE, html.unescape(h)), clean(t)) for h, t in links if EDITABLE.search(h)]
        text = clean(inner)
        if files:
            if not docs:
                raise ValueError("資料名より前にファイルのリンクがある")
            for url, label in files:
                lang = LANGS.get(re.sub(r"［.*$", "", label).strip())
                if not lang:
                    raise ValueError(f"言語が分からない: {label!r} {url}")
                docs[-1]["files"].append({"lang": lang, "url": url})
            continue
        if re.search(r"\.pdf", inner, re.I):
            continue
        t = TITLE_CELL.match(text)
        if t:
            no = int(t.group(1).translate(str.maketrans("０１２３４５６７８９", "0123456789")))
            docs.append({"no": no, "title": t.group(2).strip(), "category": [c for c in (cat1, cat2) if c], "files": []})
        elif text and 'colspan="5"' in attrs:
            cat2 = text
        elif text:
            cat1, cat2 = text, ""
    return [d for d in docs if d["files"]]


def cache_name(url: str) -> str:
    path = urllib.parse.urlsplit(url).path
    return re.sub(r"[^A-Za-z0-9._-]", "_", path.strip("/").replace("/", "__"))


def fetch_all(docs: list[dict]) -> dict[str, bytes]:
    """ファイルを取得する（.cache に置く）。URL → 中身"""
    DIR.mkdir(parents=True, exist_ok=True)
    out: dict[str, bytes] = {}
    for f in (f for d in docs for f in d["files"]):
        url = f["url"]
        if url in out:
            continue

        def fetch(url=url) -> bytes:
            time.sleep(WAIT)
            return opener().open(url, timeout=120).read()

        out[url] = cached(f"{DATASET}/{cache_name(url)}", fetch)
    return out


TARGET = {".doc": "docx", ".xls": "xlsx"}


def converted(url: str) -> Path:
    """古い形式（.doc・.xls）を LibreOffice で .docx・.xlsx に変えたファイル（.cache に置く）"""
    src = DIR / cache_name(url)
    ext = src.suffix.lower()
    if ext in (".docx", ".xlsx"):
        return src
    return DIR / "converted" / (src.stem + "." + TARGET[ext])


def convert_old_formats(docs: list[dict], batch: int = 40) -> None:
    """まだ変えていない古い形式のファイルを、まとめて LibreOffice で変える"""
    todo: dict[str, list[Path]] = {}
    for f in (f for d in docs for f in d["files"]):
        src = DIR / cache_name(f["url"])
        ext = src.suffix.lower()
        if ext in TARGET and not converted(f["url"]).exists():
            todo.setdefault(TARGET[ext], []).append(src)
    if not todo:
        return
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("古い形式のファイル（.doc・.xls）を読むには LibreOffice（soffice）が要る")
    out_dir = DIR / "converted"
    out_dir.mkdir(exist_ok=True)
    for target, srcs in todo.items():
        for i in range(0, len(srcs), batch):
            subprocess.run([soffice, "--headless", "--convert-to", target, "--outdir", str(out_dir),
                            *map(str, srcs[i:i + batch])], check=True, capture_output=True, timeout=1800)


def word_paragraphs(path: Path) -> list[str]:
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    out = []
    for p in root.iter(W + "p"):
        s = "".join((t.text or "") if t.tag == W + "t" else "\t" for t in p.iter() if t.tag in (W + "t", W + "tab"))
        s = re.sub(r"[ \t　]+", " ", s).strip()
        if s:
            out.append(s)
    return out


def excel_cells(path: Path) -> list[str]:
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(S + "si"):
            # ふりがな（rPh）は除く
            shared.append("".join(t.text or "" for r in si if r.tag in (S + "t", S + "r") for t in r.iter(S + "t")))
    sheets = sorted((n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)),
                    key=lambda n: int(re.search(r"(\d+)\.xml$", n).group(1)))
    out = []
    for name in sheets:
        for c in ET.fromstring(z.read(name)).iter(S + "c"):
            v, inline = c.find(S + "v"), c.find(S + "is")
            if c.get("t") == "s" and v is not None:
                s = shared[int(v.text)]
            elif inline is not None:
                s = "".join(t.text or "" for t in inline.iter(S + "t"))
            elif c.get("t") == "str" and v is not None:
                s = v.text or ""
            else:
                continue
            for line in s.splitlines():
                line = re.sub(r"[ \t　]+", " ", line).strip()
                if line:
                    out.append(line)
    return out


def units(paragraphs: list[str]) -> list[str]:
    """「/」で始まる段落を、前の段落に続ける"""
    out: list[str] = []
    for p in paragraphs:
        if out and p[:1] in "/／":
            out[-1] += p
        else:
            out.append(p)
    return out


def fits(part: str, kind: str, lang: str) -> bool:
    part = part.strip()
    if not part or not re.search(r"\w", part):
        return False
    if kind == "ja":
        return bool(KANA.search(part) or HAN.search(part))
    if KANA.search(part):
        return False
    if kind == "en":
        return bool(LATIN.search(part)) and not HAN.search(part)
    if lang == "zh-Hans":
        return bool(HAN.search(part))
    if lang in SCRIPTS:
        return bool(SCRIPTS[lang].search(part))
    return bool(LATIN.search(part)) and not HAN.search(part)  # pt・es・id・tl・vi


def split_unit(unit: str, lang: str) -> dict:
    """「/」で区切った部分が、言語の並びに合う区切り方が1つだけなら分ける。そうでなければ元の文字のまま"""
    order = ORDER[lang]
    seps = [m.start() for m in re.finditer(r"[/／]", unit)]
    found = []
    for cut in itertools.combinations(seps, len(order) - 1):
        bounds = [-1, *cut, len(unit)]
        parts = [unit[bounds[i] + 1:bounds[i + 1]].strip() for i in range(len(order))]
        if all(fits(p, k, lang) for p, k in zip(parts, order)):
            found.append(parts)
            if len(found) > 1:
                break
    if len(found) == 1:
        return {k: p for k, p in zip(order, found[0])}
    return {"text": unit}


def convert(docs: list[dict]) -> list[dict]:
    records = []
    for d in docs:
        for f in d["files"]:
            path = converted(f["url"])
            paras = word_paragraphs(path) if path.suffix == ".docx" else excel_cells(path)
            joined = "\n".join(paras)
            if THIRD_PARTY.search(joined):
                raise ValueError(f"（{d['no']}）{d['title']} {f['lang']}: 第三者の権利の表記がある。目で確かめる")
            us = [split_unit(u, f["lang"]) for u in units(paras)]
            if not us:
                raise ValueError(f"（{d['no']}）{d['title']} {f['lang']}: 文字が無い")
            version = "2025年2月（資料を追加）" if d["no"] == 53 else VERSIONS[f["lang"]]
            records.append({
                "source": DATASET,
                "version": version,
                "no": d["no"],
                "title": d["title"],
                "category": d["category"],
                "lang": f["lang"],
                "format": Path(urllib.parse.urlsplit(f["url"]).path).suffix.lstrip(".").lower(),
                "url": f["url"],
                "units": us,
            })
    return records


def main() -> int:
    DIR.mkdir(parents=True, exist_ok=True)

    def fetch_page() -> bytes:
        return opener().open(PAGE, timeout=60).read()

    page_raw = cached(f"{DATASET}/page.html", fetch_page)
    docs = documents(page_raw.decode("utf-8"))
    files = fetch_all(docs)
    convert_old_formats(docs)
    records = convert(docs)
    split = sum(1 for r in records for u in r["units"] if "ja" in u)
    total = sum(len(r["units"]) for r in records)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": f"厚生労働省「{TITLE}」",
        "version": "言語ごと（2018年3月版。ウクライナ語は2022年7月、ヒンディー語など6言語は2024年4月、アラビア語は2025年8月に追加）",
        "url": PAGE,
        "license": "PDL-1.0",
        "license_url": TERMS_URL,
        "attribution": f"出典：厚生労働省「{TITLE}」（{PAGE}）を加工して作成",
        "documents": len(docs),
        "units": total,
        "units_split": split,
        "source_sha256_of": "配布ページと、各ファイル（Word・Excel）を、表の並び順につないだもの",
    }, page_raw + b"".join(files[f["url"]] for d in docs for f in d["files"]))
    print(f"{DATASET}: {len(docs)} 資料・{len(records)} ファイル・単位 {total}（分けられたもの {split}）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
