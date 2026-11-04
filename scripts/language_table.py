#!/usr/bin/env python3
"""目録の前付けの languages から、資料ごとの言語の対応表（docs/language-coverage.md）を作る。

使い方:
  python3 scripts/language_table.py           docs/language-coverage.md を作り直す
  python3 scripts/language_table.py --check   作り直しが要るかだけ確かめる（要るなら終了コード 1）

目録を直したら作り直す。scripts/check_catalog.py も、この表が目録と合っているかを確かめる。
"""

from __future__ import annotations

import re
import sys

from check_catalog import CATALOG, DOMAINS, LANGUAGES, ROOT, parse_front_matter

OUT = ROOT / "docs" / "language-coverage.md"

# 表に入れる分類（catalog/ のフォルダ）。外国人や日本語の学習者が読む・使う資料の分類。
# 漢字・語彙（辞書の訳語の言語）、統計、道具、やさしい日本語（書く側の資料）は入れない
CATEGORIES = ["life-info", "terms", "official-writing", "levels"]
CATEGORY_NAMES = "生活情報・用語・公用文・レベル"

# docs/priorities.md の「併記する言語の順番（案）」。そちらを変えたら、ここも直す
GROUPS = [
    ("第1群", ["vi", "zh-Hans", "en", "tl", "ne", "id", "pt", "ko", "my"]),
    ("第2群", ["es", "th", "zh-Hant", "km", "mn"]),
    ("第3群", ["si", "bn", "ur", "ta"]),
]
GROUPED = [code for _, codes in GROUPS for code in codes]
FIRST_GROUP = GROUPS[0][1]
COLUMNS = ["ja-easy"] + GROUPED

# docs/priorities.md の分野の順位（「全般」は順位なしで先頭）
DOMAIN_RANKS = [
    ("全般", None), ("入国・在留手続", 1), ("緊急・災害", 2), ("医療", 3), ("市区町村での手続", 4),
    ("年金・福祉", 5), ("税金", 5), ("出産・子育て", 6), ("教育", 6), ("雇用・労働", 7),
    ("住居", 8), ("交通", 9), ("日常生活のルール・習慣", 9),
]
DOMAIN_POS = {d: i for i, (d, _) in enumerate(DOMAIN_RANKS)}
assert set(DOMAIN_POS) == DOMAINS, "DOMAIN_RANKS が scripts/check_catalog.py の DOMAINS と合わない"

JAPANESE = {"ja", "ja-easy"}
ZH_ANY = "zh"  # 簡体字・繁体字の区別が無い中国語（話し言葉の対応など）。表では zh-Hans の列に＊


def short_name(name: str) -> str:
    """表を狭くするため、名前から「（…）」を除き、「—」より前を取る"""
    while True:
        cut = re.sub(r"（[^（）]*）", "", name)
        if cut == name:
            break
        name = cut
    return re.split(r"[—―]", name, maxsplit=1)[0].strip()


def languages_note(text: str) -> str | None:
    """本文の「前付けの `languages` は…。」（言語の意味がほかと違う資料の注記）"""
    m = re.search(r"前付けの `languages` は[^。\n]*。", text)
    return m.group(0) if m else None


