from io import BytesIO

from pypdf import PdfReader

from app.core.exceptions import IngestionError
from app.enums.input_type import InputType
from app.services.parsers.base import BaseParser


class PDFParser(BaseParser):
    """
    Parser for PDF documents.
    """

    @property
    def supported_input(self) -> InputType:
        return InputType.PDF

    def parse(
        self,
        content: bytes,
    ) -> str:
        if not isinstance(content, bytes):
            raise IngestionError(
                message="PDFParser expects bytes input.",
                details={
                    "received_type": type(content).__name__,
                },
            )

        try:
            reader = PdfReader(BytesIO(content))

            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

            return text.strip()

        except Exception as exc:
            raise IngestionError(
                message="Failed to parse PDF document.",
                details={
                    "error": str(exc),
                },
            ) from exc