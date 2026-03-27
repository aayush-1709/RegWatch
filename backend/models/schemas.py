from typing import Any

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    regulation_text: str | None = None
    company_policy_text: str | None = None


class AnalyzeResponse(BaseModel):
    message: str
    data: dict[str, Any]
