from pathlib import Path

from app.core.exceptions import ValidationError
from app.core.stage import PipelineStage
from app.models.schemas import PipelineContext
from app.services.mitre_mapping import MitreMappingService
from app.services.providers.mitre_provider import (
    LocalMitreProvider,
)


class MitreMappingStage(PipelineStage):

    def __init__(
        self,
        service: MitreMappingService | None = None,
    ) -> None:

        self._service = (
            service
            if service is not None
            else self._build_service()
        )

    @staticmethod
    def _build_service() -> MitreMappingService:

        provider = LocalMitreProvider(
            Path("data/mitre_attack.json")
        )

        return MitreMappingService(
            provider=provider
        )

    @property
    def name(self) -> str:
        return "MITRE Mapping"

    def validate(
        self,
        context: PipelineContext,
    ) -> None:

        if not context.iocs:
            raise ValidationError(
                "No IOCs available for MITRE mapping."
            )

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        context.mitre_mapping = (
            self._service.map_iocs(
                context.iocs
            )
        )

        #print("\n=== MITRE MAPPINGS ===")
        #print(context.mitre_mapping)

        return context