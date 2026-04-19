#!/usr/bin/env python3
from __future__ import annotations

import copy
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "_data"
SITE_PROFILE_PATH = DATA_DIR / "site_profile.yml"
OVERRIDES_PATH = DATA_DIR / "publication_overrides.yml"
PUBLICATIONS_PATH = DATA_DIR / "publications.yml"

ORCID_API_BASE = "https://pub.orcid.org/v3.0"
ORCID_TOKEN_URL = "https://orcid.org/oauth/token"
CROSSREF_API_BASE = "https://api.crossref.org/works/"
USER_AGENT = "moustafa-publications-sync/1.0 (https://abdelwanismoustafa.github.io)"

DEFAULT_PROFILE: Dict[str, Any] = {
    "name": "Moustafa Abdelwanis",
    "orcid_id": "0000-0001-5034-2613",
    "profiles": {
        "scholar_url": "https://scholar.google.com/citations?hl=en&user=VwCuh7MAAAAJ&view_op=list_works",
        "scholar_label": "Google Scholar",
        "orcid_url": "https://orcid.org/0000-0001-5034-2613",
        "orcid_label": "ORCID",
    },
    "homepage": {
        "hero_badge": "Engineering Systems and Management • Khalifa University",
        "hero_title": "Moustafa Abdelwanis",
        "hero_subtitle": "Ph.D. candidate researching operations management, AI in healthcare, human-AI interaction, simulation, and optimization.",
        "selected_publications_limit": 4,
        "featured_types": ["journal", "conference", "thesis"],
    },
    "awards": [],
    "scholar_metrics": {},
}

DEFAULT_OVERRIDES: Dict[str, Any] = {"by_doi": {}, "by_title": {}}

JOURNAL_TYPES = {
    "journal-article",
    "review",
    "review-article",
    "magazine-article",
    "newspaper-article",
    "encyclopaedia-entry",
    "book-review",
    "preprint",
}
CONFERENCE_TYPES = {
    "conference-paper",
    "conference-abstract",
    "conference-poster",
    "conference-presentation",
    "lecture-speech",
}
THESIS_TYPES = {
    "dissertation-thesis",
    "dissertation",
    "thesis",
}

TYPE_LABELS = {
    "journal": "Journal article",
    "conference": "Conference paper",
    "thesis": "Thesis",
    "other": "Other output",
}

TYPE_ORDER = {"journal": 0, "conference": 1, "thesis": 2, "other": 3}

THEME_RULES: List[Tuple[str, List[str], str]] = [
    (
        "ai-healthcare",
        [
            "artificial intelligence",
            " ai ",
            "ai-",
            "healthcare",
            "health systems",
            "clinical",
            "hospital",
            "emergency department",
            "medical",
        ],
        "AI in healthcare",
    ),
    (
        "human-ai",
        [
            "automation bias",
            "adoption",
            "providers' perspectives",
            "provider perspectives",
            "trust",
            "human-ai",
            "human factors",
        ],
        "Human-AI interaction",
    ),
    (
        "operations-optimization",
        [
            "variable neighborhood",
            "optimization",
            "skill assignment",
            "skill allocation",
            "cross-training",
            "simulation",
            "queue",
            "inventory",
            "manufacturing",
            "service system",
        ],
        "Operations & optimization",
    ),
    (
        "clinical-analytics",
        [
            "classification",
            "random forest",
            "neural network",
            "biomarker",
            "cardiac",
            "depression",
            "neuropathy",
            "assessment",
        ],
        "Clinical analytics",
    ),
    (
        "reviews",
        ["review", "future directions", "comprehensive review", "survey"],
        "Review",
    ),
]

KEYWORD_STOPWORDS = {
    "a",
    "an",
    "and",
    "approach",
    "artificial",
    "based",
    "comprehensive",
    "cross",
    "driven",
    "enhancing",
    "exploring",
    "for",
    "from",
    "future",
    "healthcare",
    "in",
    "intelligence",
    "its",
    "of",
    "on",
    "perspectives",
    "review",
    "risk",
    "risks",
    "safe",
    "safety",
    "sequential",
    "simulation",
    "study",
    "the",
    "using",
    "with",
}


