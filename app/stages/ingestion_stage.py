


from app.core.exceptions import ValidationError
from app.core.stage import PipelineStage
from app.models.pipeline import PipelineContext
from app.services.ingestion import InputIngestionService


class IngestionStage(PipelineStage):


    def __init__(self,
                 service:InputIngestionService | None=None
                 )->None:
        self._service=service or InputIngestionService()


    @property
    def name(self)->str:
        return "input Ingestion"

    def validate(
            self,
            context:PipelineContext,
    )->None:
        
        if not context.raw_input:
            raise ValidationError("PipelineContext contains no input")

    def execute(self, context:PipelineContext)->PipelineContext:
        context.normalized_input=self._service.ingest(
            input_type=context.input_type,
            content=context.raw_input
        )


        return context
            
    