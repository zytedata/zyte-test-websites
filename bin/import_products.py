#!/usr/bin/python3
"""Scrapes http://books.toscrape.com/ into the format suitable for zyte_test_websites/ecommerce/data.json."""

from __future__ import annotations

import json
import operator
import re
import sys
from hashlib import md5
from pathlib import Path
from typing import TYPE_CHECKING, Any

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from twisted.python import log

if TYPE_CHECKING:
    from scrapy.http import Response

# The website has a flat list of categories, so we add some new ones (id >= 1000)
# and then put some of the website categories as subcategories of others.
# This gives us categories that have subcategories, products, or both
# (and one that has neither).

categories = {
    2: {"name": "Travel", "parent": 1003},
    3: {"name": "Mystery", "parent": 1001},
    4: {"name": "Historical Fiction"},
    5: {"name": "Sequential Art", "parent": 1000},
    6: {"name": "Classics", "parent": 1002},
    7: {"name": "Philosophy", "parent": 1002},
    8: {"name": "Romance", "parent": 1001},
    9: {"name": "Womens Fiction", "parent": 1003},
    10: {"name": "Fiction"},
    11: {"name": "Children's"},
    12: {"name": "Religion"},
    13: {"name": "Nonfiction"},
    14: {"name": "Music", "parent": 1000},
    15: {"name": "Default", "parent": 1003},
    16: {"name": "Science Fiction", "parent": 1001},
    17: {"name": "Sports and Games", "parent": 1003},
    18: {"name": "Add a comment", "parent": 1003},
    19: {"name": "Fantasy", "parent": 1001},
    20: {"name": "New Adult", "parent": 11},
    21: {"name": "Young Adult", "parent": 11},
    22: {"name": "Science", "parent": 13},
    23: {"name": "Poetry", "parent": 1000},
    24: {"name": "Paranormal", "parent": 1001},
    25: {"name": "Art", "parent": 1000},
    26: {"name": "Psychology", "parent": 13},
    27: {"name": "Autobiography", "parent": 13},
    28: {"name": "Parenting", "parent": 13},
    29: {"name": "Adult Fiction", "parent": 10},
    30: {"name": "Humor", "parent": 1003},
    31: {"name": "Horror", "parent": 1001},
    32: {"name": "History", "parent": 13},
    33: {"name": "Food and Drink", "parent": 13},
    34: {"name": "Christian Fiction", "parent": 12},
    35: {"name": "Business", "parent": 13},
    36: {"name": "Biography", "parent": 13},
    37: {"name": "Thriller", "parent": 1001},
    38: {"name": "Contemporary", "parent": 10},
    39: {"name": "Spirituality", "parent": 12},
    40: {"name": "Academic", "parent": 1002},
    41: {"name": "Self Help", "parent": 13},
    42: {"name": "Historical", "parent": 10},
    43: {"name": "Christian", "parent": 12},
    44: {"name": "Suspense", "parent": 1001},
    45: {"name": "Short Stories", "parent": 10},
    46: {"name": "Novels", "parent": 10},
    47: {"name": "Health", "parent": 13},
    48: {"name": "Politics", "parent": 13},
    49: {"name": "Cultural", "parent": 10},
    50: {"name": "Erotica"},
    51: {"name": "Crime", "parent": 1001},
    1000: {"name": "Arts & Creativity"},
    1001: {"name": "Genre Fiction"},
    1002: {"name": "Classics & Philosophy"},
    1003: {"name": "Lifestyle & Miscellaneous"},
    1004: {"name": "Empty"},
}

products: list[dict[str, Any]] = []


class BookSpider(Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    @staticmethod
    def _extract_id(url: str) -> int:
        return int(re.match(r".*_(\d+)/[^/]+\.html", url).group(1))

    @staticmethod
    def _extract_rating(s: str) -> int:
        return ["One", "Two", "Three", "Four", "Five"].index(s.split(" ", 1)[1]) + 1

    def parse(self, response: Response) -> Any:
        for category_url in response.css(
            "div.side_categories ul.nav-list > li > ul > li a::attr(href)"
        ).getall():
            yield response.follow(
                category_url,
                callback=self.parse_category,
            )

    def parse_category(self, response: Response) -> Any:
        category_id = self._extract_id(response.url)

        for book_url in response.css("article.product_pod a::attr(href)").getall():
            yield response.follow(
                book_url,
                callback=self.parse_book,
                cb_kwargs={"category_id": category_id},
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_category,
            )

    def parse_book(self, response: Response, category_id: int) -> Any:
        product_id = self._extract_id(response.url)
        name = response.css(".product_main h1::text").get()
        price = response.css(".price_color::text").get()
        description = response.xpath(
            "//div[@id='product_description']/following-sibling::p[1]/text()"
        ).get(default="")

        # all items are in stock on the website so mark some random ones as out of stock
        # (it's useful to make this deterministically)
        instock = int(md5(name.encode()).hexdigest(), 16) % 4 != 0  # noqa: S324

        properties: dict[str, str] = {}
        for row in response.css("table.table-striped tr"):
            key = row.css("th::text").get()
            if not instock and key == "Availability":
                # skip "In stock (N available)" for items which we've marked out of stock
                continue
            value = row.css("td::text").get()
            properties[key] = value

        products.append(
            {
                "id": product_id,
                "category_id": category_id,
                "name": name,
                "description": description,
                "price": price,
                "instock": instock,
                "properties": properties,
                "rating": self._extract_rating(
                    response.css(".star-rating::attr(class)").get()
                ),
            }
        )


def main() -> None:
    output_file = sys.argv[1]

    process = CrawlerProcess(
        {
            "CONCURRENT_REQUESTS": 32,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 32,
        }
    )
    d = process.crawl(BookSpider)
    d.addErrback(log.err)
    process.start()
    data = {
        "categories": [
            {
                "id": category_id,
                "name": categories[category_id]["name"],
                "parent": categories[category_id].get("parent"),
            }
            for category_id in sorted(categories)
        ],
        "products": sorted(products, key=operator.itemgetter("id")),
    }
    Path(output_file).write_text(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
