from fastapi import APIRouter, Depends

from app.api.schemas.ingestion import IngestRequest
from app.api.schemas.mitre import MitreResponse
from app.core.orchestrator import ThreatAnalysisOrchestrator
from app.dependencies import get_orchestrator


router = APIRouter(
    prefix="/api/mitre",
    tags=["MITRE Mapping"],
)


@router.post(
    "",
    response_model=MitreResponse,
)
def map_to_mitre(
    request: IngestRequest,
    orchestrator: ThreatAnalysisOrchestrator = Depends(
        get_orchestrator
    ),
) -> MitreResponse:

    context = orchestrator.analyze(
        raw_input=request.content,
        input_type=request.input_type,
    )

    return MitreResponse(
        analysis_id=context.analysis_id,
        ioc_count=context.ioc_count,
        mapping_count=len(context.mitre_mapping),
        mappings=context.mitre_mapping,
    )