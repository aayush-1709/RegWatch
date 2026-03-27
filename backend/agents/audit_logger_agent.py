from datetime import datetime
from typing import Any, Dict, Optional

from models.schemas import AuditLogEntry
from services.in_memory_store import store


class AuditLoggerAgent:
    name = "AuditLoggerAgent"

    def log(
        self,
        agent_name: str,
        action: str,
        confidence_score: float,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        entry = AuditLogEntry(
            agent_name=agent_name,
            action=action,
            timestamp=datetime.utcnow(),
            confidence_score=max(0.0, min(1.0, confidence_score)),
            details=details or {},
        )
        store.audit_logs.append(entry)
