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


class IsaIchigenSoudan(unittest.TestCase):
    records = load("isa-ichigen-soudan")

    def test_counts(self):
        # 表題は「一元的相談窓口（２９０団体）」。1行が1つの窓口の場所で、同じ団体が複数の窓口・場所を持つことがある
        self.assertEqual([r["no"] for r in self.records], list(range(1, 349)))
        self.assertEqual(len({(r["prefecture"], r["establisher"]) for r in self.records}), 290)
        self.assertEqual(len({r["prefecture"] for r in self.records}), 47)

    def test_days_and_text_are_clean(self):
        allowed = ["月", "火", "水", "木", "金", "土", "日", "祝"]
        for r in self.records:
            self.assertTrue(r["days"], r["name"])
            self.assertEqual(r["days"], [d for d in allowed if d in r["days"]])  # 月から順に並ぶ
            self.assertNotIn("※", r["establisher"])
            for key in ("name", "address", "phone", "hours", "notes"):
                if key in r:
                    self.assertNotRegex(r[key], r"\s{2,}|\n", (r["no"], key))

    def test_merged_cells_are_spread(self):
        # 豊田市は、本庁舎と支所など6か所が同じ窓口（縦に結合したセルを各行に配っている）
        toyota = [r for r in self.records if r["establisher"] == "豊田市"]
        self.assertEqual(len(toyota), 6)
        self.assertEqual({r["name"] for r in toyota}, {"豊田市多言語サービスデスク"})
        self.assertTrue(all(r["hours"] == "8:30～17:15" for r in toyota))
        # 広島市と安芸郡の4町は、共同で1つの窓口を運営している
        joint = [r for r in self.records if r.get("joint")]
        self.assertEqual([r["establisher"] for r in joint], ["広島市", "府中町", "海田町", "熊野町", "坂町"])
        self.assertEqual({r["name"] for r in joint}, {"広島市・安芸郡外国人相談窓口"})

    def test_sample(self):
        first = self.records[0]
        self.assertEqual((first["prefecture"], first["establisher"], first["name"], first["phone"], first["hours"]),
                         ("北海道", "北海道", "北海道外国人相談センター", "011-200-9595", "9:00～17:00"))
        self.assertEqual(first["days"], ["月", "火", "水", "木", "金"])
        yamagata = next(r for r in self.records if r["establisher"] == "山形県")
        self.assertEqual(yamagata["name"], "山形県外国人総合相談\u3000ワンストップセンター")  # セルの中の空白の連続を1つに


class JpsNenkinYougo(unittest.TestCase):
    records = load("jps-nenkin-yougo")

    def term(self, name: str) -> dict:
        return next(r for r in self.records if r["term"] == name)

    def test_counts(self):
        # トップのページの一覧と、行ごとの索引のページ（わ行は0語）が同じ116語（2026-11-03 に確かめた）
        self.assertEqual(len(self.records), 116)
        self.assertEqual(len({r["id"] for r in self.records}), 116)
        self.assertEqual(collections.Counter(r["row"] for r in self.records),
                         {"か行": 32, "さ行": 24, "た行": 19, "は行": 17, "な行": 11, "あ行": 5, "ま行": 4, "や行": 2, "ら行": 2})

    def test_fields(self):
        for r in self.records:
            self.assertRegex(r["version"], r"^\d{4}-\d{2}-\d{2}$")  # ページの更新日
            self.assertTrue(r["url"].startswith("https://www.nenkin.go.jp/service/yougo/"))
            self.assertNotEqual(r["definition"].split("\n")[0], r["term"])  # 名前のくり返しは除く
            self.assertNotIn("関連リンク", r["definition"])
            self.assertNotIn("新規ウィンドウで開きます", r["definition"])

    def test_see_points_to_existing_terms(self):
        ids = {r["id"]: r["term"] for r in self.records}
        see = {r["term"]: ids[r["see"]] for r in self.records if "see" in r}
        self.assertEqual(see, {"カラ期間": "合算対象期間", "障害年金等受給権者の特別一時金": "特別一時金",
                               "随時改定": "月額変更届", "追納": "国民年金保険料の追納", "定時決定": "算定基礎届"})

    def test_sample(self):
        rec = self.term("学生納付特例制度")
        self.assertEqual((rec["id"], rec["row"], rec["version"]), ("kagyo/gakuseinofu", "か行", "2013-02-21"))
        self.assertTrue(rec["definition"].startswith("大学や専修学校等の学生であって、国民年金の第1号被保険者である本人"))
        self.assertEqual(rec["related"][1], {"title": "学生納付特例申請書",
                                             "url": "https://www.nenkin.go.jp/shinsei/kokunen/menjoyuyo/gakusei.html"})

    def test_tables_and_images_outside_the_text_box(self):
        # 表は本文の枠の外にある。行は改行で、セルはタブでつなぐ
        self.assertIn("配偶者\t65歳未満の配偶者 （大正15年4月1日以前に生まれた配偶者には年齢制限はありません）",
                      self.term("加給年金額")["definition"].split("\n"))
        # 計算式は画像。alt の文字で読む
        self.assertIn("平均標準報酬月額（※2）×（7.125（※4）÷1000）×平成15年3月までの加入期間の月数",
                      self.term("報酬比例部分")["definition"].split("\n"))


