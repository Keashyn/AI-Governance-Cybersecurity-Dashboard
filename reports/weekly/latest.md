# Weekly curation 2026-11-16 run 7: 7 additions, 0 updates, 5 held

Items 1,099 → 1,106; sources 301 → 309. Base master 05b1c9ea (PR #29 merged). No US-FR-, CYBERLAW- or CYBERSTANDARD- record is touched. The Élysée charter stays held and was not added. FR ingest notes are workflow-only and were not added.

**Added:** KR-KISA-AI-SECURITY-GUIDE-2025 (Guidance, 2025-12-10; corrected reissue 2026-03-13), AU-NSW-AI-OPERATIONAL-POLICY-2026 (Adopted policy, 2026-07-30; mandatory under DCS-2026-02), SG-PDPC-GENAI-ADVISORY-GUIDELINES-2026 (Guidance, 2026-07-20), EU-GPAI-CODE-OF-PRACTICE-2025 (Guidance, 2025-07-10), EU-AIO-HIGH-RISK-CLASSIFICATION-GUIDELINES-DRAFT-2026 (Consultation, 2026-05-19; closed 23 Jul 2026), EU-DSA-ELECTION-GUIDELINES-2024 (Guidance, OJ C/2024/3014, 2024-04-26), IN-CERTIN-CIAD-2026-0020-FRONTIER-AI-ADVISORY-2026 (Guidance, 2026-04-26).

**Held (NEEDS_REVIEW):**
- KR-KISA-AGENTIC-AI-ZERO-TRUST-GUIDE-2026: the summary attributes detail to the MSIT policy-DB listing, which shows only the chapter list, and the guide's own five action types differ from the four the summary lists.
- AU-QLD-FAIRA-FRAMEWORK-2026: the QGEA page says 'Non-mandated', but the framework says applying it is 'a mandated requirement' under the AI governance policy.
- US-HR10981-2026: master has no referral-only Congress bill, and the 'no text' claim is outdated.
- UK-ARTIFICIAL-SUPERINTELLIGENCE-BILL-2026 and UK-ONLINE-PLATFORMS-REGULATION-BILL-2026: master has no comparable UK private members' bill.

## How the open questions were resolved

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

Full report: `reports/weekly/curation-2026-11-16-run-7.md`.
