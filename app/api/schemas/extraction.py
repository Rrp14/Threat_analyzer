from pydantic import Field

from app.enums.ioc import IOCType
from app.enums.reputation import Reputation
from app.models.common import Confidence, DomainModel


class IOCResponse(DomainModel):
    """
    API representation of an extracted IOC.
    """

    type: IOCType = Field(
        description="IOC category."
    )

    value: str = Field(
        description="Extracted IOC value."
    )

    reputation: Reputation = Field(
        description="Current IOC reputation."
    )

    enriched: bool = Field(
        description="Whether enrichment has been completed."
    )

    confidence: Confidence = Field(
        description="Extraction confidence score."
    )


class ExtractionResponse(DomainModel):
    """
    Response model for IOC extraction.
    """

    analysis_id: str = Field(
        description="Analysis identifier."
    )

    ioc_count: int = Field(
        ge=0,
        description="Number of extracted IOCs."
    )

    iocs: list[IOCResponse] = Field(
        default_factory=list,
        description="Extracted Indicators of Compromise."
    )