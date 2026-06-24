import json

from google import genai

from app.ai.prompts.report_prompt import (
    build_report_prompt,
)
from app.ai.providers.base import BaseAIProvider
from app.config import settings
from app.core.exceptions import AIError
from app.models.report import AIReport


class GeminiProvider(BaseAIProvider):

    def __init__(self) -> None:

        if not settings.GEMINI_API_KEY:
            raise AIError(
                "GEMINI_API_KEY not configured"
            )

        self._client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate_report(
        self,
        context: dict,
    ) -> AIReport:

        prompt = build_report_prompt(
            context
        )

        try:

            response = (
                self._client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                )
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = (
                    text
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            return AIReport.model_validate_json(
                text
            )

        except Exception as exc:
            raise AIError(
                f"Gemini report generation failed: {exc}"
            ) from exc