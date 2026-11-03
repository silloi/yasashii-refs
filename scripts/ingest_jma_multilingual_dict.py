#!/usr/bin/env python3
"""気象庁 多言語辞書（xlsx）を取得し、data/jma-multilingual-dict.jsonl にする。

xlsx は標準ライブラリ（zipfile と XML）で読む。
- 「多言語辞書（本体）」のシートの1行が1項目。番号の無い行（末尾の空行）は飛ばす
- セルの文字は、Excel のふりがな（<rPh>）を除いて読む
- 版は「更新履歴」のシートの、いちばん新しい更新日
- 空の欄は書かない（No.181 は日本語の欄が空。元のデータのまま）

使い方: python3 scripts/ingest_jma_multilingual_dict.py [--refresh]
"""

from __future__ import annotations

import datetime
import io
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

from common import cached, opener, write_dataset

DATASET = "jma-multilingual-dict"
PAGE = "https://www.data.jma.go.jp/developer/multilingual.html"
XLSX_URL = "https://www.data.jma.go.jp/developer/jma_multilingual.xlsx"
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# 列の見出しと、出力の名前（言語は BCP 47）
HEADER = ["No.", "種別", "情報種別等", "日本語", "英語", "中国語(簡体字)", "中国語(繁体字)", "韓国語", "ポルトガル語", "スペイン語",
          "インドネシア語", "ベトナム語", "タガログ語", "タイ語", "ネパール語", "クメール語", "ビルマ語", "モンゴル語",
          "備考", "XMLコード表", "コード", "更新履歴"]
LANGS = ["en", "zh-Hans", "zh-Hant", "ko", "pt", "es", "id", "vi", "tl", "th", "ne", "km", "my", "mn"]  # 4〜17列
EXTRA = {18: "note", 19: "code_table", 20: "code", 21: "history"}


def _text(si: ET.Element) -> str:
    """共有文字列の1つ分。<rPh>（ふりがな）の中の文字は入れない"""
    out = []
    for child in si:
        if child.tag == M + "t":
            out.append(child.text or "")
        elif child.tag == M + "r":
            t = child.find(M + "t")
            out.append((t.text or "") if t is not None else "")
    return "".join(out)


def _col(ref: str) -> int:
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_sheets(raw: bytes) -> dict[str, list[dict[int, str]]]:
    z = zipfile.ZipFile(io.BytesIO(raw))
    strings = [_text(si) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(M + "si")]
    names = re.findall(r'<sheet [^>]*name="([^"]+)"', z.read("xl/workbook.xml").decode("utf-8"))
    sheets = {}
    for i, name in enumerate(names, start=1):
        rows = []
        for r in ET.fromstring(z.read(f"xl/worksheets/sheet{i}.xml")).iter(M + "row"):
            cells = {}
            for c in r.findall(M + "c"):
                v = c.find(M + "v")
                if v is None:
                    continue
                cells[_col(c.get("r"))] = strings[int(v.text)] if c.get("t") == "s" else v.text
            rows.append(cells)
        sheets[name] = rows
    return sheets


def latest_update(history: list[dict[int, str]]) -> str:
    """更新履歴のシートの更新日（Excel の日付の数値）のうち、いちばん新しいもの"""
    serials = [int(float(r[1])) for r in history if re.fullmatch(r"\d+(\.0+)?", (r.get(1) or "").strip())]
    return (datetime.date(1899, 12, 30) + datetime.timedelta(days=max(serials))).isoformat()


def convert(raw: bytes) -> tuple[list[dict], str]:
    sheets = read_sheets(raw)
    version = latest_update(sheets["更新履歴"])
    rows = sheets["多言語辞書（本体）"]
    header = [(rows[0].get(i) or "").strip() for i in range(len(HEADER))]
    if header != HEADER:
        raise RuntimeError(f"列が想定と違う: {header}")
    records = []
    for cells in rows[1:]:
        no = (cells.get(0) or "").strip()
        if not no:
            continue
        get = lambda i: (cells.get(i) or "").strip()
        rec: dict = {"source": DATASET, "version": version, "no": int(no), "kind": get(1), "category": get(2)}
        if get(3):
            rec["ja"] = get(3)
        rec["tr"] = {lang: get(4 + k) for k, lang in enumerate(LANGS) if get(4 + k)}
        for i, key in EXTRA.items():
            if get(i):
                rec[key] = get(i)
        records.append(rec)
    nos = [r["no"] for r in records]
    if len(set(nos)) != len(nos):
        raise RuntimeError("番号が重なっている")
    return records, version


def main() -> int:
    raw = cached("jma-multilingual-dict.xlsx", lambda: opener().open(XLSX_URL, timeout=180).read())
    records, version = convert(raw)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": "気象庁 多言語辞書",
        "version": version,
        "url": PAGE,
        "xlsx": XLSX_URL,
        "license": "PDL-1.0",
        "attribution": f"出典：気象庁ホームページ「多言語辞書データ」（{PAGE}）を加工して作成",
    }, raw)
    print(f"{DATASET}: {len(records)} 項目（版 {version}）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
