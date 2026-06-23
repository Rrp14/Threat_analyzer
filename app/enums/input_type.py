from enum import Enum


class InputType(str, Enum):
    TEXT = "text"
    FILE = "file"
    URL = "url"
    CVE = "cve"