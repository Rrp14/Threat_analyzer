from pydantic import Field

from app.models.common import DomainModel
from app.models.mitre import MITREMapping


class MitreResponse(DomainModel):

    analysis_id: str = Field(
        description="Analysis identifier."
    )

    ioc_count: int = Field(
        ge=0,
        description="Number of extracted IOCs."
    )

    mapping_count: int = Field(
        ge=0,
        description="Number of MITRE mappings."
    )

    mappings: list[MITREMapping] = Field(
        default_factory=list,
        description="Mapped MITRE ATT&CK techniques."
    )