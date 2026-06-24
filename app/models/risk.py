from pydantic import BaseModel, ConfigDict, Field

from app.enums.risk import RiskFactorType, RiskLevel

from app.models.common import DomainModel, Score


class RiskFactor(DomainModel):
    factor:RiskFactorType

    score:Score

    description:str=Field(
        ...,
        min_length=1,
        description="explanation of why the score was added"
    )




class RiskScore(DomainModel):

    score:Score 


    level:RiskLevel

    factors:list[RiskFactor]=Field(
        default_factory=list,
        description="risk factors contributing to the final score"

    )

    @property
    def is_low(self)->bool:
        return self.level==RiskLevel.LOW

    @property
    def is_medium(self)->bool:
        return self.level==RiskLevel.MEDIUM
    

    @property 
    def is_high(self) -> bool:
       return self.level == RiskLevel.HIGH

    @property
    def is_critical(self) -> bool:
       return self.level == RiskLevel.CRITICAL
    


    
    @property
    def factor_count(self) -> int:
       return len(self.factors)


    @property
    def total_factor_score(self) -> int:
       return sum(f.score for f in self.factors)
    
    
    
    @property
    def has_factors(self) -> bool:
        return bool(self.factors)
    
    
    
    
    




