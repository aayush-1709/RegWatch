from fastapi import APIRouter

from models.schemas import AnalyzeRequest
from agents.audit_logger import log_action

from agents.action import generate_action_plan
from agents.diff import generate_policy_diff
from agents.fetcher import fetch_regulation
from agents.gap import find_compliance_gaps
from agents.impact import analyze_impact
from agents.parser import parse_regulation

from pathlib import Path

router = APIRouter(tags=["analyze"])


@router.post("/analyze")
def analyze(payload: AnalyzeRequest) -> dict:
    # Company profile is hardcoded for demo.
    company_profile = "NBFC providing digital lending services in India"

    default_company_policy = ""
    try:
        rules_path = Path(__file__).resolve().parents[2] / "rules" / "company_policy.txt"
        if rules_path.exists():
            default_company_policy = rules_path.read_text(encoding="utf-8")
    except Exception:
        default_company_policy = ""

    company_policy_text = payload.company_policy_text or default_company_policy
    if not company_policy_text.strip():
        # If nothing provided, still proceed with a minimal policy string.
        company_policy_text = "Loan limit ₹5,00,000, no video KYC, interest rate 24%"

    # 1) Fetch regulation
    fetched = fetch_regulation()
    log_action(agent_name="RegulationFetcherAgent", action="fetch_regulation", output=fetched)

    regulation_text = payload.regulation_text or fetched.get("regulation_text", "")
    regulation_text = regulation_text if regulation_text else fetched.get("regulation_text", "")

    # 2) Parse regulation
    parsed = parse_regulation(regulation_text)
    log_action(agent_name="DocumentParserAgent", action="parse_regulation", output=parsed)

    # 3) Analyze impact
    regulation_for_impact = {"raw_text": regulation_text, **parsed}
    impact = analyze_impact(regulation_for_impact, company_profile)
    log_action(agent_name="RelevanceImpactAgent", action="analyze_impact", output=impact)

    # 4) Find compliance gaps
    clauses = parsed.get("clauses") or []
    gap_result = find_compliance_gaps(clauses, company_policy_text)
    log_action(agent_name="ComplianceGapAgent", action="find_compliance_gaps", output=gap_result)

    gaps = gap_result.get("gaps") or []

    # 5) Generate action plan
    action_plan_result = generate_action_plan(gaps)
    log_action(agent_name="ActionPlanAgent", action="generate_action_plan", output=action_plan_result)

    actions = action_plan_result.get("actions") or []

    # 6) Generate policy diff
    # For demo: create a "new" policy by appending AI updates driven by generated actions.
    old_policy = company_policy_text
    updates = "\n".join([f"- {a.get('step')}" for a in actions if isinstance(a, dict) and a.get("step")])
    new_policy = (
        old_policy
        + "\n\n[AI-Generated Updates]\n"
        + (updates if updates.strip() else "- (no new actions generated)")
    )

    diff_result = generate_policy_diff(old_policy, new_policy)
    log_action(agent_name="PolicyDiffAgent", action="generate_policy_diff", output=diff_result)

    # 7) Return final structured JSON
    return {
        "summary": impact.get("summary", ""),
        "risk": impact.get("risk", "HIGH"),
        "impact": {
            "cost_of_inaction": impact.get("cost_of_inaction", ""),
            "cost_of_compliance": impact.get("cost_of_compliance", ""),
        },
        "gaps": gaps,
        "actions": actions,
        "diff": diff_result,
    }
