from fastapi import APIRouter, Depends

from app.api.schemas.extraction import (
    ExtractionResponse,
    IOCResponse,
)
from app.api.schemas.ingestion import IngestRequest
from app.core.orchestrator import ThreatAnalysisOrchestrator
from app.dependencies import get_orchestrator


router = APIRouter(
    prefix="/api/extract",
    tags=["IOC Extraction"],
)


@router.post(
    "",
    response_model=ExtractionResponse,
)
def extract(
    request: IngestRequest,
    orchestrator: ThreatAnalysisOrchestrator = Depends(
        get_orchestrator
    ),
) -> ExtractionResponse:

    context = orchestrator.analyze(
        raw_input=request.content,
        input_type=request.input_type,
    )

    return ExtractionResponse(
        analysis_id=context.analysis_id,
        ioc_count=context.ioc_count,
        iocs=[
            IOCResponse(
                type=ioc.type,
                value=ioc.value,
                reputation=ioc.reputation,
                enriched=ioc.enriched,
                confidence=ioc.confidence,
            )
            for ioc in context.iocs
        ],
    )