class MhlwTagengoYougo(unittest.TestCase):
    records = load("mhlw-tagengo-yougo")
    langs = {"en", "zh-Hans", "zh-Hant", "ko", "es", "pt", "tl", "vi", "ne", "id", "th", "my", "mn", "km"}

    def term(self, name: str) -> dict:
        return next(r for r in self.records if r["term"] == name)

    def test_counts(self):
        self.assertEqual([r["no"] for r in self.records], list(range(1, 419)))
        self.assertEqual(len({r["term"] for r in self.records}), 418)
        self.assertEqual(len({r["web_id"] for r in self.records}), 418)
        counts = collections.Counter(r["category"] for r in self.records)
        self.assertEqual(len(counts), 11)
        self.assertEqual(counts["2.賃金・社会保険料・税・給付金"], 104)
        self.assertEqual(counts["7.ハラスメント"], 10)

    def test_every_language_has_all_fields(self):
        for r in self.records:
            self.assertEqual(set(r["tr"]), self.langs, r["term"])
            for lang, t in r["tr"].items():
                self.assertEqual(set(t), {"term", "definition", "example"}, (r["term"], lang))
                for v in t.values():
                    self.assertTrue(v.strip())
                    self.assertNotIn("\n", v)  # セルの中の改行は空白にした
            self.assertEqual(set(r["ja_easy"]), {"term", "definition", "example"})

    def test_term_and_reading(self):
        for r in self.records:
            self.assertNotIn("（", r["term"])
            self.assertNotRegex(r["reading"], r"[一-鿿々〆]")
        self.assertEqual(self.term("打ち切り補償")["reading"], "うちきりほしょう")
        self.assertEqual(self.term("シフト表")["reading"], "シフトひょう")  # 片仮名はそのまま
        self.assertEqual(self.term("安全・衛生管理者")["reading"], "あんぜん・えいせいかんりしゃ")
        self.assertEqual(self.term("完全週休2日制")["reading"], "かんぜんしゅうきゅうふつかせい")

    def test_sample_and_web_id(self):
        rec = self.term("安全衛生")
        self.assertEqual((rec["no"], rec["web_id"], rec["category"]), (255, "c06_07", "6.安全衛生・災害補償"))
        self.assertEqual(rec["ja_easy"]["definition"], "安全（あんぜん）に健康（けんこう）に働（はたら）くことができること。")
        self.assertEqual(rec["tr"]["zh-Hans"]["term"], "安全卫生")
        self.assertEqual(self.term("選考試験")["tr"]["en"]["term"], "Selection test")

    def test_sheets_with_other_numbering_are_matched_by_japanese(self):
        # ポルトガル語・タガログ語のシートは項番の振り方が違う。日本語の列で突き合わせている
        self.assertEqual(self.term("消費税")["tr"]["pt"]["term"], "Imposto de consumo")
        self.assertEqual(self.term("労働時間")["tr"]["pt"]["term"], "Jornada de trabalho")
        self.assertEqual(self.term("労働時間")["tr"]["tl"]["term"], "Oras ng trabaho")


class JpsForeignResidents(unittest.TestCase):
    records = load("jps-foreign-residents")

    def test_counts(self):
        # やさしいにほんごの29ページから、リンクだけの目次の2ページを除く（2026-11-05）
        self.assertEqual(len(self.records), 27)
        self.assertEqual([r["url"] for r in self.records], sorted(r["url"] for r in self.records))
        meta = json.loads((DATA / "jps-foreign-residents.meta.json").read_text(encoding="utf-8"))
        self.assertEqual(len(meta["skipped_menu_pages"]), 2)

    def test_fields(self):
        kinds = {"p", "li", "h2", "h3", "h4", "h5", "tr", "dt", "dd", "caption"}
        for r in self.records:
            self.assertTrue(r["url"].startswith("https://www.nenkin.go.jp/international/simplejapanese/"))
            self.assertRegex(r["version"], r"^(\d{4}-\d{2}-\d{2}|更新日の記載なし)$")
            self.assertTrue(r["blocks"])
            for b in r["blocks"]:
                self.assertIn(b["type"], kinds)
                self.assertTrue(b["text"].strip())
                self.assertNotIn(b["text"], {"詳細を開く", "詳細を閉じる", "印刷"})
                self.assertNotIn("転載", b["text"])
            self.assertNotEqual(r["blocks"][0]["text"], r["title"])  # 見出しのくり返しは除く

    def test_sample(self):
        rec = next(r for r in self.records if r["url"].endswith("/benefit/withdrawalpayment.html"))
        self.assertEqual((rec["version"], rec["page_id"]), ("2026-03-02", "170010010-998-458-222"))
        self.assertTrue(rec["blocks"][0]["text"].startswith("外国人（がいこくじん）が　日本（にほん）で　短（みじか）い"))
        self.assertEqual(len(rec["links"]), 14)  # 脱退一時金の説明の、14言語の PDF
        self.assertEqual(rec["links"][0], {"text": "英語（えいご）（PDF）",
                                           "url": "https://www.nenkin.go.jp/shinsei/jukyu/sonota-kyufu/20150406.files/A.pdf"})


