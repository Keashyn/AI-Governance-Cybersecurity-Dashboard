#!/usr/bin/env python3
"""Fetch public Federal Register AI-related documents and maintain a deduplicated history."""
import json, os, re, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data.json"
API = "https://www.federalregister.gov/api/v1/documents.json?" + urllib.parse.urlencode({
    "conditions[term]": '"artificial intelligence" OR AI',
    "per_page": 100,
    "order": "newest",
    "fields[]": ["title", "document_number", "type", "publication_date", "effective_on", "agencies", "html_url", "abstract"]
}, doseq=True)

def fetch():
    req = urllib.request.Request(API, headers={"User-Agent": "AIGovernanceWatch/1.0 (public official-source tracker)"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r).get("results", [])

def norm(s): return re.sub(r"\s+", " ", (s or "")).strip()

def main():
    data = json.loads(DATA.read_text())
    now = datetime.now(timezone.utc).date().isoformat()
    byid = {x["id"]: x for x in data["items"]}
    for doc in fetch():
        ident = "US-FR-" + doc["document_number"]
        kind = (doc.get("type") or "Notice").lower()
        status = "Proposed" if "proposed" in kind else "Guidance" if "notice" in kind else "In force" if "rule" in kind else "Consultation"
        agency = ", ".join(a.get("name", "") for a in doc.get("agencies", [])) or "Federal agency"
        item = {"id": ident, "jurisdiction":"United States · Federal", "regulator":agency,
          "title":norm(doc.get("title")), "instrumentType":doc.get("type", "Federal Register document"),
          "status":status, "publicationDate":doc.get("publication_date"), "effectiveDate":doc.get("effective_on") or "—",
          "topic":"AI · federal rulemaking", "sourceUrl":doc.get("html_url"), "summary":norm(doc.get("abstract"))[:700], "history":[]}
        old = byid.get(ident)
        if old is None:
            item["history"] = [{"date":now,"change":"Added from the Federal Register’s public API."}]
            byid[ident] = item
        else:
            changed = []
            for k in ("title", "status", "effectiveDate", "summary", "sourceUrl"):
                if old.get(k) != item.get(k) and item.get(k):
                    changed.append(k)
            if changed:
                old.update(item)
                old.setdefault("history", []).append({"date":now,"change":"Material source update: " + ", ".join(changed) + "."})
    data["items"] = sorted(byid.values(), key=lambda x: (x.get("publicationDate") or "", x["id"]), reverse=True)
    data["lastChecked"] = now
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Checked Federal Register; {len(data['items'])} total records")

if __name__ == "__main__": main()
