#!/usr/bin/env python3
"""Offline checks for cybersecurity catalog jurisdiction labels and curated duplicates."""
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import cybersecurity_ingest as ingest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data.json"
DATA_DIGEST = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()

JURISDICTIONS = {
    "US": {"code": "US", "name_en": "United States", "type": "paese"},
    "KR": {"code": "KR", "name_en": "South Korea", "type": "paese"},
    "VN": {"code": "VN", "name_en": "Viet Nam", "type": "paese"},
    "CN": {"code": "CN", "name_en": "China", "type": "paese"},
    "EU": {"code": "EU", "name_en": "European Union", "type": "organizzazione_regionale"},
    "SE": {"code": "SE", "name_en": "Sweden", "type": "paese"},
}
PAYLOAD = {"jurisdictions": list(JURISDICTIONS.values())}
TODAY = "2026-11-17"
LABELS = {"United States", "South Korea", "Vietnam", "China", "Sweden", "European Union"}


def doc(**kwargs):
    base = {
        "id": kwargs.get("slug", "x"),
        "document_type": "law",
        "status": "in_vigore",
        "topics": ["governance"],
        "summary": {"en": "Catalog summary used only for import text."},
        "updated_at": "2026-11-16",
    }
    base.update(kwargs)
    return base


def curated(ident, jurisdiction, title, **kwargs):
    item = {"id": ident, "jurisdiction": jurisdiction, "title": title, "sourceUrl": kwargs.pop("sourceUrl", "https://example.test/" + ident)}
    item.update(kwargs)
    return item


