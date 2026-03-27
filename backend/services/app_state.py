from typing import Any

# Shared in-memory state for latest analysis and derived dashboard tables.
latest_analysis: dict[str, Any] | None = None
compliance_items: list[dict[str, Any]] = []
