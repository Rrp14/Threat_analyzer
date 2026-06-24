import ipaddress
import re
from urllib.parse import urlparse


_DOMAIN_PATTERN = re.compile(
    r"^(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}$"
)

_EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

_MD5_PATTERN = re.compile(
    r"^[a-fA-F0-9]{32}$"
)

_SHA1_PATTERN = re.compile(
    r"^[a-fA-F0-9]{40}$"
)

_SHA256_PATTERN = re.compile(
    r"^[a-fA-F0-9]{64}$"
)

_CVE_PATTERN = re.compile(
    r"^CVE-\d{4}-\d{4,7}$",
    re.IGNORECASE,
)

_INVALID_DOMAIN_SUFFIXES = {
    "exe",
    "dll",
    "bat",
    "ps1",
    "vbs",
    "scr",
}


def is_valid_domain(value: str) -> bool:

    if not _DOMAIN_PATTERN.fullmatch(value):
        return False

    suffix = value.rsplit(".", 1)[-1].lower()

    if suffix in _INVALID_DOMAIN_SUFFIXES:
        return False

    return True


def is_valid_ipv4(value: str) -> bool:
    try:
        return isinstance(
            ipaddress.ip_address(value),
            ipaddress.IPv4Address,
        )
    except ValueError:
        return False


def is_valid_ipv6(value: str) -> bool:
    try:
        return isinstance(
            ipaddress.ip_address(value),
            ipaddress.IPv6Address,
        )
    except ValueError:
        return False





def is_valid_url(value: str) -> bool:
    parsed = urlparse(value)

    return bool(
        parsed.scheme and
        parsed.netloc
    )


def is_valid_email(value: str) -> bool:
    return bool(_EMAIL_PATTERN.fullmatch(value))


def is_valid_md5(value: str) -> bool:
    return bool(_MD5_PATTERN.fullmatch(value))


def is_valid_sha1(value: str) -> bool:
    return bool(_SHA1_PATTERN.fullmatch(value))


def is_valid_sha256(value: str) -> bool:
    return bool(_SHA256_PATTERN.fullmatch(value))


def is_valid_cve(value: str) -> bool:
    return bool(_CVE_PATTERN.fullmatch(value))