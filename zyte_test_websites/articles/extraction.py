from __future__ import annotations

from datetime import datetime
from typing import cast

from web_poet import field
from zyte_common_items import (
    Article,
    ArticleNavigationPage,
    ArticlePage,
    Author,
    ProbabilityRequest,
    Request,
)

__all__ = [
    "TestArticleNavigationPage",
    "TestArticlePage",
]


class TestArticlePage(ArticlePage):
    def validate_input(self) -> Article | None:
        if self.css(".article-content"):
            return None
        return cast("Article", self.no_item_found())

    @field
    def headline(self) -> str | None:
        return self.css("h1::text").get()

    @field
    def datePublished(self) -> str | None:
        return datetime.strptime(self.datePublishedRaw, "%B %d, %Y").isoformat()

    @field(cached=True)  # type: ignore[misc]
    def datePublishedRaw(self) -> str | None:
        date = self.xpath(
            "//strong[text()='Published:']/following-sibling::text()[1]"
        ).get()
        return date.strip() if date else None

    @field
    def authors(self) -> list[Author] | None:
        author_a = self.xpath("//strong[text()='Author:']/following-sibling::a[1]")
        author_url = author_a.css("::attr(href)").get()
        return (
            [
                Author(
                    name=author_a.css("::text").get(),
                    url=self.urljoin(author_url),
                )
            ]
            if author_url
            else None
        )

    @field
    def description(self) -> str | None:
        return self.css(".lead::text").get()

    @field
    def articleBody(self) -> str | None:
        return self.css(".article-content div::text").get()

    @field
    def articleBodyHtml(self) -> str | None:
        return self.css(".article-content").get()


class TestArticleNavigationPage(ArticleNavigationPage):
    @field
    def categoryName(self) -> str | None:
        return self.css("h1::text").re_first(r"articles in the (.+) category")

    @field
    def items(self) -> list[ProbabilityRequest] | None:
        return [
            ProbabilityRequest(
                url=self.urljoin(item_link.css("::attr(href)").get()),
                name=item_link.css("::text").get(),
            )
            for item_link in self.css("h2.card-title a")
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
