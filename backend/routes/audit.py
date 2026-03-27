from fastapi import APIRouter

from agents.audit_logger import get_logs

router = APIRouter(tags=["audit"])


@router.get("/audit-logs")
def audit_logs() -> dict:
    return {"items": get_logs()}
