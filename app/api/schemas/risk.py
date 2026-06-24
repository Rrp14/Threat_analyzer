from pydantic import Field

from app.models.common import DomainModel
from app.models.risk import RiskScore


class RiskResponse(DomainModel):

    analysis_id: str = Field(
        description="Analysis identifier."
    )

    ioc_count: int = Field(
        ge=0,
        description="Number of extracted IOCs."
    )

    risk_score: RiskScore