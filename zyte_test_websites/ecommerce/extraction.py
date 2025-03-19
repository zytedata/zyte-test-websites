from __future__ import annotations

from typing import TYPE_CHECKING, cast
from urllib.parse import urljoin

import attrs
from web_poet import field
from zyte_common_items import (
    AdditionalProperty,
    AggregateRating,
    Breadcrumb,
    Link,
    ProbabilityRequest,
    ProductFromList,
    ProductFromListSelectorExtractor,
    ProductListPage,
    ProductNavigationPage,
    ProductPage,
    Request,
)
from zyte_common_items.pages import PriceMixin

if TYPE_CHECKING:
    from parsel import Selector, SelectorList

__all__ = [
    "TestProductListPage",
    "TestProductNavigationPage",
    "TestProductPage",
]


class TestProductPage(ProductPage):
    @field
    def additionalProperties(self) -> list[AdditionalProperty] | None:
        result: list[AdditionalProperty] = []
        for dt in self.xpath(
            "//h2[text()='Product Information']/following-sibling::dl[1]/dt"
        ):
            name = dt.xpath("text()").get().strip()
            value = dt.xpath("following-sibling::dd[1]/text()").get().strip()
            result.append(AdditionalProperty(name=name, value=value))
        return result

    @field
    def aggregateRating(self) -> AggregateRating | None:
        rating = len(self.css(".star.filled"))
        return AggregateRating(bestRating=5.0, ratingValue=rating)

    @field
    def availability(self) -> str | None:
        if self.xpath("//p[text()='In stock']"):
            return "InStock"
        if self.xpath("//p[text()='Out of stock']"):
            return "OutOfStock"
        return None

    @field
    def breadcrumbs(self) -> list[Breadcrumb] | None:
        return self.css("nav[aria-label=breadcrumb]")

    @field
    def description(self) -> SelectorList[Selector]:
        return self.xpath("//h2[text()='Product Description']/following-sibling::p[1]")

    @field
    def name(self) -> str | None:
        return self.css("h1::text").get()

    @field
    def price(self) -> SelectorList[Selector]:
        return self.xpath("//p[contains(text(), 'Price: ')]/text()")

    @field
    def productId(self) -> str | None:
        return cast(str, self.url).rstrip("/").split("/")[-1]

    @field
    def sku(self) -> str | None:
        prop: AdditionalProperty
        for prop in self.additionalProperties:
            if prop.name == "UPC":
                return prop.value
        return None


class TestProductNavigationPage(ProductNavigationPage):
    @field
    def categoryName(self) -> str | None:
        return self.css("h1::text").get()

    @field
    def items(self) -> list[ProbabilityRequest]:
        return [
            ProbabilityRequest(
                url=self.urljoin(item_link.css("::attr(href)").get()),
                name=item_link.css("::text").get(),
            )
            for item_link in self.css(".product-link")
        ]

    @field
    def nextPage(self) -> Request | None:
        next_url = self.css(".page-item.next .page-link::attr(href)").get()
        if not next_url:
            return None
        return Request(url=self.urljoin(next_url))

    @field
    def pageNumber(self) -> int | None:
        page_number = self.css(".page-item.active .page-link::text").get()
        if not page_number:
            return None
        return int(page_number.strip())

    @field
    def subCategories(self) -> list[ProbabilityRequest] | None:
        return [
            ProbabilityRequest(
                url=self.urljoin(subcat_link.css("::attr(href)").get()),
                name=subcat_link.css("::text").get(),
            )
            for subcat_link in self.css(".subcategory-link")
        ]


@attrs.define
class TestProductFromListExtractor(ProductFromListSelectorExtractor, PriceMixin):
    base_url: str

    @field
    def name(self) -> str | None:
        return self.css("a::text").get()

    @field
    def price(self) -> SelectorList[Selector]:
        return self.xpath("p[1]/text()")

    @field
    def productId(self) -> str | None:
        return cast(str, self.url).rstrip("/").split("/")[-1]

    @field
    def url(self) -> str | None:
        return urljoin(self.base_url, self.css("a.product-link::attr(href)").get())


class TestProductListPage(ProductListPage):
    @field
    def breadcrumbs(self) -> list[Breadcrumb] | None:
        return self.css("nav[aria-label=breadcrumb]")

    @field
    def categoryName(self) -> str | None:
        return self.css("h1::text").get()

    @field
    def pageNumber(self) -> int | None:
        page_number = self.css(".page-item.active .page-link::text").get()
        if not page_number:
            return None
        return int(page_number.strip())

    @field
    def paginationNext(self) -> Link | None:
        next_link = self.css(".page-item.next .page-link")
        if not next_link:
            return None
        return Link(
            url=self.urljoin(next_link.css("::attr(href)").get()),
            text=next_link.css("::text").get(),
        )

    @field
    async def products(self) -> list[ProductFromList] | None:
        return [
            await TestProductFromListExtractor(sel, str(self.response.url)).to_item()
            for sel in self.css(".product-li")
        ]
