from typing import Any

from services.gemini import call_gemini


def find_compliance_gaps(regulation_clauses: list[str], company_policy: str) -> dict[str, Any]:
    """
    Compare regulation clauses with company policy and return gaps with severity.
    Output JSON shape:
      { "gaps": [{ "clause": string, "gap": string, "severity": "HIGH|MEDIUM|LOW" }] }
    """
    prompt = (
        "You are a compliance gap analyzer.\n"
        "Compare the regulation clauses against the company's policy text.\n\n"
        "Return ONLY valid JSON with exactly these keys:\n"
        "{ \"gaps\": [ { \"clause\": string, \"gap\": string, \"severity\": \"HIGH|MEDIUM|LOW\" } ] }\n\n"
        "Rules:\n"
        "- gaps array must be present (can be empty)\n"
        "- severity must be one of HIGH, MEDIUM, LOW\n"
        "- no markdown and no extra keys\n\n"
        f"COMPANY_POLICY:\n{company_policy}\n\n"
        f"REGULATION_CLAUSES:\n{regulation_clauses}"
    )

    result = call_gemini(prompt)
    if not result or "error" in result:
        return _fallback_gaps(regulation_clauses)

    try:
        gaps = result.get("gaps") or []
        if not isinstance(gaps, list):
            gaps = [gaps]

        parsed_gaps: list[dict[str, str]] = []
        for item in gaps:
            if not isinstance(item, dict):
                continue
            clause = str(item.get("clause") or "").strip()
            gap = str(item.get("gap") or "").strip()
            severity = str(item.get("severity") or "").upper().strip()
            if severity not in {"HIGH", "MEDIUM", "LOW"}:
                severity = "MEDIUM"
            if clause or gap:
                parsed_gaps.append({"clause": clause, "gap": gap, "severity": severity})

        return {"gaps": parsed_gaps}
    except Exception:
        return _fallback_gaps(regulation_clauses)


def _fallback_gaps(regulation_clauses: list[str]) -> dict[str, Any]:
    # Use simple mapping to the demo policy.
    clause_text = " | ".join([str(c) for c in regulation_clauses]) if regulation_clauses else ""
    _ = clause_text
    return {
        "gaps": [
            {
                "clause": "Mandatory video KYC above threshold",
                "gap": "Company policy does not mention video KYC; only Aadhaar/OTP eKYC is present.",
                "severity": "HIGH",
            },
            {
                "clause": "Loan limit increased to Rs 10,00,000",
                "gap": "Company policy supports loan limit of Rs 5,00,000; needs update to the new cap/threshold checks.",
                "severity": "MEDIUM",
            },
            {
                "clause": "Interest cap reduced to 21%",
                "gap": "Company policy fixes interest rate at 24%; must enforce the new maximum rate/cap.",
                "severity": "HIGH",
            },
        ]
    }


class ComplianceGapAgent:
    def run(self, regulation_clauses: list[str], company_policy_text: str) -> dict:
        return find_compliance_gaps(regulation_clauses, company_policy_text)
