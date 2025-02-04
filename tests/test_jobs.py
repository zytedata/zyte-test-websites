from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from web_poet import HttpResponse
from zyte_common_items import JobPosting

from zyte_test_websites.jobs.app import make_app
from zyte_test_websites.jobs.extraction import TestJobPostingPage
from zyte_test_websites.utils import get_default_data

if TYPE_CHECKING:
    from aiohttp.pytest_plugin import AiohttpClient
    from aiohttp.test_utils import TestClient
    from aiohttp.web import Application, Request


@pytest.fixture
async def jobs_client(
    aiohttp_client: AiohttpClient,
) -> TestClient[Request, Application]:
    app = make_app(get_default_data("jobs"))
    return await aiohttp_client(app)


async def test_index(jobs_client):
    response = await jobs_client.get("/")
    assert response.status == 200
    text = await response.text()
    assert "<h1>192 job categories:</h1>" in text
    assert '<a href="/jobs/5">Infrastructure</a>' in text
    assert 'href="/?page=2">Next' in text


async def test_job_list(jobs_client):
    response = await jobs_client.get("/jobs/4")
    assert response.status == 200
    text = await response.text()
    assert "<h1>109 jobs in Energy:</h1>" in text
    assert (
        '<a class="job-link" href="/job/1583065288960216">Interior Designer</a>' in text
    )
    assert 'href="/jobs/4?page=2">Next' in text


async def test_job_detail(jobs_client):
    response = await jobs_client.get("/job/1888448280485890")
    assert response.status == 200
    text = await response.text()
    assert "<h1>Litigation Attorney</h1>" in text
    assert '<span class="job-location">Bogotá, Colombia</span>' in text


async def test_extraction(jobs_client):
    response = await jobs_client.get("/job/1888448280485890")
    url = str(response.url)
    web_poet_response = HttpResponse(url, await response.read())
    page = TestJobPostingPage(web_poet_response)
    descr = (
        "Family Law Attorneys deal with legal matters related to family"
        " relationships. They handle cases like divorce, child custody,"
        " adoption, and domestic disputes to provide legal guidance."
    )
    item = await page.to_item()
    assert item == JobPosting.from_dict(
        {
            "url": url,
            "datePublished": "2023-09-07T00:00:00",
            "datePublishedRaw": "Sep 07, 2023",
            "jobTitle": "Litigation Attorney",
            "jobLocation": {"raw": "Bogotá, Colombia"},
            "description": descr,
            "descriptionHtml": f"<article>\n\n<p>{descr}</p>\n\n</article>",
            "employmentType": "Contract",
            "baseSalary": {"valueMin": "63K", "valueMax": "101K", "currency": "USD"},
            "requirements": ["4 to 10 Years"],
            "hiringOrganization": {"name": "Drax Group"},
            "metadata": {
                "dateDownloaded": item.metadata.dateDownloaded,
                "probability": 1.0,
            },
        }
    )
