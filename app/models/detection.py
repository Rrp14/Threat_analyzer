from pydantic import Field

from app.models.common import DomainModel


class SigmaRule(DomainModel):
    title:str=Field(
        ...,
        min_length=1,
        description="human readable sigma rule title"


    )

    yaml:str=Field(
        ...,
        min_length=1 ,
        description= "complete sigma rule in yaml format"


    )

class YaraRule(DomainModel):
  

    rule_name: str = Field(
        ...,
        min_length=1,
        description="YARA rule name.",
    )

    source: str = Field(
        ...,
        min_length=1,
        description="Complete YARA rule source code.",
    )   


class SIEMQuery(DomainModel):
 

    platform: str = Field(
        ...,
        min_length=1,
        description="Target SIEM platform.",
    )

    query: str = Field(
        ...,
        min_length=1,
        description="Detection query for the platform.",
    )


class DetectionRules(DomainModel):

    sigma:SigmaRule | None =Field(
        default=None,
        description="Generated Sigma rules"
    )

    yara:YaraRule|None=Field(
        default=None,
        description="generated YARA rules"

    )

    siem_queires:list[SIEMQuery]=Field(
        default_factory=dict,
        description="Platform specific SIEM queries"

    )

    @property
    def has_sigma(self)->bool:
        return self.sigma is not None
    
    @property
    def has_yara(self)->bool:
        return self.yara is not None    
    
    @property
    def has_siem_queries(self) -> bool:
       return bool(self.siem_queries)


    @property
    def total_queries(self) -> int:
       return len(self.siem_queries)
    
    