def load_yaml(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return copy.deepcopy(default)
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return copy.deepcopy(default)
    data = yaml.safe_load(raw)
    if data is None:
        return copy.deepcopy(default)
    return data


def save_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dumped = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=100,
        indent=2,
    )
    path.write_text(dumped, encoding="utf-8")


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[bytes] = None,
) -> Dict[str, Any]:
    request = urllib.request.Request(url=url, method=method, data=data)
    request.add_header("User-Agent", USER_AGENT)
    if headers:
        for key, value in headers.items():
            request.add_header(key, value)
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def get_orcid_token() -> Optional[str]:
    client_id = os.getenv("ORCID_CLIENT_ID", "").strip()
    client_secret = os.getenv("ORCID_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        return None

    data = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": "/read-public",
        }
    ).encode("utf-8")
    response = http_json(
        ORCID_TOKEN_URL,
        method="POST",
        headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )
    token = response.get("access_token")
    if not token:
        raise RuntimeError("ORCID token response did not include access_token.")
    return str(token)


class OrcidClient:
    def __init__(self, token: Optional[str], fixtures_dir: Optional[Path] = None) -> None:
        self.token = token
        self.fixtures_dir = fixtures_dir

    def _fixture(self, name: str) -> Optional[Dict[str, Any]]:
        if not self.fixtures_dir:
            return None
        path = self.fixtures_dir / f"{name}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def get(self, endpoint: str, fixture_name: str) -> Dict[str, Any]:
        fixture = self._fixture(fixture_name)
        if fixture is not None:
            return fixture

        url = f"{ORCID_API_BASE}/{endpoint.lstrip('/')}"
        base_headers = {"Accept": "application/json"}
        if self.token:
            try:
                return http_json(url, headers={**base_headers, "Authorization": f"Bearer {self.token}"})
            except urllib.error.HTTPError as exc:
                if exc.code not in {401, 403}:
                    raise
        try:
            return http_json(url, headers=base_headers)
        except urllib.error.HTTPError as exc:
            if exc.code in {401, 403}:
                raise RuntimeError(
                    "ORCID refused the request. Add ORCID_CLIENT_ID and ORCID_CLIENT_SECRET as repository secrets."
                ) from exc
            raise


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def canonical_doi(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = value.strip()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = value.strip().strip("/ ")
    return value.lower() or None


def safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def title_key(title: str) -> str:
    return safe_slug(normalize_space(title))


def nested_get(data: Any, *path: str) -> Optional[Any]:
    current = data
    for key in path:
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


def extract_external_ids(work: Dict[str, Any]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = defaultdict(list)
    items = nested_get(work, "external-ids", "external-id") or []
    for item in items:
        ext_type = normalize_space(str(item.get("external-id-type", ""))).lower()
        ext_value = normalize_space(str(item.get("external-id-value", "")))
        if ext_type and ext_value:
            result[ext_type].append(ext_value)
    return dict(result)


def extract_doi(work: Dict[str, Any]) -> Optional[str]:
    ids = extract_external_ids(work)
    for value in ids.get("doi", []):
        doi = canonical_doi(value)
        if doi:
            return doi
    url_value = nested_get(work, "url", "value")
    return canonical_doi(str(url_value)) if url_value else None


def extract_title(work: Dict[str, Any]) -> str:
    for candidate in [
        nested_get(work, "title", "title", "value"),
        nested_get(work, "title", "subtitle", "value"),
    ]:
        if candidate:
            return normalize_space(str(candidate))
    raise RuntimeError("Work is missing a title.")


def extract_short_description(work: Dict[str, Any]) -> Optional[str]:
    value = work.get("short-description")
    if value:
        return normalize_space(str(value))
    return None


def extract_year(work: Dict[str, Any], crossref_message: Dict[str, Any]) -> int:
    raw = nested_get(work, "publication-date", "year", "value")
    if raw and str(raw).isdigit():
        return int(raw)

    for field in ("published-print", "published-online", "issued", "created"):
        date_parts = nested_get(crossref_message, field, "date-parts") or []
        if date_parts and date_parts[0] and str(date_parts[0][0]).isdigit():
            return int(date_parts[0][0])

    return dt.date.today().year


def extract_publication_date(work: Dict[str, Any], year: int) -> str:
    month = nested_get(work, "publication-date", "month", "value")
    day = nested_get(work, "publication-date", "day", "value")
    if month and day:
        return f"{year:04d}-{int(month):02d}-{int(day):02d}"
    if month:
        return f"{year:04d}-{int(month):02d}-01"
    return f"{year:04d}-01-01"


def infer_type(orcid_type: str, crossref_type: str, title: str, venue: str) -> str:
    ot = normalize_space(orcid_type).lower()
    ct = normalize_space(crossref_type).lower()
    text = f" {title.lower()} {venue.lower()} "

    if ot in THESIS_TYPES or ct in THESIS_TYPES or " thesis " in text or " dissertation " in text:
        return "thesis"
    if ot in CONFERENCE_TYPES or ct in CONFERENCE_TYPES:
        return "conference"
    if ot in JOURNAL_TYPES or ct in JOURNAL_TYPES:
        return "journal"
    if any(keyword in text for keyword in ["conference", "proceedings", "symposium", "workshop", "wsc", "cinc", "cie", "icvns"]):
        return "conference"
    if any(keyword in text for keyword in ["journal", "scientific reports", "safety science", "operations research", "biology and medicine"]):
        return "journal"
    return "other"


def format_crossref_authors(message: Dict[str, Any]) -> Optional[str]:
    authors = []
    for item in message.get("author", []) or []:
        given = normalize_space(str(item.get("given", "")))
        family = normalize_space(str(item.get("family", "")))
        literal = normalize_space(str(item.get("literal", "")))
        name = normalize_space(" ".join(part for part in [given, family] if part)) or literal
        if name:
            authors.append(name)
    return ", ".join(authors) if authors else None


def format_orcid_authors(work: Dict[str, Any]) -> Optional[str]:
    contributors = nested_get(work, "contributors", "contributor") or []
    authors = []
    for item in contributors:
        name = nested_get(item, "credit-name", "value")
        if name:
            authors.append(normalize_space(str(name)))
    return ", ".join(authors) if authors else None


def clean_abstract(raw: str) -> str:
    text = html.unescape(raw)
    text = re.sub(r"</?jats:[^>]+>", " ", text)
    text = re.sub(r"</?[^>]+>", " ", text)
    text = normalize_space(text)
    text = re.sub(r"^abstract\s*", "", text, flags=re.I)
    return text


def sentence_trim(text: str, max_chars: int = 260) -> str:
    text = normalize_space(text)
    if len(text) <= max_chars:
        return text
    sentences = re.split(r"(?<=[.!?])\s+", text)
    kept = []
    total = 0
    for sentence in sentences:
        if not sentence:
            continue
        if total + len(sentence) + (1 if kept else 0) > max_chars and kept:
            break
        kept.append(sentence)
        total += len(sentence) + (1 if kept else 0)
        if total >= max_chars * 0.7:
            break
    if kept:
        return normalize_space(" ".join(kept))
    return text[: max_chars - 1].rstrip() + "…"


def fallback_description(title: str, type_label: str) -> str:
    topic = title.strip().rstrip(".")
    if topic:
        first = topic[0].lower() + topic[1:] if len(topic) > 1 else topic.lower()
        return f"{type_label} on {first}."
    return f"{type_label}."


def infer_themes(title: str, description: str, type_slug: str) -> Tuple[List[str], List[str]]:
    text = f" {title.lower()} {description.lower()} "
    slugs: List[str] = []
    labels: List[str] = []
    for slug, keywords, label in THEME_RULES:
        if any(keyword in text for keyword in keywords):
            slugs.append(slug)
            labels.append(label)
    if type_slug == "thesis" and "thesis" not in labels:
        slugs.append("thesis")
        labels.append("Thesis")
    if not slugs:
        slugs.append("research")
        labels.append("Research")
    return slugs, labels


def infer_keywords(title: str, themes: Iterable[str]) -> List[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z\-']+", title)
    cleaned = []
    for token in tokens:
        lower = token.lower()
        if lower in KEYWORD_STOPWORDS or len(lower) <= 2:
            continue
        if lower not in cleaned:
            cleaned.append(lower)
    title_keywords = [token.replace("-", " ") for token in cleaned[:4]]
    for theme in themes:
        if theme.lower() not in [t.lower() for t in title_keywords]:
            title_keywords.append(theme)
    return title_keywords[:5]


def merge_links(*link_sets: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    merged: List[Dict[str, str]] = []
    for link_set in link_sets:
        for link in link_set or []:
            label = normalize_space(str(link.get("label", "")))
            url = normalize_space(str(link.get("url", "")))
            if not label or not url:
                continue
            key = (label.lower(), url)
            if key in seen:
                continue
            seen.add(key)
            merged.append({"label": label, "url": url})
    return merged


def build_generated_links(doi: Optional[str], work: Dict[str, Any], crossref_message: Dict[str, Any]) -> List[Dict[str, str]]:
    links: List[Dict[str, str]] = []
    if doi:
        links.append({"label": "DOI", "url": f"https://doi.org/{doi}"})
    work_url = nested_get(work, "url", "value")
    if work_url and (not doi or canonical_doi(str(work_url)) != doi):
        links.append({"label": "Publisher page", "url": str(work_url)})
    crossref_url = crossref_message.get("URL")
    if crossref_url and str(crossref_url) != str(work_url) and (not doi or canonical_doi(str(crossref_url)) != doi):
        links.append({"label": "Publisher page", "url": str(crossref_url)})
    return links


def format_venue(work: Dict[str, Any], crossref_message: Dict[str, Any], year: int, type_slug: str) -> str:
    journal_title = nested_get(work, "journal-title", "value")
    container = None
    if crossref_message.get("container-title"):
        container_list = crossref_message.get("container-title") or []
        if container_list:
            container = normalize_space(str(container_list[0]))
    venue_name = normalize_space(str(journal_title or container or ""))
    publisher = normalize_space(str(crossref_message.get("publisher", "")))
    volume = normalize_space(str(crossref_message.get("volume", "")))
    issue = normalize_space(str(crossref_message.get("issue", "")))
    page = normalize_space(str(crossref_message.get("page", "")))
    article_number = normalize_space(str(crossref_message.get("article-number", "")))

    detail_bits: List[str] = []
    if volume:
        detail_bits.append(volume)
    if issue:
        detail_bits.append(f"({issue})")
    if page:
        detail_bits.append(page)
    elif article_number:
        detail_bits.append(article_number)

    if venue_name and detail_bits:
        return f"{venue_name}, {' '.join(detail_bits)} ({year})"
    if venue_name:
        return f"{venue_name} ({year})"
    if type_slug == "thesis":
        return f"Thesis ({year})"
    if publisher:
        return f"{publisher} ({year})"
    return f"Research output ({year})"


def get_override(overrides: Dict[str, Any], doi: Optional[str], title: str) -> Dict[str, Any]:
    by_doi = overrides.get("by_doi", {}) or {}
    by_title = overrides.get("by_title", {}) or {}
    if doi and doi in by_doi:
        return by_doi[doi] or {}
    key = title_key(title)
    if key in by_title:
        return by_title[key] or {}
    return {}


def fetch_crossref(doi: Optional[str], fixtures_dir: Optional[Path] = None) -> Dict[str, Any]:
    if not doi:
        return {}
    if fixtures_dir:
        fixture_name = f"crossref_{safe_slug(doi)}.json"
        fixture_path = fixtures_dir / fixture_name
        if fixture_path.exists():
            data = json.loads(fixture_path.read_text(encoding="utf-8"))
            return data.get("message", data)
    url = CROSSREF_API_BASE + urllib.parse.quote(doi)
    try:
        payload = http_json(url, headers={"Accept": "application/json"})
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {}
        raise
    return payload.get("message", {})


def flatten_work_summaries(works_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    summaries: List[Dict[str, Any]] = []
    for group in works_payload.get("group", []) or []:
        for summary in group.get("work-summary", []) or []:
            summaries.append(summary)
    return summaries


def build_publication_item(
    work: Dict[str, Any],
    crossref_message: Dict[str, Any],
    profile: Dict[str, Any],
    overrides: Dict[str, Any],
) -> Dict[str, Any]:
    title = extract_title(work)
    doi = extract_doi(work)
    override = get_override(overrides, doi, title)

    year = extract_year(work, crossref_message)
    publication_date = extract_publication_date(work, year)
    orcid_type = normalize_space(str(work.get("type", ""))).lower()
    crossref_type = normalize_space(str(crossref_message.get("type", ""))).lower()

    provisional_venue = normalize_space(str(nested_get(work, "journal-title", "value") or ""))
    type_slug = infer_type(orcid_type, crossref_type, title, provisional_venue)
    type_label = TYPE_LABELS[type_slug]
    venue = override.get("venue") or format_venue(work, crossref_message, year, type_slug)

    authors = (
        override.get("authors")
        or format_crossref_authors(crossref_message)
        or format_orcid_authors(work)
        or profile.get("name", "Moustafa Abdelwanis")
    )

    description = override.get("description")
    if not description:
        description = extract_short_description(work)
    if not description and crossref_message.get("abstract"):
        description = sentence_trim(clean_abstract(str(crossref_message["abstract"])))
    if not description:
        description = fallback_description(title, type_label)

    theme_slugs = override.get("theme_slugs") or []
    themes = override.get("themes") or []
    if not theme_slugs or not themes:
        theme_slugs, themes = infer_themes(title, description, type_slug)

    keywords = override.get("keywords") or infer_keywords(title, themes)

    highlight = override.get("highlight")
    if not highlight and (crossref_type == "review-article" or "review" in title.lower()):
        highlight = "Review article"
    if not highlight and type_slug == "thesis":
        highlight = "Thesis"

    links = merge_links(
        build_generated_links(doi, work, crossref_message),
        override.get("links", []),
    )

    item: Dict[str, Any] = {
        "title": title,
        "year": year,
        "publication_date": publication_date,
        "type_slug": type_slug,
        "type_label": type_label,
        "venue": venue,
        "authors": authors,
        "description": description,
        "theme_slugs": theme_slugs,
        "themes": themes,
        "keywords": keywords,
        "links": links,
        "slug": title_key(title),
    }
    if doi:
        item["doi"] = doi
    if highlight:
        item["highlight"] = highlight
    if override.get("summary_note"):
        item["summary_note"] = override["summary_note"]
    if override.get("citations"):
        item["citations"] = override["citations"]
    return item


def unique_publications(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    best_by_key: Dict[str, Dict[str, Any]] = {}
    for item in items:
        key = item.get("doi") or item["slug"]
        current = best_by_key.get(key)
        if current is None:
            best_by_key[key] = item
            continue
        current_score = (len(current.get("links", [])), len(current.get("description", "")), TYPE_ORDER[current["type_slug"]])
        new_score = (len(item.get("links", [])), len(item.get("description", "")), TYPE_ORDER[item["type_slug"]])
        if new_score > current_score:
            best_by_key[key] = item
    return list(best_by_key.values())


def sort_publications(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (
            -int(item.get("year", 0)),
            TYPE_ORDER.get(str(item.get("type_slug", "other")), 99),
            str(item.get("title", "")).lower(),
        ),
    )


def preserve_metrics(profile: Dict[str, Any], existing_publications: Dict[str, Any]) -> Dict[str, Any]:
    metrics = {}
    existing_analytics = existing_publications.get("analytics", {}) or {}
    profile_metrics = profile.get("scholar_metrics", {}) or {}
    for key in ("citations", "h_index", "i10_index", "last_checked"):
        if key in profile_metrics and profile_metrics[key] not in (None, ""):
            metrics[key] = profile_metrics[key]
        elif key in existing_analytics and existing_analytics[key] not in (None, ""):
            metrics[key] = existing_analytics[key]
    return metrics


def build_output(profile: Dict[str, Any], items: List[Dict[str, Any]], existing_publications: Dict[str, Any]) -> Dict[str, Any]:
    counts = defaultdict(int)
    for item in items:
        counts[item["type_slug"]] += 1

    selected_limit = int(profile.get("homepage", {}).get("selected_publications_limit", 4))
    featured_types = set(profile.get("homepage", {}).get("featured_types", ["journal", "conference", "thesis"]))
    selected_outputs = [copy.deepcopy(item) for item in items if item["type_slug"] in featured_types][:selected_limit]

    analytics: Dict[str, Any] = {
        "listed_outputs": len(items),
        "journal_articles": counts["journal"],
        "conference_papers": counts["conference"],
        "theses": counts["thesis"],
        "other_outputs": counts["other"],
        "note": "Synced from ORCID and enriched with Crossref metadata when DOI metadata is available.",
        "award_count": len(profile.get("awards", []) or []),
    }
    analytics.update(preserve_metrics(profile, existing_publications))

    return {
        "profiles": copy.deepcopy(profile.get("profiles", DEFAULT_PROFILE["profiles"])),
        "analytics": analytics,
        "selected_outputs": selected_outputs,
        "outputs": items,
    }


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    profile = load_yaml(SITE_PROFILE_PATH, DEFAULT_PROFILE)
    overrides = load_yaml(OVERRIDES_PATH, DEFAULT_OVERRIDES)
    existing_publications = load_yaml(PUBLICATIONS_PATH, {}) if PUBLICATIONS_PATH.exists() else {}

    fixtures_dir_env = os.getenv("ORCID_FIXTURES_DIR", "").strip()
    fixtures_dir = Path(fixtures_dir_env) if fixtures_dir_env else None

    token = get_orcid_token()
    client = OrcidClient(token=token, fixtures_dir=fixtures_dir)
    orcid_id = str(profile.get("orcid_id", DEFAULT_PROFILE["orcid_id"]))

    works_payload = client.get(f"{orcid_id}/works", "works")
    work_summaries = flatten_work_summaries(works_payload)
    if not work_summaries:
        raise RuntimeError(f"No works found in ORCID record {orcid_id}.")

    publications: List[Dict[str, Any]] = []
    seen_put_codes = set()
    for summary in work_summaries:
        put_code = str(summary.get("put-code") or "").strip()
        if not put_code or put_code in seen_put_codes:
            continue
        seen_put_codes.add(put_code)
        work = client.get(f"{orcid_id}/work/{put_code}", f"work_{put_code}")
        doi = extract_doi(work)
        crossref_message = fetch_crossref(doi, fixtures_dir=fixtures_dir)
        publication = build_publication_item(work, crossref_message, profile, overrides)
        publications.append(publication)

    publications = unique_publications(publications)
    publications = sort_publications(publications)
    output = build_output(profile, publications, existing_publications)
    save_yaml(PUBLICATIONS_PATH, output)

    print(f"Wrote {len(publications)} synced outputs to {PUBLICATIONS_PATH.relative_to(ROOT)}")
    print(
        f"Counts: {output['analytics']['journal_articles']} journal, "
        f"{output['analytics']['conference_papers']} conference, "
        f"{output['analytics']['theses']} thesis, "
        f"{output['analytics']['other_outputs']} other"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
