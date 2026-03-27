import random
from datetime import datetime
from typing import Any

# In-memory audit log store for demo purposes.
audit_logs: list[dict[str, Any]] = []


def log_action(agent_name: str, action: str, output: Any) -> None:
    """
    Append an audit event to the in-memory store.

    Stored fields:
      - agent_name
      - timestamp (UTC ISO string)
      - action_summary (short summary derived from `output`)
      - confidence_score (random for demo)
    """
    # Derive a short, stable summary for UI consumption.
    out_str = ""
    try:
        out_str = str(output)
    except Exception:
        out_str = "<unserializable output>"

    action_summary = out_str.strip()
    if len(action_summary) > 300:
        action_summary = action_summary[:300] + "..."

    audit_logs.append(
        {
            "agent_name": agent_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "action_summary": action_summary,
            "confidence_score": random.uniform(0.7, 0.99),
        }
    )


def get_logs() -> list[dict[str, Any]]:
    return audit_logs


class AuditLoggerAgent:
    def log(self, agent_name: str, action: str, confidence: float | None = None, output: Any = None) -> None:
        # Keep backward compatibility with earlier agent interface.
        _ = confidence
        log_action(agent_name=agent_name, action=action, output=output)
