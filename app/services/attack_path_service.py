from app.ai.prompts.attack_path_prompt import build_attack_path_prompt
from app.ai.providers.attack_path_template import TemplateAttackPathProvider
from app.ai.providers.gemini import GeminiProvider
from app.config import settings
from app.models.attack_path import AttackPathPrediction
from app.models.attack_step import (
    AttackPath,
)
from app.models.pipeline import PipelineContext


class AttackPathService:

    def __init__(self):

        self._fallback = (
            TemplateAttackPathProvider()
        )

        self._gemini = (
            GeminiProvider()
            if settings.GEMINI_API_KEY
            else None
        )

    def generate(
    self,
    context: dict,
):

     if self._gemini:

        try:

            prompt = build_attack_path_prompt(
                context
            )

            return self._gemini.generate(
                prompt=prompt,
                response_model=AttackPathPrediction,
            )

        except Exception as exc:

            print(
                "ATTACK PATH GEMINI FAILED:",
                exc,
            )

     return self._fallback.generate(
        context
    )    


    def generate_from_context(
    self,
    context: PipelineContext,
) -> AttackPath:

     attack_context = {
        "risk_score": (
            context.risk_score.score
        ),
        "risk_level": (
            context.risk_score.level
        ),
        "cves": [
            cve.model_dump()
            for cve in context.enrichment.cves
        ],
        "mitre_mappings": [
            mapping.model_dump()
            for mapping in context.mitre_mapping
        ],
    }

     return self.generate(
        attack_context
    )    