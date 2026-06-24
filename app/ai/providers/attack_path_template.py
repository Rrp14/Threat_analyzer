from app.models.attack_path import (
    AttackPathPrediction,
    AttackStage,
)


class TemplateAttackPathProvider:

    def generate(
        self,
        context: dict,
    ) -> AttackPathPrediction:

        return AttackPathPrediction(
            confidence="medium",
            stages=[
                AttackStage(
                    stage="Initial Access",
                    technique_id="T1190",
                    description="Potential exploitation of a public-facing application based on observed CVE activity.",
                    confidence="0.9",
                ),
                AttackStage(
                    stage="Command and Control",
                    technique_id="T1071",
                    description="Observed network communication consistent with command-and-control activity.",
                    confidence="0.7",
                ),
            ],
        )