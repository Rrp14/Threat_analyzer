from abc import ABC,abstractmethod
from app.models.schemas import PipelineContext

class PipelineStage(ABC):

    @property
    @abstractmethod
    def name(self)->str:
        ...

    @abstractmethod
    def execute(
        self,
        context:PipelineContext,

    )->PipelineContext:
        ...

    def validate(
            self,
            context:PipelineContext
    ) ->None:
        
        pass


    def rollback(
            self,
            context:PipelineContext,

    )->None:
        pass