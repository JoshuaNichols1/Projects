import scrapy


class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["woolworths.com"]
    start_urls = ["https://woolworths.com"]

    def parse(self, response):
        pass
