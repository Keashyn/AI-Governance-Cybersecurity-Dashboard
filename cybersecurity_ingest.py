#!/usr/bin/env python3
"""Import cybersecurity-related laws and regulations from the CC BY 4.0 catalog.

Each imported record links to the issuing authority's source URL. The catalog is
used for discovery, metadata, and summaries; it is not the legal authority.
This tracker is informational, not legal advice. `python cybersecurity_ingest.py --dry-run`
prints jurisdiction and duplicate decisions and does not write data.json.

US state instruments are labelled "United States · {State}", matching the curated
register. A catalog document that is the same instrument as a curated record is
not imported again. Existing catalog rows are not deleted by this script.
"""
import json
import re
import sys
import unicodedata
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

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
# Curated US records use these labels. "New York City" is longer than "New York"
# and is checked first so a city instrument is not labelled as the state.
US_STATE_LABELS = (
    "New York City",
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming",
)
FEDERAL_ISSUER = re.compile(
    r"United States Congress|U\.S\. Congress|President of the United States|"
    r"The White House|Cybersecurity and Infrastructure Security Agency|\bCISA\b|"
    r"Department of Homeland Security|U\.S\. Department of Homeland Security|"
    r"Department of Defense|U\.S\. Department of Defense|"
    r"Department of Commerce|Federal Communications Commission|"
    r"Federal Trade Commission|Securities and Exchange Commission|"
    r"National Institute of Standards|Food and Drug Administration|"
    r"Office of the Director of National Intelligence|"
    r"National Credit Union Administration|U\.S\. Department of Health",
    re.I,
)
STATE_NOTE = re.compile(r"state law,\s+not(?:\s+a)?\s+federal", re.I)
# Known curated pairs the general matcher can miss if a future catalog edit
# drops the title or the official number. Keyed by catalog slug.
CURATED_DUPLICATE_OVERRIDES = {
    "us-new-york-raise-act-2025": "US-NY-S8828-2026",
    "kr-ai-basic-act-enforcement-decree-2026": "KR-AI-BASIC-ENFORCEMENT-DECREE-2026",
    "vn-luat-tri-tue-nhan-tao-2025": "VN-AI-2025-134",
    "cn-ai-generated-content-labelling-measures-2025": "CN-AI-LABEL-2025",
}
INGESTED_PREFIXES = ("CYBERLAW-", "CYBERSTANDARD-", "US-FR-")
WATCHED_SLUGS = (
    "us-new-york-raise-act-2025",
    "us-texas-traiga-hb-149-2025",
    "kr-ai-basic-act-enforcement-decree-2026",
    "vn-luat-tri-tue-nhan-tao-2025",
    "cn-ai-generated-content-labelling-measures-2025",
)
EFFECTIVE_RE = re.compile(
    r"(entry into force|enters? into force|comes? into force|takes? effect|"
    r"effective from|effective date|applies? from|application begins)",
    re.I,
)
STANDARD_STATUS = {
    "pubblicato": "Published standard",
    "ritirato": "Withdrawn standard",
    "in_sviluppo": "In development",
}
TITLE_STOPWORDS = {
    "the", "a", "an", "of", "and", "or", "for", "on", "to", "in", "by", "with",
}
LOGIC_FIELDS = (
    "jurisdiction", "regulator", "title", "officialTitle", "titleTranslationSource",
    "instrumentType", "status", "publicationDate", "adoptedDate", "effectiveDate",
    "topic", "sourceUrl", "summary", "catalogEntryUrl", "access", "standardEdition",
    "showInCountryFilters", "scopeNote",
)
KIND_ALIASES = {
    "presidential decree": "decree",
    "decreto": "decree",
    "decree": "decree",
    "act": "act",
    "law": "law",
    "loi": "law",
}