NY = doc(
    slug="us-new-york-raise-act-2025",
    jurisdiction="US",
    issuing_body="New York State Legislature",
    date_adopted="2025-12-19",
    date_in_force="2027-01-01",
    official_number="Chapter 699 of 2025 (S6953-B/A6453-B), amended by Chapter 96 of 2026 (S8828/A9449)",
    title_original="Responsible AI Safety and Education (RAISE) Act (New York General Business Law, Article 44-B)",
    short_title={"en": "RAISE Act (New York) – Frontier AI model safety"},
    aliases=["RAISE Act", "S6953-B", "S8828"],
    source_url="https://www.nysenate.gov/legislation/laws/GBS/A44-B",
    notes={"en": "A state law, not federal."},
)
TX = doc(
    slug="us-texas-traiga-hb-149-2025",
    jurisdiction="US",
    issuing_body="Texas Legislature",
    date_adopted="2025-06-22",
    date_in_force="2026-01-01",
    official_number="H.B. No. 149 (Tex. Bus. & Com. Code, Title 11, Subtitle D, Chapters 551-554)",
    title_original="Texas Responsible Artificial Intelligence Governance Act (H.B. No. 149, 89th Legislature)",
    short_title={"en": "TRAIGA (Texas) – AI governance act"},
    source_url="https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=HB149",
    notes={"en": "A state law, not federal."},
)
KR_DECREE = doc(
    slug="kr-ai-basic-act-enforcement-decree-2026",
    jurisdiction="KR",
    document_type="decree",
    issuing_body="President of the Republic of Korea (Presidential Decree)",
    date_adopted="2026-01-21",
    date_in_force="2026-01-22",
    official_number="Presidential Decree No. 36053",
    title_original="인공지능 발전과 신뢰 기반 조성 등에 관한 기본법 시행령",
    title_en="Enforcement Decree of the Framework Act on the Development of Artificial Intelligence and the Establishment of a Foundation for Trust (South Korea)",
    short_title={"en": "Enforcement Decree of South Korea's AI Basic Act"},
    source_url="https://www.law.go.kr/decree-example",
)
KR_ACT = doc(
    slug="kr-ai-basic-act-2025",
    jurisdiction="KR",
    issuing_body="National Assembly of the Republic of Korea",
    date_adopted="2025-01-21",
    date_in_force="2026-01-22",
    official_number="Act No. 20676",
    title_original="인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
    title_en="Framework Act on the Development of Artificial Intelligence and the Establishment of a Foundation for Trust (South Korea's AI Basic Act)",
    short_title={"en": "South Korea's AI Basic Act"},
    source_url="https://www.law.go.kr/act-example",
)
VN = doc(
    slug="vn-luat-tri-tue-nhan-tao-2025",
    jurisdiction="VN",
    issuing_body="Quốc hội (National Assembly)",
    date_adopted="2025-12-10",
    date_in_force="2026-03-01",
    official_number="134/2025/QH15",
    title_original="Luật Trí tuệ nhân tạo số 134/2025/QH15",
    title_en="Viet Nam's Law on Artificial Intelligence (134/2025/QH15)",
    source_url="https://congbao.chinhphu.vn/van-ban/luat-so-134-2025-qh15-468694.htm",
)
VN_333 = doc(
    slug="vn-nghi-dinh-333-an-ninh-mang-2026",
    jurisdiction="VN",
    document_type="decree",
    issuing_body="Government of Viet Nam",
    date_adopted="2026-06-01",
    official_number="333/2026/NĐ-CP",
    title_original="Nghị định số 333/2026/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật An ninh mạng",
    title_en="Decree No. 333/2026/ND-CP detailing certain articles of and measures to implement Viet Nam's Law on Cybersecurity",
    source_url="https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-333-2026-nd-cp-470335.htm",
)
CN = doc(
    slug="cn-ai-generated-content-labelling-measures-2025",
    jurisdiction="CN",
    document_type="regulation",
    issuing_body="Cyberspace Administration of China (CAC)",
    date_adopted="2025-03-07",
    date_in_force="2025-09-01",
    official_number="国信办通字〔2025〕2号",
    title_original="人工智能生成合成内容标识办法",
    title_en="Measures for Labelling AI-Generated and Synthetic Content",
    short_title={"en": "China – Labelling of AI-generated content (2025)"},
    source_url="https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm",
)
CO = doc(
    slug="us-colorado-admt-sb26-189-2026",
    jurisdiction="US",
    issuing_body="Colorado General Assembly",
    date_adopted="2026-05-14",
    official_number="SB 26-189, Chapter 131, Session Laws of Colorado 2026",
    title_original="Colorado Senate Bill 26-189 – Concerning automated decision-making technology",
    short_title={"en": "SB 26-189 (Colorado) – Automated decision-making and AI"},
    aliases=["Colorado AI Act", "SB 24-205", "SB24-205", "SB26-189"],
    source_url="https://leg.colorado.gov/bills/sb26-189",
    notes={"en": "A state law, not federal. It revises the earlier SB 24-205 framework."},
)
CIRCIA = doc(
    slug="us-circia-2022",
    jurisdiction="US",
    issuing_body="United States Congress",
    date_adopted="2022-03-15",
    official_number="Pub. L. 117-103, Division Y",
    title_original="Cyber Incident Reporting for Critical Infrastructure Act of 2022 (CIRCIA)",
    short_title={"en": "CIRCIA (incident reporting, 2022)"},
    source_url="https://www.cisa.gov/circia-example",
)
CCPA = doc(
    slug="us-ccpa-2018",
    jurisdiction="US",
    issuing_body="California State Legislature",
    date_adopted="2018-06-28",
    title_original="California Consumer Privacy Act of 2018 (CCPA)",
    source_url="https://cppa.ca.gov/regulations/",
    notes={"en": "A state law, not a federal one."},
)
NYDFS = doc(
    slug="us-nydfs-cybersecurity-regulation-23-nycrr-500-2023",
    jurisdiction="US",
    document_type="regulation",
    issuing_body="New York State Department of Financial Services (DFS)",
    date_adopted="2023-11-01",
    official_number="23 NYCRR Part 500",
    title_original="Cybersecurity Requirements for Financial Services Companies (23 NYCRR Part 500)",
    short_title={"en": "NYDFS Cybersecurity Regulation (23 NYCRR 500)"},
    source_url="https://www.dfs.ny.gov/example",
)
EU_ACT = doc(
    slug="eu-ai-act-2024-1689",
    jurisdiction="EU",
    issuing_body="European Parliament and Council",
    date_adopted="2024-06-13",
    official_number="Regulation (EU) 2024/1689",
    title_original="Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)",
    short_title={"en": "AI Act (Regulation (EU) 2024/1689)"},
    source_url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
)

