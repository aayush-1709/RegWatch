from typing import Any

from services.gemini import call_gemini


def parse_regulation(text: str) -> dict[str, Any]:
    """
    Parse a regulation text using Gemini into:
      - title
      - clauses
      - effective_date
    Returns strict JSON-like dict. Errors are handled safely with fallback.
    """
    prompt = (
        "You are a regulatory document parser. Extract fields from the regulation text.\n\n"
        "Return ONLY valid JSON with exactly these keys:\n"
        "- title: string\n"
        "- clauses: array of strings (each bullet/requirement line)\n"
        "- effective_date: string (if unknown, use \"Unknown\")\n\n"
        "Do not include markdown and do not include extra keys.\n\n"
        f"REGULATION_TEXT:\n{text}"
    )

    result = call_gemini(prompt)
    if not result or "error" in result:
        return _fallback_parse(text)

    try:
        title = str(result.get("title") or "").strip()
        clauses = result.get("clauses") or []
        if not isinstance(clauses, list):
            clauses = [str(clauses)]
        clauses = [str(c).strip() for c in clauses if str(c).strip()]
        effective_date = str(result.get("effective_date") or "Unknown").strip()

        return {
            "title": title or "Unknown Regulation",
            "clauses": clauses,
            "effective_date": effective_date or "Unknown",
        }
    except Exception:
        return _fallback_parse(text)


def _fallback_parse(text: str) -> dict[str, Any]:
    # Very simple heuristic fallback: first line as title and bullet lines as clauses.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = lines[0].rstrip(":") if lines else "Unknown Regulation"
    clauses = []
    for line in lines[1:]:
        cleaned = line.lstrip("-•").strip()
        if cleaned:
            clauses.append(cleaned)
    return {"title": title, "clauses": clauses, "effective_date": "Unknown"}


class DocumentParserAgent:
    def run(self, regulation_text: str) -> dict:
        return parse_regulation(regulation_text)
