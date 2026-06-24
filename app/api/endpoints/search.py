from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analysis_service import AnalysisService

router = APIRouter(
    prefix="/api/search",
    tags=["Search"],
)


@router.get("/ioc")
def search_ioc(
    value: str,
    db: Session = Depends(get_db),
):
    """
    Search for analyses containing a specific IOC value.
    """
    return AnalysisService().search_ioc(db, value)


@router.get("/cve")
def search_cve(
    cve_id: str,
    db: Session = Depends(get_db),
):
    """
    Search for analyses containing a specific CVE ID.
    """
    return AnalysisService().search_cve(db, cve_id)


@router.get("/mitre")
def search_mitre(
    technique_id: str,
    db: Session = Depends(get_db),
):
    """
    Search for analyses containing a specific MITRE ATT&CK technique ID.
    """
    return AnalysisService().search_mitre(db, technique_id)
