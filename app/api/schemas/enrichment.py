from pydantic import Field

from app.models.common import DomainModel
from app.models.enrichment import ReputationScore
from app.models.ioc import CVEDetail


class EnrichmentResponse(DomainModel):

    analysis_id: str = Field(
        description="Analysis identifier."
    )

    ioc_count: int = Field(
        ge=0,
        description="Number of IOCs processed during enrichment."
    )

    cves: list[CVEDetail] = Field(
        default_factory=list,
        description="Enriched CVE details."
    )

    reputation_scores: dict[str, ReputationScore] = Field(
        default_factory=dict,
        description="IOC reputation results."
    )