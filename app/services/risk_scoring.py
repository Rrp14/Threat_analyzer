import json
import math
from pathlib import Path

from app.enums.risk import (
    RiskFactorType,
    RiskLevel,
)
from app.models.enrichment import EnrichmentData
from app.models.mitre import MITREMapping
from app.models.risk import (
    RiskFactor,
    RiskScore,
)


class RiskScoringService:

    def __init__(
        self,
        rules_path: Path,
    ) -> None:

        with open(
            rules_path,
            encoding="utf-8",
        ) as file:
            self._rules = json.load(file)

    def calculate(
        self,
        enrichment: EnrichmentData,
        mitre_mappings: list[MITREMapping],
    ) -> RiskScore:

        factors: list[RiskFactor] = []

        # ----------------------------
        # IOC Reputation
        # ----------------------------

        for value, reputation in (
            enrichment.reputation_score.items()
        ):

            score = (
                self._rules["reputation"]
                .get(reputation.level, 0)
            )

            if score > 0:

                factors.append(
                    RiskFactor(
                        factor=RiskFactorType.IOC_REPUTATION,
                        score=score,
                        description=(
                            f"{value} reputation "
                            f"is {reputation.level}"
                        ),
                    )
                )

        # ----------------------------
        # CVE Severity
        # ----------------------------

        for cve in enrichment.cves:

            severity_score = (
                self._rules["severity"]
                .get(cve.severity, 0)
            )

            if severity_score > 0:

                factors.append(
                    RiskFactor(
                        factor=RiskFactorType.CVSS,
                        score=severity_score,
                        description=(
                            f"{cve.id} severity "
                            f"is {cve.severity}"
                        ),
                    )
                )

            if cve.exploit_available:

                factors.append(
                    RiskFactor(
                        factor=RiskFactorType.EXPLOIT,
                        score=self._rules[
                            "public_exploit"
                        ],
                        description=(
                            f"Public exploit exists "
                            f"for {cve.id}"
                        ),
                    )
                )

        # ----------------------------
        # MITRE
        # ----------------------------

        for mapping in mitre_mappings:

            score = (
                self._rules["mitre"]
                .get(mapping.id, 0)
            )

            if score > 0:

                factors.append(
                    RiskFactor(
                        factor=RiskFactorType.MITRE,
                        score=score,
                        description=(
                            f"MITRE technique "
                            f"{mapping.id}"
                        ),
                    )
                )

        # ----------------------------
        # Threat Actors
        # ----------------------------

        if enrichment.threat_actors:

            factors.append(
                RiskFactor(
                    factor=RiskFactorType.THREAT_ACTOR,
                    score=self._rules[
                        "threat_actor"
                    ],
                    description=(
                        "Known threat actor detected"
                    ),
                )
            )

        # ----------------------------
        # Malware Families
        # ----------------------------

        if enrichment.malware_families:

            factors.append(
                RiskFactor(
                    factor=RiskFactorType.MALWARE,
                    score=self._rules[
                        "malware_family"
                    ],
                    description=(
                        "Known malware family detected"
                    ),
                )
            )

        # ----------------------------
        # Final Score (0-100)
        # ----------------------------

        raw_score = sum(
            factor.score
            for factor in factors
        )

        total_score = round(
            100
            * (
                1
                - math.exp(
                    -raw_score / 100
                )
            )
        )

        return RiskScore(
            score=total_score,
            level=self._determine_level(
                total_score
            ),
            factors=factors,
        )

    @staticmethod
    def _determine_level(
        score: int,
    ) -> RiskLevel:

        if score <= 30:
            return RiskLevel.LOW

        if score <= 60:
            return RiskLevel.MEDIUM

        if score <= 80:
            return RiskLevel.HIGH

        return RiskLevel.CRITICAL