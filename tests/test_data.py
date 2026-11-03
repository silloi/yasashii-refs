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


class PlainJapaneseRewrites(unittest.TestCase):
    records = load("plain-japanese-rewrites")

    def test_numbers_are_complete(self):
        self.assertEqual([r["no"] for r in self.records], list(range(1, 135)))
        for r in self.records:
            self.assertTrue(r["term"] and r["reading"] and r["plain"], r)

    def test_no_page_numbers_or_ruby_mixed_in(self):
        import re
        for r in self.records:
            # 各ページの最後の項目に、ページ番号が混ざっていない
            self.assertIsNone(re.search(r"\d$", r["plain"]), r["plain"])
            # 読みは、ひらがなと長音などだけ（漢字が混ざっていない）
            self.assertRegex(r["reading"], r"^[ぁ-ゖァ-ヺー・]+$", r["term"])

    def test_references_point_to_existing_entries(self):
        by_no = {r["no"]: r for r in self.records}
        for r in self.records:
            for n in r.get("see", []):
                self.assertIn(n, by_no)
        self.assertEqual(by_no[2]["see"], [1, 41])  # 育児休業給付金 → 育児休業、雇用保険
        self.assertEqual(by_no[35]["see"], [106])  # 「(NO.106)」と大文字で書かれている参照も拾う

    def test_samples(self):
        by_no = {r["no"]: r for r in self.records}
        self.assertEqual((by_no[1]["term"], by_no[1]["reading"], by_no[1]["plain"]),
                         ("育児休業", "いくじきゅうぎょう", "子どもを育てるために、とることができる休み。"))
        # 語の列で折り返している長い語は、1つにつなぐ
        self.assertEqual(by_no[36]["term"], "高等学校卒業程度認定試験")
        self.assertEqual(by_no[36]["reading"], "こうとうがっこうそつぎょうていどにんていしけん")


class JmaMultilingualDict(unittest.TestCase):
    records = load("jma-multilingual-dict")
    LANGS = {"en", "zh-Hans", "zh-Hant", "ko", "pt", "es", "id", "vi", "tl", "th", "ne", "km", "my", "mn"}

    def test_counts_and_numbers(self):
        self.assertEqual([r["no"] for r in self.records], list(range(1, 7280)))
        counts = collections.Counter(r["kind"] for r in self.records)
        self.assertEqual(dict(counts), {"用語": 6894, "情報文": 198, "対応行動": 187})
        self.assertRegex(self.records[0]["version"], r"^\d{4}-\d{2}-\d{2}$")

    def test_every_record_has_all_languages(self):
        for r in self.records:
            self.assertEqual(set(r["tr"]), self.LANGS, r["no"])
        # No.181 は日本語の欄が空（元のデータのまま）。ほかは日本語がある
        self.assertEqual([r["no"] for r in self.records if "ja" not in r], [181])

    def test_excel_furigana_is_not_mixed_into_text(self):
        by_no = {r["no"]: r for r in self.records}
        self.assertEqual(by_no[1]["ja"], "気象庁")
        self.assertEqual(by_no[4]["ja"], "気象警報")  # 「気象警報キショウケイホウ」にならない
        self.assertEqual((by_no[3]["ja"], by_no[3]["tr"]["en"]), ("特別警報", "Emergency Warning"))


