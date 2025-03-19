from itemadapter import ItemAdapter

from tests.utils_extraction import get_web_poet_response
from zyte_test_websites.jobs.extraction import (
    TestJobPostingNavigationPage,
    TestJobPostingPage,
)


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
