from typing import Dict, List

from models.schemas import AuditLogEntry, FullAnalysisResponse, RegulationRecord


class InMemoryStore:
    def __init__(self) -> None:
        self.regulations: Dict[str, RegulationRecord] = {}
        self.analysis_results: Dict[str, FullAnalysisResponse] = {}
        self.compliance_register: List[dict] = []
        self.audit_logs: List[AuditLogEntry] = []


store = InMemoryStore()
