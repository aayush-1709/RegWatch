from typing import Any

from services.gemini import call_gemini


def generate_action_plan(gaps: list[dict]) -> dict[str, Any]:
    """
    Generate a step-by-step compliance action plan from gaps.

    Returns:
      { "actions": [ { "step": string, "team": string, "deadline": string } ] }
    """
    prompt = (
        "You are an action planning agent for regulatory compliance.\n"
        "Given the following compliance gaps, create a step-by-step remediation plan.\n\n"
        "Return ONLY valid JSON with exactly these keys:\n"
        "{ \"actions\": [ { \"step\": string, \"team\": string, \"deadline\": string } ] }\n\n"
        "Rules:\n"
        "- actions must be an array (can be empty)\n"
        "- team should be one of: Tech, Legal, Ops\n"
        "- deadline should be a human-readable string (e.g., \"T+7 days\")\n"
        "- no markdown and no extra keys\n\n"
        f"GAPS:\n{gaps}"
    )

    result = call_gemini(prompt)
    if not result or "error" in result:
        return _fallback_action_plan(gaps)

    try:
        actions = result.get("actions") or []
        if not isinstance(actions, list):
            actions = [actions]

        parsed_actions: list[dict[str, str]] = []
        for item in actions:
            if not isinstance(item, dict):
                continue
            step = str(item.get("step") or "").strip()
            team = str(item.get("team") or "").strip()
            deadline = str(item.get("deadline") or "").strip()
            if team not in {"Tech", "Legal", "Ops"}:
                # Default to Ops when team is unclear.
                team = "Ops"
            if step and deadline:
                parsed_actions.append({"step": step, "team": team, "deadline": deadline})

        return {"actions": parsed_actions}
    except Exception:
        return _fallback_action_plan(gaps)


def _fallback_action_plan(gaps: list[dict]) -> dict[str, Any]:
    gap_count = len(gaps) if gaps else 0
    base_deadline = "T+7 days"
    if gap_count >= 3:
        base_deadline = "T+5 days"

    actions = [
        {
            "step": "Update lending engine constraints (loan limits + KYC thresholds) and validation rules",
            "team": "Tech",
            "deadline": base_deadline,
        },
        {
            "step": "Implement video KYC workflow for loans above the required threshold",
            "team": "Tech",
            "deadline": "T+10 days",
        },
        {
            "step": "Revise interest/pricing logic to enforce the regulatory interest cap and update disclosures",
            "team": "Legal",
            "deadline": "T+7 days",
        },
        {
            "step": "Train Operations on updated KYC/pricing SOPs and update audit-ready documentation",
            "team": "Ops",
            "deadline": "T+12 days",
        },
    ]
    return {"actions": actions}


class ActionPlanAgent:
    def run(self, gaps: list[dict]) -> dict:
        return generate_action_plan(gaps)
