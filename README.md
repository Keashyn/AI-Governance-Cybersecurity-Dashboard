# AI Governance Watch

A public source tracker for AI governance laws, proposals, consultations, and official guidance. The dashboard includes search and filters, dates, official source links, and a history field for recorded material changes.

## Hosting and daily updates

The site is a static page (`index.html`) with records in `data.json`. `.github/workflows/daily.yml` runs daily at 13:17 UTC and can also be started manually. It checks the U.S. Federal Register API and the Cybersecurity Database open catalog, deduplicates records, records material changes, then publishes the site through GitHub Pages. Legal imports are limited to laws, decrees, regulations, directives, and circulars; country-specific strategy and guidance documents are not imported by that job. The same daily job also imports the catalog's standards, frameworks, and technical specifications as reference records, shown in country-filtered searches without implying local adoption or legal force.

The public dashboard is hosted on GitHub Pages at https://keashyn.github.io/AI-Governance-Dashboard/.

## Sources and coverage

`data.json` links to government and regulator sources, including EUR-Lex, U.S. Federal Register, UK legislation, Canada Gazette, China’s CAC, Japan’s Cabinet Office, Colorado’s General Assembly, and New York City’s DCWP. AI records remain a curated baseline. Cybersecurity records include cybersecurity, cybercrime, privacy/data-protection, and related digital or sector-specific laws and regulations. Their metadata and English summaries are adapted from the [Cybersecurity Database open dataset](https://www.cybersecuritydatabase.org/en/open-data/), licensed under CC BY 4.0; the official instrument source is linked on each record and remains authoritative. Standards, frameworks, and technical specifications are imported separately from the [standards catalog](https://www.cybersecuritydatabase.org/en/standards/); each links to its publisher's official catalog, and is identified as reference material rather than law. Showing these references under a country filter does not establish local adoption or legal obligation. Attribution: Cybersecurity Database – cybersecuritydatabase.org. Its legal-record country coverage is not exhaustive, so the absence of a record does not mean no applicable law exists. Verify current law with the issuing authority. This tracker is informational, not legal advice.

## Local use

Serve the repository root with any static HTTP server. Run `python3 ingest.py` to query the public Federal Register API. The script uses no credentials and accesses only public data.
