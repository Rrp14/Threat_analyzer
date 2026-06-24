from pydantic import Field

from app.models.common import DomainModel
from app.models.report import AIReport


class ReportResponse(DomainModel):

    analysis_id: str = Field(
        description="Analysis identifier."
    )

    ioc_count: int = Field(
        ge=0,
        description="Number of extracted IOCs."
    )

    report: AIReport