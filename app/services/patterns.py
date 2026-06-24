from dataclasses import dataclass
import re
from re import Pattern
from typing import Callable

from app.enums.ioc import IOCType
from app.services.validators import (
    is_valid_cve,
    is_valid_domain,
    is_valid_email,
    is_valid_ipv4,
    is_valid_ipv6,
    is_valid_md5,
    is_valid_sha1,
    is_valid_sha256,
    is_valid_url,
)


@dataclass(frozen=True, slots=True)
class IOCPattern:
    """
    Extraction configuration for a single IOC type.
    """

    pattern: Pattern[str]
    priority: int
    validator: Callable[[str], bool]


IOC_PATTERNS: dict[IOCType, IOCPattern] = {

    IOCType.URL: IOCPattern(
        pattern=re.compile(
            r"https?://[^\s\"'>]+",
            re.IGNORECASE,
        ),
        priority=1,
        validator=is_valid_url,
    ),

    IOCType.EMAIL: IOCPattern(
        pattern=re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
        priority=2,
        validator=is_valid_email,
    ),

    IOCType.DOMAIN: IOCPattern(
        pattern=re.compile(
            r"\b(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
        priority=3,
        validator=is_valid_domain,
    ),

    IOCType.IPV4: IOCPattern(
        pattern=re.compile(
            r"\b(?:25[0-5]|2[0-4]\d|1?\d?\d)"
            r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b",
            re.IGNORECASE,
        ),
        priority=4,
        validator=is_valid_ipv4,
    ),

    IOCType.IPV6: IOCPattern(
        pattern=re.compile(
            r"\b(?:[A-F0-9]{1,4}:){2,7}[A-F0-9]{1,4}\b",
            re.IGNORECASE,
        ),
        priority=5,
        validator=is_valid_ipv6,
    ),

    IOCType.CVE: IOCPattern(
        pattern=re.compile(
            r"\bCVE-\d{4}-\d{4,7}\b",
            re.IGNORECASE,
        ),
        priority=6,
        validator=is_valid_cve,
    ),

    IOCType.SHA256: IOCPattern(
        pattern=re.compile(
            r"\b[a-fA-F0-9]{64}\b",
        ),
        priority=7,
        validator=is_valid_sha256,
    ),

    IOCType.SHA1: IOCPattern(
        pattern=re.compile(
            r"\b[a-fA-F0-9]{40}\b",
        ),
        priority=8,
        validator=is_valid_sha1,
    ),

    IOCType.MD5: IOCPattern(
        pattern=re.compile(
            r"\b[a-fA-F0-9]{32}\b",
        ),
        priority=9,
        validator=is_valid_md5,
    ),
}