from uuid import uuid4
from app.core.exceptions import PipelineError, ValidationError
from app.core.exceptions import ThreatIntelError
from app.core.logger import get_logger
from app.core.pipeline import Pipeline
from app.core.stage import PipelineStage
from app.enums.input_type import InputType
from app.models.schemas import PipelineContext
from app.stages.ingestion_stage import IngestionStage
from app.stages.ioc_extraction_stage import IOCExtractionStage
from app.stages.enrichment_stage import EnrichmentStage


class ThreatAnalysisOrchestrator:


    def __init__(self)->None:
        self._logger=get_logger(__name__)
        self._stages:list[PipelineStage]=[]
        self._register_default_stages()

    def _register_default_stages(self) -> None:

       self.register_stage(IngestionStage())
       self.register_stage(IOCExtractionStage())
       self.register_stage(EnrichmentStage())

    def register_stage(
            self,
            stage:PipelineStage,

    )    ->None:
        
        if not isinstance(stage,PipelineStage):
            raise ValidationError(
                "Only PipelineStage instance can be registered"

            )
        self._stages.append(stage)


    def _build_pipeline(self)->Pipeline:
        pipeline=Pipeline()

        for stage in self._stages:
            pipeline.add_stage(stage)

        return pipeline

    def _generate_analysis_id(self)->str:
        return str(uuid4())

    def analyze(
            self,
            raw_input:str |bytes,
            input_type:InputType,
    )  ->PipelineContext:

        context=PipelineContext(
            analysis_id=self._generate_analysis_id(),
            input_type=input_type,
            raw_input=raw_input

        )  


        if not self._stages:
            raise PipelineError(
                "No stages registered in orchestrator"
            )


        pipeline=self._build_pipeline()

        self._logger.info(
            "Threat analysis started",
            analysis_id=context.analysis_id
        )

        try:
            context=pipeline.execute(context)

            self._logger.info(
                "Threat analysis completed",
                analysis_id=context.analysis_id

            )

            return context
        
        except ThreatIntelError:
            self._logger.exception(
                "Threat analysis failed",
                analysis_id=context.analysis_id
            )

            raise

    @property
    def stages(self) -> tuple[PipelineStage, ...]:
       """
       Return registered stages.
    """
       return tuple(self._stages)    

        
