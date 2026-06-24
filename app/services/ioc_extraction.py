from app.enums.ioc import IOCType
from app.models.ioc import IOC
from app.services.patterns import IOC_PATTERNS


class IOCExtractionService:
    """
    Extract and validate IOCs from normalized text.
    """

    DEFAULT_CONFIDENCE = 0.7

    def extract(
        self,
        text: str,
    ) -> list[IOC]:
        """
        Extract validated and deduplicated IOCs.
        """

        extracted: dict[tuple[IOCType, str], IOC] = {}

        patterns = sorted(
            IOC_PATTERNS.items(),
            key=lambda item: item[1].priority,
        )

        for ioc_type, config in patterns:

            matches = config.pattern.findall(text)

            for match in matches:

                if isinstance(match,tuple):
                    value="".join(match).strip()
                else:    

                   value = match.strip()
                   value = value.rstrip(".,;:!?)")

                if not config.validator(value):
                    continue

                key = (ioc_type, value.lower())

                if key in extracted:
                    continue

                extracted[key] = IOC(
                    type=ioc_type,
                    value=value,
                    confidence=self.DEFAULT_CONFIDENCE,
                )

        return list(extracted.values())