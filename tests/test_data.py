"""data/ の取り込んだデータを確かめる。

python3 -m unittest discover -s tests
"""

from __future__ import annotations

import collections
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(dataset: str) -> list[dict]:
    with open(DATA / f"{dataset}.jsonl", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


class AllDatasets(unittest.TestCase):
    def test_each_record_has_source_and_version_and_meta_matches(self):
        files = sorted(DATA.glob("*.jsonl"))
        self.assertTrue(files)
        catalog_ids = {p.stem for p in (ROOT / "catalog").glob("*/*.md")}
        for path in files:
            dataset = path.stem
            with self.subTest(dataset=dataset):
                self.assertIn(dataset, catalog_ids, "目録に同じ id の資料が無い")
                records = load(dataset)
                for rec in records:
                    self.assertEqual(rec["source"], dataset)
                    self.assertTrue(rec["version"])
                meta = json.loads((DATA / f"{dataset}.meta.json").read_text(encoding="utf-8"))
                self.assertEqual(meta["records"], len(records))
                self.assertTrue(meta["attribution"].startswith("出典："))
                self.assertTrue(meta["license"])


class JltStandardDict(unittest.TestCase):
    records = load("jlt-standard-dict")

    def test_counts(self):
        # 19.0 の CSV は 5,248 行（訳語の候補ごとに1行）、3,869 語
        self.assertEqual(len(self.records), 3869)
        self.assertEqual(sum(len(r["translations"]) for r in self.records), 5248)
        self.assertEqual(len({(r["term"], r["reading"]) for r in self.records}), 3869)

    def test_sample_term_keeps_order_and_fields(self):
        rec = next(r for r in self.records if r["term"] == "相手方")
        self.assertEqual(rec["reading"], "あいてがた")
        self.assertEqual([t["en"] for t in rec["translations"]],
                         ["opponent", "the other party/other parties", "opposite party", "counterparty", "adverse party"])
        first = rec["translations"][0]
        self.assertEqual((first["no"], first["usage"]), (1, "対審手続の場合"))
        self.assertEqual(first["example"]["source"], "刑事訴訟法第299条")

    def test_notes_stay_on_the_row_they_came_from(self):
        rec = next(r for r in self.records if r["term"] == "悪意で")
        self.assertIn("notes", rec["translations"][0])
        self.assertTrue(all("notes" not in t for t in rec["translations"][1:]))


class GakunenKanji(unittest.TestCase):
    records = load("gakunen-kanji")

    def test_counts_per_grade(self):
        counts = collections.Counter(r["grade"] for r in self.records)
        self.assertEqual(dict(counts), {1: 80, 2: 160, 3: 200, 4: 202, 5: 193, 6: 191})
        self.assertEqual(len({r["kanji"] for r in self.records}), 1026)

    def test_samples(self):
        grade = {r["kanji"]: r["grade"] for r in self.records}
        self.assertEqual(grade["一"], 1)
        # 平成29年の改訂で、都道府県名に使う漢字（茨・媛・岡など）を第4学年に加えた
        for k in "茨媛岡潟岐熊香佐埼崎滋鹿縄井沖栃奈梨阪阜":
            self.assertEqual(grade[k], 4, k)


if __name__ == "__main__":
    unittest.main()
