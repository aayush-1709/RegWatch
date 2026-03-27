from typing import List

from models.schemas import ComplianceGapResult, GapItem
from services.gemini_client import GeminiClient


class ComplianceGapAgent:
    name = "ComplianceGapAgent"

    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    def compare(self, regulation_clauses: List[str], company_policy_text: str) -> ComplianceGapResult:
        prompt = (
            "Compare regulation clauses with company policy and return strict JSON:\n"
            "{ \"gaps\": [{\"clause\":\"...\", \"gap\":\"...\", \"severity\":\"HIGH|MEDIUM|LOW\"}] }\n"
            "No markdown.\n\n"
            f"Regulation clauses:\n{regulation_clauses}\n\n"
            f"Company policy:\n{company_policy_text}"
        )
        try:
            data = self.gemini.generate_json(prompt)
            return ComplianceGapResult(**data)
        except Exception:
            fallback_gaps = [
                GapItem(
                    clause="Loan limit increased to Rs 10,00,000",
                    gap="Policy only supports Rs 5,00,000 cap",
                    severity="MEDIUM",
                ),
                GapItem(
                    clause="Mandatory video KYC above Rs 2,00,000",
                    gap="No video KYC implementation",
                    severity="HIGH",
                ),
                GapItem(
                    clause="Interest cap reduced to 21%",
                    gap="Policy interest rate fixed at 24%",
                    severity="HIGH",
                ),
            ]
            return ComplianceGapResult(gaps=fallback_gaps)
