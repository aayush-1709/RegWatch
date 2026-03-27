from typing import Any, Dict

from models.schemas import ParsedRegulation
from services.gemini_client import GeminiClient


class DocumentParserAgent:
    name = "DocumentParserAgent"

    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    def parse(self, regulation_text: str) -> ParsedRegulation:
        prompt = (
            "You are a regulatory document parser.\n"
            "Extract and return strict JSON with keys: title, effective_date, clauses.\n"
            "Rules:\n"
            "- clauses must be a string array\n"
            "- no markdown\n"
            "- do not add extra keys\n\n"
            f"Regulation text:\n{regulation_text}"
        )

        try:
            data = self.gemini.generate_json(prompt)
            return ParsedRegulation(**data)
        except Exception:
            return self._fallback_parse(regulation_text)

    @staticmethod
    def _fallback_parse(regulation_text: str) -> ParsedRegulation:
        lines = [line.strip("- ").strip() for line in regulation_text.splitlines() if line.strip()]
        title = lines[0].rstrip(":") if lines else "Unknown Regulation"
        clauses = [line for line in lines[1:] if line]
        return ParsedRegulation(
            title=title,
            effective_date="Immediate",
            clauses=clauses,
        )
