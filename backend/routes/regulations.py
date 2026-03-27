from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["regulations"])


@router.get("/regulations")
def list_regulations() -> dict:
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "items": [
            {
                "id": "reg-001",
                "title": "RBI Digital Lending Guidelines Amendment #3",
                "source": "RBI",
                "risk": "HIGH",
                "timestamp": now,
            },
            {
                "id": "reg-002",
                "title": "SEBI Disclosure Circular Update",
                "source": "SEBI",
                "risk": "MEDIUM",
                "timestamp": now,
            },
        ]
    }
