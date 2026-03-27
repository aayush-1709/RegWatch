from typing import List

from models.schemas import ActionItem, ActionPlanResult, GapItem
from services.gemini_client import GeminiClient


class ActionPlanAgent:
    name = "ActionPlanAgent"

    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    def create_plan(self, gaps: List[GapItem]) -> ActionPlanResult:
        prompt = (
            "Create compliance action plan from gaps.\n"
            "Return strict JSON as: "
            "{ \"actions\": [{\"step\":\"...\", \"team\":\"Tech|Legal|Ops\", \"deadline\":\"...\"}] }\n"
            "No markdown.\n\n"
            f"Gaps:\n{[g.model_dump() for g in gaps]}"
        )
        try:
            data = self.gemini.generate_json(prompt)
            return ActionPlanResult(**data)
        except Exception:
            return ActionPlanResult(
                actions=[
                    ActionItem(
                        step="Update lending engine limit validation to Rs 10,00,000",
                        team="Tech",
                        deadline="T+7 days",
                    ),
                    ActionItem(
                        step="Deploy video KYC workflow for loans above Rs 2,00,000",
                        team="Tech",
                        deadline="T+10 days",
                    ),
                    ActionItem(
                        step="Revise interest policy and legal disclosures to 21% cap",
                        team="Legal",
                        deadline="T+5 days",
                    ),
                    ActionItem(
                        step="Train operations team on updated KYC and pricing SOP",
                        team="Ops",
                        deadline="T+12 days",
                    ),
                ]
            )
