from enum import Enum


class IOCType(str,Enum):
    IPV4="ipv4"
    IPV6="ipv6"
    DOMAIN="domain"
    URL="url"
    EMAIL="email"
    MD5="md5"
    SHA1="sha1"
    SHA256="sha256"
    CVE="cve"




class Severity(str,Enum):
    Low='low'
    MEDIUM="medium"
    HIGH="high"
    CRITICAL="critical"