#!/usr/bin/env python3
"""目録の URL のリンク切れと、配布ページ・利用条件のページの変化を確かめる。

使い方:
  python3 scripts/check_links.py              確かめて、前回から変わったところを出し、catalog/link-state.json を書き直す
  python3 scripts/check_links.py --dry-run    書き直さない
  python3 scripts/check_links.py --only ID    目録の id（または docs/priorities.md などのファイル）で絞る。何度でも指定できる

確かめる URL と、記録すること:
- 前付けの url（配布ページ）と、取り込んだデータの配布元（data/*.meta.json の url）:
  状態と、ページの中の同じホストのファイル（PDF・Excel・Word・CSV・ZIP など）へのリンクの一覧。
  資料の新しい版は、たいていファイルの名前や番号が変わって表れる
- 前付けの license_url（利用条件のページ）: 状態と、本文の文字のハッシュ（条件が書き換わったら分かる）
- 目録の本文・catalog/README.md・docs/ に書いた URL: 状態。ファイルは大きさ（Content-Length）と更新日時（Last-Modified）も
- 状態は、HTTP のステータス、転送先、ステータスが 200 でも「ページが見つかりません」のページか

catalog/link-state.json の差分（git diff）が、そのまま変化の記録になる。
取得は1つずつ、同じホストには1秒あけ、「yasashii-refs」と名乗る（scripts/common.py の USER_AGENT）。
ボット対策で止まるサイトは、そのステータスを記録するだけにする（中身はブラウザで確かめる）。
同じ名前のまま中身が替わったファイルは、配布ページのリンクの一覧だけでは分からない。
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
from pathlib import Path

from check_catalog import CATALOG, ROOT, parse_front_matter
from common import opener

STATE = CATALOG / "link-state.json"
DOC_EXT = re.compile(r"\.(pdf|xlsx?|xlsm|docx?|csv|zip|xml|pptx?|json|gz|txt)(?=$|[?#&])", re.I)
URL_RE = re.compile(r"https?://[^\s）)」』、。，<>\[\]|`\"']+")
NOT_FOUND = re.compile(r"見つかりません|ページがありません|\b404\b|Not Found", re.I)
WAIT = 1.0  # 同じホストへの間隔（秒）
RETRY_WAIT = 5.0  # 接続の失敗や 5xx のとき、やり直すまでの間（秒）
TIMEOUT = 30
MAX_PAGE = 10_000_000
FIELDS = {"status": "状態", "final": "転送先", "not_found": "「見つかりません」のページ", "length": "大きさ", "modified": "更新日時"}


def collect_urls(root: Path = ROOT) -> dict[str, dict]:
    """URL ごとに、どこに書いてあるか（refs）と、何として確かめるか（roles: page / terms / link）"""
    catalog = root / "catalog"
    found: dict[str, dict] = {}

    def add(url: str, ref: str, role: str) -> None:
        url = url.strip().rstrip(".,:;")
        if url.startswith(("http://", "https://")):
            entry = found.setdefault(url, {"refs": set(), "roles": set()})
            entry["refs"].add(ref)
            entry["roles"].add(role)

    for path in sorted(catalog.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_front_matter(text) or {}
        ref = str(fm.get("id", path.stem))
        add(str(fm.get("url", "")), ref, "page")
        add(str(fm.get("license_url", "")), ref, "terms")
        end = text.find("\n---\n", 4)
        for url in URL_RE.findall(text[end + 5:] if end >= 0 else text):
            add(url, ref, "link")
    for path in [catalog / "README.md", *sorted((root / "docs").glob("*.md"))]:
        if path.exists():
            for url in URL_RE.findall(path.read_text(encoding="utf-8")):
                add(url, path.relative_to(root).as_posix(), "link")
    for path in sorted((root / "data").glob("*.meta.json")):
        meta = json.loads(path.read_text(encoding="utf-8"))
        add(str(meta.get("url", "")), str(meta.get("source", path.name)), "page")
    return found


def decode(raw: bytes, ctype: str) -> str:
    m = re.search(r"charset=([\w-]+)", ctype, re.I)
    enc = m.group(1) if m else None
    if not enc:
        mb = re.search(rb"charset=[\"']?([\w-]+)", raw[:4000], re.I)
        enc = mb.group(1).decode("ascii", "replace") if mb else "utf-8"
    enc = enc.lower()
    if enc in ("shift_jis", "shift-jis", "sjis", "x-sjis"):
        enc = "cp932"
    try:
        return raw.decode(enc, "replace")
    except LookupError:
        return raw.decode("utf-8", "replace")


def page_title(page: str) -> str:
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", page)
    return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip() if m else ""


def file_links(page: str, base: str) -> list[str]:
    """ページの中の、同じホストのファイル（PDF・Excel など）へのリンク"""
    host = urllib.parse.urlsplit(base).netloc
    links = set()
    for href in re.findall(r"(?is)<a\b[^>]*?\bhref\s*=\s*[\"']([^\"']+)[\"']", page):
        url = urllib.parse.urldefrag(urllib.parse.urljoin(base, html.unescape(href.strip())))[0]
        parts = urllib.parse.urlsplit(url)
        if parts.scheme in ("http", "https") and parts.netloc == host and DOC_EXT.search(url):
            links.add(url)
    return sorted(links)


def text_hash(page: str) -> str:
    """ページの文字（スクリプト・スタイル・コメントを除く）のハッシュ"""
    body = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", page)
    body = re.sub(r"(?s)<!--.*?-->", " ", body)
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", body))).strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class Fetcher:
    def __init__(self) -> None:
        self.op = opener()
        self.last: dict[str, float] = {}

    def check(self, url: str, roles: set[str]) -> dict:
        rec = self.check_once(url, roles)
        if not isinstance(rec["status"], int) or rec["status"] >= 500:  # 一時的な失敗は、少し待って1回だけやり直す
            time.sleep(RETRY_WAIT)
            rec = self.check_once(url, roles)
        return rec

    def check_once(self, url: str, roles: set[str]) -> dict:
        host = urllib.parse.urlsplit(url).netloc
        wait = self.last.get(host, 0.0) + WAIT - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        rec: dict = {}
        try:
            with self.op.open(url, timeout=TIMEOUT) as resp:
                rec["status"] = resp.status
                final = resp.geturl()
                if final != url:
                    rec["final"] = final
                ctype = resp.headers.get("Content-Type", "")
                if "html" in ctype or (not ctype and not DOC_EXT.search(url)):
                    page = decode(resp.read(MAX_PAGE), ctype)
                    if NOT_FOUND.search(page_title(page)):
                        rec["not_found"] = True
                    if "page" in roles:
                        rec["files"] = file_links(page, final)
                    if "terms" in roles:
                        rec["text"] = text_hash(page)
                else:
                    for key, header in (("length", "Content-Length"), ("modified", "Last-Modified")):
                        if resp.headers.get(header):
                            rec[key] = resp.headers[header]
        except urllib.error.HTTPError as e:
            rec["status"] = e.code
        except Exception as e:  # 接続できない・時間切れなど
            rec["status"] = f"error: {type(e).__name__}"
        finally:
            self.last[host] = time.monotonic()
        return rec


def ok(rec: dict) -> bool:
    return isinstance(rec.get("status"), int) and 200 <= rec["status"] < 300 and not rec.get("not_found")


def changes(old: dict, new: dict) -> list[str]:
    """前回の記録（old）と今回（new）の違い"""
    out = []
    for url in sorted(new):
        rec, prev = new[url], old.get(url)
        if prev is None:
            continue
        notes = []
        for key, label in FIELDS.items():
            if prev.get(key) != rec.get(key):
                notes.append(f"{label} {prev.get(key, '—')} → {rec.get(key, '—')}")
        if "text" in prev and "text" in rec and prev["text"] != rec["text"]:
            notes.append("本文が変わった")
        added = removed = []
        if "files" in prev and "files" in rec:
            added = sorted(set(rec["files"]) - set(prev["files"]))
            removed = sorted(set(prev["files"]) - set(rec["files"]))
            if added or removed:
                notes.append(f"ファイルのリンク +{len(added)} −{len(removed)}")
        if notes:
            out.append(f"- [{'・'.join(rec['refs'])}] {url}: " + "、".join(notes))
            out += [f"    + {u}" for u in added] + [f"    − {u}" for u in removed]
    return out


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    only = {argv[i + 1] for i, a in enumerate(argv[:-1]) if a == "--only"}
    targets = collect_urls()
    if only:
        targets = {u: t for u, t in targets.items() if t["refs"] & only}
    old = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}

    fetcher = Fetcher()
    new: dict[str, dict] = {}
    for i, (url, target) in enumerate(sorted(targets.items()), 1):
        print(f"\r確かめている: {i}/{len(targets)}", end="", file=sys.stderr, flush=True)
        new[url] = {"refs": sorted(target["refs"]), **fetcher.check(url, target["roles"])}
    print(file=sys.stderr)

    print(f"確かめた URL: {len(new)}")
    if old:
        diff = changes(old, new)
        print("前回から変わったところ:" if diff else "前回から変わったところは無い。")
        if diff:
            print("\n".join(diff))
        added = [u for u in new if u not in old]
        if added:
            print(f"新しく確かめた URL: {len(added)}")
    else:
        print("前回の記録が無いので、今回の結果を記録だけする。")
    bad = [(u, r) for u, r in sorted(new.items()) if not ok(r)]
    if bad:
        print("取得できなかったもの（ボット対策で止まるものや、目録にリンク切れと書いたものを含む）:")
        for url, rec in bad:
            state = "「見つかりません」のページ" if rec.get("not_found") else rec["status"]
            print(f"- [{'・'.join(rec['refs'])}] {url}: {state}")

    if not dry_run:
        if only:  # 絞ったときは、ほかの URL の記録を残す（目録から消えた URL は落とす）
            current = collect_urls()
            state = {u: r for u, r in old.items() if u in current}
            state.update(new)
        else:
            state = new
        STATE.write_text(json.dumps(dict(sorted(state.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
