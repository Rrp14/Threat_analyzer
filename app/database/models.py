from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey,String,Text
from sqlalchemy.orm import Mapped,mapped_column

from app.database.db import Base

class Analysis(Base):
    __tablename__="analysis"

    id:Mapped[int]=mapped_column(primary_key=True)

    analysis_id:Mapped[str]=mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    timestamp:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    input_type:Mapped[str] =mapped_column(
        String(20)
    )

    raw_input:Mapped[str]=mapped_column(
        Text
    )

    result_json:Mapped[str]=mapped_column(
        Text
    )


    ai_report_json: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
)

    detection_rules_json: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
)



from app.database.db import Base


class IOCRecord(Base):

    __tablename__ = "iocs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis.analysis_id"),
        index=True,
    )

    ioc_type: Mapped[str] = mapped_column(
        String(50)
    )

    value: Mapped[str] = mapped_column(
        String(500)
    )

    reputation: Mapped[str | None]


class CVERecord(Base):

    __tablename__ = "cves"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis.analysis_id"),
        index=True,
    )

    cve_id: Mapped[str] = mapped_column(
        String(50)
    )

    severity: Mapped[str]

    cvss: Mapped[float]


class MITRERecord(Base):

    __tablename__ = "mitre_mappings"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis.analysis_id"),
        index=True,
    )

    technique_id: Mapped[str] = mapped_column(
        String(50)
    )

    tactic: Mapped[str]

    technique: Mapped[str]



class ReportRecord(Base):

    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis.analysis_id"),
        unique=True,
        index=True,
    )

    report_json: Mapped[str] = mapped_column(
        Text
    )



class DetectionRuleRecord(Base):

    __tablename__ = "detection_rules"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis.analysis_id"),
        unique=True,
        index=True,
    )

    rules_json: Mapped[str] = mapped_column(
        Text
    )



class IOCGraphRecord(Base):

    __tablename__ = "ioc_graphs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis.analysis_id"),
        unique=True,
        index=True,
    )

    graph_json: Mapped[str] = mapped_column(
        Text
    )


class AttackPathRecord(Base):

    __tablename__ = "attack_paths"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis.analysis_id"),
        unique=True,
        index=True,
    )

    path_json: Mapped[str] = mapped_column(
        Text
    )