CURATED = [
    curated(
        "US-NY-S8828-2026", "United States · New York",
        "Responsible AI Safety and Education (RAISE) Act (S 8828, Chapter 96)",
        publicationDate="2026-03-27", effectiveDate="2027-01-01",
        sourceUrl="https://nyassembly.gov/leg/?default_fld=&leg_video=&bn=S08828&term=2025",
    ),
    curated(
        "US-TX-HB149-2025", "United States · Texas",
        "Texas Responsible Artificial Intelligence Governance Act (HB 149)",
        publicationDate="2025-06-22", effectiveDate="2026-01-01",
        sourceUrl="https://capitol.texas.gov/billlookup/BillSummary.aspx?Bill=HB149&LegSess=89R",
    ),
    curated(
        "US-TX-SB1964-2025", "United States · Texas",
        "Governmental Use of Artificial Intelligence and Data Management (SB 1964)",
        publicationDate="2025-06-20",
        sourceUrl="https://capitol.texas.gov/billlookup/BillSummary.aspx?Bill=SB1964&LegSess=89R",
    ),
    curated(
        "KR-AI-BASIC-ENFORCEMENT-DECREE-2026", "South Korea",
        "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법 시행령 (대통령령 제36580호) (Enforcement Decree of the Framework Act on the Development of Artificial Intelligence and the Creation of a Foundation for Trust)",
        publicationDate="2026-01-21", effectiveDate="2026-08-20",
        sourceUrl="https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=288781&efYd=20260820",
    ),
    curated(
        "KR-AI-BASIC-2025", "South Korea",
        "Framework Act on the Development of Artificial Intelligence and the Creation of a Foundation for Trust",
        publicationDate="2025-01-21", effectiveDate="2026-01-22",
        sourceUrl="https://www.law.go.kr/lsInfoP.do?lsiSeq=268543",
    ),
    curated(
        "VN-AI-2025-134", "Vietnam",
        "Law on Artificial Intelligence (Law No. 134/2025/QH15)",
        publicationDate="2025-12-10", effectiveDate="2026-03-01",
        sourceUrl="https://vanban.chinhphu.vn/?docid=216334",
    ),
    curated(
        "VN-AI-DECREE-142-2026", "Vietnam",
        "Decree No. 142/2026/NĐ-CP on implementation of the Law on Artificial Intelligence",
        officialTitle="Nghị định số 142/2026/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật Trí tuệ nhân tạo",
        publicationDate="2026-06-01",
        sourceUrl="https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-142-2026-nd-cp-469480.htm",
    ),
    curated(
        "CN-AI-LABEL-2025", "China",
        "Measures for Labeling AI-Generated and AI-Synthesized Content",
        publicationDate="2025-03-14", effectiveDate="2025-09-01",
        sourceUrl="https://www.cac.gov.cn/2025-03/14/c_1743654685899683.htm",
    ),
    curated(
        "US-CO-SB26-189-2026", "United States · Colorado",
        "Automated Decision-Making Technology (SB 26-189, Session Laws ch. 131)",
        publicationDate="2026-05-14", effectiveDate="2027-01-01",
        sourceUrl="https://leg.colorado.gov/bills/sb26-189",
    ),
    curated(
        "US-CO-SB24-205", "United States · Colorado",
        "Consumer Protections for Artificial Intelligence (SB 24-205)",
        publicationDate="2024-05-17", effectiveDate="2026-06-30",
        sourceUrl="https://leg.colorado.gov/bills/sb24-205",
    ),
    curated(
        "EU-2024-1689", "European Union",
        "Artificial Intelligence Act (Regulation (EU) 2024/1689)",
        publicationDate="2024-07-12",
        sourceUrl="https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
    ),
    curated(
        "EU-AIA-2024-1689-SWEDEN", "Sweden",
        "Artificial Intelligence Act (Regulation (EU) 2024/1689) — applies in Sweden",
        publicationDate="2024-07-12",
        sourceUrl="https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
    ),
]


