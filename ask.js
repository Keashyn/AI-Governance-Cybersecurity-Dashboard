/* Client-side register questions.
   Answers are assembled only from data.json records. Nothing here calls a
   model, API, or other service, and nothing is added that is not on a record. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.RegisterAsk = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const SHOW = 6;
  const DISCLAIMER = "This is informational, not legal advice. Titles, statuses, dates, jurisdictions, and summaries are shown only as recorded in this register. They are not a determination of legal obligations. Verify current law with the issuing authority. An absent record is not proof that no law applies, and this register is not an exhaustive catalog.";

  const STATUS_ORDER = ["In force", "Enacted", "Proposed", "Consultation", "Adopted policy", "Guidance", "Published standard", "In development", "Withdrawn standard", "Lapsed", "Withdrawn", "Superseded", "Repealed", "Expired", "Reviewed"];

  const HARD_STATUS_PHRASES = [
    ["not yet in force", "not-in-force"],
    ["not in force", "not-in-force"],
    ["in force", "in-force"],
    ["into force", "in-force"],
    ["in effect", "in-force"],
    ["formally adopted", "enacted"],
    ["adopted policies", "policy"],
    ["adopted policy", "policy"],
    ["technical specifications", "standards"],
    ["technical specification", "standards"],
    ["published standard", "standards"],
    ["consultations", "consultation"],
    ["consultation", "consultation"],
    ["proposals", "proposed"],
    ["proposal", "proposed"],
    ["proposed", "proposed"],
    ["draft laws", "proposed"],
    ["draft law", "proposed"],
    ["enacted", "enacted"],
    ["repealed", "repealed"],
    ["expired", "expired"],
    ["superseded", "superseded"],
    ["withdrawn", "withdrawn"],
    ["lapsed", "lapsed"]
  ];
  const SOFT_STATUS_PHRASES = [
    ["national strategies", "policy"],
    ["national strategy", "policy"],
    ["action plan", "policy"],
    ["strategies", "policy"],
    ["strategy", "policy"],
    ["frameworks", "standards"],
    ["framework", "standards"],
    ["standards", "standards"],
    ["standard", "standards"],
    ["guidelines", "guidance"],
    ["guideline", "guidance"],
    ["guidance", "guidance"],
    ["drafts", "proposed"],
    ["draft", "proposed"],
    ["bills", "proposed"],
    ["bill", "proposed"],
    ["policies", "policy"],
    ["policy", "policy"]
  ];
  const STATUS_PHRASES = HARD_STATUS_PHRASES.concat(SOFT_STATUS_PHRASES);

  const TOPIC_PHRASES = [
    ["artificial intelligence", "ai"],
    ["machine learning", "ai"],
    ["cyber security", "cyber"],
    ["cybersecurity", "cyber"],
    ["cyber crime", "cyber"],
    ["cybercrime", "cyber"],
    ["information security", "cyber"],
    ["data protection", "privacy"],
    ["personal information", "privacy"],
    ["personal data", "privacy"],
    ["privacy", "privacy"]
  ];

  const STATUS_SET = {
    "in-force": ["In force"],
    enacted: ["Enacted"],
    proposed: ["Proposed"],
    consultation: ["Consultation"],
    policy: ["Adopted policy"],
    guidance: ["Guidance"],
    standards: ["Published standard", "In development", "Withdrawn standard"],
    repealed: ["Repealed"],
    expired: ["Expired"],
    superseded: ["Superseded"],
    withdrawn: ["Withdrawn", "Withdrawn standard"],
    lapsed: ["Lapsed"],
    "not-in-force": ["Enacted", "Proposed", "Consultation", "Adopted policy", "Guidance", "Lapsed", "Withdrawn", "Superseded", "Repealed", "Expired"]
  };

  const NON_LAW = new Set(["Guidance", "Adopted policy", "Reviewed", "Published standard", "In development", "Withdrawn standard"]);

  const STOP = new Set(("a an the of in on for to and or about into from with without within by at as is are was were be been being do does did has have had what which who whom whose when where why how tell me please show list find give explain describe summarize summary status current official source sources there any some these those this that your our their not no yes record records register dashboard tracker instrument instruments law laws legislation statute statutes regulation regulations rule rules legal").split(/\s+/));

  const EXTRAS = [
    { phrases: ["european union", "eu"], label: "European Union", test: (j) => j === "European Union" },
    { phrases: ["united kingdom", "uk", "u k", "great britain", "britain"], label: "United Kingdom", test: (j) => j === "United Kingdom" },
    { phrases: ["united states of america", "united states", "usa", "u s a", "u s", "us"], label: "United States", broad: true, test: (j) => j === "United States" || j.startsWith("United States ·") },
    { phrases: ["united states federal", "us federal", "u s federal"], label: "United States · Federal", test: (j) => j === "United States · Federal" },
    { phrases: ["prc", "peoples republic of china"], label: "China", test: (j) => j === "China" },
    { phrases: ["south korea", "republic of korea", "rok"], label: "South Korea", test: (j) => j === "South Korea" },
    { phrases: ["north korea", "dprk"], label: "North Korea", test: (j) => j === "North Korea" },
    { phrases: ["korea"], label: "South Korea", assumption: "“Korea” is read as South Korea. North Korea is a separate jurisdiction in this register.", test: (j) => j === "South Korea" },
    { phrases: ["czech republic"], label: "Czechia", test: (j) => j === "Czechia" },
    { phrases: ["turkey", "turkiye"], label: "Türkiye", test: (j) => j === "Türkiye" },
    { phrases: ["uae", "u a e"], label: "United Arab Emirates", test: (j) => j === "United Arab Emirates" },
    { phrases: ["ivory coast", "cote divoire"], label: "Côte d’Ivoire", test: (j) => normalize(j).includes("ivoire") },
    { phrases: ["viet nam"], label: "Vietnam", test: (j) => j === "Vietnam" },
    { phrases: ["russian federation"], label: "Russia", test: (j) => j === "Russia" },
    { phrases: ["cape verde"], label: "Cabo Verde", test: (j) => j === "Cabo Verde" },
    { phrases: ["swaziland"], label: "Eswatini", test: (j) => j === "Eswatini" },
    { phrases: ["burma"], label: "Myanmar", test: (j) => j === "Myanmar" },
    { phrases: ["bahamas"], label: "The Bahamas", test: (j) => j === "The Bahamas" },
    { phrases: ["gambia"], label: "The Gambia", test: (j) => j === "The Gambia" },
    { phrases: ["dr congo", "drc"], label: "Democratic Republic of the Congo", test: (j) => j === "Democratic Republic of the Congo" },
    { phrases: ["republic of the congo"], label: "Congo (Republic of the)", test: (j) => j === "Congo (Republic of the)" },
    { phrases: ["new york city", "nyc"], label: "United States · New York City", test: (j) => j === "United States · New York City" },
    { phrases: ["holy see"], label: "Vatican City", test: (j) => j.startsWith("Vatican") },
    { phrases: ["japanese"], label: "Japan", test: (j) => j === "Japan" },
    { phrases: ["german"], label: "Germany", test: (j) => j === "Germany" },
    { phrases: ["french"], label: "France", test: (j) => j === "France" },
    { phrases: ["italian"], label: "Italy", test: (j) => j === "Italy" },
    { phrases: ["spanish"], label: "Spain", test: (j) => j === "Spain" },
    { phrases: ["chinese"], label: "China", test: (j) => j === "China" },
    { phrases: ["canadian"], label: "Canada", test: (j) => j === "Canada" },
    { phrases: ["australian"], label: "Australia", test: (j) => j === "Australia" },
    { phrases: ["indian"], label: "India", test: (j) => j === "India" },
    { phrases: ["brazilian"], label: "Brazil", test: (j) => j === "Brazil" },
    { phrases: ["mexican"], label: "Mexico", broad: true, test: (j) => j === "Mexico" || j.startsWith("Mexico ·") },
    { phrases: ["korean"], label: "South Korea", assumption: "“Korean” is read as South Korea. North Korea is a separate jurisdiction in this register.", test: (j) => j === "South Korea" },
    { phrases: ["british"], label: "United Kingdom", test: (j) => j === "United Kingdom" },
    { phrases: ["irish"], label: "Ireland", test: (j) => j === "Ireland" },
    { phrases: ["dutch"], label: "Netherlands", test: (j) => j === "Netherlands" },
    { phrases: ["swedish"], label: "Sweden", test: (j) => j === "Sweden" },
    { phrases: ["norwegian"], label: "Norway", test: (j) => j === "Norway" },
    { phrases: ["finnish"], label: "Finland", test: (j) => j === "Finland" },
    { phrases: ["danish"], label: "Denmark", test: (j) => j === "Denmark" },
    { phrases: ["swiss"], label: "Switzerland", test: (j) => j === "Switzerland" },
    { phrases: ["austrian"], label: "Austria", test: (j) => j === "Austria" },
    { phrases: ["belgian"], label: "Belgium", test: (j) => j === "Belgium" },
    { phrases: ["polish"], label: "Poland", test: (j) => j === "Poland" },
    { phrases: ["portuguese"], label: "Portugal", test: (j) => j === "Portugal" },
    { phrases: ["greek"], label: "Greece", test: (j) => j === "Greece" },
    { phrases: ["turkish"], label: "Türkiye", test: (j) => j === "Türkiye" },
    { phrases: ["vietnamese"], label: "Vietnam", test: (j) => j === "Vietnam" },
    { phrases: ["indonesian"], label: "Indonesia", test: (j) => j === "Indonesia" },
    { phrases: ["singaporean"], label: "Singapore", test: (j) => j === "Singapore" },
    { phrases: ["malaysian"], label: "Malaysia", test: (j) => j === "Malaysia" },
    { phrases: ["israeli"], label: "Israel", test: (j) => j === "Israel" },
    { phrases: ["egyptian"], label: "Egypt", test: (j) => j === "Egypt" },
    { phrases: ["nigerian"], label: "Nigeria", test: (j) => j === "Nigeria" },
    { phrases: ["kenyan"], label: "Kenya", test: (j) => j === "Kenya" },
    { phrases: ["emirati"], label: "United Arab Emirates", test: (j) => j === "United Arab Emirates" }
  ];

  function normalize(value) {
    return String(value || "")
      .replace(/[’‘]/g, "'")
      .replace(/[“”]/g, '"')
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/['’]s\b/g, "")
      .replace(/&/g, " and ")
      .replace(/\bdefence\b/g, "defense")
      .replace(/\blabour\b/g, "labor")
      .replace(/\./g, "")
      .replace(/['’]/g, "")
      .replace(/[^a-z0-9/+-]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function squash(value) {
    return normalize(value).replace(/[^a-z0-9]/g, "");
  }

  function escapeReg(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function hasPhrase(text, phrase) {
    return (" " + text + " ").includes(" " + phrase + " ");
  }

  function stripPhrase(text, phrase) {
    return (" " + text + " ").split(" " + phrase + " ").join(" ").replace(/\s+/g, " ").trim();
  }

  function isStandard(record) {
    return record.jurisdiction === "Cross-country standards reference"
      || record.catalogSource === "Cybersecurity Database standards"
      || ["Published standard", "In development", "Withdrawn standard"].includes(record.status);
  }

  function isApplicability(record) {
    return /applicability record/i.test(record.instrumentType || "") || /applies in/i.test(record.title || "");
  }

  function dateValue(value) {
    const text = String(value || "").trim();
    if (/^\d{4}(-\d{2}(-\d{2})?)?$/.test(text)) return text;
    return "";
  }

  function sortDate(record) {
    return dateValue(record.publicationDate) || dateValue(record.adoptedDate) || "";
  }

  function statusLabel(status) {
    if (status === "Enacted") return "Formally adopted (register status: Enacted)";
    return status || "Status not recorded";
  }

  function statusNote(status) {
    switch (status) {
      case "In force":
        return "Marked in force in this register, which means effective at least in part. This is the register’s label, not a fresh legal determination.";
      case "Enacted":
        return "Marked Enacted. The dashboard calls that “Formally adopted”. It is not the same label as In force.";
      case "Proposed":
        return "A proposal or draft in this register, not an instrument marked in force.";
      case "Consultation":
        return "A consultation, not enacted law.";
      case "Adopted policy":
        return "Approved policy or strategy. Not a statute.";
      case "Guidance":
        return "Official guidance. Not represented here as binding legislation.";
      case "Published standard":
      case "In development":
      case "Withdrawn standard":
        return "A standard, framework, or technical specification. Reference material, not law. Listing it does not mean any country has adopted it or given it legal force.";
      case "Reviewed":
        return "A coverage-review note, not a law. It is not proof that no law applies.";
      case "Lapsed":
      case "Withdrawn":
        return "An inactive proposal in this register, not an in-force law.";
      case "Superseded":
      case "Repealed":
      case "Expired":
        return "Not marked current in this register.";
      default:
        return "Shown only with the status recorded on the entry.";
    }
  }

  function cardCaution(record) {
    if (isApplicability(record)) return "Applicability record: the entry says an EU instrument applies in this jurisdiction. It is not a separate national statute.";
    if (isStandard(record)) return record.scopeNote || "Reference material, not law. This does not establish local adoption or legal force.";
    if (record.status === "Reviewed") return "Coverage review, not a law. A review that did not identify an instrument is not proof that no law applies.";
    if (/^(In force|Enacted)$/.test(record.status || "") && /policy|strategy|program|action plan|guidance|framework/i.test(record.instrumentType || "")) {
      return "Instrument type is “" + record.instrumentType + "”. The register status is " + record.status + ". This page does not reclassify it as a statute.";
    }
    if (record.titleTranslationSource && record.officialTitle && record.officialTitle !== record.title) {
      return "The English title is the translation recorded on this entry. The official title is listed below. The linked source controls.";
    }
    return "";
  }

  function buildRules(items) {
    const names = [...new Set(items.map((item) => item.jurisdiction).filter(Boolean))];
    const nameSet = new Set(names);
    const rules = [];
    function add(spec) {
      for (const phrase of spec.phrases) {
        const normalized = normalize(phrase);
        if (normalized.length < 2) continue;
        rules.push({
          phrase: normalized,
          test: spec.test,
          label: spec.label,
          broad: !!spec.broad,
          assumption: spec.assumption || ""
        });
      }
    }
    for (const name of names) {
      const children = names.filter((other) => other.startsWith(name + " · "));
      if (children.length && !name.includes(" · ")) {
        add({ phrases: [name], label: name, broad: true, test: (jurisdiction) => jurisdiction === name || jurisdiction.startsWith(name + " · ") });
      } else {
        add({ phrases: [name], label: name, test: (jurisdiction) => jurisdiction === name });
      }
      if (name.includes(" · ")) {
        const child = name.split(" · ").slice(1).join(" · ");
        const childNorm = normalize(child);
        const generic = ["federal", "national", "state"].includes(childNorm);
        const collides = names.some((other) => !other.includes(" · ") && normalize(other) === childNorm);
        if (!generic && !collides && childNorm.length > 2) add({ phrases: [child, name.replace(" · ", " ")], label: name, test: (jurisdiction) => jurisdiction === name });
      }
    }
    for (const extra of EXTRAS) {
      const sample = names.find(extra.test);
      if (sample || extra.test("European Union") || extra.test("United States · Federal")) add(extra);
    }
    // Drop extras whose target is absent.
    return rules.filter((rule) => names.some(rule.test) || [...nameSet].some(rule.test));
  }

  function findPhrases(text, phrases) {
    const found = [];
    let rest = text;
    const ordered = phrases.slice().sort((a, b) => b[0].length - a[0].length);
    for (const entry of ordered) {
      const phrase = normalize(entry[0]);
      if (phrase && hasPhrase(rest, phrase)) {
        found.push(entry[1]);
        rest = stripPhrase(rest, phrase);
      }
    }
    return { found: [...new Set(found)], rest };
  }

  function findJurisdictions(text, rules) {
    const grouped = new Map();
    for (const rule of rules) {
      if (!grouped.has(rule.phrase)) grouped.set(rule.phrase, []);
      grouped.get(rule.phrase).push(rule);
    }
    const phrases = [...grouped.keys()].sort((a, b) => b.length - a.length);
    const matches = [];
    let rest = text;
    for (const phrase of phrases) {
      if (!hasPhrase(rest, phrase)) continue;
      matches.push(...grouped.get(phrase));
      rest = stripPhrase(rest, phrase);
    }
    return { matches, rest };
  }

  function extractCodes(text) {
    const codes = new Set();
    const patterns = [
      /\b\d{4}\/\d{2,5}\b/g,
      /\biso\s*\/?\s*iec\s*\d{4,5}\b/g,
      /\biso\s*\d{4,5}\b/g,
      /\biec\s*\d{4,5}\b/g,
      /\b[a-z]{1,4}\s*-?\s*\d{1,4}(?:\s*-\s*\d{1,4})+\b/g,
      /\b[a-z]\s*-\s*\d{1,3}\b/g,
      /\bnis\s*2\b/g,
      /\beidas\s*2\b/g
    ];
    for (const pattern of patterns) {
      for (const match of text.match(pattern) || []) codes.add(match.replace(/\s+/g, ""));
    }
    return [...codes];
  }

  function keywordsFrom(text, codes) {
    const raw = text.split(" ").filter(Boolean);
    const keywords = [];
    for (let i = 0; i < raw.length; i++) {
      const token = raw[i];
      if (STOP.has(token)) continue;
      if (/^\d{1,2}$/.test(token) && keywords.length) {
        codes.push(keywords[keywords.length - 1] + token);
        continue;
      }
      if (/^\d+$/.test(token) && token.length < 4) continue;
      keywords.push(token);
    }
    const codeSquash = new Set(codes.map(squash));
    return keywords.filter((token) => !codeSquash.has(squash(token)) || /[a-z]/.test(token));
  }

  function parse(question, items) {
    const original = String(question || "").trim();
    const normalized = normalize(original);
    const listCue = /\b(which|what are|what laws|list|show me|how many|are there any|laws in|legislation in|records for|records in)\b/.test(normalized);
    const nameCue = /\b(status of|what is the status|what is|whats|is the|is there|about the|tell me about|describe the|does the)\b/.test(normalized);
    const keepNameWords = nameCue && !listCue;
    let text = normalized.replace(/\b(tell|show|give|help|ask|let|inform)\s+us\b/g, "$1");
    const quoted = [...original.matchAll(/["“]([^"”]{3,})["”]/g)].map((match) => normalize(match[1])).filter(Boolean);
    const rules = buildRules(items || []);
    const jurisdictions = findJurisdictions(text, rules);
    text = jurisdictions.rest;
    const statuses = findPhrases(text, keepNameWords ? HARD_STATUS_PHRASES : STATUS_PHRASES);
    text = statuses.rest;
    const topics = findPhrases(text, TOPIC_PHRASES);
    if (hasPhrase(topics.rest, "ai") || topics.rest.split(" ").includes("ai")) topics.found.push("ai");
    text = keepNameWords ? text : (topics.found.includes("ai") ? stripPhrase(topics.rest, "ai") : topics.rest);
    const codes = extractCodes(normalized);
    const additions = [];
    if (/general data protection regulation|\bgdpr\b/.test(normalized)) additions.push("gdpr");
    if (/artificial intelligence act|\bai act\b/.test(normalized)) additions.push("ai act");
    const wantsLaws = /\b(laws?|legislation|statutes?|regulations?|directives?|decrees?|legal)\b/.test(normalized);
    const wantsStandards = statuses.found.includes("standards") || (/\b(iso|iec|nist)\b/.test(normalized) && !wantsLaws);
    let keywords = keywordsFrom(text, codes);
    for (const extra of additions) {
      if (!keywords.includes(extra)) keywords.push(extra);
    }
    if (codes.length) keywords = keywords.filter((token) => !/^\d{4}\/\d+$/.test(token));
    const statusIds = [...new Set(statuses.found)];
    let mode = "catalog";
    if (!normalize(original)) mode = "empty";
    else if (nameCue || quoted.length || (codes.length && !listCue) || (keywords.length && !listCue && !statusIds.length)) mode = "lookup";
    else mode = "catalog";
    const assumptions = [];
    for (const match of jurisdictions.matches) {
      if (match.assumption && !assumptions.includes(match.assumption)) assumptions.push(match.assumption);
    }
    return {
      original,
      normalized: normalize(original),
      mode,
      matches: jurisdictions.matches,
      statusIds,
      topic: topics.found[0] || "",
      keywords,
      codes,
      quoted,
      wantsLaws,
      wantsStandards,
      listCue,
      assumptions
    };
  }

  function jurisdictionOk(record, matches) {
    if (!matches.length) return true;
    return matches.some((match) => match.test(record.jurisdiction));
  }

  function allowedStatuses(parsed) {
    if (!parsed.statusIds.length) return null;
    if (parsed.statusIds.includes("not-in-force")) {
      const banned = new Set(["In force", "Published standard", "In development", "Withdrawn standard"]);
      return STATUS_ORDER.filter((status) => !banned.has(status));
    }
    const allowed = new Set();
    for (const id of parsed.statusIds) for (const status of STATUS_SET[id] || []) allowed.add(status);
    return allowed;
  }

  function topicRank(record, topic) {
    if (!topic) return 2;
    const primary = normalize([record.title, record.officialTitle, record.topic].filter(Boolean).join(" "));
    const summary = normalize(record.summary);
    const pattern = topic === "ai"
      ? /\bartificial intelligence\b|\bai\b|\bmachine learning\b/
      : topic === "cyber"
        ? /\bcyber|\binformation security\b/
        : /\bprivacy\b|\bdata protection\b|\bpersonal data\b|\bpersonal information\b|\bgdpr\b/;
    if (pattern.test(primary)) return 2;
    if (pattern.test(summary)) return 1;
    return 0;
  }

  function keywordCoverage(record, keywords) {
    if (!keywords.length) return { all: true, titleHits: 0 };
    const title = normalize([record.title, record.officialTitle].filter(Boolean).join(" "));
    const primary = normalize([title, record.topic].filter(Boolean).join(" "));
    const summary = normalize(record.summary);
    const squashed = squash([record.title, record.officialTitle].join(" "));
    let titleHits = 0;
    let all = true;
    for (const keyword of keywords) {
      const parts = keyword.split(" ");
      const inTitle = parts.every((part) => part === "ai"
        ? /\bartificial intelligence\b|\bai\b/.test(title)
        : new RegExp("\\b" + escapeReg(part) + "\\b").test(primary) || (squash(part).length >= 4 && squashed.includes(squash(part))));
      const inSummary = parts.every((part) => part === "ai"
        ? /\bartificial intelligence\b|\bai\b/.test(summary)
        : new RegExp("\\b" + escapeReg(part) + "\\b").test(summary));
      if (inTitle) titleHits += 1;
      else if (!inSummary) all = false;
    }
    return { all, titleHits };
  }

  function placeName(parsed) {
    const labels = [...new Set(parsed.matches.map((match) => match.label))];
    if (!labels.length) return "";
    if (labels.length === 1 && parsed.matches.some((match) => match.broad && match.label === "United States")) {
      return "the United States (federal, state, and city records in this register)";
    }
    if (labels.length === 1) return labels[0];
    return labels.join(" and ");
  }

  function selectCatalog(items, parsed, honorStatus) {
    const allowed = honorStatus ? allowedStatuses(parsed) : null;
    return items.filter((record) => {
      if (!jurisdictionOk(record, parsed.matches)) return false;
      if (allowed && !allowed.has(record.status)) return false;
      if (parsed.topic && topicRank(record, parsed.topic) < 2) return false;
      if (parsed.keywords.length && !keywordCoverage(record, parsed.keywords).all) return false;
      if (parsed.wantsLaws && NON_LAW.has(record.status)) return false;
      if (isStandard(record) && !parsed.wantsStandards && (parsed.wantsLaws || parsed.matches.length || (allowed && ![...allowed].some((status) => STATUS_SET.standards.includes(status))))) return false;
      if (parsed.wantsStandards && !parsed.wantsLaws && parsed.statusIds.includes("standards") && !isStandard(record)) return false;
      return true;
    });
  }

  function groupRecords(records) {
    const buckets = new Map();
    for (const record of records) {
      const key = record.status || "Other";
      if (!buckets.has(key)) buckets.set(key, []);
      buckets.get(key).push(record);
    }
    return STATUS_ORDER.filter((status) => buckets.has(status)).map((status) => {
      const rows = buckets.get(status).slice().sort((a, b) => sortDate(b).localeCompare(sortDate(a)) || a.title.localeCompare(b.title));
      return { status, records: rows };
    }).concat([...buckets.keys()].filter((status) => !STATUS_ORDER.includes(status)).sort().map((status) => ({
      status,
      records: buckets.get(status)
    })));
  }

  function headingFor(status) {
    if (status === "Enacted") return "Formally adopted — not labeled in force";
    if (["Published standard", "In development", "Withdrawn standard"].includes(status)) return "Standards and frameworks — reference material, not law";
    if (status === "Reviewed") return "Coverage reviews — not laws";
    if (["Lapsed", "Withdrawn", "Superseded", "Repealed", "Expired"].includes(status)) return status + " — not marked current";
    return status;
  }

  function makeGroup(status, records) {
    return {
      heading: headingFor(status),
      note: statusNote(status),
      records: records.slice(0, SHOW),
      total: records.length
    };
  }

  function disclaimer(meta) {
    return DISCLAIMER + (meta && meta.lastChecked ? " Register last checked " + meta.lastChecked + "." : "");
  }

  function emptyAnswer(lead, notes, meta) {
    return { lead, groups: [], notes: notes || [], disclaimer: disclaimer(meta) };
  }

  function countSentence(groups) {
    return groups.map((group) => group.total + " " + (group.status === "Enacted" ? "formally adopted (Enacted)" : group.status)).join("; ");
  }

  function presentCatalog(records, parsed, meta, relaxed) {
    const place = placeName(parsed);
    const grouped = groupRecords(records);
    const standardCount = records.filter(isStandard).length;
    let visible = records;
    if (!parsed.wantsStandards) visible = records.filter((record) => !isStandard(record));
    const notes = parsed.assumptions.slice();
    if (standardCount && !parsed.wantsStandards) {
      notes.push("Standards and frameworks in this register are cross-country reference material, not laws of " + (place || "a country") + ". They are not listed as local law, and a country question does not mean they were adopted there or given legal force.");
    }
    if (!visible.length) {
      return emptyAnswer(
        standardCount
          ? "The only matches are standards or frameworks. Those are reference material, not law, and they do not show that a country has adopted them."
          : "No record in this register matches that question.",
        notes,
        meta
      );
    }
    const groups = groupRecords(visible).map((group) => makeGroup(group.status, group.records));
    const total = visible.length;
    let lead;
    if (relaxed) {
      const asked = parsed.statusIds.map((id) => id === "in-force" ? "In force" : id === "enacted" ? "Formally adopted (Enacted)" : id).join(" or ");
      lead = "No matching record is marked " + asked + (place ? " for " + place : "") + ". The register does have " + total + " other matching record" + (total === 1 ? "" : "s") + ", shown by the status actually recorded.";
    } else if (parsed.statusIds.length === 1 && groups.length === 1) {
      lead = "The register lists " + total + (place ? " " + place : "") + " record" + (total === 1 ? "" : "s") + " with this status.";
    } else {
      lead = "The register lists " + total + " matching record" + (total === 1 ? "" : "s") + (place ? " for " + place : "") + ". They are grouped by the status recorded on each entry so in-force instruments stay separate from proposals, consultations, guidance, adopted policy, and standards.";
    }
    if (parsed.wantsLaws) notes.unshift("The records below are the register entries that match. Guidance, adopted policy, coverage reviews, and standards are not counted as laws.");
    if (!parsed.matches.length && !parsed.keywords.length && !parsed.codes.length && total > 24) {
      return {
        lead: "The register has " + total + " matching records" + (grouped.length ? " (" + countSentence(groupRecords(visible)) + ")" : "") + ". Name a jurisdiction or an instrument to see individual entries. This is a count of the register, not a complete survey of the law.",
        groups: [],
        notes,
        disclaimer: disclaimer(meta)
      };
    }
    return { lead, groups, notes, disclaimer: disclaimer(meta) };
  }

  function noteOtherCategories(items, parsed, result) {
    const shown = new Set((result.groups || []).flatMap((group) => (group.records || []).map((record) => record.status)));
    const pool = items.filter((record) => {
      if (isStandard(record)) return false;
      if (!jurisdictionOk(record, parsed.matches)) return false;
      if (parsed.topic && topicRank(record, parsed.topic) < 2) return false;
      return NON_LAW.has(record.status) || ["Lapsed", "Withdrawn", "Superseded", "Repealed", "Expired"].includes(record.status);
    });
    const extra = pool.filter((record) => !shown.has(record.status));
    if (!extra.length) return;
    const counts = {};
    for (const record of extra) counts[record.status] = (counts[record.status] || 0) + 1;
    result.notes.push("Also recorded for this place and topic, and kept separate: " + Object.entries(counts).map(([status, count]) => count + " " + statusLabel(status)).join("; ") + ".");
  }

  function finishCatalog(items, parsed, result) {
    if (!parsed.wantsStandards && parsed.matches.length && !(result.notes || []).some((note) => note.startsWith("Standards and frameworks"))) {
      result.notes.push("Standards and frameworks in this register are cross-country reference material. They are not listed here as the law of " + placeName(parsed) + ", and a country question does not mean a country adopted them or gave them legal force.");
    }
    if (result.groups && result.groups.length) noteOtherCategories(items, parsed, result);
    return result;
  }

  function answerCatalog(items, parsed, meta) {
    const strict = selectCatalog(items, parsed, true);
    const pack = { ...meta, items };
    if (strict.length) {
      const result = presentCatalog(strict, parsed, pack, false);
      if (parsed.statusIds.includes("in-force") && !parsed.statusIds.includes("enacted") && result.groups.length) {
        const asideParsed = { ...parsed, statusIds: ["enacted"], wantsStandards: false };
        const enacted = selectCatalog(items, asideParsed, true);
        if (enacted.length) {
          result.groups.push(makeGroup("Enacted", enacted.slice().sort((a, b) => sortDate(b).localeCompare(sortDate(a)))));
          result.notes.push("Formally adopted records are listed separately. The register does not label them In force. An effective date on an entry is not a substitute for that label.");
          result.lead += " " + enacted.length + " formally adopted record" + (enacted.length === 1 ? " is" : "s are") + " listed separately and " + (enacted.length === 1 ? "is" : "are") + " not labeled In force.";
        }
      }
      return finishCatalog(items, parsed, result);
    }
    if (parsed.statusIds.length) {
      const relaxedParsed = { ...parsed, statusIds: [] };
      const relaxed = selectCatalog(items, relaxedParsed, false).filter((record) => parsed.wantsStandards || !isStandard(record));
      if (relaxed.length) return finishCatalog(items, parsed, presentCatalog(relaxed, parsed, pack, true));
    }
    const place = placeName(parsed);
    const known = place && items.some((record) => jurisdictionOk(record, parsed.matches));
    const lead = known
      ? "No " + place + " record in this register matches the rest of the question. That is not proof that no law applies."
      : "No record in this register matches that question. That is not proof that no law applies.";
    return finishCatalog(items, parsed, emptyAnswer(lead, parsed.assumptions, meta));
  }

  function scoreRecord(record, parsed) {
    const title = normalize(record.title);
    const official = normalize(record.officialTitle);
    const both = (title + " " + official).trim();
    const topic = normalize(record.topic);
    const summary = normalize(record.summary);
    const squashed = squash(both);
    let score = 0;
    const jurisdictionMatch = parsed.matches.length && jurisdictionOk(record, parsed.matches);
    if (parsed.matches.length) score += jurisdictionMatch ? 18 : -10;
    const phrase = parsed.keywords.filter((keyword) => !keyword.includes(" ")).join(" ");
    if (phrase.length > 4 && both.includes(phrase)) score += 28;
    else if (parsed.keywords.includes("ai act") && both.includes("artificial intelligence act")) score += 28;
    for (const quote of parsed.quoted) if (quote && both.includes(quote)) score += 36;
    if (parsed.keywords.includes("ai act") && (both.includes("ai act") || both.includes("artificial intelligence act"))) score += 34;
    if (parsed.keywords.includes("gdpr") && /\bgdpr\b/.test(both)) score += 34;
    for (const keyword of parsed.keywords) {
      if (keyword.includes(" ")) continue;
      const pattern = new RegExp("\\b" + escapeReg(keyword) + "\\b");
      const ai = keyword === "ai" && (/\bartificial intelligence\b/.test(both) || /\bai\b/.test(both));
      if (ai || pattern.test(both) || (squash(keyword).length >= 5 && squashed.includes(squash(keyword)))) score += keyword.length >= 4 ? 8 : 5;
      else if (pattern.test(topic)) score += 3;
      else if (pattern.test(summary)) score += 1;
      else score -= 4;
    }
    for (const code of parsed.codes) {
      if (squashed.includes(squash(code))) score += 56;
      else score -= 6;
    }
    if (title.startsWith(phrase) && phrase.length > 3) score += 8;
    const shortQuery = parsed.keywords.filter((keyword) => !keyword.includes(" ")).length <= 2;
    if (shortQuery && /\b(implementation|implementing|transpos|supplement)\b/.test(both) && !/\b(implementation|implementing|transpos|supplement)\b/.test(parsed.normalized)) score -= 8;
    if (record.status === "Reviewed" && !/\breview\b/.test(parsed.normalized)) score -= 10;
    if (isApplicability(record) && !/\b(apply|applies|applicable|applicability)\b/.test(parsed.normalized)) score -= 14;
    if (isStandard(record) && parsed.wantsLaws && !parsed.wantsStandards) score -= 12;
    if (isStandard(record) && parsed.wantsStandards) score += 8;
    return score;
  }

  function answerLookup(items, parsed, meta) {
    if (!parsed.keywords.length && !parsed.codes.length && !parsed.quoted.length) {
      return answerCatalog(items, parsed, meta);
    }
    const ranked = items.map((record) => ({ record, score: scoreRecord(record, parsed) })).filter((entry) => entry.score > 0).sort((a, b) => b.score - a.score || sortDate(b.record).localeCompare(sortDate(a.record)));
    const best = ranked[0]?.score || 0;
    if (best < 12) {
      const needles = [];
      for (const code of parsed.codes) {
        const digits = code.match(/\d{3,5}/g) || [];
        needles.push(...digits);
      }
      for (const quote of parsed.quoted) if (quote.length >= 4) needles.push(quote);
      const unique = [...new Set(needles)];
      let mentionCount = 0;
      if (unique.length) {
        mentionCount = items.filter((record) => {
          const blob = normalize([record.summary, record.title, record.officialTitle].filter(Boolean).join(" "));
          return unique.some((needle) => new RegExp("\\b" + escapeReg(needle) + "\\b").test(blob));
        }).length;
      }
      const notes = parsed.assumptions.slice();
      if (mentionCount) {
        notes.push(mentionCount + " record summaries mention " + unique.map((needle) => "“" + needle + "”").join(" or ") + ". A summary mention is not a record of that instrument, and it is not a law. Standards mentioned this way are reference material, not evidence of local legal force.");
      }
      return emptyAnswer("No record in this register uses that instrument name in its title. That is not proof that no such law or standard exists.", notes, meta);
    }
    const closest = ranked.filter((entry) => entry.score >= best - 8).map((entry) => entry.record);
    const relatedPool = ranked.filter((entry) => entry.score >= Math.max(12, best - 22) && entry.score < best - 8).map((entry) => entry.record);
    const closestLaws = closest.filter((record) => !isStandard(record));
    const closestStandards = closest.filter(isStandard);
    const primary = (parsed.wantsStandards && !parsed.wantsLaws) || !closestLaws.length ? closest : closestLaws;
    const groups = [];
    const byStatus = groupRecords(primary);
    for (const bucket of byStatus) groups.push(makeGroup(bucket.status, bucket.records));
    const notes = parsed.assumptions.slice();
    if (primary.length > 1) notes.push("Matching entries are listed separately. This page does not merge them into one instrument or fill in a date that an entry leaves blank.");
    const applicability = relatedPool.filter(isApplicability);
    const otherRelated = relatedPool.filter((record) => !isApplicability(record) && !isStandard(record));
    if (applicability.length && primary.some((record) => !isApplicability(record))) {
      notes.push("The register also has " + applicability.length + " applicability record" + (applicability.length === 1 ? "" : "s") + " whose titles say an EU instrument applies in a member state. Those are not listed here as separate national statutes.");
    }
    if (otherRelated.length) {
      groups.push({
        heading: "Other records matching some of these words",
        note: "These entries share some of the words in the question. They are separate records and may have a different status.",
        records: otherRelated.slice(0, 4),
        total: otherRelated.length
      });
    }
    if (closestStandards.length && primary !== closest) {
      groups.push(makeGroup(closestStandards[0].status || "Published standard", closestStandards));
      notes.push("A matching standard, framework, or technical specification is reference material, not law. It does not show that a country adopted it or gave it legal force.");
    } else if (primary.some(isStandard)) {
      notes.push("The closest match is reference material, not law. A published standard is not a statute, and showing it beside a country does not mean that country adopted it or made it legally binding.");
    }
    const statuses = [...new Set(primary.map((record) => record.status))];
    const askedInForce = parsed.statusIds.includes("in-force");
    let lead;
    if (askedInForce && statuses.length === 1 && statuses[0] === "In force") {
      lead = (primary.length === 1 ? "Yes. The register marks this record as In force." : "Yes. The register marks these closest records as In force.");
    } else if (askedInForce && statuses.every((status) => status !== "In force")) {
      lead = "No. The register does not mark " + (primary.length === 1 ? "this record" : "these closest records") + " as In force. The recorded status is " + statuses.map(statusLabel).join("; ") + ".";
    } else if (statuses.length === 1) {
      lead = (primary.length === 1 ? "The closest register record" : "The closest register records") + " " + (primary.length === 1 ? "is" : "are") + " marked " + statusLabel(statuses[0]) + ".";
    } else {
      lead = "The closest records do not share one status. Each status below is the status stored on that entry.";
    }
    if (primary.some(isApplicability) && primary.every(isApplicability)) {
      notes.unshift("These are applicability records. They say an EU instrument applies in the named jurisdiction. They are not separate national statutes.");
    }
    return { lead, groups, notes, disclaimer: disclaimer(meta) };
  }

  function answer(items, question, meta) {
    const parsed = parse(question, items || []);
    const context = meta || {};
    if (parsed.mode === "empty") {
      return emptyAnswer("Enter a jurisdiction, a status, or an instrument name. For example: which laws are in force in Japan.", [], context);
    }
    if (!items || !items.length) {
      return emptyAnswer("The register has not loaded, so there are no records to cite yet.", [], context);
    }
    const result = parsed.mode === "lookup" ? answerLookup(items, parsed, context) : answerCatalog(items, parsed, context);
    if (context.debug) result.debug = parsed;
    return result;
  }

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function safeUrl(value) {
    try {
      const url = new URL(value, "https://example.invalid");
      if (url.protocol === "https:" || url.protocol === "http:") return url.href;
    } catch (error) {
      return "";
    }
    return "";
  }

  function renderRecord(record) {
    const item = element("article", "ask-item");
    const title = element("div");
    const href = safeUrl(record.sourceUrl);
    const titleNode = href ? element("a", "title") : element("span", "title");
    titleNode.textContent = record.title || "Untitled record";
    if (href) {
      titleNode.href = href;
      titleNode.target = "_blank";
      titleNode.rel = "noopener";
    }
    title.append(titleNode);
    item.append(title);
    if (record.officialTitle && record.officialTitle !== record.title) item.append(element("div", "ask-meta", "Official title: " + record.officialTitle));
    const meta = [record.jurisdiction, statusLabel(record.status), record.instrumentType, record.topic, record.regulator].filter(Boolean).join(" · ");
    if (meta) item.append(element("div", "ask-meta", meta));
    const dates = [
      ["Published", record.publicationDate],
      ["Adopted", record.adoptedDate],
      ["Effective", record.effectiveDate]
    ].map(([label, value]) => (dateValue(value) ? label + " " + dateValue(value) : label + ": not recorded"));
    item.append(element("div", "ask-meta", dates.join(" · ")));
    const caution = cardCaution(record);
    if (caution) item.append(element("p", "ask-note", caution));
    const summary = String(record.summary || "").replace(/\s+/g, " ").trim();
    if (summary) {
      const excerpt = summary.length > 360 ? summary.slice(0, 360).replace(/\s+\S*$/, "") + "…" : summary;
      item.append(element("p", "ask-summary", "Register summary: " + excerpt));
    }
    if (href) {
      const link = element("a", "ask-source");
      link.href = href;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = record.sourceUrl;
      const line = element("div", "ask-meta");
      line.append("Official source: ", link);
      item.append(line);
    } else if (safeUrl(record.catalogEntryUrl)) {
      const link = element("a", "ask-source");
      link.href = safeUrl(record.catalogEntryUrl);
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = record.catalogEntryUrl;
      const line = element("div", "ask-meta");
      line.append("No official source URL is recorded. Catalog entry only: ", link);
      item.append(line);
    } else {
      item.append(element("div", "ask-meta", "No official source URL is recorded on this entry."));
    }
    return item;
  }

  function render(result) {
    const wrap = element("div", "ask-rich");
    wrap.append(element("p", "ask-lead", result.lead));
    const tailNotes = [];
    for (const note of result.notes || []) {
      if (note.startsWith("Standards and frameworks")) tailNotes.push(note);
      else wrap.append(element("p", "ask-note", note));
    }
    for (const group of result.groups || []) {
      const section = element("section", "ask-group");
      section.append(element("h3", null, group.heading));
      if (group.note) section.append(element("p", "ask-note", group.note));
      const list = element("div", "ask-list");
      for (const record of group.records || []) list.append(renderRecord(record));
      section.append(list);
      if (group.total > (group.records || []).length) {
        section.append(element("p", "ask-more", "Showing " + group.records.length + " of " + group.total + ". The rest stay in the register and are not listed in this answer."));
      }
      wrap.append(section);
    }
    for (const note of tailNotes) wrap.append(element("p", "ask-note", note));
    wrap.append(element("p", "ask-disclaimer", result.disclaimer));
    return wrap;
  }

  function mount(options) {
    const rootNode = document.getElementById(options.rootId || "askBox");
    if (!rootNode || rootNode.dataset.bound) return;
    rootNode.dataset.bound = "1";
    const form = rootNode.querySelector("form");
    const input = rootNode.querySelector("input");
    const output = rootNode.querySelector("[data-ask-answer]");
    function run(question) {
      const items = options.getItems ? options.getItems() : [];
      output.hidden = false;
      if (!items || !items.length) {
        output.replaceChildren(element("p", "ask-lead", "The register is still loading. Ask again in a moment."));
        return;
      }
      const result = answer(items, question, { lastChecked: options.getLastChecked ? options.getLastChecked() : "" });
      output.replaceChildren(render(result));
    }
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const question = input.value.trim();
      if (!question) return;
      run(question);
    });
    rootNode.querySelectorAll("[data-ask]").forEach(function (button) {
      button.addEventListener("click", function () {
        input.value = button.getAttribute("data-ask") || "";
        run(input.value);
        input.focus();
      });
    });
  }

  return { answer, parse, render, mount, normalize };
});
