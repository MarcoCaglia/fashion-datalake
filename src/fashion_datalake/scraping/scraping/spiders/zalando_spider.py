from hashlib import sha256

import scrapy
import yaml
from fashion_datalake.scraping.scraping.items import ScrapingItem
from fashion_datalake.utils.constants import SPIDER_CONFIG_PATH
from scrapy_splash import SplashRequest


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
        ).extract()

        # Follow all links
        for link in item_links:
            link = self.conform_request_schema(link)
            yield SplashRequest(url=link, callback=self.extract_item)

        # After all links have been followed, go to the next page, if there is
        # one available
        next_page = response.xpath(
            "/html/body/div/div/div/div/div/div/div/nav/div/a/@href"
        ).extract()
        next_page = (
            next_page[-1]
            if len(next_page) > 1 or next_page[-1].endswith("p=2")
            else None
        )

        if next_page is not None:
            next_page = self.conform_request_schema(next_page)
            yield SplashRequest(url=next_page, callback=self.parse)

    def extract_item(self, response):
        """Extract full HTML from an item."""
        # Initialize item
        item = ScrapingItem()

        # Fill item information
        item["id_item"] = sha256(response.url.encode("utf-8")).hexdigest()
        item["url"] = response.url
        item["source"] = "zalando"
        item["raw_html"] = response.text

        # Fill in image info TODO

        yield item

        # Load images
        item["image_urls"] = response.css(
            "img.RYghuO.u-6V88.ka2E9k.uMhVZi.FxZV-M._2Pvyxl.JT3_zV.EKabf7.mo6ZnF._1RurXL.mo6ZnF._7ZONEy"
        ).extract()

    def conform_request_schema(self, url: str) -> str:
        """Ensure that the passed URL complies with the required URL schema.

        Args:
            url (str): Compliant or un-compliant URL.

        Returns:
            str: Compliant URL.
        """
        if not url.startswith("https://www." + self.allowed_domains[0]):
            return "https://www." + self.allowed_domains[0] + url
        else:
            return url
