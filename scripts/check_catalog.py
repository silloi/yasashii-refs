#!/usr/bin/env python3
"""目録（catalog/**/*.md）の前付けを確かめる。

- 必須の項目があるか、決められた値か
- languages の言語が LANGUAGES（下）にあるか
- id がファイル名と同じか、category がフォルダ名と同じか
- checked が日付か
- catalog/README.md の一覧に、すべての id が載っているか（一覧にだけある id も見つける）
- docs/language-coverage.md（言語の対応表）が目録と合っているか（scripts/language_table.py で作り直す）

使い方: python3 scripts/check_catalog.py   （問題が無ければ何も出さずに終わる。問題があれば終了コード 1）
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"

REQUIRED = [
    "id", "name", "publisher", "url", "category", "domains", "languages", "formats",
    "version", "license", "license_url", "commercial", "redistribution", "attribution",
    "handling", "uses", "checked",
]
ALLOWED = {
    "handling": {"ingest", "link", "outreach", "exclude"},
    "commercial": {"yes", "no", "未確認"},
    "redistribution": {"yes", "no", "未確認"},
}
ALLOWED_USES = {"reference", "resource"}
# docs/priorities.md の分野（生活・就労ガイドブックの章）と「全般」
DOMAINS = {
    "全般", "入国・在留手続", "市区町村での手続", "雇用・労働", "出産・子育て", "教育", "医療",
    "年金・福祉", "税金", "交通", "緊急・災害", "住居", "日常生活のルール・習慣",
}
# 前付けの languages に使う言語と、その名前（docs/language-coverage.md の凡例にも使う）。
# 新しい言語を使ったら、ここに足す
LANGUAGES = {
    "ja": "日本語", "ja-easy": "やさしい日本語",
    "vi": "ベトナム語", "zh-Hans": "中国語（簡体字）", "en": "英語", "tl": "フィリピノ語",
    "ne": "ネパール語", "id": "インドネシア語", "pt": "ポルトガル語", "ko": "韓国語", "my": "ミャンマー語",
    "es": "スペイン語", "th": "タイ語", "zh-Hant": "中国語（繁体字）", "km": "クメール語", "mn": "モンゴル語",
    "si": "シンハラ語", "bn": "ベンガル語", "ur": "ウルドゥー語", "ta": "タミル語",
    "zh": "中国語（字体の区別なし）",
    "hi": "ヒンディー語", "tr": "トルコ語", "uk": "ウクライナ語", "ru": "ロシア語", "fr": "フランス語",
    "ar": "アラビア語", "fa": "ペルシア語", "de": "ドイツ語", "it": "イタリア語", "lo": "ラオ語",
    "hr": "クロアチア語",
}


def parse_front_matter(text: str) -> dict[str, object] | None:
    """`key: value` と `key: [a, b]` だけの、簡単な YAML を読む（標準ライブラリだけで動かすため）"""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    data: dict[str, object] = {}
    for line in text[4:end].splitlines():
        line = re.sub(r"\s+#.*$", "", line).rstrip()
        if not line:
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not m:
            raise ValueError(f"読めない行: {line}")
        key, value = m.group(1), m.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            data[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            data[key] = value.strip('"')
    return data


def main() -> int:
    problems: list[str] = []
    index = (CATALOG / "README.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"\[([a-z0-9-]+)\]\([a-z-]+/[a-z0-9-]+\.md\)", index))
    ids: set[str] = set()
    for path in sorted(CATALOG.glob("*/*.md")):
        rel = path.relative_to(ROOT)
        try:
            fm = parse_front_matter(path.read_text(encoding="utf-8"))
        except ValueError as e:
            problems.append(f"{rel}: {e}")
            continue
        if fm is None:
            problems.append(f"{rel}: 前付け（--- で囲んだ YAML）が無い")
            continue
        for key in REQUIRED:
            if key not in fm or fm[key] in ("", []):
                problems.append(f"{rel}: {key} が無い")
        for key, allowed in ALLOWED.items():
            if key in fm and fm[key] not in allowed:
                problems.append(f"{rel}: {key} は {sorted(allowed)} のどれか（いまは {fm[key]!r}）")
        for use in fm.get("uses", []) or []:
            if use not in ALLOWED_USES:
                problems.append(f"{rel}: uses の {use!r} は {sorted(ALLOWED_USES)} のどれか")
        for domain in fm.get("domains", []) or []:
            if domain not in DOMAINS:
                problems.append(f"{rel}: domains の {domain!r} は docs/priorities.md の分野ではない")
        for lang in fm.get("languages", []) or []:
            if lang not in LANGUAGES:
                problems.append(f"{rel}: languages の {lang!r} が scripts/check_catalog.py の LANGUAGES に無い")
        if fm.get("id") != path.stem:
            problems.append(f"{rel}: id（{fm.get('id')}）がファイル名と違う")
        if fm.get("category") != path.parent.name:
            problems.append(f"{rel}: category（{fm.get('category')}）がフォルダ名と違う")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fm.get("checked", ""))):
            problems.append(f"{rel}: checked は YYYY-MM-DD")
        ids.add(path.stem)
    for missing in sorted(ids - listed):
        problems.append(f"catalog/README.md: 一覧に {missing} が無い")
    for extra in sorted(listed - ids):
        problems.append(f"catalog/README.md: 一覧の {extra} に対応するファイルが無い")
    if not problems:  # 言語の対応表は、前付けに問題が無いときだけ確かめる
        from language_table import is_current

        if not is_current():
            problems.append("docs/language-coverage.md が目録と合わない（python3 scripts/language_table.py で作り直す）")
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
