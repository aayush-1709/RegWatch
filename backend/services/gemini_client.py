import json
import re
from typing import Any, Dict

import google.generativeai as genai

from services.config import GEMINI_API_KEY, GEMINI_MODEL_NAME


class GeminiClient:
    def __init__(self) -> None:
        self.enabled = bool(GEMINI_API_KEY)
        if self.enabled:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        else:
            self.model = None

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        if not self.enabled or self.model is None:
            raise RuntimeError("Gemini not configured. Set GEMINI_API_KEY.")

        response = self.model.generate_content(prompt)
        text = getattr(response, "text", "") or ""
        parsed = self._extract_json(text)
        if parsed is None:
            raise ValueError("Gemini returned non-JSON response.")
        return parsed

    @staticmethod
    def _extract_json(text: str) -> Dict[str, Any] | None:
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
