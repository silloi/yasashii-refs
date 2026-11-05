#!/usr/bin/env python3
"""厚生労働省「医療情報ネットのオープンデータ」の病院の施設票と、診療科・診療時間票の診療科の名前を、
data/iryo-joho-net-opendata.jsonl にする。

1行が1つの病院。
- 2026年6月1日時点の版（ZIP に入った CSV。https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/newpage_43373.html ）。
- 病院だけを入れる。診療所・歯科診療所・助産所・薬局と、診療時間は入れない（件数が多く、ファイルが大きくなるため。
  診療時間の票は病院だけで25万行・44MB）。
- 名前（正式名称・フリガナ・略称・英語表記）、都道府県・市区町村のコード、所在地、緯度・経度、案内用のホームページ、病床数。
  緯度・経度がどちらも 0 の病院（座標が無いもの）は、lat・lng を入れない。
- 休診日は、定義書（「0：休診 1：診療」）の値のまま、曜日の順（月火水木金土日）の7文字にまとめる。空欄は「-」。
  - weekly: 毎週決まった曜日
  - weeks: 決まった週（第1〜第5週）の曜日。5つの7文字
  - holiday: 祝日（1文字）
- 診療科は、診療科・診療時間票の診療科目名を、票に出てくる順に（重ねずに）入れる。
- CSV の列が想定と違えば止まる。

使い方: python3 scripts/ingest_iryo_joho_net_opendata.py [--refresh]
"""

from __future__ import annotations

import csv
import io
import sys
import zipfile

from common import CACHE, cached, opener, write_dataset

DATASET = "iryo-joho-net-opendata"
PAGE = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/newpage_43373.html"
DATE = "20260601"
FACILITY_URL = f"https://www.mhlw.go.jp/content/11121000/01-1_hospital_facility_info_{DATE}.csv.zip"
SPECIALITY_URL = f"https://www.mhlw.go.jp/content/11121000/01-2_hospital_speciality_hours_{DATE}.csv.zip"
TERMS_URL = "https://www.mhlw.go.jp/chosakuken/index.html"
DAYS = "月火水木金土日"

FIELDS = {
    "ID": "id", "正式名称": "name", "正式名称（フリガナ）": "name_kana", "略称": "short_name",
    "略称（フリガナ）": "short_name_kana", "英語表記（ローマ字表記）": "name_en",
    "都道府県コード": "pref_code", "市区町村コード": "city_code", "所在地": "address",
    "案内用ホームページアドレス": "url",
}
BEDS = {
    "一般病床": "general", "療養病床": "long_term_care", "療養病床のうち医療保険適用": "long_term_care_medical",
    "療養病床のうち介護保険適用": "long_term_care_nursing", "精神病床": "psychiatric", "結核病床": "tuberculosis",
    "感染症病床": "infectious", "合計病床数": "total",
}
OTHER_CLOSED = "その他の休診日（gw、お盆等）"


def read_csv(zip_bytes: bytes) -> list[dict]:
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    names = [n for n in z.namelist() if n.lower().endswith(".csv")]
    if len(names) != 1:
        raise ValueError(f"ZIP の中の CSV が1つではない: {names}")
    return list(csv.DictReader(io.StringIO(z.read(names[0]).decode("utf-8-sig"))))


def flags(row: dict, columns: list[str]) -> str:
    out = ""
    for c in columns:
        v = row[c].strip()
        if v not in ("0", "1", ""):
            raise ValueError(f"休診日の値が想定と違う: {c}={v!r}")
        out += v or "-"
    return out


def convert(facility: list[dict], speciality: list[dict]) -> list[dict]:
    header = list(facility[0])
    weekly = [f"毎週決まった曜日に休診（{d}）" for d in DAYS]
    weeks = [[f"決まった週に休診（定期週）第{n}週（{d}）" for d in DAYS] for n in range(1, 6)]
    expected = list(FIELDS) + ["所在地座標（緯度）", "所在地座標（経度）", "機関区分"] + weekly + sum(weeks, []) + \
        ["祝日に休診", OTHER_CLOSED] + list(BEDS)
    missing = [c for c in expected if c not in header]
    if missing:
        raise ValueError(f"施設票に無い列: {missing}")

    departments: dict[str, list[str]] = {}
    for row in speciality:
        names = departments.setdefault(row["ID"], [])
        name = row["診療科目名"].strip()
        if name and name not in names:
            names.append(name)

    records, seen = [], set()
    for row in facility:
        if row["機関区分"] != "1":
            raise ValueError(f"病院でない行: {row['ID']} 機関区分={row['機関区分']!r}")
        if row["ID"] in seen:
            raise ValueError(f"ID が重なる: {row['ID']}")
        seen.add(row["ID"])
        rec = {"source": DATASET, "version": f"{DATE[:4]}-{DATE[4:6]}-{DATE[6:]}"}
        for col, key in FIELDS.items():
            if row[col].strip():
                rec[key] = row[col].strip()
        lat, lng = row["所在地座標（緯度）"].strip(), row["所在地座標（経度）"].strip()
        if lat and lng and (float(lat), float(lng)) != (0.0, 0.0):  # 0 は座標が無いもの
            rec["lat"], rec["lng"] = float(lat), float(lng)
        rec["weekly"] = flags(row, weekly)
        rec["weeks"] = [flags(row, w) for w in weeks]
        rec["holiday"] = flags(row, ["祝日に休診"])
        if row[OTHER_CLOSED].strip():
            rec["closed_other"] = row[OTHER_CLOSED].strip()
        beds = {key: int(row[col]) for col, key in BEDS.items() if row[col].strip()}
        if beds:
            rec["beds"] = beds
        if departments.get(row["ID"]):
            rec["departments"] = departments[row["ID"]]
        records.append(rec)
    return records


def main() -> int:
    (CACHE / DATASET).mkdir(parents=True, exist_ok=True)
    fac_raw = cached(f"{DATASET}/{FACILITY_URL.rsplit('/', 1)[1]}", lambda: opener().open(FACILITY_URL, timeout=120).read())
    spe_raw = cached(f"{DATASET}/{SPECIALITY_URL.rsplit('/', 1)[1]}", lambda: opener().open(SPECIALITY_URL, timeout=300).read())
    records = convert(read_csv(fac_raw), read_csv(spe_raw))
    write_dataset(DATASET, records, {
        "source": DATASET,
        "name": "厚生労働省「医療情報ネットのオープンデータ」（病院の施設票と診療科）",
        "version": f"{DATE[:4]}-{DATE[4:6]}-{DATE[6:]} 時点",
        "url": PAGE,
        "files": [FACILITY_URL, SPECIALITY_URL],
        "license": "PDL-1.0",
        "license_url": TERMS_URL,
        "attribution": f"出典：厚生労働省「医療情報ネットのオープンデータ」（{PAGE}）を加工して作成",
        "source_sha256_of": "施設票の ZIP と、診療科・診療時間票の ZIP を、この順につないだもの",
    }, fac_raw + spe_raw)
    print(f"{DATASET}: 病院 {len(records)}（診療科あり {sum('departments' in r for r in records)}）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
