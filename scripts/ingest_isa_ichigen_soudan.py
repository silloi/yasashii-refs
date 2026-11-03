#!/usr/bin/env python3
"""出入国在留管理庁「外国人受入環境整備交付金を活用した地方公共団体における一元的相談窓口の現況について」の
Excel の「参考」のシート（一元的相談窓口の一覧）を、data/isa-ichigen-soudan.jsonl にする。

1行が1つの窓口の場所。
- シートでは、都道府県・設置者・窓口の名前・開所日・開所時間などのセルが縦に結合されている。
  結合の範囲の左上の値を、範囲のすべてのセルに配ってから読む（豊田市の支所のように、同じ窓口の別の場所が続く行がある）。
- セルの文字は、ふりがな（フリガナ情報、rPh）を除いて読む。
- 設置者の「※」は、窓口を共同で運営していることの印（広島市と安芸郡の4町）。`joint` にして、名前からは除く。
- 開所日は「〇」（U+3007）と「○」（U+25CB）の両方が使われている。どちらも開所の印として読む。
- 文字の中の空白の連続（セルの中の折り返し）は1つにまとめる。値が「－」だけのものは、値が無いとみなす。
設置者の数が表題の団体数（290）と合うかを確かめ、合わなければ止まる。

使い方: python3 scripts/ingest_isa_ichigen_soudan.py [--refresh]
"""

from __future__ import annotations

import collections
import io
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

from common import cached, opener, write_dataset

DATASET = "isa-ichigen-soudan"
PAGE = "https://www.moj.go.jp/isa/support/coexistence/nyuukokukanri02_00039.html"
XLSX_URL = "https://www.moj.go.jp/isa/content/001468791.xlsx"
TITLE = "令和７年度外国人受入環境整備交付金を活用した地方公共団体における一元的相談窓口の現況について"
SHEET = "参考"

M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
# 列（1始まり）: 都道府県名・設置者・窓口名称・所在地・電話番号・開所日（月〜祝の8列）・開所時間・備考
COL_PREF, COL_EST, COL_NAME, COL_ADDR, COL_TEL, COL_HOURS, COL_NOTES = 1, 2, 3, 4, 5, 14, 15
DAY_COLS = {6: "月", 7: "火", 8: "水", 9: "木", 10: "金", 11: "土", 12: "日", 13: "祝"}
OPEN_MARKS = {"〇", "○"}


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


def ref_to_rc(ref: str) -> tuple[int, int]:
    m = re.fullmatch(r"([A-Z]+)(\d+)", ref)
    col = 0
    for ch in m.group(1):
        col = col * 26 + ord(ch) - 64
    return int(m.group(2)), col


def read_sheet(raw: bytes) -> tuple[dict[int, dict[int, str]], str]:
    z = zipfile.ZipFile(io.BytesIO(raw))
    shared = shared_strings(z)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    target = None
    for s in wb.find(M + "sheets"):
        if s.get("name").strip() == SHEET:
            t = rels[s.get(R + "id")].lstrip("/")
            target = t if t.startswith("xl/") else "xl/" + t
    if target is None:
        raise RuntimeError(f"シート「{SHEET}」が無い")
    sheet = ET.fromstring(z.read(target))
    cells: dict[tuple[int, int], str] = {}
    for c in sheet.iter(M + "c"):
        v, t = c.find(M + "v"), c.get("t")
        if t == "s" and v is not None:
            value = shared[int(v.text)]
        elif t == "inlineStr":
            value = "".join(x.text or "" for x in c.iter(M + "t"))
        elif v is not None:
            value = v.text or ""
        else:
            continue
        cells[ref_to_rc(c.get("r"))] = value
    for m in sheet.iter(M + "mergeCell"):  # 結合の範囲の左上の値を、範囲のすべてのセルに配る
        a, b = m.get("ref").split(":")
        (r1, c1), (r2, c2) = ref_to_rc(a), ref_to_rc(b)
        top = cells.get((r1, c1))
        if top is None:
            continue
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                cells.setdefault((r, c), top)
    rows: dict[int, dict[int, str]] = collections.defaultdict(dict)
    for (r, c), value in cells.items():
        rows[r][c] = value
    title = next((v for r in sorted(rows) for v in rows[r].values() if "団体）" in v), "")
    return rows, title


def clean(value: str | None) -> str:
    """空白の連続を1つにまとめ、前後の空白を削る。「－」だけの値は空にする"""
    if not value:
        return ""
    value = re.sub(r"\s{2,}", lambda m: "　" if "　" in m.group(0) else " ", value.replace("\n", " ")).strip()
    return "" if re.fullmatch(r"[-－ー―]+", value) else value


def convert(raw: bytes) -> tuple[list[dict], str]:
    rows, title = read_sheet(raw)
    m = re.search(r"（([０-９0-9]+)団体）", title)
    if not m:
        raise RuntimeError(f"表題に団体数が無い: {title!r}")
    expected = int(m.group(1).translate(str.maketrans("０１２３４５６７８９", "0123456789")))
    version = next((clean(v) for r in sorted(rows)[:6] for v in rows[r].values() if "時点" in v), "")
    header = next(r for r in sorted(rows) if rows[r].get(COL_NAME) == "窓口名称")
    records: list[dict] = []
    for r in sorted(rows):
        row = rows[r]
        if r <= header + 1 or not clean(row.get(COL_NAME)):
            continue
        if clean(row.get(COL_PREF)).startswith(("※", "（注")):
            break  # 表の下の注記
        establisher = clean(row.get(COL_EST))
        rec = {
            "source": DATASET,
            "version": version,
            "no": len(records) + 1,
            "prefecture": clean(row.get(COL_PREF)),
            "establisher": establisher.rstrip("※").strip(),
        }
        if establisher.endswith("※"):
            rec["joint"] = True
        rec["name"] = clean(row.get(COL_NAME))
        for key, col in (("address", COL_ADDR), ("phone", COL_TEL)):
            if clean(row.get(col)):
                rec[key] = clean(row.get(col))
        days = [day for col, day in DAY_COLS.items() if clean(row.get(col)) in OPEN_MARKS]
        unknown = [clean(row.get(col)) for col in DAY_COLS if clean(row.get(col)) and clean(row.get(col)) not in OPEN_MARKS]
        if unknown:
            raise RuntimeError(f"{r}行目: 開所日の印が読めない: {unknown}")
        if days:
            rec["days"] = days
        for key, col in (("hours", COL_HOURS), ("notes", COL_NOTES)):
            if clean(row.get(col)):
                rec[key] = clean(row.get(col))
        if not rec["prefecture"] or not rec["establisher"]:
            raise RuntimeError(f"{r}行目: 都道府県か設置者が空")
        records.append(rec)
    establishers = {(x["prefecture"], x["establisher"]) for x in records}
    if len(establishers) != expected:
        raise RuntimeError(f"設置者の数が表題の {expected} 団体と合わない: {len(establishers)}")
    return records, version


def main() -> int:
    raw = cached("isa-ichigen-soudan-r7.xlsx", lambda: opener().open(XLSX_URL, timeout=120).read())
    records, version = convert(raw)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": f"{TITLE}（参考: 一元的相談窓口の一覧）",
        "version": version,
        "published": "令和8年8月",
        "url": PAGE,
        "xlsx": XLSX_URL,
        "license": "PDL-1.0",
        "attribution": f"出典：出入国在留管理庁「{TITLE}」（{PAGE}）を加工して作成",
    }, raw)
    print(f"{DATASET}: {len(records)} 件（{len({(r['prefecture'], r['establisher']) for r in records})} 団体）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
