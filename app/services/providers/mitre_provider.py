from pathlib import Path
import json

from app.enums.mitre import ConfidenceLevel
from app.models.mitre import MITREMapping
from app.services.providers.base import BaseProvider


class LocalMitreProvider(BaseProvider):

    def __init__(
        self,
        data_path: Path,
    ) -> None:

        with open(
            data_path,
            encoding="utf-8",
        ) as file:
            self._data = json.load(file)

    @property
    def source(self) -> str:
        return "local"

    def lookup(
        self,
        key: str,
    ) -> list[MITREMapping]:

        mappings = self._data.get(
            key.lower(),
            [],
        )

        return [
            MITREMapping(
                tactic=item["tactic"],
                technique=item["technique"],
                id=item["id"],
                confidence=ConfidenceLevel(
                    item["confidence"]
                ),
            )
            for item in mappings
        ]