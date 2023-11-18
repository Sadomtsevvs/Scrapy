from scrapy import Spider
from base64 import b64decode

PAGES_TO_PARSE = 5


class ProxiesSpider(Spider):
    name = "proxies"
    start_urls = [
        "http://free-proxy.cz/en/",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parsed_pages = 0

    def parse(self, response):

        for row in response.xpath('//*[@id="proxy_list"]//tbody//tr'):
            if row.xpath('td[1]/script[@type="text/javascript"]/text()').get() is None:
                continue
            yield {
                'ip_address': b64decode(row.xpath('td[1]/script/text()').get()[30:-3]).decode(),
                'port': row.xpath('td[2]/span/text()').get(),
            }

        self.parsed_pages += 1

        if self.parsed_pages < PAGES_TO_PARSE:
            next_page = response.urljoin(f'/en/proxylist/main/{self.parsed_pages + 1}')
            if next_page:
                yield response.follow(next_page, self.parse)
