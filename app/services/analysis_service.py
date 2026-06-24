from sqlalchemy.orm import Session
from app.models.graph import IOCRelationshipGraph
from app.models.report import AIReport
from app.models.schemas import PipelineContext
from app.repositories.analysis_repository import (
    AnalysisRepository,
)

from app.models.detection import DetectionRules
from app.database.models import IOCRecord
from app.database.models import CVERecord
from app.database.models import MITRERecord
from app.models.attack_path import (
    AttackPathPrediction,
)

class AnalysisService:

    def __init__(self) -> None:

        self._repository = (
            AnalysisRepository()
        )

    def save(
    self,
    db: Session,
    context: PipelineContext,
) -> None:

    # Save master analysis
     self._repository.create(
        db,
        analysis_id=context.analysis_id,
        input_type=str(context.input_type),
        raw_input=str(context.raw_input),
        result_json=context.model_dump_json(),
    )

    # Save IOCs
     for ioc in context.iocs:

        db.add(
            IOCRecord(
                analysis_id=context.analysis_id,
                ioc_type=str(ioc.type),
                value=ioc.value,
                reputation=ioc.reputation,
            )
        )

    # Save CVEs
     if context.enrichment:

        for cve in context.enrichment.cves:

            db.add(
                CVERecord(
                    analysis_id=context.analysis_id,
                    cve_id=cve.id,
                    severity=cve.severity,
                    cvss=cve.cvss,
                )
            )

    # Save MITRE mappings
     for mapping in context.mitre_mapping:

        db.add(
            MITRERecord(
                analysis_id=context.analysis_id,
                technique_id=mapping.id,
                tactic=mapping.tactic,
                technique=mapping.technique,
            )
        )

     db.commit()

    def get(
        self,
        db: Session,
        analysis_id: str,
    ) -> PipelineContext | None:

        record = (
            self._repository.get_by_analysis_id(
                db,
                analysis_id,
            )
        )

        if record is None:
            return None

        return (
            PipelineContext.model_validate_json(
                record.result_json
            )
        )
    
    def list_all(
    self,
    db: Session,
):
     return self._repository.list_all(db)
    
    def save_report(
    self,
    db: Session,
    analysis_id: str,
    report: AIReport,
) -> None:

     self._repository.update_report(
        db,
        analysis_id,
        report.model_dump_json(),
    )
     


    def get_report(
    self,
    db: Session,
    analysis_id: str,
) -> AIReport | None:

      report_json = (
        self._repository.get_report(
            db,
            analysis_id,
        )
    )

      if report_json is None:
        return None

      return AIReport.model_validate_json(
        report_json
    )


    def get_detection_rules(
    self,
    db: Session,
    analysis_id: str,
) -> DetectionRules | None:

     detection_json = (
        self._repository.get_detection_rules(
            db,
            analysis_id,
        )
    )

     if detection_json is None:
        return None

     return DetectionRules.model_validate_json(
        detection_json
    )


    def save_detection_rules(
    self,
    db: Session,
    analysis_id: str,
    rules: DetectionRules,
) -> None:

     self._repository.update_detection_rules(
        db,
        analysis_id,
        rules.model_dump_json(),
    )
     


    def get_iocs(
    self,
    db: Session,
    analysis_id: str,
):

     return self._repository.get_iocs(
        db,
        analysis_id,
    )


    def get_cves(
    self,
    db: Session,
    analysis_id: str,
):

     return self._repository.get_cves(
        db,
        analysis_id,
    )


    def get_mitre_mappings(
    self,
    db: Session,
    analysis_id: str,
):

      return self._repository.get_mitre_mappings(
        db,
        analysis_id,
    )


    def search_ioc(
    self,
    db: Session,
    value: str,
):

      return self._repository.search_ioc(
        db,
        value,
    )


    def search_cve(
    self,
    db: Session,
    cve_id: str,
):
 
      return self._repository.search_cve(
        db,
        cve_id,
    )


    def search_mitre(
    self,
    db: Session,
    technique_id: str,
):

      return self._repository.search_mitre(
        db,
        technique_id,
    )


    def save_graph(
    self,
    db: Session,
    analysis_id: str,
    graph: IOCRelationshipGraph,
) -> None:

     self._repository.save_graph(
        db,
        analysis_id,
        graph.model_dump_json(),
    )
     

    def get_graph(
    self,
    db: Session,
    analysis_id: str,
) -> IOCRelationshipGraph | None:

     graph_json = (
        self._repository.get_graph(
            db,
            analysis_id,
        )
    )

     if graph_json is None:
        return None

     return IOCRelationshipGraph.model_validate_json(
        graph_json
    ) 


    def save_attack_path(
    self,
    db: Session,
    analysis_id: str,
    attack_path: AttackPathPrediction,
) -> None:

       self._repository.save_attack_path(
        db,
        analysis_id,
        attack_path.model_dump_json(),
    )
       


    def get_attack_path(
    self,
    db: Session,
    analysis_id: str,
) -> AttackPathPrediction | None:

      path_json = (
        self._repository.get_attack_path(
            db,
            analysis_id,
        )
    )

      if path_json is None:
        return None

      return AttackPathPrediction.model_validate_json(
        path_json
    )   
         
     

