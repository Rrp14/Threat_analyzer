from io import BytesIO

from docx import Document

from app.core.exceptions import IngestionError
from app.enums.input_type import InputType
from app.services.parsers.base import BaseParser


class DOCXParser(BaseParser):
    """
    Parser for Microsoft Word (.docx) documents.
    """

    @property
    def supported_input(self) -> InputType:
        return InputType.DOCX

    def parse(
        self,
        content: bytes,
    ) -> str:
        if not isinstance(content, bytes):
            raise IngestionError(
                message="DOCXParser expects bytes input.",
                details={
                    "received_type": type(content).__name__,
                },
            )

        try:
            document = Document(BytesIO(content))

            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            ).strip()

        except Exception as exc:
            raise IngestionError(
                message="Failed to parse DOCX document.",
                details={
                    "error": str(exc),
                },
            ) from exc