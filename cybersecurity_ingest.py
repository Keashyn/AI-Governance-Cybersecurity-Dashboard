#!/usr/bin/env python3
"""Import cybersecurity-related laws and regulations from the CC BY 4.0 catalog.

Each imported record links to the issuing authority's source URL. The catalog is
used for discovery, metadata, and summaries; it is not the legal authority.
"""
import json
import re
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data.json"
API = "https://www.cybersecuritydatabase.org/api/v1/"
LEGAL_TYPES = {"law", "decree", "regulation", "directive", "circular"}
STATUS = {
    "in_vigore": "In force",
    "superato": "Superseded",
    "scaduto": "Expired",
    "adottato": "Enacted",
    "abrogato": "Repealed",
    "in_consultazione": "Consultation",
}
ALIASES = {
    "Côte d'Ivoire": "Côte d’Ivoire",
    "Viet Nam": "Vietnam",
    "State of Palestine": "Palestine",
    "São Tomé and Príncipe": "Sao Tome and Principe",
    "Holy See (Vatican City)": "Vatican City",
    "Republic of the Congo": "Congo (Republic of the)",
}
EFFECTIVE_RE = re.compile(
    r"(entry into force|enters? into force|comes? into force|takes? effect|"
    r"effective from|effective date|applies? from|application begins)",
    re.I,
)


