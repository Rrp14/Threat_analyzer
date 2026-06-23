from datetime import datetime, timezone

from pydantic import Field

from app.enums.input_type import InputType
from app.models.common import DomainModel
from app.models.detection import DetectionRules
from app.models.enrichment import EnrichmentData
from app.models.extensions import ExtensionFeatures
from app.models.ioc import IOC
from app.models.mitre import MITREMapping
from app.models.report import AIReport
from app.models.risk import RiskScore


class FileMetadata(DomainModel):
    """
    Metadata for uploaded files.
    """

    filename: str = Field(
        ...,
        min_length=1,
        description="Original uploaded filename.",
    )

    mime_type: str = Field(
        ...,
        min_length=1,
        description="MIME type of the uploaded file.",
    )

    size: int = Field(
        ...,
        ge=0,
        description="File size in bytes.",
    )


class PipelineContext(DomainModel):


    analysis_id: str = Field(
        ...,
        description="Unique analysis identifier.",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Analysis creation timestamp.",
    )

    input_type: InputType = Field(
        ...,
        description="Original input type.",
    )

    raw_input: str = Field(
        ...,
        min_length=1,
        description="Original input content.",
    )

    file_metadata: FileMetadata | None = Field(
        default=None,
        description="Metadata for uploaded file, if applicable.",
    )

    iocs: list[IOC] = Field(
        default_factory=list,
        description="Extracted Indicators of Compromise.",
    )

    enrichment: EnrichmentData | None = Field(
        default=None,
        description="Threat enrichment results.",
    )

    mitre_mapping: list[MITREMapping] = Field(
        default_factory=list,
        description="Mapped MITRE ATT&CK techniques.",
    )

    risk_score: RiskScore | None = Field(
        default=None,
        description="Calculated risk score.",
    )

    ai_report: AIReport | None = Field(
        default=None,
        description="Generated intelligence report.",
    )

    detection_rules: DetectionRules | None = Field(
        default=None,
        description="Generated detection rules.",
    )

    extensions: ExtensionFeatures | None = Field(
        default=None,
        description="Optional advanced analysis outputs.",
    )

    @property
    def has_iocs(self) -> bool:
        return bool(self.iocs)

    @property
    def has_enrichment(self) -> bool:
        return self.enrichment is not None

    @property
    def has_mitre_mapping(self) -> bool:
        return bool(self.mitre_mapping)

    @property
    def has_risk_score(self) -> bool:
        return self.risk_score is not None

    @property
    def has_ai_report(self) -> bool:
        return self.ai_report is not None

    @property
    def has_detection_rules(self) -> bool:
        return self.detection_rules is not None

    @property
    def has_extensions(self) -> bool:
        return self.extensions is not None

    @property
    def ioc_count(self) -> int:
        return len(self.iocs)