class IryoJohoNetOpendata(unittest.TestCase):
    records = load("iryo-joho-net-opendata")

    def test_counts(self):
        self.assertEqual(len(self.records), 7715)  # 病院の施設票（2026年6月1日時点）
        self.assertEqual(len({r["id"] for r in self.records}), 7715)
        self.assertEqual(len({r["pref_code"] for r in self.records}), 47)

    def test_fields(self):
        for r in self.records:
            self.assertEqual(r["version"], "2026-06-01")
            self.assertRegex(r["weekly"], r"^[01-]{7}$")
            self.assertEqual(len(r["weeks"]), 5)
            for w in r["weeks"]:
                self.assertRegex(w, r"^[01-]{7}$")
            self.assertRegex(r["holiday"], r"^[01-]$")
            if "lat" in r:
                self.assertTrue(20 < r["lat"] < 46 and 122 < r["lng"] < 154, r["id"])
            self.assertEqual(len(r.get("departments", [])), len(set(r.get("departments", []))))
        # 座標が 0 の病院（座標が無いもの）は lat・lng を入れていない
        self.assertEqual(sum("lat" not in r for r in self.records), 268)

    def test_sample(self):
        rec = self.records[0]
        self.assertEqual((rec["id"], rec["name"], rec["name_en"]),
                         ("0111010000010", "札幌医科大学附属病院", "Sapporo Medical University Hospital"))
        self.assertEqual((rec["weekly"], rec["holiday"]), ("1111100", "0"))  # 定義書: 0：休診 1：診療
        self.assertEqual(rec["beds"]["total"], 844)
        self.assertEqual(rec["departments"][:3], ["内科", "感染症内科", "血液内科"])


class MextShugakuGuidebook(unittest.TestCase):
    records = load("mext-shugaku-guidebook")

    def test_counts(self):
        counts = collections.Counter(r["lang"] for r in self.records)
        self.assertEqual(counts, {lang: 20 for lang in ("en", "ko", "vi", "tl", "zh-Hans", "pt", "es", "uk")})
        self.assertEqual(sorted({tuple(r["pages"]) for r in self.records}), [(p, p + 1) for p in range(2, 41, 2)])

    def test_fields(self):
        for r in self.records:
            self.assertEqual(r["version"], "2015年4月")
            self.assertTrue(r["ja"].strip() and r["tr"].strip())
            for s in r.get("sections", []):
                self.assertTrue(s["ja"].strip() and s["tr"].strip())

    def test_sample(self):
        pt = next(r for r in self.records if r["lang"] == "pt" and r["pages"] == [8, 9])
        self.assertEqual(pt["sections"][1], {"ja": "(２） 教育内容", "tr": "(2) Conteúdo educacional"})
        zh = next(r for r in self.records if r["lang"] == "zh-Hans" and r["pages"] == [8, 9])
        self.assertEqual(zh["ja"].split("\n")[0], "●高等教育について")
        self.assertEqual(zh["tr"].split("\n")[0], "●关于高等教育")
        self.assertNotRegex(zh["tr"], r"[一-鿿] [一-鿿]")  # 中国語は、漢字のあいだの空白を除いた


