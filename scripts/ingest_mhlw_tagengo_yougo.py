#!/usr/bin/env python3
"""厚生労働省「雇用管理に役立つ多言語用語集」の Excel 版を、data/mhlw-tagengo-yougo.jsonl にする。

1行が1つの用語（418語）。やさしい日本語の用語・定義・例文と、14言語の訳（用語・定義・例文）。
- Excel は15シート（やさしい日本語と14言語）。各言語のシートには、日本語の列（カテゴリー・項番・用語・定義・例文）と、
  その言語の列（用語・定義・例文）がある。
- 用語の順番と項番は「やさしい日本語」のシートのものを使う。ポルトガル語とタガログ語のシートは、項番の振り方と並びが
  ほかのシートと違う（同じ項番が別の用語を指す）。そのため、どのシートも日本語の列（カテゴリー・用語・定義・例文）で
  突き合わせる。418語すべてが、どのシートにもちょうど1回ずつあることを確かめ、合わなければ止まる。
- セルの文字は、ふりがな（フリガナ情報、rPh）を除いて読む。セルの中の改行は空白1つにする（モンゴル語のシートなどは、
  表示の折り返しのための改行が多い）。前後の空白は除く。
- 用語の「打（う）ち切（き）り補償（ほしょう）」のような読みの書き方から、括弧を除いた形（`term`）と、読み（`reading`）を作る。
  読みは、括弧の直前の漢字（数字と、漢字のあいだの「・」を含む）を、括弧の中の読みに置き換えたもの。片仮名などはそのまま。
- `web_id` は、厚生労働省のウェブ版の各言語のページの、その用語の行の id（カテゴリーの番号とカテゴリーの中の順番。例: c06_07）。

使い方: python3 scripts/ingest_mhlw_tagengo_yougo.py [--refresh]
"""

from __future__ import annotations

import re
import sys
import zipfile
import io
import xml.etree.ElementTree as ET

from common import cached, opener, write_dataset

DATASET = "mhlw-tagengo-yougo"
PAGE = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/jigyounushi/tagengoyougosyu.html"
WEB = "https://www.mhlw.go.jp/seisakunitsuite/bunya/koyou_roudou/koyou/jigyounushi/tagengoyougosyu/index.html"
XLSX_URL = "https://www.mhlw.go.jp/content/000761428.xlsx"
TITLE = "雇用管理に役立つ多言語用語集"
BASE_SHEET = "やさしい日本語"
LANGS = {  # シートの名前 → BCP 47
    "英語": "en", "中国語（簡体字）": "zh-Hans", "中国語（繁体字）": "zh-Hant", "韓国語": "ko",
    "スペイン語": "es", "ポルトガル語": "pt", "タガログ語": "tl", "ベトナム語": "vi", "ネパール語": "ne",
    "インドネシア語": "id", "タイ語": "th", "ミャンマー語": "my", "モンゴル語": "mn", "カンボジア語": "km",
}
TERMS = 418

M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
# 列（1始まり）: カテゴリー・項番・用語・定義・例文（日本語）、用語・定義・例文（各言語）
COL_CAT, COL_NO, COL_TERM, COL_DEF, COL_EX = 1, 2, 3, 4, 5
COL_TR = {"term": 6, "definition": 7, "example": 8}

KANJI_RUN = re.compile(r"[一-鿿々〆ヶ0-9０-９]+(?:・[一-鿿々〆ヶ0-9０-９]+)*$")
RUBY = re.compile(r"（([ぁ-ゖー・]+)）")


def shared_strings(z: zipfile.ZipFile) -> list[str]:
    def text(si: ET.Element) -> str:
        out = []
        for el in si:  # <t> と <r><t> だけを読む（<rPh> はふりがな）
            if el.tag == M + "t":
                out.append(el.text or "")
            elif el.tag == M + "r":
                t = el.find(M + "t")
                out.append((t.text or "") if t is not None else "")
        return "".join(out)
    return [text(si) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(M + "si")]


def col_number(ref: str) -> int:
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n


def read_sheets(raw: bytes) -> dict[str, list[dict[int, str]]]:
    z = zipfile.ZipFile(io.BytesIO(raw))
    shared = shared_strings(z)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    sheets = {}
    for s in wb.find(M + "sheets"):
        target = rels[s.get(R + "id")].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        rows = []
        for r in ET.fromstring(z.read(target)).iter(M + "row"):
            cells = {}
            for c in r.findall(M + "c"):
                v, t = c.find(M + "v"), c.get("t")
                if t == "s" and v is not None:
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(M + "t"))
                elif v is not None:
                    val = v.text
                else:
                    continue
                cells[col_number(c.get("r"))] = clean(val)
            if cells.get(COL_NO, "").isdigit():  # 用語の行だけ（見出しの行は除く）
                rows.append(cells)
        sheets[s.get("name").strip()] = rows
    return sheets


