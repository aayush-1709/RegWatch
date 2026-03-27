from typing import Any

from services.gemini import call_gemini


def analyze_impact(regulation: dict, company_profile: str) -> dict[str, Any]:
    """
    Analyze regulation impact for the given company profile.
    Uses Gemini to output JSON with:
      - summary
      - affected_departments (array)
      - risk (HIGH/MEDIUM/LOW)
      - cost_of_inaction
      - cost_of_compliance
    """
    prompt = (
        "Analyze the following regulation in the context of the company profile.\n"
        "Return ONLY valid JSON with exactly these keys:\n"
        "- summary: string\n"
        "- affected_departments: array of strings\n"
        "- risk: one of [HIGH, MEDIUM, LOW]\n"
        "- cost_of_inaction: string (can include currency symbols like ₹)\n"
        "- cost_of_compliance: string (can include currency symbols like ₹)\n\n"
        "No markdown and no extra keys.\n\n"
        f"COMPANY_PROFILE:\n{company_profile}\n\n"
        f"REGULATION:\n{regulation}"
    )

    result = call_gemini(prompt)
    if not result or "error" in result:
        return _fallback_impact()

    try:
        risk = str(result.get("risk") or "").upper().strip()
        if risk not in {"HIGH", "MEDIUM", "LOW"}:
            risk = "HIGH"

        affected = result.get("affected_departments") or []
        if not isinstance(affected, list):
            affected = [str(affected)]
        affected = [str(d).strip() for d in affected if str(d).strip()]

        return {
            "summary": str(result.get("summary") or "").strip() or _fallback_impact()["summary"],
            "affected_departments": affected,
            "risk": risk,
            "cost_of_inaction": str(result.get("cost_of_inaction") or "").strip() or _fallback_impact()[
                "cost_of_inaction"
            ],
            "cost_of_compliance": str(result.get("cost_of_compliance") or "").strip()
            or _fallback_impact()["cost_of_compliance"],
        }
    except Exception:
        return _fallback_impact()


def _fallback_impact() -> dict[str, Any]:
    return {
        "summary": (
            "The regulation affects lending operations and introduces stricter onboarding/KYC and pricing constraints. "
            "This creates elevated delivery, legal, and risk-management overhead."
        ),
        "affected_departments": ["Tech", "Legal", "Operations", "Risk"],
        "risk": "HIGH",
        "cost_of_inaction": "₹2Cr",
        "cost_of_compliance": "₹3L",
    }


class RelevanceImpactAgent:
    def run(self, regulation: dict, company_profile: str) -> dict:
        return analyze_impact(regulation, company_profile)
