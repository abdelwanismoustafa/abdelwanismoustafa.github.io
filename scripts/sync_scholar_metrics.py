#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE_PROFILE_PATH = ROOT / "_data" / "site_profile.yml"
USER_AGENT = (
    "Mozilla/5.0 (compatible; abdelwanismoustafa-site-bot/1.0; "
    "+https://abdelwanismoustafa.github.io/)"
)
SCHOLAR_URL = "https://scholar.google.com/citations"

DEFAULT_PROFILE: Dict[str, Any] = {
    "name": "Moustafa Abdelwanis",
    "orcid_id": "0000-0001-5034-2613",
    "profiles": {
        "scholar_url": "https://scholar.google.com/citations?hl=en&user=VwCuh7MAAAAJ",
        "scholar_label": "Google Scholar",
        "scholar_profile_id": "VwCuh7MAAAAJ",
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
    "scholar_metrics": {
        "citations": 197,
        "h_index": 4,
        "i10_index": 3,
        "last_checked": "2026-04-19",
        "source": "Google Scholar public profile",
    },
    "awards": [],
}


def load_yaml(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return default.copy()
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return default.copy()
    loaded = yaml.safe_load(raw)
    if loaded is None:
        return default.copy()
    return loaded


def save_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100, indent=2),
        encoding="utf-8",
    )


def get_profile_id(profile: Dict[str, Any]) -> str:
    direct = str(profile.get("profiles", {}).get("scholar_profile_id", "")).strip()
    if direct:
        return direct
    scholar_url = str(profile.get("profiles", {}).get("scholar_url", "")).strip()
    parsed = urllib.parse.urlparse(scholar_url)
    user = urllib.parse.parse_qs(parsed.query).get("user", [])
    if user and user[0].strip():
        return user[0].strip()
    raise RuntimeError("Could not find scholar_profile_id or user=... in profiles.scholar_url.")


def fetch_profile_html(profile_id: str) -> str:
    url = f"{SCHOLAR_URL}?hl=en&user={urllib.parse.quote(profile_id)}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def clean_int(text: str) -> Optional[int]:
    digits = "".join(ch for ch in text if ch.isdigit())
    if not digits:
        return None
    return int(digits)


def parse_metrics(html_text: str) -> Dict[str, int]:
    soup = BeautifulSoup(html_text, "html.parser")
    table = soup.find("table", id="gsc_rsb_st")
    if table is None:
        raise RuntimeError("Could not find the Google Scholar metrics table on the public profile page.")

    metrics: Dict[str, int] = {}
    for row in table.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        label = cells[0].get_text(" ", strip=True).lower().replace("-", "")
        value = clean_int(cells[1].get_text(" ", strip=True))
        if value is None:
            continue
        if "citation" in label:
            metrics["citations"] = value
        elif "hindex" in label:
            metrics["h_index"] = value
        elif "i10index" in label:
            metrics["i10_index"] = value

    missing = [key for key in ("citations", "h_index", "i10_index") if key not in metrics]
    if missing:
        raise RuntimeError(f"Parsed Google Scholar page but could not extract: {', '.join(missing)}")
    return metrics


def main() -> int:
    profile = load_yaml(SITE_PROFILE_PATH, DEFAULT_PROFILE)
    scholar_profile_id = get_profile_id(profile)

    try:
        html_text = fetch_profile_html(scholar_profile_id)
        metrics = parse_metrics(html_text)
    except Exception as exc:  # noqa: BLE001
        print(
            "Google Scholar sync skipped. "
            "Keeping the previous values in _data/site_profile.yml. "
            f"Reason: {exc}",
            file=sys.stderr,
        )
        return 0

    scholar_metrics = profile.get("scholar_metrics", {}) or {}
    scholar_metrics.update(metrics)
    scholar_metrics["last_checked"] = dt.date.today().isoformat()
    scholar_metrics["source"] = "Google Scholar public profile"
    profile["scholar_metrics"] = scholar_metrics

    profiles = profile.get("profiles", {}) or {}
    profiles.setdefault("scholar_profile_id", scholar_profile_id)
    if not profiles.get("scholar_url"):
        profiles["scholar_url"] = f"{SCHOLAR_URL}?hl=en&user={scholar_profile_id}"
    profile["profiles"] = profiles

    save_yaml(SITE_PROFILE_PATH, profile)
    print(
        "Updated Google Scholar metrics: "
        f"citations={scholar_metrics['citations']}, "
        f"h_index={scholar_metrics['h_index']}, "
        f"i10_index={scholar_metrics['i10_index']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
