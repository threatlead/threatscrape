import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from threatscrape.items import IanaTld
import dateparser
import idna
import re
from ipaddress import IPv4Address, IPv6Address, AddressValueError


class IanaTldSpider(CrawlSpider):
    name = 'iana_tld'
    allowed_domains = ['iana.org']
    start_urls = ['https://www.iana.org/domains/root/db']
    RE_LAST_UPDATE = re.compile(r'Record\s+last\s+updated\s+(.*?)\.', re.IGNORECASE)
    RE_REGISTRATION = re.compile(r'Registration\s+date\s+(.*?)\.', re.IGNORECASE)
    RE_TLD_NAME = re.compile(r'db/(.*?)\.html')
    RE_DESC = re.compile(r'<h2>(ccTLD Manager|Sponsoring Organisation)<\/h2>[\r\n\s]+<b>(.*?)<\/b>', re.IGNORECASE)

    rules = (
        # Select and Parse files we are interested in...
        Rule(LinkExtractor(allow=r'/domains/root/db/.*?\.html'), callback='parse_tld'),
    )

    def parse_ip(self, response, text):
        try:
            return IPv4Address(text)
        except AddressValueError:
            try:
                return IPv6Address(text)
            except AddressValueError:
                self.logger.critical(f'Unable to parse Ipaddress {text} from {response.url}')

    def parse_tld(self, response):
        name = self.RE_TLD_NAME.search(response.url)
        if not name:
            yield None
        last_update = self.RE_LAST_UPDATE.search(response.text)
        registration = self.RE_REGISTRATION.search(response.text)
        description = self.RE_DESC.search(response.text)
        tld_type = 'country-code' if 'Country-code top-level domain' in response.text else 'generic'
        nameservers = []
        for row in [row.xpath('td//text()') for row in response.css('.iana-table tbody tr')]:
            domain = row[0].extract()
            ips = [self.parse_ip(response, ip.extract()) for ip in row[1:]]
            ipv4 = list(filter(lambda ip: type(ip) == IPv4Address, ips))
            ipv6 = list(filter(lambda ip: type(ip) == IPv6Address, ips))
            nameservers.append([domain, ipv4, ipv6])
        yield IanaTld(
            idna=name[1] if name else None,
            name=idna.decode(name[1]) if name else None,
            type=tld_type,
            url=response.url,
            description=description[2] if description else '',
            nameservers=nameservers,
            last_update=dateparser.parse(last_update[1]).date() if last_update else None,
            registration=dateparser.parse(registration[1]).date() if registration else None,
        )


class IanaRootServerSpider(scrapy.Spider):
    # @TODO: Parse Root Server Information
    pass
