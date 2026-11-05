#!/usr/bin/env python3
"""文化審議会国語分科会「地域における日本語教育の在り方について」（報告）の別冊
「『日本語教育の参照枠』に基づく『生活 Can do』一覧」（令和4年11月29日、PDF 95ページ）の
「４ 生活 Can do 一覧」と「５ 生活・文化・社会的情報の整理」を、data/seikatsu-cando.jsonl にする。

`kind` で2つを分ける（常用漢字表の本表・付表と同じ形）。

`kind` が「生活Can do」の行: 1行が1つの Can do（通番 1〜785）。
- 表は 11〜89ページ（横長のページ）。どのページも列の位置が同じなので、見出しの語の位置を確かめてから、
  文字の位置（pdftotext -bbox）で列に分ける。列の境目は、どの語もかからない縦の帯の中ほど（COLUMNS）。
- 行は、通番の数字の高さで決める。列ごとに、上下に続く語（間が BLOCK_GAP 未満）を1つのマスにまとめ、
  マスの上下の中心にいちばん近い通番の行に入れる（マスの文字は上下の中央にそろえてある）。
  中心が MAX_OFFSET より離れていれば止まる。
- マスの中の改行は、空白を入れずにつなぐ（日本語の文のため）。
- 大分類は「Ⅰ」などの番号と名前、中分類は2桁の番号と名前、小分類は「（01）」の番号と名前に分ける。
  小分類の「●」は `essential`（来日間もない外国人の生活の基盤に欠かせない、または安全にかかわり緊急性がある小分類）。
- 事例１・事例２の名前の後の「（修正）」「（新規）」は、`case1_status`・`case2_status` に分ける。
- 「量的検証 代表項目」の列は `representative`（令和4年度の量的検証で、そのレベルの代表項目と認定された項目）。
- JF 番号（JF××・JF生△△）は `jf`。国際交流基金の JF Can-do・JF 生活日本語 Can-do から採用した Can do
  （文言を一部変えたものを含む）。
- 言語活動とカテゴリーは、資料の「３ 生活 Can do に付随する情報」に挙がっているものだけを受け付ける（無ければ止まる）。
- 大分類・中分類・小分類の番号と名前の組が、行によって食い違えば止まる（読み分けがくずれている）。
  事例１の番号の先頭2桁が小分類の番号と違っても止まる。

`kind` が「生活・文化・社会的情報」の行: 1行が1つの情報（小分類ごとに、知っておくと役に立つ情報の例）。
- 表は 91〜95ページ。左に大分類の見出しと小分類の名前、右に情報（「☆」か「・」で始まる。長いものは字下げして折り返す）。
- 小分類の名前は、その情報の並びの上下の中央にあるとは限らない（上にそろえた行もある）。そこで、情報の行の間が
  INFO_GAP より広いところ（表の行の境目）と大分類の見出しで区切ってまとまりを作り、小分類の名前の上下の中心が
  入るまとまりに組ませる。名前の入らないまとまり・名前が2つ入るまとまりがあれば止まる。
- 「☆」は `must_know`（来日間もないかどうかを問わず、情報として知っておく必要があるもの）。「・」と「☆」は `text` から外す。
- 「特に無し」の小分類は、行を作らない。小分類 01〜48 がちょうど1回ずつ出てくることを確かめる。
- `no` は、この表の中の順番（1から）。

元の PDF の食い違いは直さない（手で直したデータを置かないため）。標準出力に出す。
- 事例２の番号の先頭4桁が事例１の番号と違う行がある。
- 事例１・事例２の番号は、名前を一意に決めない。新しく足した事例２は関係する元の事例２の番号を使い、
  同じ事例１の番号で名前が違う行（「防犯に対処する」「犯罪に対処する」）もある。
- 5 の小分類の名前・●が、4 の一覧の表と違うものがある（5 は 5 の書き方のまま入れる）。

PDF は .cache/seikatsu-cando/ に置く。pdftotext（poppler）が要る。

使い方: python3 scripts/ingest_seikatsu_cando.py [--refresh]
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile

from common import CACHE, cached, opener, write_dataset

DATASET = "seikatsu-cando"
PAGE_URL = "https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/"
URL = "https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/94276701_01.pdf"
TITLE = "「地域における日本語教育の在り方について」（報告）別冊「日本語教育の参照枠」に基づく「生活Can do」一覧"
TERMS_URL = "https://www.mext.go.jp/b_menu/1351168.htm"
VERSION = "2022-11-29"
CANDO_KIND = "生活Can do"
INFO_KIND = "生活・文化・社会的情報"
TABLE_PAGES = range(11, 90)  # 4 の一覧の表（1始まりのページ番号）
INFO_PAGES = range(91, 96)  # 5 の表
EXPECTED = 785

# (名前, 左端, 右端)。列の間の、どの語もかからない帯の中ほどで区切る
COLUMNS = [
    ("no", 38, 63), ("activity", 63, 92), ("category", 92, 192), ("level", 192, 218), ("cando", 218, 597),
    ("major", 597, 691), ("middle", 691, 788), ("minor", 788, 890), ("case1_no", 890, 920), ("case1", 920, 1054),
    ("case2_no", 1054, 1104), ("case2", 1104, 1232), ("jf", 1232, 1267), ("representative", 1267, 1340),
]
PAGE_NO_RIGHT = 38  # これより左はページ番号（横向きのページの余白）
HEADER_BOTTOM = 145  # これより上は表の見出し
HEADER = {"通": 45, "言語": 68, "カテゴリー": 114, "レ": 201, "Can": 386, "大分類": 630, "中分類": 726, "小分類": 823,
          "事例１": 968, "事例２": 1152, "JF": 1244, "量的検証": 1272}  # 見出しの語と、その左端（pt）
BLOCK_GAP = 6.0  # 同じマスの行の間（上の行の下端から下の行の上端まで）の上限（pt）
MAX_OFFSET = 12.0  # マスの上下の中心と、通番の中心のずれの上限（pt）。行の高さはどこも約 63.6pt

# 5 の表の位置（pt）。大分類の番号（Ⅰ など）は INFO_HEAD_RIGHT より左、小分類の名前はそこから INFO_TEXT_LEFT まで、
# 情報は INFO_TEXT_LEFT より右。INFO_PAGE_NO_TOP より下はページ番号
INFO_HEAD_RIGHT = 90
INFO_TEXT_LEFT = 265
INFO_PAGE_NO_TOP = 780
INFO_GAP = 5.7  # 同じまとまりの情報の行の間の上限（pt）。同じまとまりの中は約 4.5、表の行の境目は 6.2 以上
INFO_INDENT = 3.0  # 折り返しの行の字下げの下限（pt）

# 「３ 生活 Can do に付随する情報」（２）カテゴリー
CATEGORIES = {
    "聞くこと": ["広報・アナウンスや指示を聞くこと", "音声メディアや録音を聞くこと", "テレビや映画を見ること",
             "聴衆の一人として生で聞くこと"],
    "読むこと": ["通信文を読むこと", "情報や議論を読むこと", "世情を把握するために読むこと", "説明書を読むこと"],
    "やり取り": ["情報の交換", "製品やサービスを得るための取引", "目的達成のための共同作業", "公式の議論とミーティング",
             "非公式の議論（友人との）", "会話", "インタビューすること、インタビューを受けること"],
    "発表": ["公共アナウンス", "聴衆の前での講演", "長く一人で話す：経験談", "長く一人で話す：論拠を述べること"],
    "書くこと": ["記録、メッセージ、書式", "創作", "レポートやエッセイ", "通信"],
}
LEVELS = {"A1", "A2", "B1", "B2"}
MAJOR_NO = "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ"
MAJOR = re.compile(rf"^([{MAJOR_NO}])(.+)$")
MIDDLE = re.compile(r"^(\d{2})(.+)$")
MINOR = re.compile(r"^（(\d{2})）(●?)\s*(.+)$")
STATUS = re.compile(r"[（(](修正|新規)[）)]$")
CASE2_NO = re.compile(r"^\d{7}$")
JF = re.compile(r"^JF(生)?\d+$")
NONE = "特に無し"


def words_by_page(pdf: bytes, pages: range) -> dict[int, list[tuple[float, float, float, float, str]]]:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf)
        f.flush()
        out = subprocess.run(["pdftotext", "-bbox", "-f", str(pages[0]), "-l", str(pages[-1]), f.name, "-"],
                             capture_output=True, text=True, check=True).stdout
    found = re.findall(r"(?s)<page [^>]*>(.*?)</page>", out)
    if len(found) != len(pages):
        raise SystemExit(f"表のページの数が違う: {len(found)}")
    return {n: [(float(a), float(b), float(c), float(d), html.unescape(w)) for a, b, c, d, w in re.findall(
        r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', page)]
        for n, page in zip(pages, found)}


def column_of(w) -> str:
    for name, left, right in COLUMNS:
        if left <= w[0] and w[2] <= right:
            return name
    raise SystemExit(f"どの列にも入らない語: {w}")


def lines(ws, tol: float = 2.0) -> list[list]:
    """同じ高さの語を1つの行にまとめる（上から順、行の中は左から順）"""
    out: list[list] = []
    for w in sorted(ws, key=lambda w: (w[1], w[0])):
        if out and abs(out[-1][0][1] - w[1]) <= tol:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(line) for line in out]


def line_text(line) -> str:
    """行の語をつなぐ。間が狭い語は空白を入れずにつなぐ"""
    s, last = "", None
    for x0, _, x1, _, w in line:
        s += ("" if last is None or x0 - last < 1.5 else " ") + w
        last = x1
    return s


def span(line) -> tuple[float, float]:
    return min(w[1] for w in line), max(w[3] for w in line)


def blocks(ws) -> list[tuple[float, str]]:
    """上下に続く行を1つのマスにまとめる。（マスの上下の中心, 文字）の並び"""
    out: list[list] = []
    for line in lines(ws):
        top, bottom = span(line)
        if out and top - out[-1][-1][2] < BLOCK_GAP:
            out[-1].append((top, line, bottom))
        else:
            out.append([(top, line, bottom)])
    return [((b[0][0] + b[-1][2]) / 2, "".join(line_text(line) for _, line, _ in b)) for b in out]


def check_header(page: int, ws) -> None:
    found = {}
    for w in ws:
        if w[1] < HEADER_BOTTOM and w[4] in HEADER and w[4] not in found:
            found[w[4]] = round(w[0])
    if found != HEADER:
        raise SystemExit(f"{page}ページの見出しの位置が違う: {found}")


def page_rows(page: int, ws) -> list[dict]:
    """4 の表の1ページ分の行。列ごとのマスの文字を、通番の行に入れる"""
    check_header(page, ws)
    body = [w for w in ws if w[1] >= HEADER_BOTTOM]
    margin = [w for w in body if w[2] <= PAGE_NO_RIGHT]
    if not all(w[4].isdigit() for w in margin):
        raise SystemExit(f"{page}ページの左の余白に、ページ番号でない文字がある: {margin}")
    cols: dict[str, list] = {}
    for w in body:
        if w[2] > PAGE_NO_RIGHT:
            cols.setdefault(column_of(w), []).append(w)
    anchors = blocks(cols.get("no", []))
    rows = []
    for center, text in anchors:
        if not text.isdigit():
            raise SystemExit(f"{page}ページの通番が数字でない: {text}")
        rows.append({"center": center, "pdf_page": page, "cells": {"no": text}})
    for name, ws_col in cols.items():
        if name == "no":
            continue
        for center, text in blocks(ws_col):
            row = min(rows, key=lambda r: abs(r["center"] - center))
            if abs(row["center"] - center) > MAX_OFFSET:
                raise SystemExit(f"{page}ページの「{text}」（{name}）が、どの通番の行にも近くない")
            if name in row["cells"]:
                raise SystemExit(f"{page}ページの通番 {row['cells']['no']} の {name} に、マスが2つある: {text}")
            row["cells"][name] = text
    return rows


def split_status(name: str) -> tuple[str, str]:
    """名前の後の「（修正）」「（新規）」を分ける"""
    m = STATUS.search(name)
    return (name[:m.start()], m.group(1)) if m else (name, "")


def record(row: dict, names: dict) -> dict:
    c = row["cells"]
    no = int(c["no"])
    activity, category, level = c.get("activity", ""), c.get("category", ""), c.get("level", "")
    if activity not in CATEGORIES:
        raise SystemExit(f"通番 {no}: 言語活動が一覧に無い: {activity}")
    if category not in CATEGORIES[activity]:
        raise SystemExit(f"通番 {no}: カテゴリーが「{activity}」の一覧に無い: {category}")
    if level not in LEVELS:
        raise SystemExit(f"通番 {no}: レベルが違う: {level}")
    major, middle, minor = MAJOR.match(c.get("major", "")), MIDDLE.match(c.get("middle", "")), MINOR.match(c.get("minor", ""))
    if not (major and middle and minor):
        raise SystemExit(f"通番 {no}: 分類が読めない: {c}")
    if not CASE2_NO.match(c.get("case2_no", "")):
        raise SystemExit(f"通番 {no}: 事例２の番号が読めない: {c.get('case2_no')}")
    case1, case1_status = split_status(c.get("case1", ""))
    case2, case2_status = split_status(c.get("case2", ""))
    rec = {
        "source": DATASET, "version": VERSION, "kind": CANDO_KIND, "no": no,
        "activity": activity, "category": category, "level": level, "cando": c.get("cando", ""),
        "major_no": major.group(1), "major": major.group(2),
        "middle_no": middle.group(1), "middle": middle.group(2),
        "minor_no": minor.group(1), "minor": minor.group(3), "essential": bool(minor.group(2)),
        "case1_no": c.get("case1_no", ""), "case1": case1,
    }
    if case1_status:
        rec["case1_status"] = case1_status
    rec |= {"case2_no": c["case2_no"], "case2": case2}
    if case2_status:
        rec["case2_status"] = case2_status
    if "jf" in c:
        jf = c["jf"].replace(" ", "")
        if not JF.match(jf):
            raise SystemExit(f"通番 {no}: JF 番号が読めない: {c['jf']}")
        rec["jf"] = jf
    if "representative" in c:
        if c["representative"] != "代表項目":
            raise SystemExit(f"通番 {no}: 代表項目の列が違う: {c['representative']}")
        rec["representative"] = True
    rec["pdf_page"] = row["pdf_page"]
    if not rec["cando"].endswith("。"):
        raise SystemExit(f"通番 {no}: Can do の文が「。」で終わらない: {rec['cando']}")
    if not re.fullmatch(r"\d{4}", rec["case1_no"]) or rec["case1_no"][:2] != rec["minor_no"] or not rec["case1"]:
        raise SystemExit(f"通番 {no}: 事例１が空か、番号が小分類と合わない: {rec['case1_no']} {rec['case1']}")
    # 分類一覧の番号には、同じ名前（行によって食い違えば、読み分けがくずれている）
    for key, value in [("major", rec["major"]), ("middle", rec["middle"]), ("minor", (rec["minor"], rec["essential"]))]:
        code = rec[f"{key}_no"]
        if names.setdefault((key, code), value) != value:
            raise SystemExit(f"通番 {no}: {key} {code} の名前が前の行と違う: {value} / {names[(key, code)]}")
    return rec


def case_no_mismatches(records: list[dict]) -> list[int]:
    """事例２の番号の先頭4桁が、事例１の番号と違う行の通番（元の PDF のまま）"""
    return [r["no"] for r in records if r.get("kind") == CANDO_KIND and r["case2_no"][:4] != r["case1_no"]]


def info_blocks(page: int, ws) -> list[dict]:
    """5 の表の1ページ分。小分類ごとのまとまり（大分類・小分類の名前・情報の並び）"""
    footer = [w for w in ws if w[1] >= INFO_PAGE_NO_TOP]
    if not all(w[4].isdigit() for w in footer):
        raise SystemExit(f"{page}ページの下の余白に、ページ番号でない文字がある: {footer}")
    body = [w for w in ws if w[1] < INFO_PAGE_NO_TOP]
    heads = [w for w in body if w[0] < INFO_HEAD_RIGHT and len(w[4]) == 1 and w[4] in MAJOR_NO]
    if not heads:
        raise SystemExit(f"{page}ページに大分類の見出しが無い")
    body = [w for w in body if w[1] >= min(h[1] for h in heads) - 2]  # 91ページの表の前の説明と見出しを除く
    on_head = [w for w in body if any(abs(w[1] - h[1]) < 2 for h in heads)]
    events = []  # (上端, 0: 見出し / 1: 情報の行, 中身)
    for h in heads:
        name = sorted(w for w in on_head if w[0] >= INFO_HEAD_RIGHT)
        name = [w for w in name if abs(w[1] - h[1]) < 2]
        if not name or any(w[0] >= INFO_TEXT_LEFT for w in name):
            raise SystemExit(f"{page}ページの大分類の見出しが読めない: {h}")
        events.append((h[1], 0, (h[4], line_text(name))))
    labels: list[dict] = []
    for line in lines([w for w in body if INFO_HEAD_RIGHT <= w[0] < INFO_TEXT_LEFT and w not in on_head]):
        top, bottom = span(line)
        text = line_text(line)
        if re.match(r"^（\d{2}）", text):
            labels.append({"top": top, "bottom": bottom, "text": text})
        elif labels and top - labels[-1]["bottom"] < INFO_GAP:
            labels[-1]["text"] += text  # 折り返した名前の続き
            labels[-1]["bottom"] = bottom
        else:
            raise SystemExit(f"{page}ページの小分類の名前が読めない: {text}")
    item_lines = lines([w for w in body if w[0] >= INFO_TEXT_LEFT])
    left = min(line[0][0] for line in item_lines)
    events += [(span(line)[0], 1, line) for line in item_lines]
    out: list[dict] = []
    major, last_bottom = None, None
    for top, kind, content in sorted(events, key=lambda e: (e[0], e[1])):
        if kind == 0:
            major, last_bottom = content, None
            continue
        if major is None:
            raise SystemExit(f"{page}ページの情報の前に、大分類の見出しが無い")
        bottom = span(content)[1]
        if last_bottom is None or top - last_bottom >= INFO_GAP:
            out.append({"top": top, "major": major, "items": [], "pdf_page": page})
        block = out[-1]
        block["bottom"], last_bottom = bottom, bottom
        text = line_text(content)
        if text.startswith(("☆", "・")) or text == NONE:
            block["items"].append(text)
        elif block["items"] and content[0][0] >= left + INFO_INDENT:
            block["items"][-1] += text  # 字下げした折り返しの続き
        else:
            raise SystemExit(f"{page}ページの情報の行が読めない: {text}")
    for label in labels:
        center = (label["top"] + label["bottom"]) / 2
        hits = [b for b in out if b["top"] - 3 <= center <= b["bottom"] + 3]
        if len(hits) != 1 or "label" in hits[0]:
            raise SystemExit(f"{page}ページの小分類「{label['text']}」の情報のまとまりが決まらない")
        hits[0]["label"] = label["text"]
    for b in out:
        if "label" not in b:
            raise SystemExit(f"{page}ページの情報「{b['items'][0]}」に、小分類の名前が無い")
    return out


def info_records(pdf: bytes) -> tuple[list[dict], list[str]]:
    """5 の表の行と、「特に無し」の小分類の番号"""
    records, none, seen = [], [], []
    for page, ws in words_by_page(pdf, INFO_PAGES).items():
        for b in info_blocks(page, ws):
            minor = MINOR.match(b["label"])
            if not minor:
                raise SystemExit(f"小分類の名前が読めない: {b['label']}")
            seen.append(minor.group(1))
            if b["items"] == [NONE]:
                none.append(minor.group(1))
                continue
            if NONE in b["items"]:
                raise SystemExit(f"「{NONE}」と情報が同じ小分類にある: {b['label']}")
            for text in b["items"]:
                records.append({
                    "source": DATASET, "version": VERSION, "kind": INFO_KIND, "no": len(records) + 1,
                    "major_no": b["major"][0], "major": b["major"][1],
                    "minor_no": minor.group(1), "minor": minor.group(3), "essential": bool(minor.group(2)),
                    "text": text[1:], "must_know": text.startswith("☆"), "pdf_page": b["pdf_page"],
                })
    if seen != [f"{i:02d}" for i in range(1, 49)]:
        raise SystemExit(f"5 の表の小分類が 01〜48 の順にちょうど1回ずつ出てこない: {seen}")
    return records, none


def info_differences(cando: list[dict], info: list[dict]) -> list[str]:
    """5 の表の大分類・小分類の名前と●が、4 の一覧の表と違うところ（元の PDF のまま）"""
    table = {r["minor_no"]: (r["major_no"], r["major"], r["minor"], r["essential"]) for r in cando}
    out = []
    for no in sorted({r["minor_no"] for r in info}):
        r = next(r for r in info if r["minor_no"] == no)
        if (r["major_no"], r["major"], r["minor"], r["essential"]) != table[no]:
            out.append(f"（{no}）5: {r['major_no']} {r['major']} / {r['minor']} / ●{r['essential']}、"
                       f"4: {table[no][0]} {table[no][1]} / {table[no][2]} / ●{table[no][3]}")
    return out


def convert(pdf: bytes) -> tuple[list[dict], list[dict], list[str]]:
    rows = []
    for page, ws in words_by_page(pdf, TABLE_PAGES).items():
        rows += page_rows(page, ws)
    names: dict = {}
    cando = [record(r, names) for r in rows]
    nos = [r["no"] for r in cando]
    if nos != list(range(1, EXPECTED + 1)):
        raise SystemExit(f"通番が 1〜{EXPECTED} の連番でない（{len(nos)}件）")
    info, none = info_records(pdf)
    return cando, info, none


def main() -> int:
    (CACHE / DATASET).mkdir(parents=True, exist_ok=True)
    pdf = cached(f"{DATASET}/94276701_01.pdf", lambda: opener().open(URL, timeout=120).read())
    cando, info, none = convert(pdf)
    write_dataset(DATASET, cando + info, {
        "source": DATASET,
        "name": f"文化審議会国語分科会 {TITLE}",
        "version": VERSION,
        "url": PAGE_URL,
        "pdf": URL,
        "license": "PDL-1.0（文部科学省ウェブサイト利用規約に準拠）。jf の付いた Can do は、国際交流基金の JF Can-do・"
                   "JF生活日本語Can-do から採用したもの（みんなのCan-doサイトの著作権ポリシーでは、無料で新たに許諾を得ることなく使える）",
        "license_url": TERMS_URL,
        "attribution": f"出典：文化審議会国語分科会 {TITLE}（令和4年11月29日、文化庁 {PAGE_URL}）を加工して作成",
    }, pdf)
    jf = sum("jf" in r for r in cando)
    must = sum(r["must_know"] for r in info)
    print(f"{DATASET}: Can do {len(cando)}（JF 番号あり {jf}）、生活・文化・社会的情報 {len(info)}（☆ {must}）", file=sys.stderr)
    print(f"「{NONE}」の小分類: {none}", file=sys.stderr)
    print(f"事例２の番号が事例１と合わない行（元の PDF のまま）: {case_no_mismatches(cando)}", file=sys.stderr)
    for d in info_differences(cando, info):
        print(f"5 と 4 の表の違い（元の PDF のまま）: {d}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
