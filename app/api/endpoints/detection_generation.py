



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analysis_service import AnalysisService
from app.services.detection_rule import DetectionRuleService


router = APIRouter(
    prefix="/api/analyses",
    tags=["Detection"],
)


@router.post(
    "/{analysis_id}/detection"
)
def generate_detection(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    
    analysis_service = AnalysisService()

    cached = (
    analysis_service.get_detection_rules(
        db,
        analysis_id,
    )
)

    if cached:
       return cached
    
    context = analysis_service.get(
    db,
    analysis_id,
)

    if context is None:
       raise HTTPException(
        status_code=404,
        detail="Analysis not found",
    ) 


    rules = (
    DetectionRuleService()
    .generate_from_context(
        context
    )
)
    

    analysis_service.save_detection_rules(
    db,
    analysis_id,
    rules,
)
    
    return rules