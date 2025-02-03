import pytest
from aiohttp.test_utils import TestClient

from zyte_test_websites.jobs.app import make_app
from zyte_test_websites.utils import get_default_data


@pytest.fixture
async def jobs_client(aiohttp_client) -> TestClient:
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