class Kanjidic2(unittest.TestCase):
    records = load("kanjidic2")

    def test_grades_match_the_official_lists(self):
        counts = collections.Counter(r["grade"] for r in self.records if "grade" in r)
        self.assertEqual(dict(counts), {1: 80, 2: 160, 3: 200, 4: 202, 5: 193, 6: 191, 8: 1110, 9: 651, 10: 212})
        # 学年 1〜6 は学年別漢字配当表と1字も違わない
        gakunen = {r["kanji"]: r["grade"] for r in load("gakunen-kanji")}
        self.assertEqual({r["kanji"]: r["grade"] for r in self.records if r.get("grade", 99) <= 6}, gakunen)
        self.assertEqual(sum(1 for r in self.records if "freq" in r), 2501)  # 頻度順位は 2,500 位まで（同順位が1つ）

    def test_old_jlpt_levels_are_kept_apart_from_n_levels(self):
        counts = collections.Counter(r["jlpt_old"] for r in self.records if "jlpt_old" in r)
        self.assertEqual(dict(counts), {1: 1207, 2: 739, 3: 181, 4: 103})
        # いまの N1〜N5 と取り違えないよう、旧試験の級は jlpt_old に入れる
        self.assertTrue(all("jlpt" not in r for r in self.records))

    def test_sample(self):
        a = next(r for r in self.records if r["kanji"] == "亜")
        self.assertEqual((a["grade"], a["strokes"], a["jlpt_old"], a["on"], a["kun"]), (8, 7, 1, ["ア"], ["つ.ぐ"]))
        self.assertIn("Asia", a["meanings"]["en"])
        self.assertIn("A", a["readings_other"]["vi"])

    def test_license_is_share_alike(self):
        meta = json.loads((DATA / "kanjidic2.meta.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["license"], "CC-BY-SA-4.0")
        self.assertIn("Electronic Dictionary Research and Development Group", meta["attribution"])


class JoyoKanjiHyo(unittest.TestCase):
    records = load("joyo-kanji-hyo")
    main = [r for r in records if r["kind"] == "本表"]
    appendix = [r for r in records if r["kind"] == "付表"]
    by_kanji = {r["kanji"]: r for r in main}

    def test_counts(self):
        # 2,136字は表の見方 2 による。音訓の数は、辞典類が示す数（4,388、音 2,352・訓 2,036）と合う
        self.assertEqual([r["no"] for r in self.main], list(range(1, 2137)))
        self.assertEqual(len(self.by_kanji), 2136)
        readings = [x for r in self.main for x in r["readings"]]
        self.assertEqual(len(readings), 4388)
        self.assertEqual(dict(collections.Counter(x["type"] for x in readings)), {"on": 2352, "kun": 2036})
        self.assertEqual({r["kind"] for r in self.records}, {"本表", "付表"})

    def test_same_kanji_as_kanjidic2_and_covers_gakunen(self):
        kanjidic2 = {r["kanji"] for r in load("kanjidic2") if r.get("grade", 99) <= 8}
        self.assertEqual(set(self.by_kanji), kanjidic2)
        self.assertLessEqual({r["kanji"] for r in load("gakunen-kanji")}, set(self.by_kanji))

    def test_old_and_allowed_forms(self):
        self.assertEqual(sum(len(r.get("kyuji", [])) for r in self.main), 364)
        self.assertEqual(self.by_kanji["亜"]["kyuji"], ["亞"])
        self.assertEqual(self.by_kanji["弁"]["kyuji"], ["辨", "瓣", "辯"])
        self.assertEqual(self.by_kanji["亀"]["kyuji"], ["龜"])  # PDF から取り出せない字を補ったもの（スクリプトの MISSING_KYUJI）
        # 康熙字典体の一部は CJK 互換漢字。正規化（NFC）していない
        self.assertEqual(self.by_kanji["海"]["kyuji"], ["海"])
        self.assertEqual({k for k, r in self.by_kanji.items() if r.get("allowed_form")}, set("餌遡遜謎餅"))

    def test_readings_and_examples(self):
        self.assertEqual([x["reading"] for x in self.by_kanji["生"]["readings"]],
                         ["セイ", "ショウ", "いきる", "いかす", "いける", "うまれる", "うむ", "おう", "はえる", "はやす", "き", "なま"])
        # 1字下げの音訓（特別なもの・用法のごく狭いもの）
        self.assertEqual([(x["reading"], x.get("special", False)) for x in self.by_kanji["上"]["readings"]][:4],
                         [("ジョウ", False), ("ショウ", True), ("うえ", False), ("うわ", True)])
        self.assertNotIn("examples", self.by_kanji["宮"]["readings"][2])  # 「ク」は例が無く、備考に「宮内庁」
        # 折り返した例はつなぐ。例にはその字が必ず入っている
        self.assertEqual(self.by_kanji["今"]["readings"][0]["examples"], ["今後", "今日", "今朝", "今年", "昨今"])
        for r in self.main:
            for x in r["readings"]:
                for e in x.get("examples", []):
                    self.assertIn(r["kanji"], e)

    def test_notes(self):
        self.assertEqual(self.by_kanji["二"]["notes"][:2], ["十重二十重（とえはたえ）", "二十・二十歳（はたち）"])
        # 折り返した注記はつなぎ、詰めて組んだ約物の順番を直す
        self.assertEqual(self.by_kanji["羽"]["notes"], ["「羽（は）」は，前に来る音によって「わ」，「ば」，「ぱ」になる。"])
        self.assertEqual(self.by_kanji["雨"]["notes"][-1], "「春雨」，「小雨」，「霧雨」などは，「はるさめ」，「こさめ」，「きりさめ」。")
        self.assertEqual(self.by_kanji["差"]["notes"], ["差し支える（さしつかえる）", "⇔刺す，指す，挿す"])

    def test_appendix(self):
        self.assertEqual([r["no"] for r in self.appendix], list(range(1, 117)))
        by_reading = {r["reading"]: r for r in self.appendix}
        self.assertEqual(by_reading["あす"]["words"], ["明日"])
        self.assertEqual(by_reading["かわら"]["words"], ["河原", "川原"])
        self.assertEqual(by_reading["しわす"]["notes"], ["（「しはす」とも言う。）"])
        self.assertEqual(self.appendix[-1]["reading"], "わこうど")


if __name__ == "__main__":
    unittest.main()
