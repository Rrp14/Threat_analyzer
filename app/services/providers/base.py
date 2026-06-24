from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):

    @property
    @abstractmethod
    def source(self) -> str:
        ...

    @abstractmethod
    def lookup(
        self,
        value: str,
    ) -> Any:
        ...