from abc import ABC, abstractmethod

from app.models.report import AIReport


class BaseAIProvider(ABC):

    @abstractmethod
    def generate(
        self,
        *,
        prompt:str,
        response_model:type
    ) -> AIReport:
        ...