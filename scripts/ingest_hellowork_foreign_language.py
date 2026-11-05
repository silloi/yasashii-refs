#!/usr/bin/env python3
"""厚生労働省「通訳がいるハローワークのご紹介」（PDF、2026年8月）の表を、data/hellowork-foreign-language.jsonl にする。

1行が1つのハローワーク（出張所・外国人雇用サービスセンターなどを含む）。
- PDF（https://www.mhlw.go.jp/content/000592865.pdf ）の、都道府県ごとの表を読む。目次のページは除く。
  目録の hellowork-foreign-language のうち、この一覧だけを取り込む（外国語で電話ができるハローワークのチラシと、
  利用チェックリストは入れない）。
- 各表は、事業所の名前（英語と日本語）・電話番号と、言語（行）× 曜日（列、月〜金）のマス。
  マスの中に、対応する時間（「13:00～17:00」）と注記（「※第 1､2､4 のみ」「Only 1st,2nd,4th」「※隔週」）がある。
  - 文字の位置（pdftotext -bbox）で読む。言語の行は、言語の名前（English・英語 など）の位置で決め、行の上下の中間で区切る。
    英語と日本語の名前は、上下の近さで組にする（片方しか無い行もある）。列は、曜日の見出し（Mon.〜Fri.）の位置で決める。
  - 「―」のマスは、その曜日は対応しない（入れない）。
  - マスの文字は `text` に元のまま（行は改行でつなぐ）入れる。そこから、時間を `times`（全角の数字は半角にする）、
    「※」で始まる注記を `note`、英語の注記を `note_en` に分ける。数字と記号だけの行（日付の並び）は、直前の注記につなげる。
  - 表の最後の行は、左の余白から始まる行（次の事業所の英語の名前）かページ番号の行の手前までを読む。
  - 同じ高さで近くに並ぶ語は1つのまとまりにし、まとまりの中心で曜日を決める（曜日の列をまたぐ長い注記があるため）。
  - 言語の名前の書き方の揺れ（「ベトナム」「スペイン」「Indonesia」「ミヤンマー語」）も読む。
  - 時間が3つ以上のマスがある事業所（注記の日付の並びが長い一宮など）は、マスの読み分けがくずれているので `check` を付ける。
- 都道府県の見出し（「01 Hokkaido 北海道」）は、次の見出しまでの事業所に付ける。
- 事業所の数が、電話番号のある行の数と合わなければ止まる。PDF は .cache/hellowork-foreign-language/ に置く。
  pdftotext（poppler）が要る。

使い方: python3 scripts/ingest_hellowork_foreign_language.py [--refresh]
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile

from common import CACHE, cached, opener, write_dataset

DATASET = "hellowork-foreign-language"
URL = "https://www.mhlw.go.jp/content/000592865.pdf"
TITLE = "通訳がいるハローワークのご紹介"
TERMS_URL = "https://www.mhlw.go.jp/chosakuken/index.html"
VERSION = "2026-08"
EN_LANGS = {
    "English": "en", "Chinese": "zh", "Korean": "ko", "Portuguese": "pt", "Spanish": "es", "Tagalog": "tl",
    "Vietnamese": "vi", "Nepali": "ne", "Ukrainian": "uk", "Thai": "th", "Indonesian": "id", "Burmese": "my",
    "Myanmar": "my", "Indonesia": "id",  # 名古屋の表は「Indonesia」
}
JA_LANGS = {
    "英語": "en", "中国語": "zh", "韓国語": "ko", "ポルトガル語": "pt", "スペイン語": "es", "タガログ語": "tl",
    "ベトナム語": "vi", "ネパール語": "ne", "ウクライナ語": "uk", "タイ語": "th", "インドネシア語": "id",
    "ミャンマー語": "my", "ミヤンマー語": "my", "ビルマ語": "my",  # 名古屋の表は「ミヤンマー語」
}
JA_LANGS.update({k[:-1]: v for k, v in list(JA_LANGS.items())})  # 「語」の無い書き方（沼津の「ベトナム」、伊賀の「スペイン」）
PAIR_GAP = 16.5  # 英語の名前の上端から、日本語の名前の上端までの、ふつうの間（pt）
PAIR_MAX = 40.0  # 同じ言語の英語と日本語の名前を組にする、上下の間の上限（pt。行の高い表がある）
DAYS_EN = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]
DAYS_JA = "月火水木金土日"
PREF = re.compile(r"^(\d{2}) (.+?) (\S+[都道府県])$")
OFFICE = re.compile(r"^(.*?)\s*([　-鿿＀-￯].*?)（TEL[：:]\s*([0-9０-９－-]+)\s*）$")
PAGE_NO = re.compile(r"^-\s*[0-9０-９]+\s*-$")
CHECK = "表が込み入っていて（時間が3つ以上のマスがある）、マスの読み分けがくずれているところがある。元の PDF（pdf_page）で確かめる"
SEGMENT_GAP = 6.0  # 同じ高さの語を1つのまとまりにする間（pt）
WIDE_LATIN = str.maketrans({chr(c): chr(c - 0xFEE0) for c in [*range(0xFF21, 0xFF3B), *range(0xFF41, 0xFF5B)]})
TEL = re.compile(r"（TEL[：:]")
TIME = re.compile(r"\d{1,2}:\d{2}～\d{1,2}:\d{2}")
WIDE = str.maketrans("０１２３４５６７８９：－", "0123456789:-")


def words_by_page(pdf: bytes) -> list[list[tuple[float, float, float, float, str]]]:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf)
        f.flush()
        out = subprocess.run(["pdftotext", "-bbox", f.name, "-"], capture_output=True, text=True, check=True).stdout
    pages = []
    for page in re.findall(r"(?s)<page [^>]*>(.*?)</page>", out):
        pages.append([(float(a), float(b), float(c), float(d), html.unescape(w)) for a, b, c, d, w in re.findall(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', page)])
    return pages


def rows(words, tol: float = 2.0) -> list[tuple[float, list]]:
    """同じ高さの語を1つの行にまとめる（上から順）"""
    out: list[tuple[float, list]] = []
    for w in sorted(words, key=lambda w: (w[1], w[0])):
        if out and abs(out[-1][0] - w[1]) <= tol:
            out[-1][1].append(w)
        else:
            out.append((w[1], [w]))
    return [(y, sorted(ws)) for y, ws in out]


def line_text(ws) -> str:
    """語をつなぐ。間が狭い語（「1」「st」など）は空白を入れずにつなぐ"""
    s, last = "", None
    for x0, _, x1, _, w in sorted(ws):
        s += ("" if last is None or x0 - last < 1.5 else " ") + w
        last = x1
    return s


def parse_cell(ws) -> dict:
    """マスの文字（text）と、時間（times）・注記（note・note_en）。数字と記号だけの行（日付の並び）は、直前の注記につなげる"""
    lines = [line_text(r).strip() for _, r in rows(ws)]
    lines = [x for x in lines if x and x != "―"]
    if not lines:
        return {}
    times, note, note_en = [], [], []
    last = None
    for line in lines:
        norm = line.translate(WIDE).replace(" ", "")
        found = TIME.findall(norm)
        times += found
        rest = TIME.sub("", norm).strip() if found else norm
        if not rest:
            continue
        if rest.startswith("※"):
            note.append(line)
            last = note
        elif not re.search(r"[A-Za-z]", rest) and last is not None:
            last.append(line)
        else:
            note_en.append(line)
            last = note_en
    cell: dict = {"text": "\n".join(lines)}
    if times:
        cell["times"] = times
    if note:
        cell["note"] = " ".join(note)
    if note_en:
        cell["note_en"] = " ".join(note_en)
    return cell


def parse(pdf: bytes) -> tuple[list[dict], int]:
    offices: list[dict] = []
    tel_rows = 0
    pref = None
    for page_no, words in enumerate(words_by_page(pdf), 1):
        rs = rows(words)
        texts = [(y, line_text(ws), ws) for y, ws in rs]
        if any("Prefecture" in t for _, t, _ in texts):
            continue  # 目次
        # 表の区切り: 事業所の行と、曜日の見出しの行
        office_rows = []
        page_offices: list[tuple[float, dict]] = []
        before = offices[-1] if offices else None  # 前のページの最後の事業所（表がページをまたぐとき）
        for y, t, ws in texts:
            m = PREF.match(t)
            if m:
                pref = {"pref_code": m.group(1), "pref_en": m.group(2), "pref": m.group(3)}
            if TEL.search(t):
                tel_rows += 1
                o = OFFICE.match(t.translate(WIDE_LATIN))
                if not o:
                    raise ValueError(f"{page_no} ページ: 事業所の行が読めない: {t!r}")
                office_rows.append(y)
                rec = {**(pref or {}), "office": o.group(2).strip(), "tel": o.group(3).translate(WIDE)}
                if o.group(1).strip():
                    rec["office_en"] = o.group(1).strip()
                rec["pdf_page"] = page_no
                rec["languages"] = []
                offices.append(rec)
                page_offices.append((y, rec))
        headers = [(y, ws) for y, t, ws in texts if t.startswith("言語") and "Mon." in t]
        page_bottom = max((w[3] for w in words), default=0)
        for hi, (hy, hws) in enumerate(headers):
            cols = [((w[0] + w[2]) / 2, DAYS_JA[DAYS_EN.index(w[4])]) for w in hws if w[4] in DAYS_EN]
            left = min(w[0] for w in hws if w[4] in DAYS_EN) - 15
            # この表の範囲: 見出しの下から、次の事業所の行（または次の見出し・ページの下）まで
            nexts = [y for y in office_rows if y > hy] + [y for y, _ in headers[hi + 1:]]
            bottom = min(nexts) if nexts else page_bottom + 1
            day_row = next((y for y, t, _ in texts if hy < y < hy + 30 and t.replace(" ", "").startswith("月")), hy)
            body = [w for w in words if day_row + 5 < w[1] < bottom and not PREF.match(w[4])]
            labels = sorted((w for w in body if (w[4] in EN_LANGS or w[4] in JA_LANGS) and w[2] <= left + 15),
                            key=lambda w: w[1])
            # 表の下の端: 最後の言語の名前より下で、左の余白から始まる行（次の事業所の英語の名前）か、ページ番号の行
            if labels:
                last_label = labels[-1][1]
                ends = [y for y, t, ws in texts if last_label + 4 < y < bottom and (
                    PAGE_NO.match(t) or (ws[0][0] < left - 40 and not any(
                        w[4] in EN_LANGS or w[4] in JA_LANGS for w in ws)))]
                if ends:
                    bottom = min(ends)
                    body = [w for w in body if w[1] < bottom]
            # 英語の名前と、そのすぐ下の日本語の名前を組にする（片方しか無い行もある。松戸のポルトガル語など）
            centers: list[tuple[float, tuple | None, tuple | None]] = []
            i = 0
            while i < len(labels):
                w = labels[i]
                nxt = labels[i + 1] if i + 1 < len(labels) else None
                if (w[4] in EN_LANGS and nxt and nxt[4] in JA_LANGS and EN_LANGS[w[4]] == JA_LANGS[nxt[4]]
                        and nxt[1] - w[1] < PAIR_MAX):
                    centers.append(((w[1] + nxt[3]) / 2, w, nxt))
                    i += 2
                elif w[4] in JA_LANGS:
                    centers.append(((w[1] - PAIR_GAP + w[3]) / 2, None, w))
                    i += 1
                else:
                    centers.append(((w[1] + w[3] + PAIR_GAP) / 2, w, None))
                    i += 1
            if not centers:
                raise ValueError(f"{page_no} ページ: 言語の名前が無い")
            above = [rec for y, rec in page_offices if y < hy]
            office = above[-1] if above else before
            if office is None:
                raise ValueError(f"{page_no} ページ: 事業所の行より前に表がある")
            label_ids = {id(w) for _, e, j in centers for w in (e, j) if w is not None}
            for k, (c, e, j) in enumerate(centers):
                top = day_row + 5 if k == 0 else (centers[k - 1][0] + c) / 2
                low = bottom if k == len(centers) - 1 else (c + centers[k + 1][0]) / 2
                inside = [w for w in body
                          if id(w) not in label_ids and top <= (w[1] + w[3]) / 2 < low and w[2] > left]
                # 同じ高さで近くに並ぶ語を1つのまとまりにし、まとまりの中心で曜日を決める（列をまたぐ注記のため）
                cells: dict[str, list] = {}
                for _, row in rows(inside, tol=3.0):
                    groups: list[list] = []
                    for w in row:
                        if groups and w[0] - groups[-1][-1][2] < SEGMENT_GAP:
                            groups[-1].append(w)
                        else:
                            groups.append([w])
                    for g in groups:
                        xc = (g[0][0] + g[-1][2]) / 2
                        day = min(cols, key=lambda col: abs(col[0] - xc))[1]
                        cells.setdefault(day, []).extend(g)
                schedule = []
                for _, day in cols:
                    cell = parse_cell(cells.get(day, []))
                    if cell:
                        schedule.append({"day": day, **cell})
                entry = {"lang": EN_LANGS[e[4]] if e else JA_LANGS[j[4]]}
                if j:
                    entry["name"] = j[4]
                if e:
                    entry["name_en"] = e[4]
                entry["schedule"] = schedule
                office["languages"].append(entry)
    return offices, tel_rows


def convert(pdf: bytes) -> list[dict]:
    offices, tel_rows = parse(pdf)
    if len(offices) != tel_rows:
        raise ValueError(f"事業所の数が合わない: {len(offices)} / {tel_rows}")
    records = []
    for o in offices:
        if not o["languages"]:
            raise ValueError(f"{o['office']}: 言語が無い")
        if not any(lang["schedule"] for lang in o["languages"]):
            raise ValueError(f"{o['office']}: 対応する曜日が無い")
        if any(len(s.get("times", [])) > 2 for lang in o["languages"] for s in lang["schedule"]):
            o["check"] = CHECK
        records.append({"source": DATASET, "version": VERSION, **o})
    return records


def main() -> int:
    (CACHE / DATASET).mkdir(parents=True, exist_ok=True)
    pdf = cached(f"{DATASET}/000592865.pdf", lambda: opener().open(URL, timeout=120).read())
    records = convert(pdf)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": f"厚生労働省・都道府県労働局・ハローワーク「{TITLE}」",
        "version": "2026年8月",
        "url": URL,
        "license": "PDL-1.0",
        "license_url": TERMS_URL,
        "attribution": f"出典：厚生労働省「{TITLE}」（{URL}）を加工して作成",
    }, pdf)
    langs = sum(len(r["languages"]) for r in records)
    print(f"{DATASET}: 事業所 {len(records)}・言語の行 {langs}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
