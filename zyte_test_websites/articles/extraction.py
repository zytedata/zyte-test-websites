from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from clear_html import clean_node, cleaned_node_to_html
from web_poet import field
from zyte_common_items import (
    Article,
    ArticleNavigationPage,
    ArticlePage,
    Author,
    ProbabilityRequest,
    Request,
)

if TYPE_CHECKING:
    from parsel import Selector


__all__ = [
    "TestArticleNavigationPage",
    "TestArticlePage",
]


def article_body_html_processor(value: Selector, page: Any) -> str:
    """Extract and clean the HTML from the provided selector."""
    cleaned_node = clean_node(value.root, page.url)
    return cleaned_node_to_html(cleaned_node)


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

    @field(out=[article_body_html_processor])
    def articleBodyHtml(self) -> Selector:
        return self.css(".article-content")[0]


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
