from app.ai.prompts.detection_prompt import (
    build_detection_prompt,
)
from app.ai.providers.detection_template import (
    TemplateDetectionProvider,
)
from app.ai.providers.gemini import (
    GeminiProvider,
)
from app.config import settings
from app.models.detection import (
    DetectionRules,
)
from app.models.pipeline import PipelineContext


class DetectionRuleService:

    def __init__(self) -> None:

        self._fallback = (
            TemplateDetectionProvider()
        )

        self._gemini = (
            GeminiProvider()
            if settings.GEMINI_API_KEY
            else None
        )

    def generate(
        self,
        context: dict,
    ) -> DetectionRules:

        if self._gemini:

            try:

                prompt = (
                    build_detection_prompt(
                        context
                    )
                )

                return (
                    self._gemini.generate(
                        prompt=prompt,
                        response_model=DetectionRules,
                    )
                )

            except Exception as exc:

                print(
                    "DETECTION GEMINI FAILED:",
                    exc,
                )

        return (
            self._fallback.generate_rules(
                context
            )
        )

    def generate_from_context(
        self,
        context: PipelineContext,
    ) -> DetectionRules:

        detection_context = {
            "iocs": [
                ioc.model_dump()
                for ioc in context.iocs
            ],
            "risk_score": (
                context.risk_score.model_dump()
            ),
            "mitre_mappings": [
                mapping.model_dump()
                for mapping in context.mitre_mapping
            ],
        }

        return self.generate(
            detection_context
        )