class HelloworkForeignLanguage(unittest.TestCase):
    records = load("hellowork-foreign-language")

    def office(self, name: str) -> dict:
        return next(r for r in self.records if r["office"] == name)

    def test_counts(self):
        self.assertEqual(len(self.records), 139)  # 電話番号のある行の数
        self.assertEqual(len({r["pref_code"] for r in self.records}), 32)
        langs = collections.Counter(lang["lang"] for r in self.records for lang in r["languages"])
        self.assertEqual(sum(langs.values()), 360)
        self.assertEqual((langs["pt"], langs["en"], langs["es"], langs["zh"]), (113, 82, 78, 39))

    def test_fields(self):
        days = list("月火水木金")
        for r in self.records:
            self.assertRegex(r["tel"], r"^[0-9-]+$")
            self.assertNotRegex(r["office"], r"[A-Za-z]")
            for lang in r["languages"]:
                self.assertTrue(lang.get("name") or lang.get("name_en"))
                self.assertEqual([s["day"] for s in lang["schedule"]],
                                 [d for d in days if d in {s["day"] for s in lang["schedule"]}])
                for s in lang["schedule"]:
                    self.assertTrue(s["text"])
                    for t in s.get("times", []):
                        self.assertRegex(t, r"^\d{1,2}:\d{2}～\d{1,2}:\d{2}$")
                    self.assertNotRegex(s["text"], r"^-\s*\d+\s*-$|Office|Center")  # ページ番号や次の事業所の名前は入れない
        self.assertEqual([r["office"] for r in self.records if "check" in r], ["ハローワーク一宮"])

    def test_sample(self):
        sapporo = self.office("ハローワーク札幌")
        self.assertEqual((sapporo["pref"], sapporo["office_en"], sapporo["tel"]), ("北海道", "Sapporo Office", "011-200-9923"))
        self.assertEqual(sapporo["languages"][0]["schedule"][0],
                         {"day": "火", "text": "13:00～17:00\n※第 1､2､4 のみ\nOnly 1st,2nd,4th", "times": ["13:00～17:00"],
                          "note": "※第 1､2､4 のみ", "note_en": "Only 1st,2nd,4th"})
        # 名前の書き方の揺れ・抜け（元の PDF のまま）
        self.assertEqual(self.office("ハローワーク沼津")["languages"][-1]["name"], "ベトナム")
        self.assertNotIn("name_en", self.office("ハローワーク松戸")["languages"][2])
        # 列をまたぐ注記は、まとまりの中心の曜日に入れる
        fushimi = self.office("ハローワーク伏見")["languages"][0]["schedule"]
        self.assertEqual([s["day"] for s in fushimi], ["火", "木"])
        self.assertIn("7/16,8/20,9/17", fushimi[1]["note"])


class MhlwMultilingualMedicalDocs(unittest.TestCase):
    records = load("mhlw-multilingual-medical-docs")
    langs = {"en", "zh-Hans", "ko", "pt", "es", "uk", "hi", "id", "ne", "tl", "th", "vi", "ar"}

    def doc(self, no: int, lang: str) -> dict:
        return next(r for r in self.records if r["no"] == no and r["lang"] == lang)

    def test_counts(self):
        self.assertEqual(len(self.records), 53 * 13)  # 53資料 × 13言語
        self.assertEqual({(r["no"], r["lang"]) for r in self.records},
                         {(n, lang) for n in range(1, 54) for lang in self.langs})

    def test_units(self):
        order = {"en": ["en", "ja"], "zh-Hans": ["tr", "ja"], "ko": ["tr", "ja"], "pt": ["tr", "ja"], "es": ["tr", "ja"]}
        split = collections.Counter()
        for r in self.records:
            self.assertTrue(r["units"])
            self.assertIn(r["format"], {"doc", "docx", "xls", "xlsx"})
            for u in r["units"]:
                if "text" in u:
                    self.assertEqual(set(u), {"text"})
                else:
                    self.assertEqual(list(u), order.get(r["lang"], ["tr", "en", "ja"]), (r["no"], r["lang"]))
                    self.assertTrue(all(v.strip() for v in u.values()))
                    split[r["lang"]] += 1
        for lang in self.langs:
            total = sum(len(r["units"]) for r in self.records if r["lang"] == lang)
            self.assertGreater(split[lang] / total, 0.5, lang)  # 半分より多くを、日本語と訳の組に分けられた

    def test_sample(self):
        first = self.doc(1, "en")
        self.assertEqual((first["title"], first["category"]), ("診療申込書", ["受付", "外来"]))
        self.assertIn({"en": "Name", "ja": "氏名"}, first["units"])
        self.assertIn({"tr": "姓名", "ja": "氏名"}, self.doc(1, "zh-Hans")["units"])
        self.assertIn({"tr": "Nama", "en": "Name", "ja": "氏名（カナ）"}, self.doc(1, "id")["units"])
        # 文の中に「/」がある単位は、区切り方が決まらないので元の文字のまま
        self.assertIn({"text": "Date of birth (YYYY/MM/DD)/生年月日"}, first["units"])
        self.assertEqual(self.doc(53, "en")["version"], "2025年2月（資料を追加）")


if __name__ == "__main__":
    unittest.main()
