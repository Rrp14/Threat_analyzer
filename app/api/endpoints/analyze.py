from fastapi import APIRouter, File, UploadFile
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.schemas.ingestion import IngestRequest
from app.core.exceptions import ValidationError
from app.core.orchestrator import (
    ThreatAnalysisOrchestrator,
)
from app.database.db import get_db
from app.dependencies import get_orchestrator
from app.enums.input_type import InputType
from app.services.analysis_service import (
    AnalysisService,
)

router = APIRouter(
    prefix="/api/analyze",
    tags=["Analysis"],
)

from pathlib import Path

_EXTENSION_MAP = {
    ".txt": InputType.TEXT,
    ".json": InputType.JSON,
    ".csv": InputType.CSV,
    ".pdf": InputType.PDF,
    ".docx": InputType.DOCX,
}


def _detect_input_type(
    filename: str,
) -> InputType:

    extension = (
        Path(filename)
        .suffix
        .lower()
    )

    input_type = (
        _EXTENSION_MAP.get(extension)
    )

    if input_type is None:
        raise ValidationError(
            message="Unsupported file type.",
            details={
                "filename": filename,
                "extension": extension,
            },
        )

    return input_type


@router.post("")
def analyze(
    request: IngestRequest,
    db: Session = Depends(get_db),
    orchestrator: ThreatAnalysisOrchestrator = Depends(
        get_orchestrator
    ),
):

    context = orchestrator.analyze(
        raw_input=request.content,
        input_type=request.input_type,
    )

    AnalysisService().save(
        db,
        context,
    )

    return {
        "analysis_id": context.analysis_id,
        "ioc_count": context.ioc_count,
        "risk_score": (
            context.risk_score.model_dump()
            if context.risk_score
            else None
        ),
        "mitre_mappings": [
            m.model_dump()
            for m in context.mitre_mapping
        ],
    }


@router.post("/upload")
async def analyze_upload(
    file: UploadFile = File(...),
    orchestrator: ThreatAnalysisOrchestrator = (
        Depends(get_orchestrator)
    ),
    db: Session = Depends(get_db),
):
    content = await file.read()

    input_type = _detect_input_type(
        file.filename or ""
    )

    if input_type in {
        InputType.TEXT,
        InputType.JSON,
        InputType.CSV,
    }:
        content = content.decode(
            "utf-8"
        )

    context = orchestrator.analyze(
        raw_input=content,
        input_type=input_type,
    )

    AnalysisService().save(
        db,
        context,
    )

    return {
        "analysis_id": context.analysis_id,
        "ioc_count": context.ioc_count,
        "risk_score": context.risk_score,
    }