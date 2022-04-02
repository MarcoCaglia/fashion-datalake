"""Test module for fashion-datalake library."""

import types
from hashlib import sha256

import pytest
from fashion_datalake.scraping.scraping.spiders.zalando_spider import (
    ZalandoSpiderSpider,
)
from fashion_datalake.utils.constants import TEST_ASSETS_PATH, ZALANDO_SOURCE_NAME
from scrapy.http import TextResponse

ZALANDO_CATALOGUE_FIRST_PAGE_PATH = TEST_ASSETS_PATH.joinpath(
    "zalando_catalogue_first_page.html"
)

ZALANDO_CATALOGUE_LAST_PAGE_PATH = TEST_ASSETS_PATH.joinpath(
    "zalando_catalogue_last_page.html"
)
ZALANDO_ITEM_PAGE_PATH = TEST_ASSETS_PATH.joinpath("zalando_last_page.html")


class TestZalandoSpiderGroup:
    """Test parsing functionality of zalando spider."""

    EXPECTED_SECOND_PAGE_URL = (
        "https://www.zalando.nl/dameskleding/?p=2&order=activation_date"
    )
    FIRST_PAGE_URL = "first_page.test"
    LAST_PAGE_URL = "last_page.test"
    ITEM_PAGE_URL = "item_page.test"

    EXPECTED_ITEM_ID = sha256(ITEM_PAGE_URL.encode("utf-8")).hexdigest()
    EXPECTED_URL = ITEM_PAGE_URL
    EXPECTED_SOURCE = ZALANDO_SOURCE_NAME
    EXPECTED_NUM_IMAGES = 97

    @pytest.fixture(scope="class")
    def zalando_catalogue_first_page(self):
        """Simulate text response for initial catalogue page."""
        with ZALANDO_CATALOGUE_FIRST_PAGE_PATH.open("r") as f:
            response = TextResponse(
                url=self.FIRST_PAGE_URL, body=f.read().encode("utf-8")
            )

        return response

    @pytest.fixture(scope="class")
    def zalando_catalogue_last_page(self):
        """Simulate text response for final catalogue page."""
        with ZALANDO_CATALOGUE_LAST_PAGE_PATH.open("r") as f:
            response = TextResponse(
                url=self.LAST_PAGE_URL, body=f.read().encode("utf-8")
            )

        return response

    @pytest.fixture(scope="class")
    def zalando_item_page(self):
        """Simulate text response for item page."""
        with ZALANDO_CATALOGUE_LAST_PAGE_PATH.open("r") as f:
            response = TextResponse(
                url=self.ITEM_PAGE_URL, body=f.read().encode("utf-8")
            )

        return response

    @pytest.fixture(scope="function")
    def test_spider(self):
        """Initialize test_spider."""
        test_spider = ZalandoSpiderSpider()

        return test_spider

    def start_request_returns_generator_test(self, test_spider):
        """Assert, that start_requests method returns a generator."""
        actual = test_spider.start_requests()

        assert isinstance(actual, types.GeneratorType)

    def parse_finds_second_page_test(self, test_spider, zalando_catalogue_first_page):
        """Assert that spider finds next page in catalogue on the first page."""
        actual = list(test_spider.parse(zalando_catalogue_first_page))

        assert actual[-1].url == self.EXPECTED_SECOND_PAGE_URL

    def parse_detects_last_page_test(self, test_spider, zalando_catalogue_last_page):
        """Assert, that the spider correctly recognizes final page of catalogue."""
        actual = list(test_spider.parse(zalando_catalogue_last_page))

        assert actual[-1].url.find("p=") == -1

    def parse_finds_items_on_item_page_test(self, test_spider, zalando_item_page):
        """Assert, that the spider finds all relevant information on the item page."""
        actual = list(test_spider.extract_item(zalando_item_page))[0]

        assert actual["id_item"] == self.EXPECTED_ITEM_ID
        assert actual["url"] == self.EXPECTED_URL
        assert actual["source"] == self.EXPECTED_SOURCE
        assert actual["raw_html"] == zalando_item_page.text
        assert len(actual["image_urls"]) == self.EXPECTED_NUM_IMAGES
