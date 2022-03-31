import scrapy


class ZalandoSpiderSpider(scrapy.Spider):
    name = "zalando-spider"
    allowed_domains = ["zalando.nl"]
    start_urls = ["http://zalando.nl/"]

    def parse(self, response):
        pass
