from fastapi import APIRouter, Depends

from app.api.schemas.ingestion import IngestRequest
from app.api.schemas.risk import RiskResponse
from app.core.orchestrator import ThreatAnalysisOrchestrator
from app.dependencies import get_orchestrator


router = APIRouter(
    prefix="/api/risk",
    tags=["Risk Scoring"],
)


@router.post(
    "",
    response_model=RiskResponse,
)
def score_risk(
    request: IngestRequest,
    orchestrator: ThreatAnalysisOrchestrator = Depends(
        get_orchestrator,
    ),
) -> RiskResponse:

    context = orchestrator.analyze(
        raw_input=request.content,
        input_type=request.input_type,
    )

    return RiskResponse(
        analysis_id=context.analysis_id,
        ioc_count=context.ioc_count,
        risk_score=context.risk_score,
    )