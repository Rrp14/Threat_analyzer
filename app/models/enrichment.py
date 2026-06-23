from enum import Enum

from pydantic import BaseModel,ConfigDict,Field

from app.enums.reputation import ReputationLevel
from app.models.common import DomainModel, Score
from app.models.ioc import CVEDetail


class ReputationScore(DomainModel):
    
    score:Score


    level :ReputationLevel

    source:str=Field(
        default="local",
        description="source of reputation data"
         
    )




class EnrichmentData(DomainModel):


    cves:list[CVEDetail]=Field(
        default_factory=list,
        description="Detailed information about detected CVEs."

    )

    malware_families:list[str]=Field(
        default_factory=list,
        description="Associated malware families"
    )

    threat_actors:list[str]=Field(
        default_factory=list,
        description="Known threat actors linked to the indicators"
    )

    reputation_score:dict[str,ReputationScore]=Field(
        default_factory=dict,
        description="Mapping of IOC value to Score"
    )

 



    