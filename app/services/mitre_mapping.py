from app.models.ioc import IOC
from app.models.mitre import MITREMapping
from app.services.providers.mitre_provider import (
    LocalMitreProvider,
)


class MitreMappingService:

    def __init__(
        self,
        provider: LocalMitreProvider,
    ) -> None:
        self._provider = provider

    def map_iocs(
        self,
        iocs: list[IOC],
    ) -> list[MITREMapping]:

        mappings: dict[str, MITREMapping] = {}

        for ioc in iocs:

            results = self._provider.lookup(
                str(ioc.type)
            )

            for mapping in results:

                mappings[
                    mapping.id
                ] = mapping

        return list(
            mappings.values()
        )