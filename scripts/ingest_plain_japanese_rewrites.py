#!/usr/bin/env python3
"""別冊「やさしい日本語書き換え例」（出入国在留管理庁・文化庁、2020年8月）の PDF から、
番号・語・読み・やさしい日本語の意味を取り出し、data/plain-japanese-rewrites.jsonl にする。

PDF は「番号・語彙・意味」の3列の表。ふりがなは本文の上に小さな文字の行として入っているので、
poppler の `pdftotext -bbox-layout` で語ごとの位置と大きさを取り、大きさで本文とふりがなを分ける。
- 語（語彙の列）の上のふりがなは、その語の読みとして残す
- 意味の列のふりがなは捨てる（意味は本文の文字だけ）
- 意味の中の「(No.41)」のような参照は、そのまま残し、参照先の番号を `see` にも入れる
取り出した番号が 1 から欠けずに続くかを確かめ、合わなければ止まる。

必要なもの: pdftotext（poppler-utils）
使い方: python3 scripts/ingest_plain_japanese_rewrites.py [--refresh]
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from common import cached, opener, write_dataset

DATASET = "plain-japanese-rewrites"
PAGE = "https://www.moj.go.jp/isa/support/portal/plainjapanese_guideline.html"
PDF_URL = "https://www.moj.go.jp/isa/content/930006077.pdf"
VERSION = "2020年8月"

# 列の境目（ポイント）と、文字の高さ（ポイント）。2020年8月版の PDF で測った値
TERM_X = 90.0      # これより左は番号の列
MEANING_X = 200.0  # これより右は意味の列
BASE_H = 12.2      # 本文の文字
RUBY_H = 6.1       # ふりがな
BIG_H = 21.9       # 五十音の見出し（「あ」など）
# 長い語は語彙の列の中で折り返す（行の間隔は約 20pt）。別の項目どうしは 45pt 以上離れている
WRAP_GAP = 30.0
# これより下はページ番号（y≈805）。各ページの最後の項目の意味に混ざらないよう除く
FOOTER_Y = 790.0
# 参照は「(No.41)」のほか「(NO.106)」とも書かれている
SEE = re.compile(r"\(No\.(\d+)\)", re.I)


def words_by_page(pdf: bytes) -> list[list[tuple[float, float, float, str]]]:
    """ページごとに (x, y, 高さ, 文字) の一覧を返す"""
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "in.pdf"
        src.write_bytes(pdf)
        out = subprocess.run(["pdftotext", "-bbox-layout", str(src), "-"], check=True, capture_output=True).stdout.decode("utf-8")
    pages = []
    for page in re.findall(r"<page [^>]*>(.*?)</page>", out, re.S):
        ws = []
        for x0, y0, _x1, y1, w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', page):
            ws.append((float(x0), float(y0), float(y1) - float(y0), html.unescape(w)))
        pages.append(ws)
    return pages


def near(h: float, target: float) -> bool:
    return abs(h - target) < 1.0


def lines(ws: list[tuple[float, float, float, str]]) -> list[tuple[float, str]]:
    """同じ高さ（y が近い）の語を1行にまとめ、左から順につなぐ"""
    rows: list[list[tuple[float, float, str]]] = []
    for x, y, _h, w in sorted(ws, key=lambda t: (t[1], t[0])):
        if rows and abs(rows[-1][0][1] - y) < 3:
            rows[-1].append((x, y, w))
        else:
            rows.append([(x, y, w)])
    return [(r[0][1], "".join(w for _x, _y, w in sorted(r))) for r in rows]


def convert(pdf: bytes) -> list[dict]:
    entries: list[dict] = []
    section = None
    for ws in words_by_page(pdf):
        # 五十音の見出し（大きな文字と、同じ高さに続く「いうえお」など）と、表の見出しの行は除く
        skip_y = [y for x, y, h, w in ws if near(h, BIG_H)]
        for x, y, h, w in ws:
            if near(h, BIG_H):
                section = w
        header_y = [y for x, y, h, w in ws if w == "番号" and x < TERM_X]
        def skipped(y: float) -> bool:
            return any(abs(y - s) < 14 for s in skip_y) or any(abs(y - s) < 4 for s in header_y)

        base = [t for t in ws if near(t[2], BASE_H) and not skipped(t[1]) and t[1] < FOOTER_Y]
        ruby = [t for t in ws if near(t[2], RUBY_H)]
        # 語彙の列の行。折り返した長い語は1つの語にまとめる（行の y の一覧と、つないだ文字）
        terms: list[tuple[list[float], str]] = []
        for y, text in lines([t for t in base if TERM_X <= t[0] < MEANING_X]):
            if terms and y - terms[-1][0][-1] < WRAP_GAP:
                terms[-1] = (terms[-1][0] + [y], terms[-1][1] + text)
            else:
                terms.append(([y], text))
        for i, (ys, term) in enumerate(terms):
            end = terms[i + 1][0][0] - 8 if i + 1 < len(terms) else float("inf")
            top = ys[0] - 8
            nums = [w for x, yy, h, w in base if x < TERM_X and top <= yy < end and w.isdigit()]
            meaning = "".join(text for _y, text in lines([t for t in base if t[0] >= MEANING_X and top <= t[1] < end]))
            # 語の各行の真上にあるふりがなを、行の順・左から順につなぐ
            reading = "".join(
                w for y in ys for x, yy, h, w in sorted(ruby, key=lambda t: t[0])
                if TERM_X <= x < MEANING_X and y - 9 <= yy < y
            ).replace(" ", "")
            if len(nums) != 1:
                raise RuntimeError(f"「{term}」の番号が1つに決まらない: {nums}")
            rec = {"source": DATASET, "version": VERSION, "no": int(nums[0]), "term": term}
            if reading:
                rec["reading"] = reading
            elif re.fullmatch(r"[ぁ-ゖァ-ヺー・]+", term):
                rec["reading"] = term  # かなだけの語には、ふりがなが無い
            rec["plain"] = meaning
            see = [int(n) for n in SEE.findall(meaning)]
            if see:
                rec["see"] = see
            rec["section"] = section
            entries.append(rec)
    numbers = [e["no"] for e in entries]
    if numbers != list(range(1, len(entries) + 1)):
        missing = sorted(set(range(1, max(numbers) + 1)) - set(numbers))
        raise RuntimeError(f"番号が 1 から続いていない（抜け: {missing[:10]}、重なり: {len(numbers) - len(set(numbers))}）")
    for e in entries:
        if not e["plain"]:
            raise RuntimeError(f"No.{e['no']}「{e['term']}」の意味が空")
        for n in e.get("see", []):
            if not 1 <= n <= len(entries):
                raise RuntimeError(f"No.{e['no']} が存在しない番号 {n} を参照している")
    return entries


def main() -> int:
    raw = cached("plain-japanese-rewrites-2020-08.pdf", lambda: opener().open(PDF_URL, timeout=120).read())
    records = convert(raw)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": "在留支援のためのやさしい日本語ガイドライン 別冊「やさしい日本語書き換え例」",
        "version": VERSION,
        "url": PAGE,
        "pdf": PDF_URL,
        "license": "PDL-1.0",
        "attribution": f"出典：出入国在留管理庁・文化庁「在留支援のためのやさしい日本語ガイドライン 別冊 やさしい日本語書き換え例」（{PAGE}）を加工して作成",
    }, raw)
    print(f"{DATASET}: {len(records)} 語", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
