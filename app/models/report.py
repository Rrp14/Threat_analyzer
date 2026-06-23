from pydantic import Field

from app.enums.priority import Priority
from app.models.common import DomainModel


class Recommendation(DomainModel):


    title:str=Field(
        ...,
        min_length=1,
        description="short title of the recommnedation"


    )


    description:str=Field(
        ...,
        min_length=1,
        description="detailed recommendation"

    )


    priority:Priority=Field(
        default=Priority.MEDIUM,
        description="Recommendation priority"
    )
    


class AIReport(DomainModel):

        summary:str=Field(
            ...,
            description="Short executive summary"




        )

        analysis_overview: str = Field(
        ...,
        description="Detailed analysis of the threat.",
    )

        attack_scenario: str = Field(
        ...,
        description="Likely attack scenario.",
    )

        business_impact: str = Field(
        ...,
        description="Business impact assessment.",
    )

        immediate_actions: list[Recommendation] = Field(
        default_factory=list,
        description="Immediate response actions.",
    )

        long_term_remediation: list[Recommendation] = Field(
        default_factory=list,
        description="Long-term remediation recommendations.",
    )

        monitoring: list[Recommendation] = Field(
        default_factory=list,
        description="Monitoring recommendations.",
    )
        

        @property
        def total_recommendation(self)->int:
              return(
                    len(self.immediate_actions)
                    +len(self.long_term_remediation)
                    +len(self.monitoring)
              )
        
        @property
        def has_recommendation(self)->bool:
              return self.total_recommendation>0
        
    

        