# Weekly curation report — 2026-11-10 run 3 (verified research pass, run 3)

Verifier: Dashboard Verifier. Candidate package: research-pass-2026-11-10-run-3 (5 candidates: 3 re-submissions of PR #19 NEEDS_REVIEW items, 2 new gap fills), checked against master 56058c6d (988 items, 271 sources). Every candidate was re-checked by the verifier at its official source; research notes were not treated as proof. This report is not legal advice and the search was bounded, so it is not an exhaustive inventory.

## Results

- Records added: **4**
- Existing records materially changed: **0**
- Candidates needing review (not added): **1**
- Candidates rejected (not added): **0**
- New official sources added to the sources list: **4**
- Item count 988 → 992; source count 271 → 275.
- No record was deleted or changed, and no US-FR-, CYBERLAW- or CYBERSTANDARD- record was touched. FR-PARIS-CALL-AI-SAFETY-SECURITY-2026 was not processed (on hold for Keashyn's jurisdiction decision). The FinCEN MEXC item remains an ingest-feed note. This change is submitted for human review; it does not merge or deploy.

## Records added

| id | jurisdiction | title | status | published | effective | official source |
| --- | --- | --- | --- | --- | --- | --- |
| CA-ISED-AI-TRANSPARENCY-CONSULTATION-2026 | Canada | Have your say on advancing AI transparency in Canada | Consultation | 2026-07-23 | — | [Innovation, Science and Economic Development Canada (Minister of Artificial Intelligence and Digital Innovation)](https://ised-isde.canada.ca/site/ised/en/have-your-say-advancing-ai-transparency-canada) |
| KR-PIPC-SAFETY-MEASURES-GUIDE-2026 | South Korea | 개인정보의 안전성 확보조치 기준 안내서(2026.11.) (Guide to the Standards for Measures to Ensure the Safety of Personal Information, November 2026) | Guidance | 2026-11-05 | — | [Personal Information Protection Commission (PIPC), New Technology Personal Information Division](https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS217&mCode=D010030000&nttId=12611) |
| JP-DIGITAL-GENNAI-STANDARDS-2026 | Japan | Government AI GENAI Standards on Governance, Security, and Safety (“GENAI Standards”), First Edition (ガバメントAI 源内 ガバナンス・セキュリティ・セーフティに関する基準（「源内基準」）第1版) | Guidance | 2026-10-20 | — | [Digital Agency (デジタル庁), Team GENAI, developed with the Japan AI Safety Institute (AISI)](https://www.digital.go.jp/policies/genai/agent-safety-standard) |
| JP-DS920-GENAI-GOV-GUIDELINE-2026 | Japan | 行政の進化と革新のための生成AIの調達・利活用に係るガイドライン（第2.0版）(DS-920) (The Guideline for Japanese Government's Procurements and Utilizations of Generative AI for the sake of Evolution and Innovation of Public Administration, Ver. 2.0) | Adopted policy | 2026-06-12 | 2026-09-01 | [Digital Agency · Executive Committee of the Digital Society Promotion Council (デジタル社会推進会議幹事会)](https://www.digital.go.jp/news/decb64eb-f26e-41cb-8d37-f3dd173108b8) |

Verification notes:

- **CA-ISED-AI-TRANSPARENCY-CONSULTATION-2026** — PR #19 issue resolved: sourceUrl is now the ISED consultation page (ised-isde.canada.ca, curl 200), which carries the exact title 'Have your say on advancing AI transparency in Canada', 'From: Innovation, Science and Economic Development Canada', 'Current status: Closed', 'This consultation ran from July 23 to September 23, 2026', the 'What We Heard' note, the five areas and the discussion-paper title (date modified 2026-09-24). The canada.ca release (WebFetch; already in master sources) is dated 'July 23, 2026' and names Minister Evan Solomon. Consultation status matches master practice for closed consultations; effectiveDate '—' correct; summary does not overstate. No duplicate (CA-NAIS-AIFORALL-2026 is the strategy).
- **KR-PIPC-SAFETY-MEASURES-GUIDE-2026** — PR #19 issue resolved: sourceUrl is now the PIPC guide-board post (pipc.go.kr, curl 200): title '[현재 안내서] 개인정보의 안전성 확보조치 기준 안내서(2026.11.)', 작성부서 신기술개인정보과, 작성일 2026-11-05, note '고시 일부 개정(2026.7.1.) 사항 등을 반영한 ... 안내서입니다'. Korean title matches exactly (English gloss in parentheses follows the KR-PIPC-SMART-GLASSES-ADVISORY-2026 convention). Guide PDF purpose statement (「개인정보 보호법」 and the 고시; '최소한의 안전성 확보 기준을 안내') and the 4 Nov release (nttId=12609) support every summary point (annual vulnerability checks and penetration tests for public systems from the 1 July amendment, authentication examples 7→12 incl. passkeys, AI, post-quantum cryptography, key management, API FAQs). Guidance; no duplicate.
- **JP-DIGITAL-GENNAI-STANDARDS-2026** — Status now supportable as Guidance from the official text: the standard is issued by 'デジタル庁 源内班 / Team GENAI, Digital Agency' (no Cabinet or council decision), s.1.1 says it 'set[s] out the matters to be observed by each party involved in GENAI' and 'appl[ies] to GENAI as provided under the Digital Agency-hosted model', and it places DS-920 as the government-wide 'rules for administrative practice'; the page offers it to local governments and businesses as a reference 'model case'. Consistent with master's BT/IE/AR public-service AI precedents (Guidance). Dates: Japanese edition revision table '第1版 2026年10月20日 初版発行' and overview PDF dated 2026/10/20; page last updated 2026-11-06 with English translation. Title matches the page and PDF; summary accurate; no duplicate.
- **JP-DS920-GENAI-GOV-GUIDELINE-2026** — Adopted policy is supported by the official text: Digital Agency release (公開日 2026-06-12) says Ver. 2.0 was decided at the 23rd Executive Committee of the Digital Society Promotion Council (written meeting) and revises the 27 May 2025 edition. The PDF cover reads 'デジタル社会推進標準ガイドライン DS-920 … 2026年（令和８年）6月12日 デジタル社会推進会議幹事会決定' and '〔ドキュメントの位置付け〕Normative 政府情報システムの整備及び管理に関するルールとして遵守する内容を定めたドキュメント'; s.1.2 places it among the standard guidelines to be complied with as norms (規範として遵守). So it is a government decision binding ministries, not advisory guidance, and not a law. 附則: in force from 2026-09-01 (effectiveDate matches); CAIO measures by 2026-06-30; governance-framework scope from 2026-07-01. CAIO, Advisory Board reporting for high-risk uses, risk-case reporting and procurement checklists confirmed in the English translation. No duplicate.

Each added record carries one history entry dated 2026-11-10 noting it was added after verification against the named official source; the researcher's dated stage notes were not carried into history (the stage dates are stated in the summaries).

## Materially changed

None. No existing record was changed.

## Checked without change

- **JP-AI-PROMOTION-2025**: compared with the AI Basic Plan, GENAI and DS-920 candidates; it is the AI Promotion Act, a distinct instrument. Not altered.
- **CA-NAIS-AIFORALL-2026**: compared with the ISED consultation; it is the national strategy. Not altered.
- **KR-PIPC-SMART-GLASSES-ADVISORY-2026**: compared with the PIPC guide; distinct. Not altered.
- **BT-CIVIL-SERVICE-GENAI-GUIDELINE-2024**, **IE-TRUSTWORTHY-AI-PUBLIC-SERVICE-2024**, **AR-SIGEN-RES-197-2026-AI-CONTROLS**, **GH-PUBLIC-SECTOR-AI-PROCUREMENT-2026**: used as status precedents for the two Japanese public-sector instruments. Not altered.
- No master item matches any added record by id, sourceUrl or normalized title; no existing AI Basic Plan or DS-920 record exists.

## Needs review (not added)

- **JP-AI-BASIC-PLAN-2025** — Artificial Intelligence Basic Plan (人工知能基本計画) (Japan, proposed status Adopted policy, [source](https://www8.cao.go.jp/cstp/ai/ai_plan/ai_plan.html)). Reason: Cabinet Office page (cao.go.jp, curl 200) shows '人工知能基本計画 / 令和８年７月14日 閣議決定' as current and '令和7年12月23日 閣議決定' under past plans; Kantei agenda for 23 Dec 2025 lists '人工知能基本計画について（決定）'; Article 18(1) basis and annual revision confirmed in the English PDFs. But the summary says the plan 'rests on three principles' while calling the Second Plan the current version; the Second Plan's English text (As of July 14, 2026) sets out 'Four Principles' (adds 'Trial, learning and iteration'), and its fourth pillar is 'Building an AI-powered Society'. The record also mixes two Cabinet decisions (publicationDate and id for the 2025 plan, content for the 2026 plan), so which instrument it represents needs a decision. Suggested fix: Choose the instrument: (a) record the current Second AI Basic Plan (publicationDate 2026-07-14, e.g. id JP-AI-BASIC-PLAN-2026) with a summary of its four principles and four pillars, noting the first plan of 23 Dec 2025 in the summary; or (b) keep the 2025 record and describe only the first plan's three principles, adding the 14 July 2026 second plan as history. Then re-submit.

## Rejected

None.

## Not processed

- **FR-PARIS-CALL-AI-SAFETY-SECURITY-2026** — on hold for Keashyn's decision on the jurisdiction label for multi-country declarations.

## What could not be checked

- The canada.ca news release timed out over curl; it was read via WebFetch (it is already in master's sources).
- The PIPC guide PDF download needs a JavaScript form post; the verifier read the guide post page directly and used the researcher's downloaded PDF copy only for the purpose statement.
- The PIPC 1 July 2026 notice amendment text on law.go.kr was not opened; the guide and release describe it.
- The Japanese full text of the Second AI Basic Plan was downloaded but only the English provisional translation was compared against the summary.
- The DS-920 English translation is provisional; status was decided from the Japanese cover and s.1.2.

## Coverage limits

- Verification covered only the 5 candidates in this research pass and the existing records they could duplicate. It is not a full sweep of all jurisdictions; the coverage gaps listed in the run 2 report (EU OJ 11 Nov, French AI-and-children charter, U.S. states, India, Korea MSIT/KISA, Singapore, China CAC, EU AI Office, DIFC, Jordan) stand.
- data.json item order on master is not globally sorted by (publicationDate, id). New records were inserted at their sorted position without reordering existing records, so the diff contains only additions.
- A failed or bounded search is not evidence that no instrument exists.
