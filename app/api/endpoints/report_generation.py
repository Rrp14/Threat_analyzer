


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.ai_report import AIReportService
from app.services.analysis_service import AnalysisService


router = APIRouter(
    prefix="/api/analyses",
    tags=["Reports"],
)


@router.post(
    "/{analysis_id}/report"
)
def generate_report(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    
    analysis_service = (
    AnalysisService()
)

    cached_report = (
    analysis_service.get_report(
        db,
        analysis_id,
    )
)

    if cached_report:
      return cached_report
    
    context = (
    analysis_service.get(
        db,
        analysis_id,
    )
)

    if context is None:
     raise HTTPException(
        status_code=404,
        detail="Analysis not found",
    )


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


    report = AIReportService().generate(
    gemini_context,
    template_context,
)
    

    analysis_service.save_report(
    db,
    analysis_id,
    report,
)
    
    return report