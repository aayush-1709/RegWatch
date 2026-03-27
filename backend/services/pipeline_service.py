from typing import List

from agents.action_plan_agent import ActionPlanAgent
from agents.audit_logger_agent import AuditLoggerAgent
from agents.compliance_gap_agent import ComplianceGapAgent
from agents.document_parser_agent import DocumentParserAgent
from agents.policy_diff_agent import PolicyDiffAgent
from agents.regulation_fetcher_agent import RegulationFetcherAgent
from agents.relevance_impact_agent import RelevanceImpactAgent
from models.schemas import AnalyzeRequest, FullAnalysisResponse, GapItem, RegulationRecord
from services.config import DEFAULT_COMPANY_POLICY, DEFAULT_COMPANY_PROFILE
from services.gemini_client import GeminiClient
from services.in_memory_store import store


class RegWatchPipelineService:
    def __init__(self) -> None:
        self.gemini = GeminiClient()
        self.logger = AuditLoggerAgent()
        self.fetcher = RegulationFetcherAgent()
        self.parser = DocumentParserAgent(self.gemini)
        self.impact = RelevanceImpactAgent(self.gemini)
        self.gap = ComplianceGapAgent(self.gemini)
        self.action = ActionPlanAgent(self.gemini)
        self.diff = PolicyDiffAgent(self.gemini)

    def run_full_pipeline(self, request: AnalyzeRequest) -> FullAnalysisResponse:
        regulation = self._fetch_or_create_regulation(request.regulation_text)
        self.logger.log(self.fetcher.name, "Fetched latest regulation", 0.93, {"id": regulation.id})

        parsed = self.parser.parse(regulation.raw_text)
        self.logger.log(self.parser.name, "Parsed regulation document", 0.88, {"title": parsed.title})

        impact = self.impact.assess(regulation.raw_text, DEFAULT_COMPANY_PROFILE)
        self.logger.log(self.impact.name, "Assessed relevance and impact", 0.86, {"risk": impact.risk_score})

        company_policy = request.company_policy_text or DEFAULT_COMPANY_POLICY
        gap_result = self.gap.compare(parsed.clauses, company_policy)
        self.logger.log(self.gap.name, "Compared policy with regulation", 0.89, {"gap_count": len(gap_result.gaps)})

        action_plan = self.action.create_plan(gap_result.gaps)
        self.logger.log(self.action.name, "Generated action plan", 0.87, {"action_count": len(action_plan.actions)})

        old_policy = request.old_policy_text or company_policy
        new_policy_text = self._build_new_policy_text(gap_result.gaps)
        diff = self.diff.diff(old_policy, new_policy_text)
        self.logger.log(self.diff.name, "Computed policy diff", 0.85, {"modified": len(diff.modified_lines)})

        timeline = [f"{item.deadline}: {item.step}" for item in action_plan.actions]

        analysis = FullAnalysisResponse(
            regulation_id=regulation.id,
            title=parsed.title,
            summary=impact.summary,
            risk=impact.risk_score,
            impact={
                "cost_of_inaction": impact.cost_of_inaction,
                "cost_of_compliance": impact.cost_of_compliance,
            },
            parsed=parsed,
            gaps=gap_result.gaps,
            actions=action_plan.actions,
            diff=diff,
            timeline=timeline,
        )

        store.analysis_results[regulation.id] = analysis
        store.compliance_register = [
            {
                "regulation_id": regulation.id,
                "title": parsed.title,
                "risk": impact.risk_score,
                "open_gaps": len([g for g in gap_result.gaps if g.severity in ("HIGH", "MEDIUM")]),
                "last_updated": "now",
            }
        ]
        return analysis

    def _fetch_or_create_regulation(self, regulation_text: str | None) -> RegulationRecord:
        if regulation_text:
            regulation = self.fetcher.fetch_latest()
            regulation.raw_text = regulation_text
            store.regulations[regulation.id] = regulation
            return regulation
        regulation = self.fetcher.fetch_latest()
        store.regulations[regulation.id] = regulation
        return regulation

    @staticmethod
    def _build_new_policy_text(gaps: List[GapItem]) -> str:
        base = [
            "Digital lending operations updated for RBI Amendment #3",
            "Loan limit support extended to Rs 10,00,000",
            "Video KYC mandatory above Rs 2,00,000",
            "Interest cap fixed at max 21%",
        ]
        if gaps:
            base.append("Remediation tracked against all identified compliance gaps")
        return "\n".join(base)


pipeline_service = RegWatchPipelineService()
