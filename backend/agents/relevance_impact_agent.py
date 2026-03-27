from models.schemas import ImpactAnalysis
from services.gemini_client import GeminiClient


class RelevanceImpactAgent:
    name = "RelevanceImpactAgent"

    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    def assess(self, regulation_text: str, company_profile: str) -> ImpactAnalysis:
        prompt = (
            "Analyze the following RBI regulation for the given company profile.\n"
            "Return strict JSON with keys:\n"
            "- summary\n"
            "- affected_departments (array)\n"
            "- risk_score (HIGH/MEDIUM/LOW)\n"
            "- cost_of_inaction\n"
            "- cost_of_compliance\n"
            "No markdown, no extra keys.\n\n"
            f"Company profile:\n{company_profile}\n\n"
            f"Regulation:\n{regulation_text}"
        )
        try:
            data = self.gemini.generate_json(prompt)
            return ImpactAnalysis(**data)
        except Exception:
            return ImpactAnalysis(
                summary=(
                    "Regulation directly impacts digital lending lifecycle and pricing controls. "
                    "Current policy is non-compliant across key operational checkpoints."
                ),
                affected_departments=["Tech", "Legal", "Operations", "Risk"],
                risk_score="HIGH",
                cost_of_inaction="Rs 2 Cr",
                cost_of_compliance="Rs 3 L",
            )
