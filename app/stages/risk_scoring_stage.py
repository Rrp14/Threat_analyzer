from pathlib import Path

from app.core.exceptions import ValidationError
from app.core.stage import PipelineStage
from app.models.schemas import PipelineContext
from app.services.risk_scoring import (
    RiskScoringService,
)


class RiskScoringStage(PipelineStage):

    def __init__(
        self,
        service: RiskScoringService | None = None,
    ) -> None:

        self._service = (
            service
            if service is not None
            else self._build_service()
        )

    @staticmethod
    def _build_service() -> RiskScoringService:

        return RiskScoringService(
            Path("data/risk_rules.json")
        )

    @property
    def name(self) -> str:
        return "Risk Scoring"

    def validate(
        self,
        context: PipelineContext,
    ) -> None:

        if context.enrichment is None:
            raise ValidationError(
                "Enrichment data required for risk scoring."
            )

        if not context.mitre_mapping:
            raise ValidationError(
                "MITRE mappings required for risk scoring."
            )

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        context.risk_score = (
            self._service.calculate(
                enrichment=context.enrichment,
                mitre_mappings=context.mitre_mapping,
            )
        )

        #print("\n=== RISK SCORE ===")
        #print(context.risk_score)

        return context