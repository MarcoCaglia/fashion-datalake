import scrapy
from scrapy_splash import SplashRequest
from fashion_datalake.utils.constants import SPIDER_CONFIG_PATH
import yaml


class ZalandoSpiderSpider(scrapy.Spider):
    name = "zalando-spider"
    with SPIDER_CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f)
        allowed_domains = config[name].get("allowed_domains")
        start_urls = config[name].get("start_urls")

    def start_requests(self):
        """Request webpages through Splash API."""
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        """Extract items from webpages.

        After all items received, move to next page, if one is available.
        """
        # Get all items on this site
        item_links = response.css(
            "a._LM.JT3_zV.CKDt_l.CKDt_l.LyRfpJ::attr(href)"
        ).extract_all()

        # Follow all links
        for link in item_links:
            yield SplashRequest(url=link, callback=self.extract_item)

        # After all links have been followed, go to the next page # TODO

    def extract_item(self, response):
        """Extract full HTML from an item."""
        pass  # TODO
