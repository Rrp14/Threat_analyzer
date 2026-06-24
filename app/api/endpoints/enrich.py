from fastapi import APIRouter, Depends

from app.api.schemas.enrichment import (
    EnrichmentResponse,
)
from app.api.schemas.ingestion import (
    IngestRequest,
)
from app.core.orchestrator import (
    ThreatAnalysisOrchestrator,
)
from app.dependencies import (
    get_orchestrator,
)


router = APIRouter(
    prefix="/api/enrich",
    tags=["Enrichment"],
)


@router.post(
    "",
    response_model=EnrichmentResponse,
)
def enrich(
    request: IngestRequest,
    orchestrator: ThreatAnalysisOrchestrator = Depends(
        get_orchestrator
    ),
) -> EnrichmentResponse:

    context = orchestrator.analyze(
        raw_input=request.content,
        input_type=request.input_type,
    )

    enrichment = context.enrichment

    return EnrichmentResponse(
        analysis_id=context.analysis_id,
        ioc_count=context.ioc_count,
        cves=enrichment.cves,
        reputation_scores=enrichment.reputation_score,
    )