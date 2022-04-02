# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapingItem(scrapy.Item):
    """Holds scraped item information of HTMLs and images."""

    id_item = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    raw_html = scrapy.Field()
    image_urls = scrapy.Field()
