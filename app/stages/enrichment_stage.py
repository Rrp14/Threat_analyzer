from pathlib import Path

from app.core.exceptions import ValidationError
from app.core.stage import PipelineStage
from app.models.schemas import PipelineContext
from app.services.enrichment import EnrichmentService
from app.services.providers.cve_provider import (
    LocalCVEProvider,
)
from app.services.providers.reputation_provider import (
    LocalReputationProvider,
)


class EnrichmentStage(PipelineStage):

    def __init__(
        self,
        service: EnrichmentService | None = None,
    ) -> None:

      

        self._service =(
            service
            if service is not None
            else self._build_service()
        )


    
    @staticmethod
    def _build_service() -> EnrichmentService:
        reputation_provider = LocalReputationProvider(
        Path("data/ioc_reputation.json")
    )

        cve_provider = LocalCVEProvider(
        Path("data/cve_lookup.json")
    )

        return EnrichmentService(
        reputation_provider=reputation_provider,
        cve_provider=cve_provider,
    )    

    @property
    def name(self) -> str:
        return "Enrichment"

    def validate(
        self,
        context: PipelineContext,
    ) -> None:

        if not context.iocs:
            raise ValidationError(
                "No IOCs available for enrichment."
            )

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        context.enrichment = self._service.enrich(
            context.iocs
        )

        #"""temporary"""
        #print("\n===enriched iocs===")
        #print(context.iocs)

        #print("\n===enrichment data===")
        #print(context.enrichment)



        return context