def fresh_for(document, state=True):
    jurisdiction = ingest.jurisdiction_for(document, JURISDICTIONS, state_jurisdictions=state)
    return ingest.make_item(document, jurisdiction, "2026-11-16", TODAY)


def matched_id(document, items=None, state=True, overrides=True):
    fresh = fresh_for(document, state=state)
    match = ingest.CuratedIndex(items if items is not None else CURATED, use_overrides=overrides).match(document, fresh)
    return None if match is None else match["id"]


class JurisdictionTests(unittest.TestCase):
    def test_state_slug_and_issuer_use_curated_labels(self):
        self.assertEqual(ingest.detect_us_state(NY), "New York")
        self.assertEqual(ingest.detect_us_state(TX), "Texas")
        self.assertEqual(ingest.detect_us_state(CO), "Colorado")
        self.assertEqual(ingest.detect_us_state(CCPA), "California")
        self.assertEqual(ingest.detect_us_state(NYDFS), "New York")
        self.assertEqual(ingest.jurisdiction_for(NY, JURISDICTIONS), "United States · New York")
        self.assertEqual(ingest.jurisdiction_for(TX, JURISDICTIONS), "United States · Texas")
        self.assertEqual(ingest.jurisdiction_for(CCPA, JURISDICTIONS), "United States · California")
        self.assertEqual(ingest.jurisdiction_for(NYDFS, JURISDICTIONS), "United States · New York")

    def test_federal_instruments_stay_federal(self):
        mentioned = doc(
            slug="us-ports-notice-2025",
            jurisdiction="US",
            issuing_body="United States Congress",
            title_original="Notice about New York and Texas port security",
            short_title={"en": "Notice about New York and Texas port security"},
            source_url="https://www.congress.gov/example",
        )
        self.assertEqual(ingest.detect_us_state(CIRCIA), "")
        self.assertEqual(ingest.detect_us_state(mentioned), "")
        self.assertEqual(ingest.jurisdiction_for(CIRCIA, JURISDICTIONS), "United States · Federal")
        self.assertEqual(ingest.jurisdiction_for(NY, JURISDICTIONS, state_jurisdictions=False), "United States · Federal")

    def test_note_names_one_state_when_the_issuer_pattern_does_not(self):
        agency = doc(
            slug="us-ccpa-2018",
            jurisdiction="US",
            issuing_body="Privacy Protection Agency",
            title_original="California Consumer Privacy Act of 2018",
            source_url="https://cppa.ca.gov/regulations/",
            notes={"en": "A state law, not a federal one."},
        )
        self.assertEqual(ingest.detect_us_state(agency), "California")

    def test_new_york_city_is_not_relabelled_as_the_state(self):
        city = doc(
            slug="us-new-york-city-local-law-144",
            jurisdiction="US",
            issuing_body="New York City Department of Consumer and Worker Protection",
            title_original="Automated Employment Decision Tools",
            source_url="https://www.nyc.gov/example",
        )
        self.assertEqual(ingest.detect_us_state(city), "New York City")
        self.assertEqual(ingest.jurisdiction_for(city, JURISDICTIONS), "United States · New York City")


