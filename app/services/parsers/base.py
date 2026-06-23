from abc import ABC, abstractmethod
from typing import Any

from app.enums.input_type import InputType


class BaseParser(ABC):

    """
    Base contract for all input parsers.

    Every parser converts a supported input type into normalized plain text
    for downstream pipeline stages.
    """

    @property
    @abstractmethod
    def supported_input(self)->InputType:
        """
        Return the InputType handled by this parser.
        """
        


        ...

    @abstractmethod
    def parse(
        self,
        content:Any,
    )    ->str:
        ...