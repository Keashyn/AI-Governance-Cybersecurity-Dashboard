# AI Governance Watch

A public source tracker for AI governance laws, proposals, consultations, and official guidance. The dashboard includes search and filters, dates, official source links, and a history field for recorded material changes.

## Hosting and daily updates

The site is a static page (`index.html`) with source records in `data.json`. `.github/workflows/daily.yml` runs daily at 13:17 UTC and can also be started manually. It checks the U.S. Federal Register API, deduplicates records by document number, stores changes, then publishes the site through GitHub Pages. Other jurisdiction links are curated references; they are not automatically polled daily.

The public dashboard is hosted on GitHub Pages at https://keashyn.github.io/AI-Governance-Dashboard/.

## Sources and coverage

`data.json` links to government and regulator sources, including EUR-Lex, U.S. Federal Register, UK legislation, Canada Gazette, China’s CAC, Japan’s Cabinet Office, Colorado’s General Assembly, and New York City’s DCWP. The country directory distinguishes countries with verified records from countries whose official-source review is incomplete. “Not yet reviewed” is not a finding that no AI law applies. Records remain a curated baseline rather than an exhaustive survey of every AI-related law, sector rule, or subnational instrument. The current scheduled ingestion automatically checks only the U.S. Federal Register; other sources require curation. Verify current law with the issuing authority. This tracker is informational, not legal advice.

## Local use

Serve the repository root with any static HTTP server. Run `python3 ingest.py` to query the public Federal Register API. The script uses no credentials and accesses only public data.
