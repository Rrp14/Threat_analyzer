from pydantic import BaseModel


class AttackStep(BaseModel):
    order: int
    tactic: str
    technique: str
    reasoning: str


class AttackPath(BaseModel):
    confidence: int
    steps: list[AttackStep]