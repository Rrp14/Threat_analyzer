from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile
from app.api.schemas.ingestion import IngestRequest, IngestResponse
from app.core.exceptions import ValidationError
from app.core.orchestrator import ThreatAnalysisOrchestrator
from app.dependencies import get_orchestrator
from app.enums.input_type import InputType

router = APIRouter(
    prefix="/api/ingest",
    tags=["Ingestion"],
)



_EXTENSION_MAP = {
    ".txt": InputType.TEXT,
    ".json": InputType.JSON,
    ".csv": InputType.CSV,
    ".pdf": InputType.PDF,
    ".docx": InputType.DOCX,
}


def _detect_input_type(filename: str) -> InputType:
    """
    Determine the input type from a file extension.
    """
    extension = Path(filename).suffix.lower()

    input_type = _EXTENSION_MAP.get(extension)

    if input_type is None:
        raise ValidationError(
            message="Unsupported file type.",
            details={
                "filename": filename,
                "extension": extension,
            },
        )

    return input_type

@router.post("",response_model=IngestResponse)
def ingest(
    request: IngestRequest,
    orchestrator: ThreatAnalysisOrchestrator = Depends(get_orchestrator),
):
    context=orchestrator.analyze(
        raw_input=request.content,
        input_type=request.input_type,
    )
    

    return IngestResponse(
    analysis_id=context.analysis_id,
    input_type=context.input_type,
    normalized_input=context.normalized_input,
)


@router.post(
    "/upload",
    response_model=IngestResponse,
)
async def upload(
    file: UploadFile = File(...),
    orchestrator: ThreatAnalysisOrchestrator = Depends(get_orchestrator),
) -> IngestResponse:
    """
    Upload and normalize a supported document.
    """

    content = await file.read()

    input_type = _detect_input_type(file.filename or "")

    if input_type in {
        InputType.TEXT,
        InputType.JSON,
        InputType.CSV,
    }:
        content = content.decode("utf-8")

    context = orchestrator.analyze(
        raw_input=content,
        input_type=input_type,
    )

    return IngestResponse(
        analysis_id=context.analysis_id,
        input_type=context.input_type,
        normalized_input=context.normalized_input,
    )





