# Weekly curation report, 2026-11-09 (follow-up run 2)

Run date (UTC): 2026-11-09. This is a bounded follow-up to the report in `curation-2026-11-09.md`, prompted by additional official-source checks. It is not exhaustive. An absent record or an unsuccessful search does not establish that no law or guidance exists.

## Summary

| Measure | Count |
| --- | ---: |
| Added to `data.json` | 6 |
| Existing records materially changed | 1 |
| Ingestion-feed additions or updates | 0 |

All six additions below were checked against official sources. The EU standard is separately labeled reference material, not a law. The existing EU AI Act record now notes the verified amendment and its application timetable.

## Added

| Jurisdiction | Title | Status | Primary source | Verification |
| --- | --- | --- | --- | --- |
| European Union | Proposal for a Regulation on the Cloud and AI Development Act (COM(2026) 502) | Proposed | [European Commission proposal page](https://digital-strategy.ec.europa.eu/en/library/proposal-cloud-and-ai-development-act-cada) | The Commission page identifies COM(2026) 502 as a proposal adopted 3 June 2026 and describes its research/innovation, capacity and cloud/AI sovereignty objectives. No claim of enactment is made. Parliamentary and Council progress was not checked in this bounded pass. |
| European Union | Regulation (EU) 2026/1744 (Digital Omnibus on AI) | In force | [EUR-Lex official text](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) | Verified title, adoption and publication dates, 27 July 2026 entry into force, Article 5 amendments and amended Article 113 dates in the legal text. The new Article 5 points apply from 2 December 2026; specified Annex III high-risk requirements apply from 2 December 2027 and Annex I requirements from 2 August 2028. |
| European Union | Commission Implementing Decision (EU) 2026/2274 on harmonised standards for high-risk AI systems | In force | [EUR-Lex official text](https://eur-lex.europa.eu/eli/dec_impl/2026/2274/oj/eng) | Verified that it was adopted 12 October and published and entered into force 14 October 2026. It publishes the reference to EN 18286:2026 for high-risk AI systems. |
| Cross-country standards reference | EN 18286:2026 — Artificial intelligence — Quality management system for EU AI Act regulatory purposes | Published standard | [European Commission publication](https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal) | Commission material and the linked EUR-Lex decision identify the CEN/CENELEC standard and explain its presumption of conformity for the covered Article 17 requirements. The register labels it as a standard reference, not legislation or proof of national adoption. |
| United Kingdom | Protecting people and businesses in an agentic economy: DRCF joint statement | Guidance | [DRCF joint statement](https://www.drcf.org.uk/siteassets/drcf/pdf-files/drcf-joint-statement-protecting-people-and-businesses-in-and-agentic-economy3.pdf?v=427454) | Verified publication date 30 October 2026, member regulators and statement content. It describes how existing legal regimes apply to personal AI agents and regulator coordination; it is not recorded as a new statute. |
| United Kingdom | Government Response to the National Commission's Recommendations on the Regulation of AI in Healthcare | Adopted policy | [GOV.UK policy paper](https://www.gov.uk/government/publications/government-response-to-the-national-commissions-recommendations-on-the-regulation-of-ai-in-healthcare/government-response-to-the-national-commissions-recommendations-on-the-regulation-of-ai-in-healthcare) | Verified the 6 October 2026 publication and that government accepts all 44 recommendations. The summary describes planned lifecycle-based work, including cybersecurity guidance; it does not present those plans as enacted law. |

## Materially changed

| Jurisdiction | Record | Change | Primary source |
| --- | --- | --- | --- |
| European Union | [Artificial Intelligence Act (Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) | Summary updated and dated history appended to reference Regulation (EU) 2026/1744 and its verified high-risk application dates. The amendment is also recorded as its own instrument. | [EUR-Lex amending text](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) |

## Checked without a register change

- The official [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1) was queried by `ingest.py`; it reported 943 total dashboard records and produced no additions or material updates.
- The [Cybersecurity Database open catalog](https://www.cybersecuritydatabase.org/en/open-data/) and standards feed were checked by `cybersecurity_ingest.py`; it reported zero legal-record additions or updates and zero standards additions or updates (7 duplicate legal records skipped; 9 out-of-scope records skipped).
- The [NIST incident-readiness guidance](https://www.nist.gov/news-events/news/2026/10/key-practices-incident-readiness-and-response-super-intelligence-training) surfaced in the source review but is already in the register; no new record was added.
- The UK government's [12 October AI and cyber-defence announcement](https://www.gov.uk/government/news/britain-steps-up-national-defences-against-growing-ai-risks) describes work underway and measures being considered. No separate adopted instrument or published guidance was verified from that announcement, so it was not presented as a law or added as one.

## Coverage limits

This follow-up focused on newly surfaced official EU and UK policy/legal items, verified relevant EUR-Lex text, and refreshed the two available ingestion catalogs. It did not systematically review all countries, U.S. states, national gazettes, legislative-status databases, or sector regulators. In particular, this pass does not establish worldwide completeness; EU proposal progress after the Commission publication date and UK devolved/local measures were not comprehensively checked. The daily feeds are discovery aids and their no-change results do not establish that no other item exists. Records and summaries remain informational; consult linked authorities for current law.
