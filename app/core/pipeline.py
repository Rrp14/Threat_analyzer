from app.core.exceptions import ValidationError
from app.core.logger import get_logger
from app.core.stage import PipelineStage
from app.models.schemas import PipelineContext


class Pipeline:

    def __init__(self)->None:
        self._stages=list[PipelineStage]=[]
        self._logger=get_logger(__name__)


    def add_stage(self,stage:PipelineStage)->None:

        if not isinstance(stage,PipelineStage):
            raise ValidationError(
                "Only PipelineStage instances can be added to pipeline"
            )

        self._stages.append(stage)   


    def remove_stage(self,stage:PipelineStage)->None:

        try:

           self._stages.remove(stage)
        except ValueError:
            raise ValidationError(
                f"Stage '{stage.name} is not registered"
            )   


    def clear(self)->None:

        self._stages.clear()

    @property
    def stage_count(self)->int:
        return len(self._stages)
    
    def execute(
            self,
            context:PipelineContext,
            
    )->PipelineContext:

        self._logger.info(
            "pipeline execution started",
            stage_count=self.stage_count,
            analysis_id=context.analysis_id
        )            


        for stage in self._stages:
            self._logger.info(
                "Executing pipeline stage",
                stage=stage.name,
            )

            stage.validate(context)
            context=stage.execute(context)

            self._logger.info(
                "completed stage",
                stage=stage.name
            )

        self._logger.info(
            "pipeline execution completed",
            analysis_id=context.analysis_id
        )    



        return context     