def fetch(path):
    req = urllib.request.Request(
        API + path,
        headers={"User-Agent": "AIGovernanceWatch/1.0 (public legal source register)"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def norm(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def title_key(value):
    return re.sub(r"[^a-z0-9]", "", norm(value).lower())


def country_name(code, jurisdictions):
    record = jurisdictions.get(code, {})
    name = record.get("name_en", code)
    name = ALIASES.get(name, name)
    if name == "United States":
        return "United States · Federal"
    return name


def effective_date(doc):
    for event in doc.get("key_dates", []):
        label = event.get("label", {}).get("en", "")
        if EFFECTIVE_RE.search(label):
            return event.get("date") or ""
    return ""


def make_item(doc, jurisdiction, catalog_date, today):
    summary = doc.get("summary", {})
    topics = doc.get("topics", [])
    title = doc.get("title_original") or doc.get("short_title", {}).get("en") or doc["slug"]
    return {
        "id": "CYBERLAW-" + re.sub(r"[^A-Za-z0-9_-]", "-", doc["slug"]).upper(),
        "jurisdiction": jurisdiction,
        "regulator": norm(doc.get("issuing_body")) or "Issuing authority",
        "title": norm(title),
        "officialTitle": norm(doc.get("title_original")),
        "instrumentType": doc.get("document_type", "law").replace("_", " ").title(),
        "status": STATUS.get(doc.get("status"), "Reviewed"),
        "publicationDate": "",
        "adoptedDate": doc.get("date_adopted") or "",
        "effectiveDate": effective_date(doc),
        "topic": "Cybersecurity · " + " · ".join(t.replace("-", " ") for t in topics),
        "sourceUrl": doc.get("source_url"),
        "summary": norm(summary.get("en") if isinstance(summary, dict) else summary)[:1800],
        "history": [{
            "date": today,
            "change": "Added from the Cybersecurity Database open catalog (CC BY 4.0); the linked issuing-authority source is the legal reference.",
        }],
        "catalogSource": "Cybersecurity Database",
        "catalogRecordId": doc.get("id"),
        "catalogSlug": doc.get("slug"),
        "catalogUpdatedAt": doc.get("updated_at") or catalog_date,
    }


def materially_update(old, fresh, today):
    fields = (
        "jurisdiction", "regulator", "title", "officialTitle", "instrumentType",
        "status", "adoptedDate", "effectiveDate", "topic", "sourceUrl", "summary",
    )
    changed = [key for key in fields if old.get(key, "") != fresh.get(key, "")]
    if not changed:
        old["catalogUpdatedAt"] = fresh.get("catalogUpdatedAt", old.get("catalogUpdatedAt"))
        return False
    history = old.setdefault("history", [])
    for key in fields:
        if key in fresh:
            old[key] = fresh[key]
    old["catalogUpdatedAt"] = fresh.get("catalogUpdatedAt", old.get("catalogUpdatedAt"))
    history.append({
        "date": today,
        "change": "Catalog update: " + ", ".join(changed) + ". Official issuing-authority source remains linked.",
    })
    return True


def main():
    data = json.loads(DATA.read_text())
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        documents_payload = fetch("documents.json")
        jurisdiction_payload = fetch("jurisdictions.json")
    except Exception as exc:
        print(f"Cybersecurity catalog unavailable; preserving existing records: {exc}")
        return
    jurisdictions = {x["code"]: x for x in jurisdiction_payload.get("jurisdictions", [])}
    country_labels = {x.get("jurisdiction", "").split(" · ")[0] for x in data.get("items", [])}

    by_id = {x["id"]: x for x in data.get("items", [])}
    source_urls = {norm(x.get("sourceUrl")) for x in data.get("items", []) if x.get("sourceUrl")}
    title_index = {}
    for item in data.get("items", []):
        base = item.get("jurisdiction", "").split(" · ")[0]
        title_index.setdefault(base, []).append(title_key(item.get("title")))

    added = 0
    updated = 0
    skipped_scope = 0
    skipped_duplicate = 0
    for doc in documents_payload.get("documents", []):
        if doc.get("document_type") not in LEGAL_TYPES:
            continue
        jurisdiction_meta = jurisdictions.get(doc.get("jurisdiction"), {})
        # This register is for countries and the EU-level legal framework.
        if jurisdiction_meta.get("type") not in {"paese", "territorio", "organizzazione_regionale"}:
            skipped_scope += 1
            continue
        jurisdiction = country_name(doc.get("jurisdiction"), jurisdictions)
        base = jurisdiction.split(" · ")[0]
        if jurisdiction_meta.get("type") != "organizzazione_regionale" and base not in country_labels:
            skipped_scope += 1
            continue
        if not doc.get("source_url"):
            skipped_scope += 1
            continue

        fresh = make_item(doc, jurisdiction, documents_payload.get("updated_at", today), today)
        ident = fresh["id"]
        old = by_id.get(ident)
        if old:
            if materially_update(old, fresh, today):
                updated += 1
            continue

        # Avoid adding another copy of an instrument already hand-curated in the register.
        if norm(doc.get("source_url")) in source_urls:
            skipped_duplicate += 1
            continue
        key = title_key(fresh["title"])
        if any(SequenceMatcher(None, key, other).ratio() >= 0.86 for other in title_index.get(base, [])):
            skipped_duplicate += 1
            continue

        by_id[ident] = fresh
        source_urls.add(norm(fresh["sourceUrl"]))
        title_index.setdefault(base, []).append(key)
        added += 1

    data["items"] = sorted(
        by_id.values(),
        key=lambda x: (x.get("publicationDate") or x.get("adoptedDate") or "", x["id"]),
        reverse=True,
    )
    data["cybersecurityCatalog"] = {
        "name": "Cybersecurity Database",
        "url": "https://www.cybersecuritydatabase.org/en/open-data/",
        "apiUrl": API + "documents.json",
        "license": "CC BY 4.0",
        "attribution": documents_payload.get("attribution", "Cybersecurity Database – cybersecuritydatabase.org"),
        "catalogUpdatedAt": documents_payload.get("updated_at", today),
        "lastChecked": today,
    }
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(
        f"Cybersecurity catalog {documents_payload.get('updated_at', 'unknown')}: "
        f"added {added}, updated {updated}, skipped {skipped_duplicate} duplicates, "
        f"skipped {skipped_scope} out-of-scope records; {len(data['items'])} total dashboard records."
    )


if __name__ == "__main__":
    main()
