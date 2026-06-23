from enum import Enum


class RiskFactorType(str, Enum):
    CVSS = "cvss"
    EXPLOIT = "exploit"
    MALWARE = "malware"
    THREAT_ACTOR = "threat_actor"
    IOC_REPUTATION = "ioc_reputation"
    MITRE = "mitre"
    CUSTOM = "custom"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"    