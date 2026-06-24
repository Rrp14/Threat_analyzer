from pydantic import Field

from app.models.common import DomainModel
from app.models.detection import DetectionRules


class DetectionResponse(DomainModel):

    analysis_id: str = Field(
        description="Analysis identifier."
    )

    detection_rules: DetectionRules = Field(
        description="Generated detection rules."
    )