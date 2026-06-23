from pydantic import Field

from app.enums.input_type import InputType
from app.models.common import DomainModel


class IngestRequest(DomainModel):
    """
    Request model for text-based ingestion.
    """

    input_type: InputType = Field(
        description="Type of input being submitted."
    )

    content: str = Field(
        min_length=1,
        description="Raw input content."
    )


class IngestResponse(DomainModel):
    """
    Response after successful ingestion.
    """

    analysis_id: str = Field(
        description="Generated analysis identifier."
    )

    input_type: InputType = Field(
        description="Detected input type."
    )

    normalized_input: str = Field(
        description="Normalized plain text."
    )