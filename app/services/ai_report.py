from app.ai.providers.gemini import GeminiProvider
from app.ai.providers.template import TemplateProvider
from app.config import settings
from app.models.report import AIReport
from app.ai.prompts.report_prompt import (
    build_report_prompt,
)


class AIReportService:

    def __init__(self) -> None:

        self._fallback = TemplateProvider()

        self._gemini = (
            GeminiProvider()
            if settings.GEMINI_API_KEY
            else None
        )

        #print("GEMINI_API_KEY =", settings.GEMINI_API_KEY)
        print("Gemini Enabled =", bool(settings.GEMINI_API_KEY))

    def generate(
    self,
    gemini_context: dict,
    template_context: dict,
) -> AIReport:

     if self._gemini:

        try:

            prompt = build_report_prompt(
                gemini_context
            )

            return self._gemini.generate(
                prompt=prompt,
                response_model=AIReport,
            )

        except Exception as exc:

            print(
                "GEMINI FAILED:",
                exc,
            )

     return self._fallback.generate_report(
        template_context
    )