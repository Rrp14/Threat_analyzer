

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analysis_service import AnalysisService


router = APIRouter(
    prefix="/api/analyses",
    tags=["Analyses"],
)


@router.get("")
def list_analyses(
    db: Session = Depends(get_db),
):

    analyses = (
        AnalysisService().list_all(db)
    )

    return [
        {
            "analysis_id": a.analysis_id,
            "timestamp": a.timestamp,
            "input_type": a.input_type,
        }
        for a in analyses
    ]


@router.get("/{analysis_id}")
def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
):

    context = (
        AnalysisService().get(
            db,
            analysis_id,
        )
    )

    if context is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    return context