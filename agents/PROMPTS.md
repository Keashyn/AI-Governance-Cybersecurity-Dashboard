# Weekly public-law curation pipeline

Use this process when the weekly curation workflow runs. Work from the checked-out `master` snapshot and prepare a reviewable pull request. The Grok GitHub Actions workflow publishes its prepared files on `grok/weekly-curation`; a standalone run must create a new branch. Never push to `master`, merge a pull request, or deploy directly.

## Research

1. Read `README.md`, `data.json`, `ingest.py`, and `cybersecurity_ingest.py` to understand the existing schema, sources, import rules, and deduplication.
2. Review the official source feeds and source catalogs used by the dashboard for new records and material changes since the previous weekly run. Prioritize official government gazettes, legislation databases, regulator publications, and the linked issuer pages. Use secondary sources only to discover a possible instrument, then verify it at the official source before adding it.
3. Cover AI governance instruments and cybersecurity, cybercrime, privacy/data-protection, and related digital or sector-specific laws and regulations across the dashboard's country and U.S. state jurisdictions. Also review standards and frameworks in the standards feed, keeping them separate in meaning from laws. Work through jurisdictions systematically; do not claim exhaustive coverage from a bounded search or catalog.
4. Use public material only. Record the authoritative source URL for every legal record. Catalog metadata and summaries may be reused only within their stated license and attribution terms; the issuer's official text remains authoritative.

## Verify and classify

- Verify the instrument title, issuing authority, jurisdiction, type, stage, publication/adoption date, and effective date against an official source. If an attribute is unclear, leave it empty or state the uncertainty in the summary; do not guess.
- Clearly distinguish enacted or in-force instruments, proposals, consultations, adopted policy, and guidance. A standards body marking a standard “published” does not mean a government adopted it or made it legally binding. Preserve repealed, expired, withdrawn, or superseded records when source evidence supports that status.
- Deduplicate by stable record ID, jurisdiction plus official source URL, and instrument title. Update an existing record when appropriate instead of creating a second copy. Append a dated `history` entry for every material change; do not overwrite prior history.
- Keep summaries neutral, concise, and grounded in cited source content. Do not infer obligations absent from the source. An absent record or unsuccessful search is not evidence that no law applies.
- Do not add broad “reviewed” placeholders as if they were laws. Do not remove records solely because a source is temporarily unavailable.

## Update and report

1. Update `data.json` using its existing record structure. Keep source references and catalog attribution current. Update ingestion code or source documentation only when a repeatable source check needs to change.
2. Create `reports/weekly/curation-YYYY-MM-DD.md` for the UTC date of the run. Report records added, materially changed, or checked without a change; include jurisdiction, title, status, primary source link, and a short note on verification. State which jurisdictions or feeds could not be checked and any coverage limitations. If no material records changed, make that explicit.
3. Validate the JSON, unique record IDs, required source links for additions, change-history entries for updates, and that standards are not labeled as laws. Review `git diff` for accidental deletions, unrelated edits, fabricated dates, or unsupported status changes.
4. For the Grok workflow, leave branch creation, commit, push, and pull-request creation to `.github/workflows/grok-weekly-curation.yml`; write the dated report and `reports/weekly/latest.md` for that action. For a standalone run, create `weekly-curation/YYYY-MM-DD` (append the workflow run number if it already exists), commit only the curation update and report, push that branch, and open a pull request against `master`. The PR title and description must summarize the number of additions and material updates, note major source and coverage limits, and link the report. Never merge the PR or trigger a deployment.
5. If research cannot verify an item, exclude it from the legal register and describe the limitation in the report instead of presenting it as fact.
