import scrapy
from threatscrape.items import DomainItem
import zipfile
import io


class OpenDnsTopDomainsSpider(scrapy.Spider):
    name = 'opendns_top_domains'
    allowed_domains = ['amazonaws.com', ]
    base_url = 'http://s3-us-west-1.amazonaws.com/umbrella-static'
    opendns_files = ('top-1m-TLD.csv', 'top-1m.csv')        # TLD, Domains
    default_file = opendns_files[1]                         # default is Domain data
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(OpenDnsTopDomainsSpider, self).__init__(*args, **kwargs)
        if kwargs.get('type') and kwargs.get('type').upper() == 'TLD':
            self.default_file = self.opendns_files[0]
        self.start_urls = [f'{self.base_url}/{self.default_file}.zip', ]

    def parse_zip(self, response, filename):
        opendns_zip = zipfile.ZipFile(io.BytesIO(response.body))
        with opendns_zip.open(filename) as opendns_file:
            return opendns_file.read()

    def parse(self, response):
        for line in self.parse_zip(response=response, filename=self.default_file).splitlines()[0:10]:
            rank, suffix = line.split(b',')
            yield DomainItem(name=suffix.decode('idna'), id=int(rank))
