"""取り込みのスクリプトで共通に使うもの（標準ライブラリだけ）。"""

from __future__ import annotations

import datetime
import hashlib
import http.cookiejar
import json
import os
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
DATA = ROOT / "data"

# 取得するときの名乗り。ブラウザには偽装しない
USER_AGENT = "yasashii-refs/0.1 (+https://github.com/silloi/yasashii-refs)"


def opener() -> urllib.request.OpenerDirector:
    """クッキーを保つ取得用の opener。SSL_CERT_FILE があれば、その証明書で検証する（プロキシ環境のため）"""
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
    op = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
        urllib.request.HTTPSHandler(context=ctx),
    )
    op.addheaders = [("User-Agent", USER_AGENT)]
    return op


def cached(name: str, fetch) -> bytes:
    """.cache/<name> があればそれを使い、無ければ fetch() で取得して保存する。--refresh で取り直す"""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / name
    if path.exists() and "--refresh" not in os.sys.argv:
        return path.read_bytes()
    data = fetch()
    path.write_bytes(data)
    return data


def write_dataset(dataset_id: str, records: list[dict], meta: dict, source_bytes: bytes) -> None:
    """data/<id>.jsonl（1行1項目）と data/<id>.meta.json（出典・版・件数など）を書く"""
    DATA.mkdir(exist_ok=True)
    with open(DATA / f"{dataset_id}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
    meta = {
        **meta,
        "records": len(records),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "generated": datetime.date.today().isoformat(),
    }
    with open(DATA / f"{dataset_id}.meta.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
