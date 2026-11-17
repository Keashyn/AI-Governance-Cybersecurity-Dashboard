# Curation report: 2026-11-16 run 7

Run: 2026-11-16 19:42–19:55 CST. Base master 05b1c9ea41be4152235b25f53c9b32ff83d01814 (PR #29 merged), 1,099 items, 301 sources.
Input: /workspace/research/research-pass-2026-11-16-run-7.json, 12 candidates.
Result: 7 APPROVED (new records), 5 NEEDS_REVIEW, 0 REJECTED, 0 updates. Items 1,099 → 1,106; sources 301 → 309.
Base data.json sha256 d44238a6cef5ca98b105bf5def8633772ab97085a4f240daf2e446b8d9ff27d5; data.dryrun.json sha256 cb9b6d081392d133beacd7bfa42e448bcca5a626412969b5f9d1b254fe2a2796.

New records carry one history entry dated 2026-11-16 ('Added after verification against the official source (...)'); the researcher's history is not carried over. Candidate fields are otherwise unchanged. No US-FR-, CYBERLAW- or CYBERSTANDARD- record is touched. The Élysée charter stays held. FR ingest notes are not added.


## Decisions

### KR-KISA-AGENTIC-AI-ZERO-TRUST-GUIDE-2026: NEEDS_REVIEW
Official URL: https://www.kisa.or.kr/2060204/form?postSeq=25&page=1

Default (f). I opened the KISA post and its PDF (261106_에이전틱_AI_제로트러스트_안내서.pdf) myself. Post: 등록일 2026-11-06; made with 산·학·연 AI zero trust experts after analysing domestic and international AI security and zero trust guides. The PDF is dated 2026.11, by MSIT and KISA. It builds on 제로트러스트 가이드라인 2.0 and its 4-level maturity model, and has an architecture chapter, a maturity-model chapter and an adoption and operation chapter with scenarios. It covers tool calls, delegation, external communication, and 'human approval or pre-approved policies' for irreversible actions. Foreword: '실질적인 참고가 되기를 바랍니다', so 'non-binding' is supportable. HELD because the summary attributes detail to the wrong source. It says 'Per the MSIT policy-DB listing, this includes verifying agent actions at input handling, tool calls, task delegation and external communication'. The korea.kr listing (MSIT 정보보호산업과, 등록일 2026.11.06, type 매뉴얼) shows only the chapter list. Also, the guide's own list of action-control types is five: 입력·내부 실행·물리 명령·위임·외부 통신 (input, internal execution, physical commands, delegation, external communication). Not corrected silently.

Suggested fix (needs approval): Replace 'Per the MSIT policy-DB listing, this includes verifying agent actions at input handling, tool calls, task delegation and external communication, and applying human approval or pre-approved policies according to risk.' with 'The guide calls for controlling individual agent actions, including tool calls, delegation and external communication, across five action types (input, internal execution, physical commands, delegation and external communication), with human approval or pre-approved policies for irreversible actions.'

Evidence: evidence/kisa25.html, evidence/kisa25.txt, evidence/kisa25.pdf, evidence/kisa25.pdf.txt, evidence/koreakr_41939.html, evidence/koreakr_41939.txt

### KR-KISA-AI-SECURITY-GUIDE-2025: APPROVED
Official URL: https://www.kisa.or.kr/2060204/form?postSeq=19&page=1

Default (f). I opened the KISA post (postSeq=19) and both attachments. The post shows 등록일 2025-12-10, distribution also via the MSIT site, and a corrected reissue with 정오표 on 2026-03-13. The corrected PDF is titled 인공지능(AI) 보안 안내서; its 일러두기 says it is an MSIT–KISA policy-research output, for developers, service providers and users. It is '참고 자료로 활용할 수 있도록 편찬', so 'non-binding' is supported. The errata PDF lists the corrections (p.17, p.25 item 3.4.8, p.54 item 3.4.7). Status Guidance. 'South Korea' matches master.

Evidence: evidence/kisa19.html, evidence/kisa19.txt, evidence/kisa19.pdf, evidence/kisa19.pdf.txt, evidence/kisa19_errata.pdf, evidence/kisa19_errata.pdf.txt

### AU-NSW-AI-OPERATIONAL-POLICY-2026: APPROVED
Official URL: https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-strategy-and-operational-policy/nsw-ai-operational-policy

The Digital NSW page describes an all-of-government policy with mandatory agency requirements. It replaces the NSW AI Ethics Policy and adopts Australia's AI Ethics Principles. Requirements: an accountable official, AIAF Platform registration, referral to the AI Review Committee, ICT acceptable use and AI literacy training. The PDF reads 'Final version 1.1 – 30 July 2026', 'First published: 30 July 2026' and 'Compliance with this policy is mandatory in accordance with DCS Circular DCS-2026-02'. arp.nsw.gov.au: DCS-2026-02 'Issued: 30 July 2026 by Secretary, Department of Customer Service', Status Active, Compliance Mandatory, 'Updated 1 September 2026'. The AIAF page says 'The AIAF Platform is mandatory from 30 September 2026'. Status Adopted policy. Default (b): master has no Australian state string (all 20 Australian records use 'Australia'). 'Australia · New South Wales' follows master's 'Country · subunit' form (for example 'Mexico · Federal' and 'Bosnia and Herzegovina · Federation of Bosnia and Herzegovina') with no conflicting spelling, so it is kept as the candidate gave it and flagged as a new jurisdiction string.

Evidence: evidence/nsw.html, evidence/nsw.txt, evidence/nsw.pdf, evidence/nsw.pdf.txt, evidence/nsw_arp.html, evidence/nsw_arp.txt, evidence/nsw_aiaf.html, evidence/nsw_aiaf.txt

### AU-QLD-FAIRA-FRAMEWORK-2026: NEEDS_REVIEW
Official URL: https://www.forgov.qld.gov.au/information-technology/queensland-government-enterprise-architecture-qgea/qgea-directions-and-guidance/qgea-policies-standards-and-guidelines/faira-framework

The QGEA page shows Version v2.0.0, Status 'Current' and 'Non-mandated', 'Effective: September 2026–current' and 'Last updated: 29 September 2026'. Default (c): the DOCX (FAIRA-framework-v2.0.0.docx) shows only 'Final V2.0.0 September 2026', a month without a day, so the last-updated date 2026-09-29 is the right publicationDate under (c). HELD because the official sources contradict each other on whether it is mandatory. The QGEA page says 'Non-mandated', and the candidate summary repeats that. The framework document itself says 'Under the AI governance policy, application of the FAIRA framework is a mandated requirement for all deployed uses of AI in the Queensland Government.' So 'Guidance' versus 'Adopted policy', and the 'Non-mandated' wording, are a judgement call. Default (b): 'Australia · Queensland' would be a new string; see NSW.

Suggested fix (needs approval): Either keep status Guidance and add: 'The framework states that, under the Queensland AI governance policy, applying FAIRA is a mandated requirement for all deployed uses of AI in the Queensland Government, although the QGEA entry is labelled Non-mandated.', or use status 'Adopted policy'. Keeper's call; optionally open the AI governance policy to settle it.

Evidence: evidence/qld.html, evidence/qld.txt, evidence/qld_faira.docx, evidence/qld_faira.docx.txt

### SG-PDPC-GENAI-ADVISORY-GUIDELINES-2026: APPROVED
Official URL: https://www.pdpc.gov.sg/organisations/regulations-decisions/regulatory-guidance/advisory-guidelines-on-use-of-personal-data-in-generative-ai

The PDPC page shows the exact title and 'Published on 20 Jul 2026'. The PDF reads 'Issued 20 July 2026', with Part II covering the Publicly Available Exception, documentation of the assessment, and consent and notification. Part III covers model providers, system providers and system deployers: 'System Deployers bear primary responsibility', with agentic functionalities at para 9. Part IV covers access and correction. Para 1.4 says it is read with the AI Recommendation and Decision Systems and Key Concepts guidelines; the former page shows '01 Mar 2024', which confirms '2024'. Para 1.5: 'advisory in nature, are not legally binding'. The consultation page (HTML) has 2 June 2026, 1 July 2026 (closed) and 20 July 2026 entries. No duplicate: master SG records are SG-AI-AGENTS-CONSUMER-ADVISORY-2026, SG-MGF-AGENTIC-2026 and CYBERLAW items. Status Guidance.

Evidence: evidence/pdpc.html, evidence/pdpc.txt, evidence/pdpc.pdf, evidence/pdpc.pdf.txt, evidence/pdpc_consult2.html, evidence/pdpc_ards.html

### EU-GPAI-CODE-OF-PRACTICE-2025: APPROVED
Official URL: https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai

Default (e), status Guidance; this follows EU-COP-AI-CONTENT-MARKING-2026. The Commission policy page (last update 7 October 2026) says 'code was published on July 10, 2025'. Its three chapters: Transparency (with the Model Documentation Form) and Copyright cover all GPAI providers under Article 53, and Safety and Security covers systemic-risk providers under Article 55. It records the Commission and AI Board adequacy confirmation, the Signatory Taskforce 'chaired by the AI Office', and signatories including Amazon, Anthropic, Google, IBM, Microsoft, Mistral AI and OpenAI. The news page (Publication 10 July 2025) mentions '13 independent experts, with input from over 1,000 stakeholders'. The opinion library page (Publication 01 August 2025) has the Commission and AI Board confirmation. No duplicate: EU-COP-AI-CONTENT-MARKING-2026 is a different code, and EU-AIO-GPAI-GUIDELINES-2025 is the Commission guidelines.

Evidence: evidence/gpai_cop.html, evidence/gpai_cop.txt, evidence/gpai_news.html, evidence/gpai_news.txt, evidence/gpai_opinion.html, evidence/gpai_opinion.txt

### EU-AIO-HIGH-RISK-CLASSIFICATION-GUIDELINES-DRAFT-2026: APPROVED
Official URL: https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems

Default (d), status Consultation; feedback closed 23 July 2026. The library page shows 'Publication 19 May 2026' and Last update 23 July 2026. It describes Article 6(5) practical examples, Section III for Art. 6(1) (Annex I, third-party conformity assessment) and Section IV for Art. 6(2) (Annex III), with documents 128559–128561. The targeted consultation page reads 'Opening: 19 May 2026 / Closing: 23 July 2026', and a deadline extension from 23 June to 23 July 2026, via EUSurvey (AIhighrisks_2026). It says 'The final guidelines will be adopted by the end of 2026', so the text is still a draft. Note: the 19 May news page still shows the original '23 June 2026' deadline, which the consultation page supersedes. The candidate cited the AI Act Service Desk for the closing date. I confirmed the date on the Commission consultation page instead; the Service Desk URL I tried returned 404.

Evidence: evidence/hr_draft.html, evidence/hr_draft.txt, evidence/hr_consult.html, evidence/hr_consult.txt, evidence/hr_news.html, evidence/hr_news.txt

### EU-DSA-ELECTION-GUIDELINES-2024: APPROVED
Official URL: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC03014

EUR-Lex CELEX 52024XC03014: 'OJ C, C/2024/3014, 26.4.2024', 'Date of document: 26/04/2024'. The full title, 'Communication from the Commission – Commission Guidelines for providers of Very Large Online Platforms … pursuant to Article 35(3) of Regulation (EU) 2022/2065', matches the candidate without the 'Communication from the Commission –' prefix. The text lists the related DSA obligations as summarised: terms and conditions, recommender systems, Articles 36 and 48 crisis response, transparency and audits, advertising and data access. The Commission library page says 'formally adopted by the Commission on 26 April 2024'. The 10 Nov 2026 revision consultation is master record EU-DSA-ELECTION-GUIDELINES-REVISION-CONSULTATION-2026, so this is not a duplicate. Status Guidance; publicationDate is the OJ date, following master's EU convention.

Evidence: evidence/dsa2024_eurlex.html, evidence/dsa2024_eurlex.txt, evidence/dsa2024_all.html, evidence/dsa2024_all.txt, evidence/dsa2024_lib.html, evidence/dsa2024_lib.txt

### IN-CERTIN-CIAD-2026-0020-FRONTIER-AI-ADVISORY-2026: APPROVED
Official URL: https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIAD-2026-0020&pageid=PUBVLNOTES02

The CERT-In page VLCODE=CIAD-2026-0020 shows 'Defending Against Frontier AI Driven Cyber Risks', 'Original Issue Date: April 26, 2026' and 'Severity Rating: High'. It covers autonomous vulnerability discovery, accelerated exploit development, automated reconnaissance, credential harvesting, AI-generated phishing and impersonation, and multi-stage orchestration. Recommendations: vigilance and monitoring for unusually fast activity, attack-surface reduction, DDoS protection, Zero Trust with MFA, rapid risk-based patching, supply-chain controls, and log preservation and reporting 'as per CERT-In Directions 2022'. There is a 'For Individuals' section. Master's IN-CERTIN-CISG-2026-03 cites this advisory, and no record exists for the advisory itself. Status Guidance.

Evidence: evidence/ciad.html, evidence/ciad.txt

### US-HR10981-2026: NEEDS_REVIEW
Official URL: https://www.congress.gov/bill/119th-congress/house-bill/10981

Default (a). api.congress.gov confirms H.R.10981 'American AI Security Act': introduced 2026-11-10 by Rep. Gottheimer [D-NJ-5], 1 cosponsor, referred to Energy and Commerce and Intelligence (Permanent Select), official title as given. In scope (AI model regulation). HELD for two reasons. (1) No precedent: every federal Congress bill in master has committee action or beyond, and none is referral-only, so master does not treat a bill at this stage as a record. (2) The summary's 'No text or CRS summary was available yet' is now outdated: the API lists the text version 'Introduced in House' (BILLS-119hr10981ih, dated 2026-11-10). There is still no CRS summary. Not corrected silently.

Suggested fix (needs approval): If the keeper wants referral-only bills tracked, change 'No text or CRS summary was available yet.' to 'Introduced text is available; no CRS summary was available yet.' and approve as Proposed. Otherwise hold until committee action.

Evidence: evidence/api_hr10981.json, evidence/api_hr10981_actions.json, evidence/api_hr10981_titles.json, evidence/api_hr10981_cosponsors.json, evidence/api_hr10981_summaries.json, evidence/api_hr10981_text.json

### UK-ARTIFICIAL-SUPERINTELLIGENCE-BILL-2026: NEEDS_REVIEW
Official URL: https://bills.parliament.uk/bills/4288

bills-api.parliament.uk (bills.parliament.uk returns 403 to scripts) confirms Bill 4288, 'Artificial Superintelligence Bill', a Ten Minute Rule bill by Alex Sobel (Labour), with the long title as given. Commons 1st reading 2026-09-08 and 2nd reading 2026-11-27. Default (a): master's only UK bill is UK-CYBER-SECURITY-RESILIENCE-BILL-2025, a government bill. Master has no private members' bill, so there is no comparable precedent and the record is held for the keeper's scope decision. Not added.

Evidence: evidence/uk4288.json, evidence/uk4288_st.json

### UK-ONLINE-PLATFORMS-REGULATION-BILL-2026: NEEDS_REVIEW
Official URL: https://bills.parliament.uk/bills/4324

bills-api.parliament.uk confirms Bill 4324, 'Online Platforms (Regulation) Bill', a Presentation Bill by Manuela Perteghella (Liberal Democrat). Commons 1st reading 2026-11-11 and 2nd reading 2027-03-19, and the long title is paraphrased accurately. Default (a): master's only UK bill is UK-CYBER-SECURITY-RESILIENCE-BILL-2025, a government bill. Master has no private members' bill, so there is no comparable precedent and the record is held for the keeper's scope decision. Not added.

Evidence: evidence/uk4324.json, evidence/uk4324_st.json

## Default resolutions

- **(a) Introduced-only bills:**
  - **H.R.10981:** verified on api.congress.gov (American AI Security Act; introduced and referred 2026-11-10; Gottheimer; 1 cosponsor). It is in scope. Every federal Congress bill in master has committee action or beyond, so master has no precedent for a referral-only bill. It is NEEDS_REVIEW. The summary's 'No text … available yet' is also outdated, because BILLS-119hr10981ih is now listed.
  - **UK bills 4288 and 4324:** verified via bills-api.parliament.uk (bills.parliament.uk returns 403 to scripts). Master's only UK bill is a government bill (UK-CYBER-SECURITY-RESILIENCE-BILL-2025), so there is no comparable private members' bill precedent. Both are NEEDS_REVIEW.
- **(b) Australian state strings:** master has no Australian state string; all 20 Australian records use 'Australia'. Master does use the 'Country · subunit' form outside the US, for example 'Mexico · Federal', 'Pakistan · Federal' and 'Bosnia and Herzegovina · Federation of Bosnia and Herzegovina'. No conflicting spelling exists, so 'Australia · New South Wales' is kept as given and **flagged as a new jurisdiction string**. 'Australia · Queensland' would also be new, but that record is held for another reason.
- **(c) QLD FAIRA date:** the DOCX shows only 'Final V2.0.0 September 2026', a month without a day, so the page's last-updated date of 29 Sep 2026 is the correct publicationDate. The record is held anyway because of the mandated/non-mandated contradiction.
- **(d) EU high-risk draft:** status is Consultation. The Commission consultation page shows 'Closing: 23 July 2026', extended from 23 June, and says final guidelines are due by end-2026, so the text is still a draft.
- **(e) GPAI CoP:** status is Guidance, following the precedent of EU-COP-AI-CONTENT-MARKING-2026.
- **(f) KISA:** I opened both KISA posts and both guide PDFs myself, plus the errata and the korea.kr MSIT listing; the press was not relied on.
  - **AI Security Guide:** fully confirmed, and the guide calls itself '참고 자료' (reference material).
  - **Agentic AI zero-trust guide:** its content is confirmed by the PDF, but it is held because of the misattribution in its summary. A suggested fix is in decisions.json.

Open PRs (read-only check): #30 is a report-only weekly-curation PR (branch weekly-curation/2026-11-17) and #31 is an ingest-script and test fix. Neither changes data.json, and no Verifier PR is open.

## Validation

```
roundtrip True
dup ids 0
updates: none in this run
KR-KISA-AI-SECURITY-GUIDE-2025 | jur in master True | topic ' · ' True | status allowed True | Guidance 2025-12-10 — | hist 1 | reserved prefix False | in base False
AU-NSW-AI-OPERATIONAL-POLICY-2026 | jur in master False (FLAGGED new string: Australia · New South Wales) | topic ' · ' True | status allowed True | Adopted policy 2026-07-30 — | hist 1 | reserved prefix False | in base False
SG-PDPC-GENAI-ADVISORY-GUIDELINES-2026 | jur in master True | topic ' · ' True | status allowed True | Guidance 2026-07-20 — | hist 1 | reserved prefix False | in base False
EU-GPAI-CODE-OF-PRACTICE-2025 | jur in master True | topic ' · ' True | status allowed True | Guidance 2025-07-10 — | hist 1 | reserved prefix False | in base False
EU-AIO-HIGH-RISK-CLASSIFICATION-GUIDELINES-DRAFT-2026 | jur in master True | topic ' · ' True | status allowed True | Consultation 2026-05-19 — | hist 1 | reserved prefix False | in base False
EU-DSA-ELECTION-GUIDELINES-2024 | jur in master True | topic ' · ' True | status allowed True | Guidance 2024-04-26 — | hist 1 | reserved prefix False | in base False
IN-CERTIN-CIAD-2026-0020-FRONTIER-AI-ADVISORY-2026 | jur in master True | topic ' · ' True | status allowed True | Guidance 2026-04-26 — | hist 1 | reserved prefix False | in base False
dup new sourceUrls []
dup new titles []
protected changed []
changed existing []
existing order kept True
held ids absent True ['KR-KISA-AGENTIC-AI-ZERO-TRUST-GUIDE-2026', 'AU-QLD-FAIRA-FRAMEWORK-2026', 'US-HR10981-2026', 'UK-ARTIFICIAL-SUPERINTELLIGENCE-BILL-2026', 'UK-ONLINE-PLATFORMS-REGULATION-BILL-2026']
FR-ELYSEE absent True
catalog/lastChecked same True True sources prefix True
dup source urls 0
items 1099 -> 1106 sources 301 -> 309
```