def clean(s: str) -> str:
    s = re.sub(r"[ \t]*[\r\n]+[ \t]*", " ", s or "")
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip(" \t")


def split_ruby(s: str) -> tuple[str, str]:
    """「打（う）ち切（き）り補償（ほしょう）」→（「打ち切り補償」,「うちきりほしょう」）"""
    plain, reading, pos = [], [], 0
    for m in RUBY.finditer(s):
        before = s[pos:m.start()]
        run = KANJI_RUN.search(before)
        if not run:
            raise ValueError(f"読みの前に漢字が無い: {s!r}")
        plain.append(before)
        reading.append(before[:run.start()] + m.group(1))
        pos = m.end()
    plain.append(s[pos:])
    reading.append(s[pos:])
    plain_s, reading_s = "".join(plain), "".join(reading)
    if re.search(r"[一-鿿々〆]", reading_s):
        raise ValueError(f"読みに漢字が残る: {s!r} → {reading_s!r}")
    return plain_s, reading_s


def ja_key(cells: dict[int, str]) -> tuple[str, str, str, str]:
    return tuple(cells.get(k, "") for k in (COL_CAT, COL_TERM, COL_DEF, COL_EX))


def xlsx_modified(raw: bytes) -> str:
    """Excel の文書のプロパティの更新日（docProps/core.xml の modified）。版として使う"""
    core = zipfile.ZipFile(io.BytesIO(raw)).read("docProps/core.xml").decode("utf-8")
    m = re.search(r"<dcterms:modified[^>]*>(\d{4}-\d{2}-\d{2})", core)
    if not m:
        raise ValueError("Excel の更新日が読めない")
    return m.group(1)


def convert(raw: bytes) -> tuple[list[dict], str]:
    version = xlsx_modified(raw)
    sheets = read_sheets(raw)
    if set(sheets) != {BASE_SHEET, *LANGS}:
        raise ValueError(f"シートが想定と違う: {sorted(sheets)}")
    base = sheets[BASE_SHEET]
    if len(base) != TERMS or [int(c[COL_NO]) for c in base] != list(range(1, TERMS + 1)):
        raise ValueError(f"やさしい日本語のシートの用語の数か項番が想定と違う: {len(base)}")
    keys = [ja_key(c) for c in base]
    if len(set(keys)) != TERMS:
        raise ValueError("日本語の列が同じ用語がある")
    translations: dict[str, dict[tuple, dict[str, str]]] = {}
    for sheet, lang in LANGS.items():
        rows = sheets[sheet]
        by_key = {ja_key(c): c for c in rows}
        if len(rows) != TERMS or set(by_key) != set(keys):
            raise ValueError(f"{sheet}: 日本語の列が、やさしい日本語のシートと合わない")
        tr = {}
        for k, c in by_key.items():
            t = {name: c[col] for name, col in COL_TR.items() if c.get(col)}
            if "term" not in t:
                raise ValueError(f"{sheet}: 訳の用語が無い: {k[1]}")
            tr[k] = t
        translations[lang] = tr
    records, per_cat = [], {}
    for cells, k in zip(base, keys):
        cat = cells[COL_CAT]
        cat_no = int(cat.split(".", 1)[0])
        per_cat[cat_no] = per_cat.get(cat_no, 0) + 1
        term, reading = split_ruby(cells[COL_TERM])
        records.append({
            "source": DATASET,
            "version": version,
            "no": int(cells[COL_NO]),
            "web_id": f"c{cat_no:02d}_{per_cat[cat_no]:02d}",
            "category": cat,
            "term": term,
            "reading": reading,
            "ja_easy": {"term": cells[COL_TERM], "definition": cells[COL_DEF], "example": cells[COL_EX]},
            "tr": {lang: translations[lang][k] for lang in LANGS.values()},
        })
    return records, version


def main() -> int:
    raw = cached("mhlw-tagengo-yougo.xlsx", lambda: opener().open(XLSX_URL, timeout=120).read())
    records, version = convert(raw)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": f"厚生労働省「{TITLE}」（Excel 版）",
        "version": version,
        "url": PAGE,
        "web": WEB,
        "xlsx": XLSX_URL,
        "languages": ["ja-easy", *LANGS.values()],
        "license": "PDL-1.0",
        "license_url": "https://www.mhlw.go.jp/chosakuken/index.html",
        "attribution": f"出典：厚生労働省「{TITLE}」（{PAGE}）を加工して作成",
    }, raw)
    print(f"{DATASET}: {len(records)} 語（{len(LANGS)} 言語）、版 {version}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
