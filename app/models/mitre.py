from enum import Enum

from pydantic import BaseModel,ConfigDict,Field

from app.enums.mitre import ConfidenceLevel

from app.models.common import DomainModel



class MITREMapping(DomainModel):


    tactic:str=Field(
        ...,
        min_length=1,
        description="MITRE ATT&CK tactic"
    )

    technique:str=Field(
        ...,
        min_length=1,
        description="MITRE ATT&CK technique name"
    )
    
    id:str=Field(
        ...,
        pattern=r"^T\d{4}(\.\d{3})?$",
        description="MITRE ATT&CK technique ID"
    )

    confidence:ConfidenceLevel=Field(
        default=ConfidenceLevel.MEDIUM,
        description="Confidence Of mapping"
    )

