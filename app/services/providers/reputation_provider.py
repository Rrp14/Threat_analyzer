from pathlib import Path
import json

from app.enums.reputation import ReputationLevel
from app.models.enrichment import ReputationScore
from app.services.providers.base import BaseProvider


class LocalReputationProvider(BaseProvider):

    def __init__(
        self,
        data_path: Path,
    ) -> None:
        self._data_path = data_path

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
        value: str,
    ) -> ReputationScore | None:

        result = self._data.get(value)

        if result is None:
            return None

        return ReputationScore(
            score=result["score"],
            level=ReputationLevel(result["level"]),
            source=self.source,
        )