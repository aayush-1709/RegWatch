from datetime import datetime
from uuid import uuid4

from models.schemas import RegulationMetadata, RegulationRecord
from services.config import DEFAULT_REGULATION_TEXT


class RegulationFetcherAgent:
    name = "RegulationFetcherAgent"

    def fetch_latest(self) -> RegulationRecord:
        regulation_id = str(uuid4())
        title = "RBI Digital Lending Guidelines Amendment #3"
        return RegulationRecord(
            id=regulation_id,
            title=title,
            raw_text=DEFAULT_REGULATION_TEXT,
            metadata=RegulationMetadata(
                source="RBI (demo hardcoded feed)",
                detected_at=datetime.utcnow(),
            ),
        )
