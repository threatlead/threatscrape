from dataclasses import dataclass
import datetime
from ipaddress import IPv4Address


@dataclass
class BlogPostItem:
    title: str
    url: str
    published: datetime.date
    authors: list
    source: str
    content: str = None


@dataclass
class IpaddressBlacklistItem:
    ipaddress: IPv4Address
    service: str
    last_seen: datetime.datetime


@dataclass
class IntelItem:
    source: str
    md5: str = None
    sha1: str = None
    sha256: str = None
    date: datetime.date = None
    domain: str = None
    url: str = None
    ipaddress: IPv4Address = None
    country: str = None
    asn: str = None


@dataclass
class IanaTldItem:
    description: str
    idna: str
    name: str
    nameservers: list
    type: str
    url: str
    registration: datetime.date = None
    last_update: datetime.date = None


@dataclass
class AsnItem:
    id: int
    name: str
    country_code: str = None


@dataclass
class DomainItem:
    name: str
    id: int = None


@dataclass
class CveItem:
    cve: str
    json: dict
    description: str = None
    cvss3_score: float = None
    cvss3_severity: str = None
    cvss2_score: float = None
    cvss2_severity: str = None
    published: datetime.datetime = None
    modified: datetime.datetime = None
