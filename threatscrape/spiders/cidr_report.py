import scrapy
import re
from threatscrape.items import IpaddressBlacklistItem
from ..items import AsnItem


class CidrReportAsnSpider(scrapy.Spider):
    name = 'cidr_report_asn'
    allowed_domains = ['cidr-report.org']
    start_urls = ['https://www.cidr-report.org/as2.0/autnums.html']
    re_parse = re.compile('^.*?>AS(\d+)\s*<\/a>\s*(.*?),\s([A-Z]+)\s*$', re.MULTILINE)

    def parse(self, response):
        for asn in re.findall(self.re_parse, response.text):
            yield AsnItem(
                id=int(asn[0]),
                name=asn[1],
                country_code=asn[2],
            )



def cidr_report_asn_list():
    regex_cidr_report = re.compile('^.*?>AS(\d+)\s*<\/a>\s*(.*?),\s([A-Z]+)\s*$', re.MULTILINE)
    response = requests.get('https://www.cidr-report.org/as2.0/autnums.html')
    asn_list = regex_cidr_report.findall(response.text)
    return [[int(asn[0]), asn[1], asn[2]] for asn in asn_list[1:]]