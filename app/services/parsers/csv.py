import csv
import io

from app.core.exceptions import IngestionError
from app.enums.input_type import InputType
from app.services.parsers.base import BaseParser


class CSVParser(BaseParser):

    @property
    def supported_input(self) -> InputType:
        return InputType.CSV

    def parse(
        self,
        content: str,
    ) -> str:
        if not isinstance(content, str):
            raise IngestionError(
                message="CSVParser expects string input.",
                details={
                    "received_type": type(content).__name__,
                },
            )

        try:
            reader = csv.reader(io.StringIO(content))

            lines = [
                " ".join(cell.strip() for cell in row if cell.strip())
                for row in reader
            ]

            return "\n".join(lines).strip()

        except csv.Error as exc:
            raise IngestionError(
                message="Invalid CSV input.",
                details={
                    "error": str(exc),
                },
            ) from exc