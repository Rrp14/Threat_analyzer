from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analysis_service import (
    AnalysisService,
)
from app.services.graph_service import (
    GraphService,
)

router = APIRouter(
    prefix="/api/analyses",
    tags=["Graph"],
)


@router.post(
    "/{analysis_id}/graph",
)
def generate_graph(
    analysis_id: str,
    db: Session = Depends(get_db),
):

    analysis_service = AnalysisService()

    graph = analysis_service.get_graph(
        db,
        analysis_id,
    )

    if graph:
        return graph

    context = analysis_service.get(
        db,
        analysis_id,
    )

    graph = GraphService().build(
        context
    )

    analysis_service.save_graph(
        db,
        analysis_id,
        graph,
    )

    return graph