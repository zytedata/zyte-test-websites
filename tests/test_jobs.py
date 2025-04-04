from __future__ import annotations

from zyte_test_websites.jobs.views import CATS_PER_PAGE, JOBS_PER_PAGE


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


async def test_job_detail_404(jobs_client):
    response = await jobs_client.get("/job/33333333333333")
    assert response.status == 404


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
