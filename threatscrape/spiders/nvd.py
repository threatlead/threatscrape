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

    rules = (
        # Select and Parse files we are interested in...
        # add deny_extensions as by default scrapy ignores zip files
        Rule(LinkExtractor(allow=r'/feeds/json/cve/1\.1/.*?\.json\.zip', deny_extensions=[]), callback='parse_cve'),
    )

    def parse_cve(self, response):
        cvefilename = '.'.join(response.url.split('/')[-1].split('.')[0:-1])
        with zipfile.ZipFile(io.BytesIO(response.body)).open(cvefilename) as cvecontents:
            cve_json = json.loads(cvecontents.read())
            for cve in cve_json['CVE_Items']:
                yield CveItem(
                    cve=cve['cve']['CVE_data_meta']['ID'],
                    published=dateparser.parse(cve['publishedDate']),
                    modified=dateparser.parse(cve['lastModifiedDate']),
                    json=cve,
                )
                sys.exit()