from app.enums.ioc import IOCType
from app.enums.reputation import (
    Reputation,
    ReputationLevel,
)
from app.models.enrichment import (
    EnrichmentData,
    ReputationScore,
)
from app.models.ioc import IOC
from app.services.providers.cve_provider import (
    LocalCVEProvider,
)
from app.services.providers.reputation_provider import (
    LocalReputationProvider,
)


class EnrichmentService:

    LEVEL_TO_REPUTATION = {
        ReputationLevel.CLEAN: Reputation.CLEAN,
        ReputationLevel.LOW_RISK: Reputation.CLEAN,
        ReputationLevel.SUSPICIOUS: Reputation.SUSPICIOUS,
        ReputationLevel.MALICIOUS: Reputation.MALICIOUS,
    }

    def __init__(
        self,
        reputation_provider: LocalReputationProvider,
        cve_provider: LocalCVEProvider,
    ) -> None:

        self._reputation_provider = reputation_provider
        self._cve_provider = cve_provider

    def enrich(
        self,
        iocs: list[IOC],
    ) -> EnrichmentData:

        enrichment = EnrichmentData()

        for ioc in iocs:

            reputation = self._reputation_provider.lookup(
                ioc.value
            )

            if reputation is not None:

                enrichment.reputation_score[
                    ioc.value
                ] = reputation

                ioc.reputation = (
                    self.LEVEL_TO_REPUTATION[
                        reputation.level
                    ]
                )

            ioc.enriched = True

            if ioc.type == IOCType.CVE:

                cve = self._cve_provider.lookup(
                    ioc.value
                )

                if cve is not None:
                    enrichment.cves.append(cve)

        return enrichment