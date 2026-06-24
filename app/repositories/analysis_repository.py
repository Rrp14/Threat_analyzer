from sqlalchemy.orm import Session

from app.database.models import (
    Analysis,
    IOCGraphRecord,
    IOCRecord,
    CVERecord,
    MITRERecord,
    AttackPathRecord
)




class AnalysisRepository:

    def create(
        self,
        db: Session,
        *,
        analysis_id: str,
        input_type: str,
        raw_input: str,
        result_json: str,
    ) -> Analysis:

        analysis = Analysis(
            analysis_id=analysis_id,
            input_type=input_type,
            raw_input=raw_input,
            result_json=result_json,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    def get_by_analysis_id(
        self,
        db: Session,
        analysis_id: str,
    ) -> Analysis | None:

        return (
            db.query(Analysis)
            .filter(
                Analysis.analysis_id == analysis_id
            )
            .first()
        )

    def list_all(
        self,
        db: Session,
    ) -> list[Analysis]:

        return (
            db.query(Analysis)
            .order_by(
                Analysis.timestamp.desc()
            )
            .all()
        )

    # ==========================
    # Report
    # ==========================

    def update_report(
        self,
        db: Session,
        analysis_id: str,
        report_json: str,
    ) -> None:

        record = self.get_by_analysis_id(
            db,
            analysis_id,
        )

        if record is None:
            return

        record.ai_report_json = report_json

        db.commit()

    def get_report(
        self,
        db: Session,
        analysis_id: str,
    ) -> str | None:

        record = self.get_by_analysis_id(
            db,
            analysis_id,
        )

        if record is None:
            return None

        return record.ai_report_json

    # ==========================
    # Detection Rules
    # ==========================

    def update_detection_rules(
        self,
        db: Session,
        analysis_id: str,
        detection_json: str,
    ) -> None:

        record = self.get_by_analysis_id(
            db,
            analysis_id,
        )

        if record is None:
            return

        record.detection_rules_json = (
            detection_json
        )

        db.commit()

    def get_detection_rules(
        self,
        db: Session,
        analysis_id: str,
    ) -> str | None:

        record = self.get_by_analysis_id(
            db,
            analysis_id,
        )

        if record is None:
            return None

        return record.detection_rules_json

    # ==========================
    # IOC Queries
    # ==========================

    def get_iocs(
        self,
        db: Session,
        analysis_id: str,
    ) -> list[IOCRecord]:

        return (
            db.query(IOCRecord)
            .filter(
                IOCRecord.analysis_id
                == analysis_id
            )
            .all()
        )

    # ==========================
    # CVE Queries
    # ==========================

    def get_cves(
        self,
        db: Session,
        analysis_id: str,
    ) -> list[CVERecord]:

        return (
            db.query(CVERecord)
            .filter(
                CVERecord.analysis_id
                == analysis_id
            )
            .all()
        )

    # ==========================
    # MITRE Queries
    # ==========================

    def get_mitre_mappings(
        self,
        db: Session,
        analysis_id: str,
    ) -> list[MITRERecord]:

        return (
            db.query(MITRERecord)
            .filter(
                MITRERecord.analysis_id
                == analysis_id
            )
            .all()
        )

    # ==========================
    # Threat Hunting Queries
    # ==========================

    def search_ioc(
        self,
        db: Session,
        value: str,
    ) -> list[IOCRecord]:

        return (
            db.query(IOCRecord)
            .filter(
                IOCRecord.value == value
            )
            .all()
        )

    def search_cve(
        self,
        db: Session,
        cve_id: str,
    ) -> list[CVERecord]:

        return (
            db.query(CVERecord)
            .filter(
                CVERecord.cve_id == cve_id
            )
            .all()
        )

    def search_mitre(
        self,
        db: Session,
        technique_id: str,
    ) -> list[MITRERecord]:

        return (
            db.query(MITRERecord)
            .filter(
                MITRERecord.technique_id
                == technique_id
            )
            .all()
        )
    
    def save_graph(
    self,
    db: Session,
    analysis_id: str,
    graph_json: str,
) -> None:

     record = (
        db.query(IOCGraphRecord)
        .filter(
            IOCGraphRecord.analysis_id
            == analysis_id
        )
        .first()
    )

     if record:

        record.graph_json = graph_json

     else:

        record = IOCGraphRecord(
            analysis_id=analysis_id,
            graph_json=graph_json,
        )

        db.add(record)

     db.commit()



    def get_graph(
    self,
    db: Session,
    analysis_id: str,
) -> str | None:

     record = (
        db.query(IOCGraphRecord)
        .filter(
            IOCGraphRecord.analysis_id
            == analysis_id
        )
        .first()
    )
 
     if record is None:
        return None

     return record.graph_json 
    


    def save_attack_path(
    self,
    db: Session,
    analysis_id: str,
    path_json: str,
) -> None:

      record = (
        db.query(AttackPathRecord)
        .filter(
            AttackPathRecord.analysis_id
            == analysis_id
        )
        .first()
    )

      if record:

        record.path_json = path_json

      else:

        record = AttackPathRecord(
            analysis_id=analysis_id,
            path_json=path_json,
        )

        db.add(record)

      db.commit()


    def get_attack_path(
    self,
    db: Session,
    analysis_id: str,
) -> str | None:

       record = (
        db.query(AttackPathRecord)
        .filter(
            AttackPathRecord.analysis_id
            == analysis_id
        )
        .first()
    )

       if record is None:
        return None

       return record.path_json  