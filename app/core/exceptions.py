from __future__ import annotations

class ThreatIntelError(Exception):


    error_code="THREAT_INTEL_ERROR"


    def __init__(self, 
                 message:str,
                 details:dict | None=None):
        super().__init__(message)

        self.message=message
        self.details=details


    def to_dict(self)->dict:
        return{
            "error":self.error_code,
            "message":self.message,
            "details":self.details,
        }
    

class FeatureError(ThreatIntelError):
    """base class for feature-specific exceptions"""    


class ConfigurationError(ThreatIntelError):
    error_code = "CONFIGURATION_ERROR"


class ValidationError(ThreatIntelError):
    error_code = "VALIDATION_ERROR"


class PipelineError(ThreatIntelError):
    error_code = "PIPELINE_ERROR"


class DatabaseError(ThreatIntelError):
    error_code = "DATABASE_ERROR"


class AIError(ThreatIntelError):
    error_code = "AI_ERROR"


class IngestionError(FeatureError):
    error_code = "INGESTION_ERROR"


class IOCExtractionError(FeatureError):
    error_code = "IOC_EXTRACTION_ERROR"    


class EnrichmentError(FeatureError):
    error_code = "ENRICHMENT_ERROR"


class MITREMappingError(FeatureError):
    error_code = "MITRE_MAPPING_ERROR"


class RiskScoringError(FeatureError):
    error_code = "RISK_SCORING_ERROR"


class ReportGenerationError(FeatureError):
    error_code = "REPORT_GENERATION_ERROR"


class DetectionRuleError(FeatureError):
    error_code = "DETECTION_RULE_ERROR"

