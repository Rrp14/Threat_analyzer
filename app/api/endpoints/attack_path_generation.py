from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analysis_service import (
    AnalysisService,
)
from app.services.attack_path_service import (
    AttackPathService,
)

router = APIRouter(
    prefix="/api/analyses",
    tags=["Attack Path"],
)


@router.post(
    "/{analysis_id}/attack-path",
)
def generate_attack_path(
    analysis_id: str,
    db: Session = Depends(get_db),
):

    analysis_service = AnalysisService()

    existing = (
        analysis_service.get_attack_path(
            db,
            analysis_id,
        )
    )

    if existing:
        return existing

    context = analysis_service.get(
        db,
        analysis_id,
    )

    if context is None:
        return {
            "error": "analysis not found"
        }

    attack_path = (
        AttackPathService()
        .generate_from_context(
            context
        )
    )

    analysis_service.save_attack_path(
        db,
        analysis_id,
        attack_path,
    )

    return attack_path