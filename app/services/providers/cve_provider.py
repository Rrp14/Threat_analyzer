from pathlib import Path
import json

from app.enums.ioc import Severity
from app.models.ioc import CVEDetail
from app.services.providers.base import BaseProvider


class LocalCVEProvider(BaseProvider):

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
    ) -> CVEDetail | None:

        result = self._data.get(value)

        if result is None:
            return None

        return CVEDetail(
            id=value,
            cvss=result["cvss"],
            severity=Severity(result["severity"]),
            description=result["description"],
            exploit_available=result.get(
                "exploit_available",
                False,
            ),
            affected_products=result.get(
                "affected_products",
                [],
            ),
        )