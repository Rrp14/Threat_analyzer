from abc import ABC, abstractmethod

from app.models.report import AIReport


class BaseAIProvider(ABC):

    @abstractmethod
    def generate_report(
        self,
        context: dict,
    ) -> AIReport:
        ...