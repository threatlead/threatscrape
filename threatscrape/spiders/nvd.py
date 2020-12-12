from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from threatscrape.items import CveItem
import zipfile
import io
import json
import dateparser


class NvdCveSpider(CrawlSpider):
    name = 'nvd_cve'
    allowed_domains = ['nvd.nist.gov']
    start_urls = ['https://nvd.nist.gov/vuln/data-feeds']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # to support pagination that uses "search"
    }
    rules = ()

    def __init__(self, *args, **kwargs):
        if kwargs.get('type') and kwargs.get('type').upper() == 'MODIFIED':
            rule = LinkExtractor(allow=r'feeds/json/cve/1\.1/.*?modified\.json\.zip', deny_extensions=[])
        else:
            rule = LinkExtractor(allow=r'/feeds/json/cve/1\.1/.*?\.json\.zip', deny_extensions=[])
        self.rules = self.rules = (Rule(rule, callback='parse_cve'), )
        super(NvdCveSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def description(cve):
        try:
            for desc in cve['cve']['description']['description_data']:
                if desc['lang'] == 'en':
                    return desc['value']
        except KeyError:
            pass

    @staticmethod
    def cvss3_score(cve):
        try:
            return cve['impact']['baseMetricV3']['cvssV3']['baseScore']
        except KeyError:
            pass

    @staticmethod
    def cvss2_score(cve):
        try:
            return cve['impact']['baseMetricV2']['cvssV2']['baseScore']
        except KeyError:
            pass

    @staticmethod
    def cvss3_severity(cve):
        try:
            return cve['impact']['baseMetricV3']['cvssV3']['baseSeverity']
        except KeyError:
            pass

    @staticmethod
    def cvss2_severity(cve):
        try:
            return cve['impact']['baseMetricV2']['severity']
        except KeyError:
            pass

    def parse_cve(self, response):
        cvefilename = '.'.join(response.url.split('/')[-1].split('.')[0:-1])
        with zipfile.ZipFile(io.BytesIO(response.body)).open(cvefilename) as cvecontents:
            cve_json = json.loads(cvecontents.read())
            for cve in cve_json['CVE_Items']:
                yield CveItem(
                    cve=cve['cve']['CVE_data_meta']['ID'],
                    description=NvdCveSpider.description(cve),
                    cvss3_score=NvdCveSpider.cvss3_score(cve),
                    cvss3_severity=NvdCveSpider.cvss3_severity(cve),
                    cvss2_score=NvdCveSpider.cvss2_score(cve),
                    cvss2_severity=NvdCveSpider.cvss2_severity(cve),
                    published=dateparser.parse(cve['publishedDate']),
                    modified=dateparser.parse(cve['lastModifiedDate']),
                    json=cve,
                )
