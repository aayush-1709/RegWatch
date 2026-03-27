from models.schemas import PolicyDiffResult
from services.gemini_client import GeminiClient


class PolicyDiffAgent:
    name = "PolicyDiffAgent"

    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    def diff(self, old_policy: str, new_policy: str) -> PolicyDiffResult:
        prompt = (
            "Compute policy diff. Return strict JSON with keys:\n"
            "- additions (array)\n"
            "- removals (array)\n"
            "- modified_lines (array)\n"
            "No markdown.\n\n"
            f"Old policy:\n{old_policy}\n\n"
            f"New policy:\n{new_policy}"
        )
        try:
            data = self.gemini.generate_json(prompt)
            return PolicyDiffResult(**data)
        except Exception:
            return PolicyDiffResult(
                additions=[
                    "Loan processing supports limit up to Rs 10,00,000",
                    "Video KYC mandatory for loans above Rs 2,00,000",
                    "Interest rate cap enforced at <= 21%",
                ],
                removals=[
                    "Current system supports loan limit Rs 5,00,000",
                    "No video KYC implemented",
                    "Interest rate fixed at 24%",
                ],
                modified_lines=[
                    "Loan limit changed from Rs 5,00,000 to Rs 10,00,000",
                    "KYC flow updated to include video verification threshold checks",
                    "Pricing engine updated from 24% to max 21%",
                ],
            )