def fetch(path):
    req = urllib.request.Request(
        API + path,
        headers={"User-Agent": "AIGovernanceWatch/1.0 (public legal source register)"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def norm(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def fold(value):
    text = norm(value).lower().replace("đ", "d")
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def title_key(value):
    return re.sub(r"[^a-z0-9]", "", norm(value).lower())


def is_curated(item):
    return not (item.get("id") or "").startswith(INGESTED_PREFIXES)


def generated_id(slug):
    return "CYBERLAW-" + re.sub(r"[^A-Za-z0-9_-]", "-", slug or "").upper()


def detect_us_state(doc):
    """Return the curated state label, or '' when the US instrument is federal."""
    slug = (doc.get("slug") or "").lower()
    labels = sorted(US_STATE_LABELS, key=len, reverse=True)
    for name in labels:
        token = name.lower().replace(" ", "-")
        if slug.startswith("us-" + token + "-") or slug == "us-" + token:
            return name
    issuing = norm(doc.get("issuing_body"))
    for name in labels:
        escaped = re.escape(name)
        patterns = (
            rf"\b{escaped} State Legislature\b",
            rf"\b{escaped} Legislature\b",
            rf"\b{escaped} General Assembly\b",
            rf"\b{escaped} State Department\b",
            rf"\bState of {escaped}\b",
        )
        if any(re.search(pattern, issuing, re.I) for pattern in patterns):
            return name
    if FEDERAL_ISSUER.search(issuing):
        return ""
    notes = doc.get("notes") if isinstance(doc.get("notes"), dict) else {}
    if STATE_NOTE.search(notes.get("en") or ""):
        blob = " ".join([issuing, norm(doc.get("title_original")), slug.replace("-", " ")])
        hits = [name for name in labels if re.search(rf"\b{re.escape(name)}\b", blob, re.I)]
        in_issuer = [name for name in hits if re.search(rf"\b{re.escape(name)}\b", issuing, re.I)]
        if len(in_issuer) == 1:
            return in_issuer[0]
        if len(hits) == 1:
            return hits[0]
    return ""


def jurisdiction_for(doc, jurisdictions, state_jurisdictions=True):
    record = jurisdictions.get(doc.get("jurisdiction"), {})
    name = ALIASES.get(record.get("name_en", doc.get("jurisdiction")), record.get("name_en", doc.get("jurisdiction")))
    if name == "United States":
        if state_jurisdictions:
            state = detect_us_state(doc)
            if state:
                return "United States · " + state
        return "United States · Federal"
    return name


# EUR-Lex serves one act at /oj and at /oj/{language}. Those are the same instrument.
EUR_LEX_LANG = {
    "bg", "cs", "da", "de", "el", "en", "eng", "es", "et", "fi", "fr", "fra",
    "ga", "hr", "hu", "it", "lt", "lv", "mt", "nl", "pl", "pt", "ro", "sk",
    "sl", "sv",
}


def canonical_url(url):
    raw = norm(url)
    if not raw:
        return ""
    parts = urlsplit(raw)
    if not parts.netloc:
        return raw.lower().rstrip("/")
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = (parts.path or "/").rstrip("/").lower() or "/"
    if host == "eur-lex.europa.eu":
        segments = [segment for segment in path.split("/") if segment]
        if len(segments) >= 2 and segments[-1] in EUR_LEX_LANG:
            path = "/" + "/".join(segments[:-1])
    pairs = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        if key.lower().startswith("utm_"):
            continue
        pairs.append((key.lower(), value.lower()))
    pairs.sort()
    query = "&".join(f"{key}={value}" for key, value in pairs)
    return host + path + (("?" + query) if query else "")


def bill_query_signature(url):
    """Bill id and session from legislature lookup query strings, not from the path."""
    raw = norm(url)
    if not raw:
        return None
    parts = urlsplit(raw)
    if not parts.netloc:
        return None
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    params = {key.lower(): value.lower() for key, value in parse_qsl(parts.query)}
    bill = params.get("bill") or params.get("billnumber") or ""
    bill_id = re.sub(r"[^a-z0-9]", "", bill)
    bill_id = re.sub(r"([a-z])0+(\d)", r"\1\2", bill_id)
    if len(bill_id) < 3:
        return None
    session = re.sub(r"[^a-z0-9]", "", params.get("legsess") or params.get("session") or "")
    return host, bill_id, session


def _add_identifier(found, token):
    token = token.lower()
    if len(token) >= 5:
        found.add(token)


def official_identifiers(text):
    """Specific instrument numbers from a title, official number, slug, or id.

    Predecessor-law aliases are not scanned. Colorado SB 26-189 cites SB 24-205
    in its alias list; that citation is a different act.
    """
    text = fold(text)
    found = set()
    for match in re.finditer(r"\b(\d{1,4}/\d{4}/[a-z0-9]{1,8}(?:-[a-z0-9]{1,8})?)\b", text):
        _add_identifier(found, match.group(1))
    for match in re.finditer(r"\b([hs]b)[\s-]*(\d{2})-(\d{1,5})\b", text):
        _add_identifier(found, f"{match.group(1)}{match.group(2)}-{match.group(3)}")
    for match in re.finditer(r"\b([hs])b-(\d{1,5})(?:-((?:19|20)\d{2}))?\b", text):
        _add_identifier(found, f"{match.group(1)}b{match.group(2)}")
    for match in re.finditer(r"\b([hs]b)(\d{1,5})\b", text):
        end = match.end()
        rest = text[end:]
        if rest.startswith("-") and re.match(r"(19|20)\d{2}\b", rest[1:]):
            _add_identifier(found, f"{match.group(1)}{match.group(2)}")
            continue
        if rest.startswith("-") and re.match(r"\d", rest[1:]):
            continue
        _add_identifier(found, f"{match.group(1)}{match.group(2)}")
    for match in re.finditer(
        r"\b([hs])[\s.-]*b[\s.-]*(?:no[\s.-]*)?(\d{1,5})\b(?![\s.-]*\d)",
        text,
    ):
        _add_identifier(found, f"{match.group(1)}b{match.group(2)}")
    for match in re.finditer(r"(?<![a-z0-9])([sa])\s*\.?\s*(\d{3,5})([a-z])?(?!\d)", text):
        number = int(match.group(2))
        if 1900 <= number <= 2099 and not match.group(3):
            continue
        _add_identifier(found, f"{match.group(1)}{match.group(2)}{match.group(3) or ''}")
    for match in re.finditer(
        r"\b(presidential decree|decreto|decree|act|law|loi)\b(?:\s+[a-z]+){0,4}\s*"
        r"(?:n[o.]|no|n)?\s*[°.]*\s*(\d{3,6}(?:\.\d{1,4})?|\d{1,3}\.\d{1,4})\b",
        text,
    ):
        kind = KIND_ALIASES[match.group(1)]
        _add_identifier(found, kind + match.group(2).replace(".", ""))
    return found


def catalog_identifier_text(doc):
    short = doc.get("short_title") if isinstance(doc.get("short_title"), dict) else {}
    parts = [
        doc.get("official_number"),
        doc.get("title_original"),
        doc.get("title_en"),
        short.get("en"),
        doc.get("slug"),
    ]
    return " ".join(norm(part) for part in parts if part)


def item_identifier_text(item):
    return " ".join(norm(item.get(key)) for key in ("title", "officialTitle", "id") if item.get(key))


def years_in(*values):
    found = set()
    for value in values:
        for match in re.findall(r"\b(?:19|20)\d{2}\b", str(value or "")):
            found.add(int(match))
    return found


def identifiers_conflict(catalog_ids, item_ids):
    """True when both sides name an instrument and the numbers do not overlap.

    A shared weak token such as law134 must not override a different
    134/2025/QH15 versus 134/2024/QH15 citation.
    """
    if not catalog_ids or not item_ids:
        return False
    catalog_slash = {token for token in catalog_ids if "/" in token}
    item_slash = {token for token in item_ids if "/" in token}
    if catalog_slash and item_slash and catalog_slash.isdisjoint(item_slash):
        return True
    return catalog_ids.isdisjoint(item_ids)


def years_compatible(doc, item):
    catalog_years = years_in(
        doc.get("date_adopted"), doc.get("date_in_force"), doc.get("slug"), doc.get("official_number"),
    )
    curated_years = years_in(
        item.get("publicationDate"), item.get("adoptedDate"), item.get("effectiveDate"),
        item.get("id"), item.get("title"),
    )
    if not catalog_years or not curated_years:
        return True
    return min(abs(left - right) for left in catalog_years for right in curated_years) <= 1


def enforcement_decree(text):
    raw = text or ""
    return "enforcement decree" in fold(raw) or "시행령" in raw


def script_key(text):
    return "".join(re.findall(r"[\uac00-\ud7a3\u4e00-\u9fff]", text or ""))


def original_title_match(doc, item):
    catalog_key = script_key(doc.get("title_original"))
    curated_text = (item.get("title") or "") + " " + (item.get("officialTitle") or "")
    curated_key = script_key(curated_text)
    if len(catalog_key) < 12 or len(curated_key) < 12 or catalog_key not in curated_key:
        return False
    if enforcement_decree(doc.get("title_original")) != enforcement_decree(curated_text):
        return False
    if len(catalog_key) / len(curated_key) < 0.72:
        return False
    return True


def title_parts(value):
    text = fold(value)
    text = text.replace("labelling", "labeling").replace("labelled", "labeled")
    text = text.replace("synthesised", "synthetic").replace("synthesized", "synthetic")
    text = re.sub(r"[^a-z0-9\uac00-\ud7a3\u4e00-\u9fff]+", " ", text)
    tokens = [token for token in text.split() if token not in TITLE_STOPWORDS and len(token) > 1]
    return "".join(tokens), tokens


def title_score(left, right):
    if enforcement_decree(left) != enforcement_decree(right):
        return 0.0, 0
    compact_left, tokens_left = title_parts(left)
    compact_right, tokens_right = title_parts(right)
    if len(compact_left) < 8 or len(compact_right) < 8:
        return 0.0, 0
    ratio = SequenceMatcher(None, compact_left, compact_right).ratio()
    return ratio, len(set(tokens_left) & set(tokens_right))


def latin_pieces(text):
    pieces = []
    for match in re.findall(r"\(([^)]*[A-Za-z]{4,}[^)]*)\)", text or ""):
        pieces.append(match)
    return pieces


def candidate_titles(doc, fresh):
    short = doc.get("short_title") if isinstance(doc.get("short_title"), dict) else {}
    values = [
        short.get("en"), doc.get("title_en"), doc.get("title_original"),
        fresh.get("title"), fresh.get("officialTitle"),
    ]
    seen = []
    for value in values:
        text = norm(value)
        if text and text not in seen:
            seen.append(text)
    return seen


def best_title_score(doc, fresh, item):
    rights = []
    for key in ("title", "officialTitle"):
        text = norm(item.get(key))
        if not text:
            continue
        rights.append(text)
        for piece in latin_pieces(text):
            if piece not in rights:
                rights.append(piece)
    best_ratio = 0.0
    best_shared = 0
    for left in candidate_titles(doc, fresh):
        for right in rights:
            ratio, shared = title_score(left, right)
            if ratio > best_ratio:
                best_ratio, best_shared = ratio, shared
    return best_ratio, best_shared


class CuratedIndex:
    def __init__(self, items, use_overrides=True):
        self.use_overrides = use_overrides
        self.items = [item for item in items if is_curated(item)]
        self.by_id = {item["id"]: item for item in self.items if item.get("id")}
        self.by_url = {}
        self.by_identifier = {}
        self.by_jurisdiction = {}
        for item in self.items:
            url = canonical_url(item.get("sourceUrl"))
            if url:
                self.by_url.setdefault(url, []).append(item)
            jurisdiction = item.get("jurisdiction") or ""
            self.by_jurisdiction.setdefault(jurisdiction, []).append(item)
            for token in official_identifiers(item_identifier_text(item)):
                self.by_identifier.setdefault((jurisdiction, token), []).append(item)

    def match(self, doc, fresh):
        jurisdiction = fresh.get("jurisdiction") or ""
        best = None

        def consider(score, item, reason):
            nonlocal best
            if not item or not item.get("id"):
                return
            candidate = (score, item["id"], reason)
            if best is None or candidate[0] > best[0] or (candidate[0] == best[0] and candidate[1] < best[1]):
                best = candidate

        url = canonical_url(doc.get("source_url"))
        for item in self.by_url.get(url, []):
            consider(100, item, "normalized source URL")

        signature = bill_query_signature(doc.get("source_url"))
        if signature:
            for item in self.by_jurisdiction.get(jurisdiction, []):
                other = bill_query_signature(item.get("sourceUrl"))
                if not other or other[0] != signature[0] or other[1] != signature[1]:
                    continue
                if signature[2] and other[2] and signature[2] != other[2]:
                    continue
                consider(92, item, "same legislature bill URL")

        catalog_ids = official_identifiers(catalog_identifier_text(doc))
        seen = set()
        for token in sorted(catalog_ids):
            for item in self.by_identifier.get((jurisdiction, token), []):
                if item["id"] in seen or not years_compatible(doc, item):
                    continue
                item_ids = official_identifiers(item_identifier_text(item))
                if identifiers_conflict(catalog_ids, item_ids):
                    continue
                seen.add(item["id"])
                shared = ", ".join(sorted(catalog_ids & item_ids))
                consider(84, item, "official identifier " + shared)

        for item in self.by_jurisdiction.get(jurisdiction, []):
            if not years_compatible(doc, item):
                continue
            item_ids = official_identifiers(item_identifier_text(item))
            if identifiers_conflict(catalog_ids, item_ids):
                continue
            if original_title_match(doc, item):
                consider(88, item, "original-language title")
            ratio, shared = best_title_score(doc, fresh, item)
            if ratio >= 0.98 or (ratio >= 0.92 and shared >= 4):
                consider(70 + ratio, item, f"normalized title {ratio:.2f}")

        override_id = CURATED_DUPLICATE_OVERRIDES.get(doc.get("slug")) if self.use_overrides else None
        if override_id and override_id in self.by_id and (best is None or best[1] != override_id):
            return {"id": override_id, "reason": "curated override", "item": self.by_id[override_id]}
        if best is None:
            return None
        return {"id": best[1], "reason": best[2], "item": self.by_id.get(best[1])}


def legacy_duplicate(doc, fresh, source_urls, title_index, base):
    url = norm(doc.get("source_url"))
    if url and url in source_urls:
        return "source URL already in the register"
    key = title_key(fresh.get("title"))
    for other in title_index.get(base, []):
        if other and SequenceMatcher(None, key, other).ratio() >= 0.86:
            return "title similarity >= 0.86"
    return ""


def effective_date(doc):
    for event in doc.get("key_dates", []) or []:
        label = (event.get("label") or {}).get("en", "")
        if EFFECTIVE_RE.search(label):
            return event.get("date") or ""
    return ""


def make_item(doc, jurisdiction, catalog_date, today):
    summary = doc.get("summary", {})
    topics = doc.get("topics", [])
    english_title = (doc.get("short_title") or {}).get("en")
    title = english_title or doc.get("title_original") or doc["slug"]
    return {
        "id": generated_id(doc.get("slug")),
        "jurisdiction": jurisdiction,
        "regulator": norm(doc.get("issuing_body")) or "Issuing authority",
        "title": norm(title),
        "officialTitle": norm(doc.get("title_original")),
        "titleTranslationSource": ("Cybersecurity Database English short title" if english_title else ""),
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


def make_standard(record, today):
    summary = record.get("summary", {})
    kind = record.get("kind", "standard").replace("_", " ").title()
    sectors = record.get("sectors", [])
    status = STANDARD_STATUS.get(record.get("status"), "Published standard")
    return {
        "id": "CYBERSTANDARD-" + re.sub(r"[^A-Za-z0-9_-]", "-", record["slug"]).upper(),
        "jurisdiction": "Cross-country standards reference",
        "showInCountryFilters": True,
        "scopeNote": "Reference surfaced alongside country results for research; this does not establish local adoption, applicability, or legal force.",
        "regulator": ", ".join(record.get("bodies", [])) or "Standards body",
        "title": norm(record.get("title") or record.get("reference") or record["slug"]),
        "officialTitle": norm(record.get("reference")),
        "instrumentType": kind,
        "status": status,
        "publicationDate": record.get("date_published") or "",
        "adoptedDate": "",
        "effectiveDate": "",
        "topic": "Cybersecurity standard · " + " · ".join(s.replace("-", " ") for s in sectors),
        "sourceUrl": record.get("catalog_url"),
        "catalogEntryUrl": record.get("url"),
        "summary": norm(summary.get("en") if isinstance(summary, dict) else summary)[:1800],
        "access": record.get("access"),
        "standardEdition": record.get("edition") or "",
        "history": [{
            "date": today,
            "change": "Added from the Cybersecurity Database standards catalog (CC BY 4.0); the linked standards-body catalog is the source reference.",
        }],
        "catalogSource": "Cybersecurity Database standards",
        "catalogRecordId": record.get("id"),
        "catalogSlug": record.get("slug"),
        "catalogUpdatedAt": record.get("updated_at", today),
    }


def materially_update(old, fresh, today):
    fields = LOGIC_FIELDS
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


def lookup_tables(items):
    source_urls = {norm(item.get("sourceUrl")) for item in items if item.get("sourceUrl")}
    title_index = {}
    for item in items:
        base = (item.get("jurisdiction") or "").split(" · ")[0]
        title_index.setdefault(base, []).append(title_key(item.get("title")))
    return source_urls, title_index


def prepare_document(doc, jurisdictions, country_labels, state_jurisdictions, catalog_date, today):
    if doc.get("document_type") not in LEGAL_TYPES:
        return None
    meta = jurisdictions.get(doc.get("jurisdiction"), {})
    if meta.get("type") not in {"paese", "territorio", "organizzazione_regionale"}:
        return None
    if not doc.get("source_url"):
        return None
    jurisdiction = jurisdiction_for(doc, jurisdictions, state_jurisdictions=state_jurisdictions)
    base = jurisdiction.split(" · ")[0]
    if meta.get("type") != "organizzazione_regionale" and base not in country_labels:
        return None
    fresh = make_item(doc, jurisdiction, catalog_date, today)
    return {"base": base, "fresh": fresh, "jurisdiction": jurisdiction}


def creation_outcome(doc, items, jurisdictions, country_labels, today, *, state_jurisdictions, strong_dedupe, use_overrides=True):
    """How this catalog document would be created if its generated id were absent."""
    prepared = prepare_document(
        doc, jurisdictions, country_labels, state_jurisdictions,
        doc.get("updated_at") or today, today,
    )
    if prepared is None:
        return {"slug": doc.get("slug"), "outcome": "out of scope", "jurisdiction": "", "matched_id": "", "reason": ""}
    fresh = prepared["fresh"]
    others = [item for item in items if item.get("id") != fresh["id"]]
    source_urls, title_index = lookup_tables(others)
    reason = legacy_duplicate(doc, fresh, source_urls, title_index, prepared["base"])
    matched_id = ""
    if not reason and strong_dedupe:
        match = CuratedIndex(others, use_overrides=use_overrides).match(doc, fresh)
        if match:
            reason = match["reason"]
            matched_id = match["id"]
    outcome = "skip" if reason else "add"
    return {
        "slug": doc.get("slug"),
        "id": fresh["id"],
        "outcome": outcome,
        "jurisdiction": fresh["jurisdiction"],
        "matched_id": matched_id,
        "reason": reason,
    }


def outcome_text(decision):
    if decision["outcome"] == "out of scope":
        return "out of scope"
    if decision["outcome"] == "skip":
        target = decision["matched_id"] or "an existing register record"
        via = decision["reason"] or "duplicate"
        return f"skip — duplicate of {target} ({via}); jurisdiction label {decision['jurisdiction']}"
    return "add — jurisdiction " + decision["jurisdiction"]


def apply_ingest(data, documents_payload, jurisdiction_payload, standards_payload, today, *, state_jurisdictions=True, strong_dedupe=True):
    """Update data in memory. Does not write data.json and does not delete rows."""
    jurisdictions = {row["code"]: row for row in jurisdiction_payload.get("jurisdictions", [])}
    country_labels = {(item.get("jurisdiction") or "").split(" · ")[0] for item in data.get("items", [])}
    by_id = {item["id"]: item for item in data.get("items", [])}
    source_urls, title_index = lookup_tables(data.get("items", []))
    curated_index = CuratedIndex(data.get("items", [])) if strong_dedupe else None
    catalog_date = documents_payload.get("updated_at", today)
    added = updated = skipped_scope = skipped_duplicate = 0
    decisions = []

    for doc in documents_payload.get("documents", []):
        if doc.get("document_type") not in LEGAL_TYPES:
            continue
        prepared = prepare_document(doc, jurisdictions, country_labels, state_jurisdictions, catalog_date, today)
        if prepared is None:
            skipped_scope += 1
            continue
        fresh = prepared["fresh"]
        ident = fresh["id"]
        matched = curated_index.match(doc, fresh) if curated_index else None
        old = by_id.get(ident)
        if old:
            if (old.get("titleTranslationSource") or "").startswith("Manual English translation"):
                fresh["title"] = old.get("title", fresh["title"])
                fresh["officialTitle"] = old.get("officialTitle") or fresh.get("officialTitle")
                fresh["titleTranslationSource"] = old["titleTranslationSource"]
            changed = materially_update(old, fresh, today)
            if changed:
                updated += 1
            decisions.append({
                "slug": doc.get("slug"), "id": ident, "outcome": "update",
                "jurisdiction": fresh["jurisdiction"],
                "matched_id": matched["id"] if matched else "",
                "reason": matched["reason"] if matched else "",
                "changed": changed,
            })
            continue
        legacy_reason = legacy_duplicate(doc, fresh, source_urls, title_index, prepared["base"])
        if legacy_reason or matched:
            skipped_duplicate += 1
            decisions.append({
                "slug": doc.get("slug"), "id": ident, "outcome": "skip",
                "jurisdiction": fresh["jurisdiction"],
                "matched_id": matched["id"] if matched else "",
                "reason": (matched["reason"] if matched else legacy_reason),
                "changed": False,
            })
            continue
        by_id[ident] = fresh
        source_urls.add(norm(fresh["sourceUrl"]))
        title_index.setdefault(prepared["base"], []).append(title_key(fresh["title"]))
        added += 1
        decisions.append({
            "slug": doc.get("slug"), "id": ident, "outcome": "add",
            "jurisdiction": fresh["jurisdiction"], "matched_id": "", "reason": "", "changed": True,
        })

    standards_added = standards_updated = standards_skipped = 0
    for record in standards_payload.get("standards", []):
        if not record.get("catalog_url"):
            standards_skipped += 1
            continue
        fresh = make_standard(record, today)
        old = by_id.get(fresh["id"])
        if old:
            if materially_update(old, fresh, today):
                standards_updated += 1
            continue
        if norm(fresh["sourceUrl"]) in source_urls:
            standards_skipped += 1
            continue
        by_id[fresh["id"]] = fresh
        source_urls.add(norm(fresh["sourceUrl"]))
        standards_added += 1

    data["items"] = sorted(
        by_id.values(),
        key=lambda item: (item.get("publicationDate") or item.get("adoptedDate") or "", item["id"]),
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
        "standardsApiUrl": API + "standards.json",
        "standardsCount": standards_payload.get("count", len(standards_payload.get("standards", []))),
        "standardsUpdatedAt": standards_payload.get("updated_at", documents_payload.get("updated_at", today)),
    }
    return {
        "added": added,
        "updated": updated,
        "skipped_duplicate": skipped_duplicate,
        "skipped_scope": skipped_scope,
        "standards_added": standards_added,
        "standards_updated": standards_updated,
        "standards_skipped": standards_skipped,
        "decisions": decisions,
        "items": data["items"],
    }


def copy_data(data):
    return json.loads(json.dumps(data))


def logic_diff(original_items, legacy_items, new_items):
    legacy = {item["id"]: item for item in legacy_items}
    updated = {item["id"]: item for item in new_items}
    original = {item["id"]: item for item in original_items}
    jurisdiction_changes = []
    unexpected = []
    removed = []
    for ident, before in original.items():
        if ident not in updated:
            removed.append(ident)
            continue
        if ident not in legacy:
            continue
        fields = [key for key in LOGIC_FIELDS if legacy[ident].get(key, "") != updated[ident].get(key, "")]
        if not fields:
            continue
        old_label = legacy[ident].get("jurisdiction", "")
        new_label = updated[ident].get("jurisdiction", "")
        if fields == ["jurisdiction"] and old_label == "United States · Federal" and new_label.startswith("United States · ") and new_label != old_label:
            jurisdiction_changes.append({
                "id": ident,
                "before": before.get("jurisdiction", ""),
                "legacy": old_label,
                "after": new_label,
            })
        else:
            unexpected.append({"id": ident, "fields": fields})
    legacy_added = sorted(set(legacy) - set(original))
    new_added = sorted(set(updated) - set(original))
    return {
        "jurisdiction_changes": jurisdiction_changes,
        "unexpected": unexpected,
        "removed": sorted(removed),
        "skipped_by_new_logic": sorted(set(legacy_added) - set(new_added)),
        "added_only_by_new_logic": sorted(set(new_added) - set(legacy_added)),
    }


def dry_run_report(data, documents_payload, jurisdiction_payload, standards_payload, today):
    jurisdictions = {row["code"]: row for row in jurisdiction_payload.get("jurisdictions", [])}
    country_labels = {(item.get("jurisdiction") or "").split(" · ")[0] for item in data.get("items", [])}
    documents = {doc.get("slug"): doc for doc in documents_payload.get("documents", [])}
    lines = ["DRY RUN — data.json is not written", ""]
    lines.append("Creation outcome if the catalog id were not already in the register")
    lines.append("record | before (previous ingest logic) | after (this ingest logic)")
    for slug in WATCHED_SLUGS:
        doc = documents.get(slug)
        ident = generated_id(slug)
        if doc is None:
            lines.append(f"{ident} | catalog document not in this snapshot | catalog document not in this snapshot")
            continue
        before = creation_outcome(
            doc, data["items"], jurisdictions, country_labels, today,
            state_jurisdictions=False, strong_dedupe=False,
        )
        after = creation_outcome(
            doc, data["items"], jurisdictions, country_labels, today,
            state_jurisdictions=True, strong_dedupe=True,
        )
        lines.append(f"{ident} | {outcome_text(before)} | {outcome_text(after)}")

    legacy_data = copy_data(data)
    new_data = copy_data(data)
    apply_ingest(legacy_data, documents_payload, jurisdiction_payload, standards_payload, today, state_jurisdictions=False, strong_dedupe=False)
    new_stats = apply_ingest(new_data, documents_payload, jurisdiction_payload, standards_payload, today, state_jurisdictions=True, strong_dedupe=True)
    diff = logic_diff(data["items"], legacy_data["items"], new_data["items"])
    lines.append("")
    lines.append("Existing rows on the next ingest (new logic keeps the row; it does not delete it)")
    lines.append("record | jurisdiction now | jurisdiction after next ingest | removed")
    new_by_id = {item["id"]: item for item in new_data["items"]}
    original_by_id = {item["id"]: item for item in data["items"]}
    for slug in WATCHED_SLUGS:
        ident = generated_id(slug)
        current = original_by_id.get(ident)
        nxt = new_by_id.get(ident)
        if current and nxt:
            lines.append(f"{ident} | {current.get('jurisdiction', '')} | {nxt.get('jurisdiction', '')} | no")
        elif current and not nxt:
            lines.append(f"{ident} | {current.get('jurisdiction', '')} | (absent) | yes")
        elif nxt:
            lines.append(f"{ident} | (not in the register) | {nxt.get('jurisdiction', '')} | no — would be added")
        else:
            decision = next((row for row in new_stats["decisions"] if row["slug"] == slug), None)
            detail = outcome_text({
                "outcome": decision["outcome"] if decision else "skip",
                "matched_id": decision["matched_id"] if decision else "",
                "reason": decision["reason"] if decision else "",
                "jurisdiction": decision["jurisdiction"] if decision else "",
            }) if decision else "not added"
            lines.append(f"{ident} | (not in the register) | not added | no — {detail}")

    lines.append("")
    lines.append("Logic diff versus the previous ingest on the same catalog snapshot")
    lines.append(f"existing records removed: {len(diff['removed'])}")
    lines.append(f"existing records with unexpected field changes: {len(diff['unexpected'])}")
    lines.append(f"existing records with jurisdiction-only corrections: {len(diff['jurisdiction_changes'])}")
    for row in diff["jurisdiction_changes"]:
        lines.append(f"  {row['id']}: {row['legacy']} -> {row['after']}")
    lines.append(f"catalog ids the previous logic would add and this logic skips: {len(diff['skipped_by_new_logic'])}")
    for ident in diff["skipped_by_new_logic"]:
        lines.append(f"  {ident}")
    lines.append(f"catalog ids only this logic would add: {len(diff['added_only_by_new_logic'])}")
    for ident in diff["added_only_by_new_logic"]:
        lines.append(f"  {ident}")
    if diff["unexpected"]:
        lines.append("unexpected field diffs:")
        for row in diff["unexpected"]:
            lines.append(f"  {row['id']}: {', '.join(row['fields'])}")

    original = {item["id"]: item for item in data["items"]}
    produced = {item["id"]: item for item in new_data["items"]}
    previous = {item["id"]: item for item in legacy_data["items"]}
    changed_existing = []
    for ident, item in original.items():
        if ident not in produced:
            continue
        fields = [key for key in LOGIC_FIELDS if item.get(key, "") != produced[ident].get(key, "")]
        if fields:
            changed_existing.append((ident, fields))
    both_add = sorted((set(produced) & set(previous)) - set(original))
    lines.append("")
    lines.append("Compared with the current register file")
    lines.append(f"existing records whose stored logic fields would change on the next ingest: {len(changed_existing)}")
    for ident, fields in changed_existing:
        if fields == ["jurisdiction"]:
            lines.append(f"  {ident}: jurisdiction -> {produced[ident].get('jurisdiction', '')}")
        else:
            lines.append(f"  {ident}: {', '.join(fields)}")
    lines.append(f"existing records removed: {len(set(original) - set(produced))}")
    lines.append(f"catalog records both the previous and the new logic would add: {len(both_add)}")
    for ident in both_add:
        same = previous[ident].get("jurisdiction") == produced[ident].get("jurisdiction")
        note = "same jurisdiction as the previous logic" if same else "jurisdiction differs from the previous logic"
        lines.append(f"  {ident}: {produced[ident].get('jurisdiction')} ({note})")
    return "\n".join(lines) + "\n", diff


def load_payloads():
    return fetch("documents.json"), fetch("jurisdictions.json"), fetch("standards.json")


def main(argv=None, data_path=None):
    args = list(sys.argv[1:] if argv is None else argv)
    dry_run = False
    for arg in args:
        if arg == "--dry-run":
            dry_run = True
        else:
            raise SystemExit(f"Unknown argument: {arg}")
    path = Path(data_path) if data_path else DATA
    data = json.loads(path.read_text())
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        documents_payload, jurisdiction_payload, standards_payload = load_payloads()
    except Exception as exc:
        print(f"Cybersecurity catalog unavailable; preserving existing records: {exc}")
        return 0
    if dry_run:
        report, _diff = dry_run_report(data, documents_payload, jurisdiction_payload, standards_payload, today)
        print(report, end="")
        return 0
    stats = apply_ingest(data, documents_payload, jurisdiction_payload, standards_payload, today)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(
        f"Cybersecurity catalog {documents_payload.get('updated_at', 'unknown')}: "
        f"added {stats['added']}, updated {stats['updated']}, skipped {stats['skipped_duplicate']} duplicates, "
        f"skipped {stats['skipped_scope']} out-of-scope records; standards added {stats['standards_added']}, "
        f"updated {stats['standards_updated']}, skipped {stats['standards_skipped']}; {len(data['items'])} total dashboard records."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
