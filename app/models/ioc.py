from pydantic import Field
from app.enums.ioc import IOCType, Severity
from app.enums.reputation import Reputation
from app.models.common import Confidence, DomainModel



class IOC(DomainModel):

    type:IOCType=Field(
        description="IOC category"
    )

    value:str=Field(
        min_length=1,
        description="Actual IOC value",
    )

    reputation:Reputation=Field(
        default=Reputation.UNKNOWN,
        description="Current repuation of IOC"
    )

    enriched:bool=Field(
        default=False,
        description="whether enrichment has been completed"
    )

    confidence:Confidence



class CVEDetail(DomainModel):

    id:str=Field(
        ...,
        pattern=r"^CVE-\d{4}-\d{4,}$",
        description="CVE identifier"
    )    

    cvss: float=Field(
        ...,
        ge=0.0,
        le=10.0,
        description="CVSS score",
    )

    severity:Severity=Field(
        ...,
        description="Calculated severity",
    )

    description:str=Field(
        ...,
        description="Description of vulnerbility"
    )


    exploit_available:bool=Field(
        default=False,
        description="Whether a public exploit exists"
    )

    affected_products:list[str]=Field(
        default_factory=list,
        description="Affected software/products"
    )


   






