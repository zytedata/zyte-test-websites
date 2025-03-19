from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from itemadapter import ItemAdapter

from tests.utils import get_web_poet_response
from zyte_test_websites.jobs.app import make_app
from zyte_test_websites.jobs.extraction import (
    TestJobPostingNavigationPage,
    TestJobPostingPage,
)
from zyte_test_websites.jobs.views import CATS_PER_PAGE, JOBS_PER_PAGE

if TYPE_CHECKING:
    from aiohttp.pytest_plugin import AiohttpClient
    from aiohttp.test_utils import TestClient
    from aiohttp.web import Application, Request


@pytest.fixture
async def jobs_client(
    aiohttp_client: AiohttpClient,
) -> TestClient[Request, Application]:
    app = make_app()
    return await aiohttp_client(app)


async def test_index(jobs_client):
    response = await jobs_client.get("/")
    assert response.status == 200
    text = await response.text()
    assert "<h1>192 job categories:</h1>" in text
    assert '<ol id="categories" start="1">' in text
    assert text.count('class="category-li"') == CATS_PER_PAGE
    assert '<a href="/jobs/5">Infrastructure</a>' in text
    assert 'href="/?page=2">Next' in text


async def test_index_page_3(jobs_client):
    response = await jobs_client.get("/?page=3")
    assert response.status == 200
    text = await response.text()
    assert "<h1>192 job categories:</h1>" in text
    assert f'<ol id="categories" start="{2 * CATS_PER_PAGE + 1}">' in text
    assert text.count('class="category-li"') == CATS_PER_PAGE
    assert '<a href="/jobs/44">Retail</a>' in text
    assert 'href="/?page=4">Next' in text


async def test_job_list(jobs_client):
    response = await jobs_client.get("/jobs/4")
    assert response.status == 200
    text = await response.text()
    assert "<h1>109 jobs in Energy:</h1>" in text
    assert '<ol id="jobs" start="1">' in text
    assert text.count('class="job-li"') == JOBS_PER_PAGE
    assert (
        '<a class="job-link" href="/job/1583065288960216">Interior Designer</a>' in text
    )
    assert 'href="/jobs/4?page=2">Next' in text


async def test_job_list_page_3(jobs_client):
    response = await jobs_client.get("/jobs/4?page=3")
    assert response.status == 200
    text = await response.text()
    assert "<h1>109 jobs in Energy:</h1>" in text
    assert f'<ol id="jobs" start="{2 * JOBS_PER_PAGE + 1}">' in text
    assert text.count('class="job-li"') == JOBS_PER_PAGE
    assert '<a class="job-link" href="/job/2549680429101422">Brand Manager</a>' in text
    assert 'href="/jobs/4?page=4">Next' in text


async def test_job_detail(jobs_client):
    response = await jobs_client.get("/job/1888448280485890")
    assert response.status == 200
    text = await response.text()
    assert "<h1>Litigation Attorney</h1>" in text
    assert '<span class="job-location">Bogotá, Colombia</span>' in text


async def test_job_extraction(jobs_client):
    response = await get_web_poet_response(jobs_client, "/job/1888448280485890")
    page = TestJobPostingPage(response)
    descr = (
        "Family Law Attorneys deal with legal matters related to family"
        " relationships. They handle cases like divorce, child custody,"
        " adoption, and domestic disputes to provide legal guidance."
    )
    item = await page.to_item()
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "jobPostingId": "1888448280485890",
        "datePublished": "2023-09-07T00:00:00Z",
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


async def test_nav_extraction(jobs_client):
    response = await get_web_poet_response(jobs_client, "/jobs/4")
    page = TestJobPostingNavigationPage(response)
    item = await page.to_item()
    jobs = [
        ("1888448280485890", "Litigation Attorney"),
        ("1583065288960216", "Interior Designer"),
        ("2505213971303748", "IT Administrator"),
        ("2973702198556912", "Digital Marketing Specialist"),
        ("160399666386920", "Legal Assistant"),
        ("2226428310491314", "Customer Support Specialist"),
        ("2962173505197183", "Substance Abuse Counselor"),
        ("895360732760260", "Social Media Manager"),
        ("360775924046834", "Procurement Manager"),
        ("1939835498099785", "Physician Assistant"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "items": [
            {
                "url": str(response.urljoin(f"/job/{job[0]}")),
                "method": "GET",
                "name": job[1],
            }
            for job in jobs
        ],
        "nextPage": {"url": str(response.urljoin("/jobs/4?page=2")), "method": "GET"},
        "pageNumber": 1,
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }


async def test_nav_extraction_last_page(jobs_client):
    response = await get_web_poet_response(jobs_client, "/jobs/10?page=7")
    page = TestJobPostingNavigationPage(response)
    item = await page.to_item()
    jobs = [
        ("1387505175033096", "Event Coordinator"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "items": [
            {
                "url": str(response.urljoin(f"/job/{job[0]}")),
                "method": "GET",
                "name": job[1],
            }
            for job in jobs
        ],
        "pageNumber": 7,
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }


async def test_search(jobs_client):
    response = await jobs_client.get("/search?q=dEsIgn")
    assert response.status == 200
    text = await response.text()
    assert '<h1>437 jobs for search query "design":</h1>' in text
    assert '<ol id="jobs" start="1">' in text
    assert text.count('class="job-li"') == JOBS_PER_PAGE
    assert text.count(" Designer") == JOBS_PER_PAGE
    assert '<a class="job-link" href="/job/515759414812463">Web Designer</a>' in text
    assert 'href="/search?q=dEsIgn&amp;page=2">Next' in text


async def test_search_page_3(jobs_client):
    response = await jobs_client.get("/search?q=dEsIgn&page=3")
    assert response.status == 200
    text = await response.text()
    assert '<h1>437 jobs for search query "design":</h1>' in text
    assert f'<ol id="jobs" start="{2 * JOBS_PER_PAGE + 1}">' in text
    assert text.count('class="job-li"') == JOBS_PER_PAGE
    assert text.count(" Designer") == JOBS_PER_PAGE
    assert '<a class="job-link" href="/job/691709241515804">UX/UI Designer</a>' in text
    assert 'href="/search?q=dEsIgn&amp;page=4">Next' in text


async def test_search_empty(jobs_client):
    response = await jobs_client.get("/search?q=does-not-exist")
    assert response.status == 200
    text = await response.text()
    assert '<h1>0 jobs for search query "does-not-exist":</h1>' in text
    assert '<ol id="jobs" start="1">' in text
    assert 'class="job-li"' not in text
