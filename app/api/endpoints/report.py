from fastapi import APIRouter, Depends

from app.api.schemas.ingestion import IngestRequest
from app.api.schemas.report import ReportResponse
from app.core.orchestrator import ThreatAnalysisOrchestrator
from app.dependencies import get_orchestrator


router = APIRouter(
    prefix="/api/report",
    tags=["AI Report"],
)


@router.post(
    "",
    response_model=ReportResponse,
)
def generate_report(
    request: IngestRequest,
    orchestrator: ThreatAnalysisOrchestrator = Depends(
        get_orchestrator,
    ),
) -> ReportResponse:

    context = orchestrator.analyze(
        raw_input=request.content,
        input_type=request.input_type,
    )

    return ReportResponse(
        analysis_id=context.analysis_id,
        ioc_count=context.ioc_count,
        report=context.ai_report,
    )