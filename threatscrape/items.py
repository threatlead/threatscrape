from dataclasses import dataclass
import datetime
import ipaddr


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
    ipaddress: ipaddr.IPAddress
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
    ipaddress: ipaddr.IPAddress = None
    country: str = None
    asn: str = None


@dataclass
class IanaTld:
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
