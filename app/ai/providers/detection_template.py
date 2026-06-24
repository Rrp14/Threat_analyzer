from app.models.detection import (
    DetectionRules,
    SigmaRule,
    YaraRule,
    SIEMQuery,
)


class TemplateDetectionProvider:

    def generate_rules(
        self,
        context: dict,
    ) -> DetectionRules:

        domain = None
        hash_value = None

        for ioc in context["iocs"]:

            if (
                ioc["type"] == "domain"
                and domain is None
            ):
                domain = ioc["value"]

            if (
                ioc["type"] in {
                    "md5",
                    "sha1",
                    "sha256",
                }
                and hash_value is None
            ):
                hash_value = ioc["value"]

        sigma_yaml = self._build_sigma_rule(
            domain
        )

        yara_source = self._build_yara_rule(
            hash_value
        )

        splunk_query = self._build_splunk_query(
            domain
        )

        sentinel_query = (
            self._build_sentinel_query(
                domain
            )
        )

        return DetectionRules(
            sigma=SigmaRule(
                title=(
                    "Suspicious Domain Communication"
                ),
                yaml=sigma_yaml,
            ),
            yara=YaraRule(
                rule_name=(
                    "GeneratedThreatRule"
                ),
                source=yara_source,
            ),
            siem_queries=[
                SIEMQuery(
                    platform="splunk",
                    query=splunk_query,
                ),
                SIEMQuery(
                    platform="sentinel",
                    query=sentinel_query,
                ),
            ],
        )

    def _build_sigma_rule(
        self,
        domain: str | None,
    ) -> str:

        if not domain:
            domain = "suspicious-domain"

        return f"""
title: Suspicious Domain Communication
status: experimental
logsource:
  category: network_connection
detection:
  selection:
    DestinationHostname:
      - {domain}
  condition: selection
level: high
""".strip()

    def _build_yara_rule(
        self,
        hash_value: str | None,
    ) -> str:

        if not hash_value:
            hash_value = "UNKNOWN_HASH"

        return f"""
rule GeneratedThreatRule
{{
    strings:
        $ioc = "{hash_value}"

    condition:
        $ioc
}}
""".strip()

    def _build_splunk_query(
        self,
        domain: str | None,
    ) -> str:

        if not domain:
            domain = "suspicious-domain"

        return (
            f'search index=* "{domain}"'
        )

    def _build_sentinel_query(
        self,
        domain: str | None,
    ) -> str:

        if not domain:
            domain = "suspicious-domain"

        return f"""
DeviceNetworkEvents
| where RemoteUrl contains "{domain}"
""".strip()