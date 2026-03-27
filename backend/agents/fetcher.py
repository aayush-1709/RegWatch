import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import feedparser
import requests


BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / "data"
CACHE_PATH = CACHE_DIR / "regulations_cache.json"
REFRESH_HOURS = 24


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def _fetch_rss(source: str, feed_url: str, limit: int = 8) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    try:
        parsed = feedparser.parse(feed_url)
        for item in parsed.entries[:limit]:
            title = str(getattr(item, "title", "")).strip()
            summary = str(getattr(item, "summary", "")).strip()
            link = str(getattr(item, "link", "")).strip()
            published = str(getattr(item, "published", "") or getattr(item, "updated", "")).strip()
            if not title:
                continue
            entries.append(
                {
                    "id": f"reg-{uuid4()}",
                    "title": title,
                    "source": source,
                    "risk": "HIGH" if "rbi" in source.lower() else "MEDIUM",
                    "timestamp": _utc_now_iso(),
                    "published": published,
                    "url": link,
                    "summary": re.sub(r"<[^>]+>", "", summary),
                }
            )
    except Exception:
        return []
    return entries


def _fetch_gst_updates(limit: int = 8) -> list[dict[str, Any]]:
    # GST does not provide a stable public RSS across all update categories,
    # so we parse headline links from the public updates page.
    entries: list[dict[str, Any]] = []
    url = "https://www.gst.gov.in/newsandupdates"
    try:
        response = requests.get(url, timeout=12)
        response.raise_for_status()
        html = response.text
        matches = re.findall(r"<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>", html, flags=re.IGNORECASE | re.DOTALL)
        for href, raw_title in matches:
            title = re.sub(r"<[^>]+>", "", raw_title).strip()
            if not title or len(title) < 15:
                continue
            if not any(k in title.lower() for k in ["gst", "advisory", "notification", "circular", "update"]):
                continue
            full_url = href if href.startswith("http") else f"https://www.gst.gov.in{href}"
            entries.append(
                {
                    "id": f"reg-{uuid4()}",
                    "title": title,
                    "source": "GST",
                    "risk": "MEDIUM",
                    "timestamp": _utc_now_iso(),
                    "published": "",
                    "url": full_url,
                    "summary": title,
                }
            )
            if len(entries) >= limit:
                break
    except Exception:
        return []
    return entries


def _fallback_regulations_from_rules() -> list[dict[str, Any]]:
    rules_file = BASE_DIR.parents[0] / "rules" / "regulations.txt"
    regulation_text = ""
    if rules_file.exists():
        regulation_text = rules_file.read_text(encoding="utf-8")
    if not regulation_text.strip():
        regulation_text = (
            "RBI Digital Lending Guidelines Amendment #3:\n"
            "- Loan limit increased to ₹10,00,000\n"
            "- Mandatory video KYC above ₹2,00,000\n"
            "- Interest cap reduced to 21%"
        )
    return [
        {
            "id": f"reg-{uuid4()}",
            "title": "RBI Digital Lending Guidelines Amendment #3",
            "source": "RBI",
            "risk": "HIGH",
            "timestamp": _utc_now_iso(),
            "published": "",
            "url": "",
            "summary": regulation_text[:600],
            "regulation_text": regulation_text,
        }
    ]


def _load_cache() -> dict[str, Any] | None:
    try:
        if not CACHE_PATH.exists():
            return None
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def _save_cache(items: list[dict[str, Any]]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"fetched_at": _utc_now_iso(), "items": items}
    CACHE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_regulations(force_refresh: bool = False) -> list[dict[str, Any]]:
    cache = _load_cache()
    if cache and not force_refresh:
        fetched_at = _parse_time(cache.get("fetched_at"))
        if fetched_at and datetime.now(timezone.utc) - fetched_at < timedelta(hours=REFRESH_HOURS):
            items = cache.get("items") or []
            if isinstance(items, list) and len(items) > 0:
                return items

    rbi_items = _fetch_rss("RBI", "https://www.rbi.org.in/Scripts/RSS.aspx?Id=1")
    sebi_items = _fetch_rss("SEBI", "https://www.sebi.gov.in/sebirss.xml")
    gst_items = _fetch_gst_updates()

    combined = [*rbi_items, *sebi_items, *gst_items]
    if not combined:
        combined = _fallback_regulations_from_rules()

    _save_cache(combined)
    return combined


def fetch_regulation() -> dict:
    """
    Fetch latest regulation item from cached/live sources and return detail text.
    """
    items = fetch_regulations()
    first = items[0] if items else _fallback_regulations_from_rules()[0]
    regulation_text = first.get("regulation_text") or first.get("summary") or first.get("title") or ""
    return {
        "regulation_text": regulation_text,
        "source": first.get("source", "Unknown"),
        "id": first.get("id", f"reg-{uuid4()}"),
        "title": first.get("title", "Untitled Regulation"),
        "timestamp": first.get("timestamp", _utc_now_iso()),
        "url": first.get("url", ""),
    }


class RegulationFetcherAgent:
    def run(self) -> dict:
        return fetch_regulation()