def load_entries() -> list[dict]:
    every_domain = DOMAINS - {"全般"}
    entries = []
    for path in sorted(CATALOG.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_front_matter(text)
        if fm is None or fm.get("category") not in CATEGORIES:
            continue
        domains = fm["domains"]
        langs = list(dict.fromkeys(fm["languages"]))
        entries.append({
            "id": fm["id"],
            "ref": f"[{short_name(fm['name'])}](../catalog/{fm['category']}/{fm['id']}.md)",
            "handling": fm["handling"],
            "domains": domains,
            # 最初の分野の表に入れる（すべての分野にわたるものは「全般」）
            "primary": "全般" if "全般" in domains or every_domain <= set(domains) else domains[0],
            "langs": langs,
            "foreign": [lang for lang in langs if lang not in JAPANESE],
            "note": languages_note(text),
        })
    return entries


def lang_order(code: str) -> int:
    return list(LANGUAGES).index(code)


def others(e: dict) -> list[str]:
    return sorted((c for c in e["foreign"] if c not in GROUPED and c != ZH_ANY), key=lang_order)


def has(e: dict, code: str) -> bool:
    """その言語があるか（字体の区別が無い中国語は、簡体字があるものとして数える）"""
    return code in e["langs"] or (code == "zh-Hans" and ZH_ANY in e["langs"])


def cell(e: dict, code: str) -> str:
    if code in e["langs"]:
        return "○"
    if code == "zh-Hans" and ZH_ANY in e["langs"]:
        return "＊"
    return ""


def table(entries: list[dict]) -> list[str]:
    head = ["資料", "扱い"] + COLUMNS + ["その他", "外国語"]
    align = ["----", "----"] + [":-:"] * len(COLUMNS) + ["----", "--:"]
    lines = ["| " + " | ".join(head) + " |", "| " + " | ".join(align) + " |"]
    for e in entries:
        cells = [e["ref"], e["handling"]] + [cell(e, c) for c in COLUMNS]
        cells += ["・".join(others(e)), str(len(e["foreign"]))]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def render() -> str:
    entries = load_entries()
    rows = [e for e in entries if e["foreign"]]
    no_foreign = [e for e in entries if not e["foreign"]]
    others_used = sorted({c for e in rows for c in others(e)}, key=lang_order)
    by_domain = lambda e: (DOMAIN_POS[e["primary"]], -len(e["foreign"]), e["id"])  # noqa: E731

    out = [
        "# 資料ごとの言語の対応",
        "",
        "<!-- scripts/language_table.py が目録の前付けから作るファイル。手で直さない。 -->",
        "",
        "目録の資料が、どの言語で読めるか（使えるか）の一覧。目録の前付けの `languages` から"
        " `python3 scripts/language_table.py` で作る。手で直さず、目録を直してから作り直す。",
        "",
        f"- 対象: {CATEGORY_NAMES}の分類の資料のうち、外国語が1つ以上あるもの（{len(rows)}件）。"
        f"外国語が無いもの（{len(no_foreign)}件）は、最後の「外国語の版が無い資料」にまとめた。",
        "- 分野: 前付けの `domains` の最初の分野の表に入れる（すべての分野にわたるものは「全般」）。"
        "分野の順は [priorities.md](priorities.md) の順位。",
        "- 列の言語は、[priorities.md](priorities.md) の「併記する言語の順番（案）」の群の順。日本語の列は省いた。",
        f"  - ja-easy: {LANGUAGES['ja-easy']}",
    ]
    for group, codes in GROUPS:
        out.append(f"  - {group}: " + "、".join(f"{c} {LANGUAGES[c]}" for c in codes))
    if others_used:
        out.append("  - その他の列: " + "、".join(f"{c} {LANGUAGES[c]}" for c in others_used))
    out += [
        "- ○＝ある。＊＝中国語だが、簡体字・繁体字の区別が無い（話し言葉の対応など）。空欄＝無い。",
        "- 資料の中の一部の文書だけにある言語も○にした（どの文書にあるかは各項目の本文）。"
        "言語は、各項目を確かめた日（前付けの `checked`）の時点。",
        "",
        "## 分野ごとの表",
    ]

    for domain, rank in DOMAIN_RANKS:
        own = sorted((e for e in rows if e["primary"] == domain), key=by_domain)
        related = sorted(
            (e for e in rows if e["primary"] not in (domain, "全般") and domain in e["domains"]), key=by_domain
        )
        out += ["", f"### {domain}" if rank is None else f"### {rank}. {domain}", ""]
        out += table(own) if own else ["この分野を最初に挙げた資料は無い。"]
        if related:
            out += ["", "ほかの分野の表にある関連の資料: " + "、".join(f"{e['ref']}（{e['primary']}）" for e in related)]

    def count(code: str) -> str:
        have = [e for e in rows if code in e["langs"]]
        text = str(len(have))
        if 0 < len(have) <= 3:
            text += "（" + "、".join(e["ref"] for e in have) + "）"
        return text

    out += [
        "",
        "## 言語ごとの数",
        "",
        f"表の{len(rows)}件のうち、その言語がある資料の数。3件以下のときは資料も挙げた。",
        "",
        "| 群 | 言語 | 資料の数 |",
        "| -- | ---- | -------- |",
        f"| — | {LANGUAGES['ja-easy']}（ja-easy） | {count('ja-easy')} |",
    ]
    for group, codes in GROUPS:
        out += [f"| {group} | {LANGUAGES[c]}（{c}） | {count(c)} |" for c in codes]
    if any(ZH_ANY in e["langs"] for e in rows):
        out.append(f"| — | {LANGUAGES[ZH_ANY]}（{ZH_ANY}）＊ | {count(ZH_ANY)} |")
    for c in sorted(others_used, key=lambda c: (-sum(c in e["langs"] for e in rows), lang_order(c))):
        out.append(f"| その他 | {LANGUAGES[c]}（{c}） | {count(c)} |")

    out += [
        "",
        "## 第1群の言語が欠けている資料",
        "",
        "第1群の9言語のうち、無いものがある資料（分野の順）。＊の中国語は、あるものとして数えた。",
        "",
    ]
    english_only = [e for e in sorted(rows, key=by_domain) if e["foreign"] == ["en"]]
    for e in sorted(rows, key=by_domain):
        missing = [c for c in FIRST_GROUP if not has(e, c)]
        if missing and e not in english_only:
            out.append(f"- {e['ref']}（{e['primary']}）: " + "、".join(LANGUAGES[c] for c in missing))
    if english_only:
        out.append("- 外国語が英語だけ: " + "、".join(f"{e['ref']}（{e['primary']}）" for e in english_only))

    noted = [e for e in sorted(rows, key=by_domain) if e["note"]]
    if noted:
        out += ["", "## 注記", ""]
        out += [f"- {e['ref']}: {e['note']}" for e in noted]

    out += [
        "",
        "## 外国語の版が無い資料",
        "",
        f"{CATEGORY_NAMES}の分類で、前付けの `languages` が日本語・やさしい日本語だけのもの。"
        "外国人に向けた資料とは限らない（自治体・医療機関・日本語教育の関係者に向けたものや、公用文の決まりを含む）。",
        "",
    ]
    out += [f"- {e['ref']}（{e['primary']}）" for e in sorted(no_foreign, key=by_domain)]
    return "\n".join(out) + "\n"


def is_current() -> bool:
    return OUT.exists() and OUT.read_text(encoding="utf-8") == render()


def main() -> int:
    if "--check" in sys.argv[1:]:
        if is_current():
            return 0
        print("docs/language-coverage.md が目録と合わない（python3 scripts/language_table.py で作り直す）")
        return 1
    OUT.write_text(render(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
