from enum import Enum


class Reputation(str,Enum):
    MALICIOUS="malicious"
    SUSPICIOUS="suspicious"
    CLEAN="clean"
    UNKNOWN="unknown"

class ReputationLevel(str,Enum):
    CLEAN="clean"
    LOW_RISK="low_risk"
    SUSPICIOUS="suspicious"
    MALICIOUS="malicious"    