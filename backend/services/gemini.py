import json
import os
import re
from typing import Any

import google.generativeai as genai


MODEL_NAME = "gemini-2.5-flash"


def _extract_json(text: str) -> dict[str, Any] | None:
    clean = text.strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```json\s*(\{.*?\})\s*```", clean, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            return None
    return None


def call_gemini(prompt: str) -> dict:
    try:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            return {"error": "GEMINI_API_KEY is not set"}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)

        final_prompt = (
            "Return ONLY valid JSON object. No markdown or explanations.\n\n"
            f"{prompt}"
        )

        response = model.generate_content(final_prompt)
        text = getattr(response, "text", "") or ""
        parsed = _extract_json(text)
        if parsed is None:
            return {"error": "Gemini response was not valid JSON", "raw_response": text}
        return parsed
    except Exception as exc:
        return {"error": "Gemini call failed", "details": str(exc)}
