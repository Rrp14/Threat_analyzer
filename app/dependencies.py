from app.core.orchestrator import ThreatAnalysisOrchestrator

orchestrator = ThreatAnalysisOrchestrator()


def get_orchestrator() -> ThreatAnalysisOrchestrator:
    return orchestrator