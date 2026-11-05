#!/usr/bin/env python3
"""文部科学省「外国人児童生徒のための就学ガイドブック」（8言語、日本語併記）を、
data/mext-shugaku-guidebook.jsonl にする。

1行が、1つの言語の、日本語のページとその訳のページの組。
- 配布ページ（https://www.mext.go.jp/a_menu/shotou/clarinet/003/1320860.htm ）の「就学ガイドブック」の PDF（8言語）。
  要約版の「就学ガイド」は入れない。
- どの言語の PDF も、2ページ目からは、日本語のページの次のページがその訳（1ページ目は表紙、最後は裏表紙）。
  偶数ページと次のページを組にする。組の85%以上で日本語のページのほうが仮名が多くなければ止まる
  （図や表のページは仮名が少ない）。
- 文字は pdftotext（-layout）で取り出し、行をつないで段落にする（日本語と中国語は行をそのままつなぎ、ほかの言語は
  空白でつなぐ。中国語は、割り付けで入った漢字のあいだの空白も除く）。
  ページ番号だけの行は除く。図のページ（学校系統図など）は、文字の並びがくずれる。
- 見出しの印（●・■・①〜⑳・(1)・（１）など）で段落を区切り、日本語と訳で見出しの数が同じなら `sections` に組にして入れる。
- PDF は .cache/mext-shugaku-guidebook/ に置く。pdftotext（poppler）が要る。

使い方: python3 scripts/ingest_mext_shugaku_guidebook.py [--refresh]
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import time

from common import CACHE, cached, opener, write_dataset

DATASET = "mext-shugaku-guidebook"
PAGE = "https://www.mext.go.jp/a_menu/shotou/clarinet/003/1320860.htm"
TITLE = "外国人児童生徒のための就学ガイドブック"
TERMS_URL = "https://www.mext.go.jp/b_menu/1351168.htm"
VERSION = "2015年4月"
AFIELD = "https://www.mext.go.jp/component/a_menu/education/micro_detail/__icsFiles/afieldfile/2015/"
PDFS = {
    "en": "https://www.mext.go.jp/content/20220506-mxt_kouhou02-000022321_1.pdf",
    "ko": AFIELD + "06/01/1358299_02_1.pdf",
    "vi": AFIELD + "06/01/1358299_03.pdf",
    "tl": AFIELD + "06/19/1358299_04_1.pdf",
    "zh-Hans": AFIELD + "06/01/1358299_05_1.pdf",
    "pt": AFIELD + "06/19/1358299_06_1.pdf",
    "es": AFIELD + "06/01/1358299_07.pdf",
    "uk": "https://www.mext.go.jp/content/20220428-mxt_kouhou02-000022321_1.pdf",
}
WAIT = 1.0
KANA = re.compile(r"[぀-ヿ]")
MARK = re.compile(r"^(●|■|◆|○|[①-⑳]|[(（]\s*[0-9０-９]+\s*[)）]|[0-9０-９]+[.．]\s)")
PAGE_NUMBER = re.compile(r"^[-－ ]*[0-9０-９]+[-－ ]*$")


def pdf_pages(data: bytes) -> list[str]:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data)
        f.flush()
        out = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True, check=True).stdout
    pages = out.split("\f")
    return pages[:-1] if pages and not pages[-1].strip() else pages


def kana(page: str) -> int:
    return len(KANA.findall(page))


def paragraphs(page: str, japanese: bool) -> list[str]:
    """行をつないで段落にする。空の行・見出しの印・字下げで段落を分ける"""
    out: list[list[str]] = []
    prev_blank, prev_indent = True, 0
    for line in page.splitlines():
        text = line.strip()
        if not text or PAGE_NUMBER.match(text):
            prev_blank = True
            continue
        indent = len(line) - len(line.lstrip(" 　"))
        ends = out[-1][-1][-1:] if out else ""
        heading = bool(out) and len(out[-1]) == 1 and MARK.match(out[-1][0])  # 見出しの1行のあと
        new = prev_blank or MARK.match(text) or ((ends in "。．.:：!?！？" or heading) and indent > prev_indent)
        if new or not out:
            out.append([text])
        else:
            out[-1].append(text)
        prev_blank, prev_indent = False, indent
    sep = "" if japanese else " "
    return [re.sub(r" {2,}", " ", sep.join(p)) for p in out]


CJK_SPACE = re.compile(r"(?<=[　-〿㐀-鿿＀-￯]) +| +(?=[　-〿㐀-鿿＀-￯])")


def chinese_paragraphs(page: str) -> list[str]:
    """中国語は、行を空白なしでつなぎ、漢字のあいだの空白（割り付けで入ったもの）を除く"""
    return [CJK_SPACE.sub("", p) for p in paragraphs(page, True)]


def sections(paras: list[str]) -> list[str]:
    """見出しの印のある段落で区切る（最初の見出しより前の段落も1つの区切りにする）"""
    out: list[list[str]] = []
    for p in paras:
        if MARK.match(p) or not out:
            out.append([p])
        else:
            out[-1].append(p)
    return ["\n".join(s) for s in out]


def convert(pdfs: dict[str, bytes]) -> list[dict]:
    records = []
    for lang, data in pdfs.items():
        pages = pdf_pages(data)
        # 2ページ目から、日本語のページと次のページ（訳）の組。図や表のページは仮名が少ないので、組の大部分で
        # 日本語のページのほうが仮名が多いことを確かめる
        pairs = [(i, i + 1) for i in range(1, len(pages) - 1, 2)]
        ok = sum(kana(pages[i]) > kana(pages[j]) for i, j in pairs)
        if len(pairs) < 15 or ok < 0.85 * len(pairs):
            raise ValueError(f"{lang}: 日本語のページと訳のページの並びが想定と違う（{ok}/{len(pairs)} 組）")
        for i, j in pairs:
            ja_p = paragraphs(pages[i], True)
            tr_p = chinese_paragraphs(pages[j]) if lang == "zh-Hans" else paragraphs(pages[j], False)
            if not ja_p and not tr_p:
                continue
            rec = {
                "source": DATASET, "version": VERSION, "lang": lang, "pages": [i + 1, j + 1],
                "ja": "\n".join(ja_p), "tr": "\n".join(tr_p),
            }
            ja_s, tr_s = sections(ja_p), sections(tr_p)
            if len(ja_s) > 1 and len(ja_s) == len(tr_s):
                rec["sections"] = [{"ja": a, "tr": b} for a, b in zip(ja_s, tr_s)]
            records.append(rec)
    return records


def main() -> int:
    (CACHE / DATASET).mkdir(parents=True, exist_ok=True)
    pdfs = {}
    for lang, url in PDFS.items():
        def fetch(url=url) -> bytes:
            time.sleep(WAIT)
            return opener().open(url, timeout=120).read()
        pdfs[lang] = cached(f"{DATASET}/{lang}.pdf", fetch)
    records = convert(pdfs)
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": f"文部科学省「{TITLE}」",
        "version": f"{VERSION}（英語版・ウクライナ語版の PDF は2022年に作り直したもの）",
        "url": PAGE,
        "files": PDFS,
        "license": "PDL-1.0",
        "license_url": TERMS_URL,
        "attribution": f"出典：文部科学省「{TITLE}」（{PAGE}）を加工して作成",
        "source_sha256_of": "8言語の PDF を、files の順につないだもの",
    }, b"".join(pdfs[k] for k in PDFS))
    aligned = sum("sections" in r for r in records)
    print(f"{DATASET}: {len(records)} 組（見出しで組にできたもの {aligned}）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
