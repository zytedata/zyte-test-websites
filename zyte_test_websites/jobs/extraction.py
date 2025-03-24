from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, cast

from web_poet import field
from zyte_common_items import (
    BaseSalary,
    HiringOrganization,
    JobLocation,
    JobPosting,
    JobPostingNavigationPage,
    JobPostingPage,
    ProbabilityRequest,
    Request,
)
from zyte_common_items.util import format_datetime

if TYPE_CHECKING:
    from parsel import Selector, SelectorList

__all__ = [
    "TestJobPostingNavigationPage",
    "TestJobPostingPage",
]


class TestJobPostingPage(JobPostingPage):
    def validate_input(self) -> JobPosting | None:
        if self.xpath("//dt[text()='Job description']"):
            return None
        return cast(JobPosting, self.no_item_found())

    @field
    def jobPostingId(self) -> str | None:
        return cast(str, self.url).rstrip("/").split("/")[-1]

    @field
    def datePublished(self) -> str | None:
        return format_datetime(datetime.strptime(self.datePublishedRaw, "%b %d, %Y"))

    @field(cached=True)  # type: ignore[misc]
    def datePublishedRaw(self) -> str | None:
        return self.css(".job-date::text").re_first(r"Published on (.+)")

    @field
    def jobTitle(self) -> str | None:
        return self.css("h1::text").get()

    @field
    def jobLocation(self) -> JobLocation | None:
        return JobLocation(raw=self.css(".job-location::text").get())

    @field
    def description(self) -> SelectorList[Selector]:
        return self.xpath("//dt[text()='Job description']/following-sibling::dd[1]")

    @field
    def employmentType(self) -> str | None:
        return self.css(".job-work-type::text").get()

    @field
    def baseSalary(self) -> BaseSalary | None:
        salary_range = self.xpath(
            "//dt[text()='Salary range']/following-sibling::dd/text()"
        ).get()
        if not salary_range:
            return None
        salary_min, salary_max = salary_range.strip().split("-", 1)
        return BaseSalary(
            valueMin=salary_min.lstrip("$"),
            valueMax=salary_max.lstrip("$"),
            currency="USD",
        )

    @field
    def requirements(self) -> list[str]:
        experience = self.xpath(
            "//dt[text()='Required experience']/following-sibling::dd/text()"
        ).get()
        return [experience.strip()] if experience else []

    @field
    def hiringOrganization(self) -> HiringOrganization | None:
        return HiringOrganization(name=self.css(".job-company::text").get())


class TestJobPostingNavigationPage(JobPostingNavigationPage):
    @field
    def items(self) -> list[ProbabilityRequest]:
        return [
            ProbabilityRequest(
                url=self.urljoin(item_link.css("::attr(href)").get()),
                name=item_link.css("::text").get(),
            )
            for item_link in self.css(".job-link")
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
