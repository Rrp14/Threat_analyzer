from pydantic import Field

from app.models.common import Confidence, DomainModel


class AttackStage(DomainModel):


    stage: str = Field(
        ...,
        min_length=1,
        description="Attack stage name.",
    )

    technique_id: str = Field(
        ...,
        pattern=r"^T\d{4}(\.\d{3})?$",
        description="MITRE ATT&CK technique ID.",
    )

    description: str = Field(
        ...,
        min_length=1,
        description="Description of the attack stage.",
    )

    confidence: Confidence