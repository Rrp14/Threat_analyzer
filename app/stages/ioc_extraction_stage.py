from app.core.exceptions import ValidationError
from app.core.stage import PipelineStage
from app.models.schemas import PipelineContext
from app.services.ioc_extraction import IOCExtractionService


class IOCExtractionStage(PipelineStage):
    """
    Extract IOCs from normalized input.
    """

    def __init__(
        self,
        service: IOCExtractionService | None = None,
    ) -> None:
        self._service = service or IOCExtractionService()

    @property
    def name(self) -> str:
        return "IOC Extraction"

    def validate(
        self,
        context: PipelineContext,
    ) -> None:

        if not context.normalized_input:
            raise ValidationError(
                message="No normalized input available for IOC extraction."
            )

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        context.iocs = self._service.extract(
            context.normalized_input
        )

        return context