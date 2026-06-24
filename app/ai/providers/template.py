from app.enums.priority import Priority
from app.enums.risk import RiskLevel
from app.models.enrichment import EnrichmentData
from app.models.mitre import MITREMapping
from app.models.report import (
    AIReport,
    Recommendation,
)
from app.models.risk import RiskScore


class TemplateProvider:

    def generate_report(
        self,
        context:dict,
       
    ) -> AIReport:
        ioc_count = context["ioc_count"]
        enrichment = context["enrichment"]
        mitre_mappings = context["mitre_mappings"]
        risk_score = context["risk_score"]

        summary = (
            f"The analysis identified {ioc_count} indicators of compromise. "
            f"The overall risk level was classified as "
            f"{risk_score.level.upper()} with a score of "
            f"{risk_score.score}."
        )

        analysis_overview = (
            f"The investigation discovered {ioc_count} indicators, "
            f"{len(enrichment.cves)} CVE references, and "
            f"{len(mitre_mappings)} MITRE ATT&CK mappings. "
            f"The calculated risk score indicates "
            f"{risk_score.level.upper()} threat activity."
        )

        attack_scenario = self._build_attack_scenario(
            mitre_mappings
        )

        business_impact = self._build_business_impact(
            risk_score.level
        )

        immediate_actions = [
            Recommendation(
                title="Contain Malicious Infrastructure",
                description=(
                    "Block identified malicious domains, URLs, "
                    "and IP addresses at network boundaries."
                ),
                priority=Priority.CRITICAL,
            ),
            Recommendation(
                title="Patch Vulnerable Systems",
                description=(
                    "Apply vendor patches for affected "
                    "vulnerabilities immediately."
                ),
                priority=Priority.HIGH,
            ),
            Recommendation(
                title="Investigate Impacted Assets",
                description=(
                    "Review affected hosts for evidence of "
                    "compromise and lateral movement."
                ),
                priority=Priority.HIGH,
            ),
        ]

        long_term_remediation = [
            Recommendation(
                title="Improve Vulnerability Management",
                description=(
                    "Implement regular vulnerability scanning "
                    "and patch governance."
                ),
                priority=Priority.HIGH,
            ),
            Recommendation(
                title="Security Awareness Training",
                description=(
                    "Conduct phishing and security awareness "
                    "training for employees."
                ),
                priority=Priority.MEDIUM,
            ),
            Recommendation(
                title="Strengthen Endpoint Protection",
                description=(
                    "Deploy advanced endpoint monitoring "
                    "and response capabilities."
                ),
                priority=Priority.MEDIUM,
            ),
        ]

        monitoring = [
            Recommendation(
                title="Monitor Network Traffic",
                description=(
                    "Track outbound communications to suspicious "
                    "domains and infrastructure."
                ),
                priority=Priority.HIGH,
            ),
            Recommendation(
                title="Monitor Authentication Events",
                description=(
                    "Review authentication logs for signs of "
                    "account compromise."
                ),
                priority=Priority.MEDIUM,
            ),
            Recommendation(
                title="Monitor Exploit Activity",
                description=(
                    "Alert on exploitation attempts against "
                    "internet-facing services."
                ),
                priority=Priority.HIGH,
            ),
        ]

        return AIReport(
            summary=summary,
            analysis_overview=analysis_overview,
            attack_scenario=attack_scenario,
            business_impact=business_impact,
            immediate_actions=immediate_actions,
            long_term_remediation=long_term_remediation,
            monitoring=monitoring,
        )

    def _build_attack_scenario(
        self,
        mappings: list[MITREMapping],
    ) -> str:

        techniques = {
            mapping.id
            for mapping in mappings
        }

        scenario_parts: list[str] = []

        if "T1566" in techniques:
            scenario_parts.append(
                "The attack likely involved phishing activity."
            )

        if "T1190" in techniques:
            scenario_parts.append(
                "A public-facing application may have been exploited."
            )

        if "T1071" in techniques:
            scenario_parts.append(
                "Communication with attacker-controlled infrastructure was observed."
            )

        if not scenario_parts:
            scenario_parts.append(
                "The observed indicators suggest suspicious activity requiring investigation."
            )

        return " ".join(scenario_parts)

    def _build_business_impact(
        self,
        level: str,
    ) -> str:

        if level == RiskLevel.CRITICAL:
            return (
                "High likelihood of system compromise, "
                "data exposure, service disruption, and "
                "unauthorized access."
            )

        if level == RiskLevel.HIGH:
            return (
                "Potential compromise of systems and "
                "sensitive information."
            )

        if level == RiskLevel.MEDIUM:
            return (
                "Moderate operational risk with "
                "limited exposure."
            )

        return (
            "Low immediate business impact "
            "based on current evidence."
        )