class DuplicateTests(unittest.TestCase):
    def test_known_pairs_match_without_the_override_map(self):
        pairs = (
            (NY, "US-NY-S8828-2026"),
            (TX, "US-TX-HB149-2025"),
            (KR_DECREE, "KR-AI-BASIC-ENFORCEMENT-DECREE-2026"),
            (VN, "VN-AI-2025-134"),
            (CN, "CN-AI-LABEL-2025"),
        )
        for document, ident in pairs:
            found = ingest.CuratedIndex(CURATED, use_overrides=False).match(document, fresh_for(document))
            self.assertIsNotNone(found, document["slug"])
            self.assertEqual(found["id"], ident, found["reason"])
            self.assertNotEqual(found["reason"], "curated override")

    def test_korea_decree_does_not_match_the_framework_act(self):
        self.assertEqual(matched_id(KR_DECREE, overrides=False), "KR-AI-BASIC-ENFORCEMENT-DECREE-2026")
        # The curated act title says "Creation" and does not carry Act No. 20676,
        # so the general threshold does not collapse it into the decree or the act.
        self.assertNotEqual(matched_id(KR_ACT, overrides=False), "KR-AI-BASIC-ENFORCEMENT-DECREE-2026")
        self.assertIsNone(matched_id(KR_ACT, overrides=False))

    def test_vietnam_cybersecurity_decree_is_not_the_ai_decree(self):
        self.assertIsNone(matched_id(VN_333, overrides=False))

    def test_colorado_matches_the_2026_bill_not_the_2024_act(self):
        self.assertEqual(matched_id(CO, overrides=False), "US-CO-SB26-189-2026")

    def test_texas_does_not_match_the_other_texas_bill(self):
        self.assertNotEqual(matched_id(TX, overrides=False), "US-TX-SB1964-2025")

    def test_eu_act_does_not_match_a_member_state_applicability_record(self):
        self.assertEqual(matched_id(EU_ACT, overrides=False), "EU-2024-1689")

    def test_state_rules_without_a_curated_twin_are_not_duplicates(self):
        self.assertIsNone(matched_id(CCPA, overrides=False))
        self.assertIsNone(matched_id(NYDFS, overrides=False))
        self.assertIsNone(matched_id(CIRCIA, overrides=False))

    def test_override_map_is_only_the_known_pairs_and_is_a_backstop(self):
        self.assertEqual(
            set(ingest.CURATED_DUPLICATE_OVERRIDES),
            {
                "us-new-york-raise-act-2025",
                "kr-ai-basic-act-enforcement-decree-2026",
                "vn-luat-tri-tue-nhan-tao-2025",
                "cn-ai-generated-content-labelling-measures-2025",
            },
        )
        bare = doc(
            slug="us-new-york-raise-act-2025",
            jurisdiction="US",
            issuing_body="New York State Legislature",
            title_original="Untitled instrument",
            source_url="https://example.test/bare-raise",
        )
        self.assertIsNone(matched_id(bare, overrides=False))
        self.assertEqual(matched_id(bare, overrides=True), "US-NY-S8828-2026")

    def test_creation_outcomes_for_the_six_named_records(self):
        existing = [
            *CURATED,
            curated("CYBERLAW-US-NEW-YORK-RAISE-ACT-2025", "United States · Federal", "RAISE Act (New York) – Frontier AI model safety", sourceUrl=NY["source_url"]),
            curated("CYBERLAW-US-TEXAS-TRAIGA-HB-149-2025", "United States · Federal", "TRAIGA (Texas) – AI governance act", sourceUrl=TX["source_url"]),
        ]
        expected = (
            (NY, "US-NY-S8828-2026", "United States · New York"),
            (TX, "US-TX-HB149-2025", "United States · Texas"),
            (KR_DECREE, "KR-AI-BASIC-ENFORCEMENT-DECREE-2026", "South Korea"),
            (VN, "VN-AI-2025-134", "Vietnam"),
            (CN, "CN-AI-LABEL-2025", "China"),
        )
        for document, ident, jurisdiction in expected:
            before = ingest.creation_outcome(
                document, existing, JURISDICTIONS, LABELS, TODAY,
                state_jurisdictions=False, strong_dedupe=False,
            )
            after = ingest.creation_outcome(
                document, existing, JURISDICTIONS, LABELS, TODAY,
                state_jurisdictions=True, strong_dedupe=True, use_overrides=False,
            )
            self.assertEqual(before["outcome"], "add", before)
            self.assertEqual(before["jurisdiction"], "United States · Federal" if document["jurisdiction"] == "US" else jurisdiction)
            self.assertEqual(after["outcome"], "skip", after)
            self.assertEqual(after["matched_id"], ident)
            self.assertEqual(after["jurisdiction"], jurisdiction)


