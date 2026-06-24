
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analysis_service import (
    AnalysisService,
)

router = APIRouter(
    prefix="/api/analyses",
    tags=["Threat Intelligence"],
)


@router.get("/{analysis_id}/iocs")
def get_iocs(
    analysis_id: str,
    db: Session = Depends(get_db),
):

    return (
        AnalysisService()
        .get_iocs(
            db,
            analysis_id,
        )
    )


@router.get("/{analysis_id}/cves")
def get_cves(
    analysis_id: str,
    db: Session = Depends(get_db),
):

    return (
        AnalysisService()
        .get_cves(
            db,
            analysis_id,
        )
    )


@router.get("/{analysis_id}/mitre")
def get_mitre(
    analysis_id: str,
    db: Session = Depends(get_db),
):

    return (
        AnalysisService()
        .get_mitre_mappings(
            db,
            analysis_id,
        )
    )