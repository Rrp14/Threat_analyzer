from app.core.exceptions import ValidationError
from app.core.stage import PipelineStage
from app.models.schemas import PipelineContext
from app.services.detection_rule import (
    DetectionRuleService,
)


class DetectionRuleStage(PipelineStage):

    def __init__(
        self,
        service: DetectionRuleService | None = None,
    ) -> None:

        self._service = (
            service
            if service is not None
            else DetectionRuleService()
        )

    @property
    def name(self) -> str:
        return "Detection Rules"

    def validate(
        self,
        context: PipelineContext,
    ) -> None:

        if not context.iocs:
            raise ValidationError(
                "IOCs required before detection generation."
            )

        if context.risk_score is None:
            raise ValidationError(
                "Risk score required before detection generation."
            )

        if not context.mitre_mapping:
            raise ValidationError(
                "MITRE mappings required before detection generation."
            )

    def execute(
    self,
    context: PipelineContext,
) -> PipelineContext:

     gemini_context = {
        "iocs": [
            {
                "type": ioc.type,
                "value": ioc.value,
                "reputation": ioc.reputation,
            }
            for ioc in context.iocs
        ],
        "risk_score": context.risk_score.score,
        "risk_level": context.risk_score.level,
        "mitre_mappings": [
            {
                "id": mapping.id,
                "tactic": mapping.tactic,
                "technique": mapping.technique,
            }
            for mapping in context.mitre_mapping
        ],
    }

     template_context = {
        "iocs": context.iocs,
        "risk_score": context.risk_score,
        "mitre_mappings": context.mitre_mapping,
    }

     context.detection_rules = (
        self._service.generate(
            gemini_context,
            template_context,
        )
    )

     return context