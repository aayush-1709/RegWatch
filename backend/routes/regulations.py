from fastapi import APIRouter
from agents.fetcher import fetch_regulations
from services import app_state

router = APIRouter(tags=["regulations"])


@router.get("/regulations")
def list_regulations() -> dict:
    items = fetch_regulations()
    return {"items": items}


@router.get("/compliance")
def compliance() -> dict:
    return {"items": app_state.compliance_items}


@router.get("/regulations/last-updates")
def last_updates() -> dict:
    items = fetch_regulations()
    sources = ["RBI", "SEBI", "GST"]

    grouped: dict[str, dict] = {}
    for source in sources:
        source_items = [x for x in items if str(x.get("source", "")).upper().startswith(source)]
        if not source_items:
            grouped[source] = {
                "source": source,
                "last_seen": None,
                "latest_title": "No recent updates found",
                "published": None,
                "url": None,
            }
            continue
        latest = max(source_items, key=lambda x: str(x.get("timestamp", "")))
        grouped[source] = {
            "source": source,
            "last_seen": latest.get("timestamp"),
            "latest_title": latest.get("title"),
            "published": latest.get("published"),
            "url": latest.get("url"),
        }

    return {"items": [grouped[s] for s in sources]}
