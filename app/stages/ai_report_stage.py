from app.core.exceptions import ValidationError
from app.core.stage import PipelineStage
from app.models.schemas import PipelineContext
from app.services.ai_report import AIReportService


class AIReportStage(PipelineStage):

    def __init__(
        self,
        service: AIReportService | None = None,
    ) -> None:

        self._service = (
            service
            if service is not None
            else AIReportService()
        )

    @property
    def name(self) -> str:
        return "AI Report"

    def validate(
        self,
        context: PipelineContext,
    ) -> None:

        if context.risk_score is None:
            raise ValidationError(
                "Risk score required before report generation."
            )

        if context.enrichment is None:
            raise ValidationError(
                "Enrichment data required before report generation."
            )
         
        if not context.mitre_mapping:
            raise ValidationError(
            "MITRE mappings required before report generation."
        )

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        
        gemini_context = {
    "ioc_count": context.ioc_count,

    "risk_score": context.risk_score.score,
    "risk_level": context.risk_score.level,

    "iocs": [
        {
            "type": ioc.type,
            "value": ioc.value,
            "reputation": ioc.reputation,
        }
        for ioc in context.iocs
    ],

    "cves": [
        {
            "id": cve.id,
            "cvss": cve.cvss,
            "severity": cve.severity,
            "exploit_available": cve.exploit_available,
        }
        for cve in context.enrichment.cves
    ],

    "mitre_mappings": [
        {
            "id": mapping.id,
            "tactic": mapping.tactic,
            "technique": mapping.technique,
        }
        for mapping in context.mitre_mapping
    ],
     }
        
        template_context = {
    "ioc_count": context.ioc_count,
    "enrichment": context.enrichment,
    "mitre_mappings": context.mitre_mapping,
    "risk_score": context.risk_score,
}

        context.ai_report = (
            self._service.generate(
                gemini_context,
                template_context
            )
        )

        #print("\n=== AI REPORT ===")
        #print(context.ai_report)

        return context