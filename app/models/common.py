from pydantic import BaseModel, ConfigDict,Field


from typing import Annotated

Score=Annotated[int,Field(ge=0,le=100)]
Confidence=Annotated[float,Field(ge=0.0,le=1.0)]



class DomainModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )

    def to_dict(self) -> dict:
        return self.model_dump()

    def to_json(self) -> str:
        return self.model_dump_json()