class IngestRunTests(unittest.TestCase):
    def test_existing_catalog_rows_are_kept_and_state_labels_are_corrected(self):
        items = [
            *CURATED,
            {
                "id": "CYBERLAW-US-NEW-YORK-RAISE-ACT-2025",
                "jurisdiction": "United States · Federal",
                "title": "RAISE Act (New York) – Frontier AI model safety",
                "sourceUrl": NY["source_url"],
                "history": [{"date": "2026-11-16", "change": "Added from the catalog."}],
            },
            {
                "id": "CYBERLAW-KR-AI-BASIC-ACT-ENFORCEMENT-DECREE-2026",
                "jurisdiction": "South Korea",
                "title": "Enforcement Decree of South Korea's AI Basic Act",
                "sourceUrl": KR_DECREE["source_url"],
                "history": [{"date": "2026-11-16", "change": "Added from the catalog."}],
            },
            curated("US-CA-SB53-2025", "United States · California", "California SB 53", sourceUrl="https://leginfo.legislature.ca.gov/example"),
        ]
        data = {"items": json.loads(json.dumps(items)), "lastChecked": "2026-11-16"}
        documents = {"documents": [NY, TX, KR_DECREE, CIRCIA, CCPA], "updated_at": "2026-11-16", "attribution": "Cybersecurity Database"}
        standards = {"standards": [], "count": 0, "updated_at": "2026-11-16"}
        stats = ingest.apply_ingest(data, documents, PAYLOAD, standards, TODAY)
        by_id = {item["id"]: item for item in data["items"]}
        self.assertIn("CYBERLAW-US-NEW-YORK-RAISE-ACT-2025", by_id)
        self.assertEqual(by_id["CYBERLAW-US-NEW-YORK-RAISE-ACT-2025"]["jurisdiction"], "United States · New York")
        self.assertIn("CYBERLAW-KR-AI-BASIC-ACT-ENFORCEMENT-DECREE-2026", by_id)
        self.assertEqual(by_id["CYBERLAW-KR-AI-BASIC-ACT-ENFORCEMENT-DECREE-2026"]["jurisdiction"], "South Korea")
        self.assertEqual(by_id["US-NY-S8828-2026"]["title"], CURATED[0]["title"])
        self.assertEqual(by_id["US-CA-SB53-2025"]["jurisdiction"], "United States · California")
        added = {row["id"] for row in stats["decisions"] if row["outcome"] == "add"}
        skipped = {row["id"]: row["matched_id"] for row in stats["decisions"] if row["outcome"] == "skip"}
        self.assertIn("CYBERLAW-US-CCPA-2018", added)
        self.assertEqual(by_id["CYBERLAW-US-CCPA-2018"]["jurisdiction"], "United States · California")
        self.assertIn("CYBERLAW-US-CIRCIA-2022", added)
        self.assertEqual(by_id["CYBERLAW-US-CIRCIA-2022"]["jurisdiction"], "United States · Federal")
        self.assertEqual(skipped["CYBERLAW-US-TEXAS-TRAIGA-HB-149-2025"], "US-TX-HB149-2025")
        self.assertNotIn("CYBERLAW-US-TEXAS-TRAIGA-HB-149-2025", by_id)

    def test_logic_diff_on_a_fixture_is_only_the_state_correction(self):
        items = [
            curated("US-NY-S8828-2026", "United States · New York", "Responsible AI Safety and Education (RAISE) Act (S 8828, Chapter 96)", publicationDate="2026-03-27", effectiveDate="2027-01-01", sourceUrl="https://nyassembly.gov/leg/?bn=S08828"),
            {
                "id": "CYBERLAW-US-NEW-YORK-RAISE-ACT-2025",
                "jurisdiction": "United States · Federal",
                "title": "Keep the stored title",
                "titleTranslationSource": "Manual English translation; verify wording against the linked official source.",
                "officialTitle": "Stored official title",
                "sourceUrl": NY["source_url"],
                "summary": "Stored summary",
                "history": [],
            },
        ]
        data = {"items": items}
        documents = {"documents": [NY], "updated_at": "2026-11-16"}
        standards = {"standards": []}
        legacy = json.loads(json.dumps(data))
        updated = json.loads(json.dumps(data))
        ingest.apply_ingest(legacy, documents, PAYLOAD, standards, TODAY, state_jurisdictions=False, strong_dedupe=False)
        ingest.apply_ingest(updated, documents, PAYLOAD, standards, TODAY, state_jurisdictions=True, strong_dedupe=True)
        diff = ingest.logic_diff(data["items"], legacy["items"], updated["items"])
        self.assertEqual(diff["removed"], [])
        self.assertEqual(diff["unexpected"], [])
        self.assertEqual(diff["added_only_by_new_logic"], [])
        self.assertEqual([row["id"] for row in diff["jurisdiction_changes"]], ["CYBERLAW-US-NEW-YORK-RAISE-ACT-2025"])
        stored = next(item for item in updated["items"] if item["id"] == "CYBERLAW-US-NEW-YORK-RAISE-ACT-2025")
        self.assertEqual(stored["title"], "Keep the stored title")
        self.assertEqual(stored["jurisdiction"], "United States · New York")

    def test_dry_run_does_not_write_the_register(self):
        payload_documents = {"documents": [NY, KR_DECREE, VN, CN, TX, CIRCIA], "updated_at": "2026-11-16", "attribution": "Catalog"}
        calls = {}

        def fake_load():
            calls["loaded"] = True
            return payload_documents, PAYLOAD, {"standards": [], "count": 0}

        items = [*CURATED]
        for document, jurisdiction in (
            (NY, "United States · Federal"),
            (TX, "United States · Federal"),
            (KR_DECREE, "South Korea"),
            (VN, "Vietnam"),
            (CN, "China"),
        ):
            items.append({
                "id": ingest.generated_id(document["slug"]),
                "jurisdiction": jurisdiction,
                "title": (document.get("short_title") or {}).get("en") or document.get("title_original"),
                "sourceUrl": document["source_url"],
            })
        original = {"items": items, "lastChecked": "2026-11-16"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            path.write_text(json.dumps(original), encoding="utf-8")
            before = path.read_bytes()
            original_load = ingest.load_payloads
            ingest.load_payloads = fake_load
            output = io.StringIO()
            try:
                with redirect_stdout(output):
                    code = ingest.main(["--dry-run"], data_path=path)
            finally:
                ingest.load_payloads = original_load
            self.assertEqual(code, 0)
            self.assertEqual(path.read_bytes(), before)
            self.assertTrue(calls["loaded"])
            report = output.getvalue()
            self.assertIn("skip — duplicate of US-NY-S8828-2026", report)
            self.assertIn("skip — duplicate of US-TX-HB149-2025", report)
            self.assertIn("jurisdiction label United States · New York", report)
            self.assertIn("jurisdiction label United States · Texas", report)
            self.assertIn("existing records removed: 0", report)
            self.assertIn("existing records with unexpected field changes: 0", report)
        self.assertEqual(hashlib.sha256(DATA_PATH.read_bytes()).hexdigest(), DATA_DIGEST)


if __name__ == "__main__":
    unittest.main()
