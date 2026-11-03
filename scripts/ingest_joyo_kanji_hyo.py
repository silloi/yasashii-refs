#!/usr/bin/env python3
"""常用漢字表（平成22年内閣告示第2号）の PDF から、本表（字種・康熙字典体・音訓・例・備考）と付表（熟字訓など）を取り出し、
data/joyo-kanji-hyo.jsonl にする。

PDF は InDesign で組んだ表。poppler の `pdftotext -bbox-layout` で語ごとの位置と大きさを取り、位置で列を分ける。
- 本表は「漢字・音訓・例・備考」の4列。漢字の列は大きな文字（高さ約21.5pt）、ほかは本文の文字（約12.55pt）
- 漢字の列の、字種の右の丸括弧は康熙字典体、角括弧は許容字体（表の見方 5・6）
- 音訓の列で1字下げのもの（約10.5pt右）は、特別なもの・用法のごく狭いもの（表の見方 7）
- 例が長いと次の行に折り返す（前の行は「，」で終わる）
- 備考の1つのます目には、注記がいくつか入ることもあり、1つの注記が折り返すこともある。前の行が「，」で終わるか、
  列の右端近くまで届いていて「。」で終わらないときは、続きとみなす
- 付表は、読み（平仮名）と語の組を2段に並べたもの。1つの読みに語が2つあるもの（「河原・川原」など）がある
本表が 2,136 字で重ならないこと、各字に音訓があること、音訓が片仮名か平仮名だけであることを確かめ、合わなければ止まる。

必要なもの: pdftotext（poppler-utils）
使い方: python3 scripts/ingest_joyo_kanji_hyo.py [--refresh]
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from common import cached, opener, write_dataset

DATASET = "joyo-kanji-hyo"
PAGE = "https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/"
PDF_URL = "https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf"
VERSION = "平成22年内閣告示第2号"

# 平成22年11月30日付けの PDF（164ページ）で測った値（ポイント）。偶数ページは奇数ページより約1.9pt左にずれる
MAIN_FIRST_PAGE = 11   # 本表の最初のページ（見出し「本表」と列の見出しがある）
TOP_Y = 100.0          # これより上は柱（「ア－イ」など）
BOTTOM_Y = 880.0       # これより下はノンブルなど
BIG_H = 19.0           # これより高い文字は漢字の列の字（字種・康熙字典体は約21.5pt、許容字体は約19.8pt）
TITLE_H = 21.65        # 表の見出し「本表」「付表」は約21.8pt
TEXT_H = 12.55         # 本文の文字
KANJI_X = 112.0        # 漢字の列: これより左が字種、右が康熙字典体・許容字体
READING_X = 165.0      # 音訓の列の左端
INDENT_X = 177.5       # 音訓の列でこれより右は1字下げ
EXAMPLE_X = 240.0      # 例の列の左端
NOTE_X = 390.0         # 備考の列の左端
NOTE_FULL_X = 549.0    # 備考の行がここより右まで届いていれば（列は約16字、15字以上）、次の行に折り返している
ROW_TOL = 2.0          # 同じ行とみなす y の差

# PDF に文字の情報（ToUnicode）が無く、括弧だけが取り出される康熙字典体。PDF の表の字形を目で確かめて補う（2026-11-03）。
# PDF が直って字が取り出せるようになったら、ここから外す（外さないと止まる）
MISSING_KYUJI = {"亀": "龜"}

KATAKANA = re.compile(r"[ァ-ヺー]+")
HIRAGANA = re.compile(r"[ぁ-ゖー]+")
KANJI = re.compile("[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0003134f]")  # 康熙字典体には CJK 互換漢字もある


class Word:
    def __init__(self, x0: float, y0: float, x1: float, y1: float, text: str):
        self.x, self.y, self.x1, self.h, self.text = x0, y0, x1, y1 - y0, text

    def is_text(self) -> bool:
        return abs(self.h - TEXT_H) < 0.5


def words_by_page(pdf: bytes) -> list[list[Word]]:
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "in.pdf"
        src.write_bytes(pdf)
        out = subprocess.run(["pdftotext", "-f", str(MAIN_FIRST_PAGE), "-bbox-layout", str(src), "-"],
                             check=True, capture_output=True).stdout.decode("utf-8")
    pages = []
    for page in re.findall(r"<page [^>]*>(.*?)</page>", out, re.S):
        ws = [Word(float(a), float(b), float(c), float(e), html.unescape(t))
              for a, b, c, e, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', page)]
        pages.append([w for w in ws if TOP_Y <= w.y < BOTTOM_Y and w.text.strip()])
    return pages


OPENING = tuple("「『（［【〔")


def x_order(w: Word) -> float:
    """行の中の並べ順。約物を詰めて組んだところ（「」，「」など）では「，」と「「」の枠がほぼ重なるので、始めの括弧を後ろに回す"""
    return w.x + (0.9 if w.text.startswith(OPENING) else 0.0)


def rows(ws: list[Word]) -> list[list[Word]]:
    """y が近い語を1行にまとめ、上から順に、行の中は左から順に並べる"""
    out: list[list[Word]] = []
    for w in sorted(ws, key=lambda w: (w.y, w.x)):
        if out and abs(out[-1][0].y - w.y) < ROW_TOL:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(r, key=x_order) for r in out]


def is_title(page: list[Word], text: str) -> bool:
    """ページの中央にある表の見出し（「本」「表」「付」）。漢字の列の字（約21.5pt）より少し大きい"""
    return any(w.h > TITLE_H and w.text == text and w.x > 250 for w in page)


def continues(prev_text: str, prev_x1: float, text: str) -> bool:
    """備考の前の行（prev_text）が、次の行（text で始まる）に続いているか"""
    if prev_text.endswith(("，", "、")):
        return True
    if prev_text.endswith("。") or text.startswith(("⇔", "＊")):  # 「⇔」（異字同訓）と「＊」（字体の注記）は新しい注記
        return False
    return prev_x1 >= NOTE_FULL_X


def parse_main(pages: list[list[Word]]) -> list[dict]:
    entries: list[dict] = []
    reading: dict | None = None
    note_x1 = 0.0  # 備考の直前の行の右端
    for pno, page in enumerate(pages):
        if pno == 0:
            # 見出し「本表」と列の見出し（漢字・音訓・例・備考）の行より下だけを読む
            header_y = next(w.y for w in page if w.text == "例" and w.is_text())
            page = [w for w in page if w.y > header_y + ROW_TOL]
        for row in rows(page):
            for w in row:
                text = w.text.strip().replace(" ", "")
                if w.h > BIG_H and w.x < KANJI_X:
                    if len(text) != 1 or not KANJI.fullmatch(text):
                        raise RuntimeError(f"字種が1字でない: {w.text!r}")
                    entries.append({"kanji": text, "readings": []})
                    reading = None
                elif w.h > BIG_H and w.x < READING_X:
                    entry = entries[-1]
                    if text.startswith("［"):
                        if text != f"［{entry['kanji']}］":
                            raise RuntimeError(f"許容字体の形が違う: {entry['kanji']} {text!r}")
                        entry["allowed_form"] = True
                    elif text.strip("（）"):
                        entry.setdefault("kyuji", []).append(text.strip("（）"))
                    else:  # 括弧だけ（字が取り出せない）
                        entry["_kyuji_missing"] = True
                elif not w.is_text() or w.x < READING_X:
                    continue  # 漢字の列の括弧（「弁」の3つの康熙字典体）など
                elif w.x < EXAMPLE_X:
                    if KATAKANA.fullmatch(text):
                        kind = "on"
                    elif HIRAGANA.fullmatch(text):
                        kind = "kun"
                    else:
                        raise RuntimeError(f"音訓が片仮名・平仮名だけでない: {entries[-1]['kanji']} {text!r}")
                    reading = {"reading": text, "type": kind}
                    if w.x >= INDENT_X:
                        reading["special"] = True
                    reading["_y"] = w.y
                    entries[-1]["readings"].append(reading)
                elif w.x < NOTE_X:
                    if reading is None:
                        raise RuntimeError(f"音訓の無い行に例がある: {entries[-1]['kanji']} {text!r}")
                    if abs(reading["_y"] - w.y) < ROW_TOL:
                        reading["_examples"] = reading.get("_examples", "") + text
                    else:  # 折り返した続き
                        if not reading.get("_examples", "").endswith("，"):
                            raise RuntimeError(f"例の折り返しが「，」の後でない: {entries[-1]['kanji']} {reading.get('_examples')!r} / {text!r}")
                        reading["_examples"] += text
                else:
                    # 備考は字ごとにまとめる。備考のます目は、音訓の行とそろっていないこともある（「二」など、字全体で1つのます目）
                    entry = entries[-1]
                    notes = entry.setdefault("notes", [])
                    if notes and abs(entry["_note_y"] - w.y) < ROW_TOL:  # 同じ行の続きの語（「⇔」と「当てる，充てる」など）
                        notes[-1] += text
                    elif notes and continues(notes[-1], note_x1, text):
                        notes[-1] += text
                    else:
                        notes.append(text)
                    entry["_note_y"] = w.y
                    note_x1 = w.x1
    for e in entries:
        e.pop("_note_y", None)
        if e.pop("_kyuji_missing", False):
            if e["kanji"] not in MISSING_KYUJI or "kyuji" in e:
                raise RuntimeError(f"康熙字典体が取り出せない: {e['kanji']}")
            e["kyuji"] = [MISSING_KYUJI[e["kanji"]]]
        elif e["kanji"] in MISSING_KYUJI:
            raise RuntimeError(f"{e['kanji']} の康熙字典体は取り出せるようになった。MISSING_KYUJI から外す")
        if not e["readings"]:
            raise RuntimeError(f"音訓が無い: {e['kanji']}")
        for r in e["readings"]:
            r.pop("_y")
            examples = [s for s in r.pop("_examples", "").split("，") if s]
            if examples:
                r["examples"] = examples
    return entries


def parse_appendix(pages: list[list[Word]]) -> list[dict]:
    """付表: 左右2段。各段の左が読み（平仮名）、右が語。小さい文字（約9pt）は読みの補足"""
    out: list[dict] = []
    for page in pages:
        if is_title(page, "付"):
            # 見出しと「※以下に挙げられている語を…」の注記（約10.8pt）は除く
            page = [w for w in page if w.h <= TITLE_H and not (10.0 < w.h < 11.5)]
        for left in (True, False):
            col = [w for w in page if (w.x < 300) == left]
            if not col:
                continue
            x0 = min(w.x for w in col if w.is_text())
            readings = [w for w in col if w.is_text() and w.x < x0 + 60]
            words = [w for w in col if w.is_text() and w.x >= x0 + 60]
            small = [w for w in col if not w.is_text()]
            items = [{"reading": w.text, "_y": w.y, "words": []} for w in sorted(readings, key=lambda w: w.y)]
            for w in sorted(words, key=lambda w: w.y):
                near = min(items, key=lambda it: abs(it["_y"] - w.y))
                if abs(near["_y"] - w.y) > 9:
                    raise RuntimeError(f"付表の語に対応する読みが無い: {w.text!r}")
                near["words"].append(w.text)
            for w in small:
                above = [it for it in items if it["_y"] < w.y]
                if not above:
                    raise RuntimeError(f"付表の補足に対応する読みが無い: {w.text!r}")
                above[-1].setdefault("notes", []).append(w.text)
            for it in items:
                it.pop("_y")
                if not HIRAGANA.fullmatch(it["reading"]) or not it["words"] or not all(KANJI.search(x) for x in it["words"]):
                    raise RuntimeError(f"付表の組がおかしい: {it}")
            out.extend(items)
    return out


def convert(pdf: bytes) -> list[dict]:
    pages = words_by_page(pdf)
    split = next(i for i, p in enumerate(pages) if is_title(p, "付"))
    main = parse_main(pages[:split])
    appendix = parse_appendix(pages[split:])
    if len(main) != 2136 or len({e["kanji"] for e in main}) != 2136:
        raise RuntimeError(f"本表の字数が 2,136 字ではない: {len(main)}（重なりを除くと {len({e['kanji'] for e in main})}）")
    order = ("kanji", "kyuji", "allowed_form", "readings", "notes")
    records = [{"source": DATASET, "version": VERSION, "kind": "本表", "no": i, **{k: e[k] for k in order if k in e}}
               for i, e in enumerate(main, start=1)]
    records += [{"source": DATASET, "version": VERSION, "kind": "付表", "no": i, **e} for i, e in enumerate(appendix, start=1)]
    return records


def main() -> int:
    pdf = cached("joyo-kanji-hyo-20101130.pdf", lambda: opener().open(PDF_URL, timeout=120).read())
    records = convert(pdf)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": "常用漢字表（平成22年内閣告示第2号）",
        "version": VERSION,
        "url": PAGE,
        "pdf": PDF_URL,
        "license": "告示（著作権の対象外）。配布元は文部科学省ウェブサイト利用規約（PDL-1.0 に準拠）",
        "attribution": f"出典：「常用漢字表」（平成22年内閣告示第2号、文化庁 {PAGE}）を加工して作成",
    }, pdf)
    main_n = sum(1 for r in records if r["kind"] == "本表")
    print(f"{DATASET}: 本表 {main_n} 字、付表 {len(records) - main_n} 語", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
