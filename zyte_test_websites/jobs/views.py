from __future__ import annotations

import operator
from collections import defaultdict
from typing import Any

import aiohttp_jinja2
from aiohttp import web

from .items import Job, JobsDataKey

routes = web.RouteTableDef()


CATS_PER_PAGE = 20
JOBS_PER_PAGE = 10


@routes.get("/")
@aiohttp_jinja2.template("index.jinja2")
async def index(request: web.Request) -> dict[str, Any]:
    """Home page with a list of categories."""
    categories = request.app[JobsDataKey].categories

    try:
        page = int(request.query.get("page", 1))
    except ValueError:
        raise web.HTTPNotFound
    total_pages = len(categories) // CATS_PER_PAGE + 1
    if page > total_pages:
        raise web.HTTPNotFound

    start = CATS_PER_PAGE * (page - 1)
    return {
        "categories": sorted(categories.values(), key=operator.attrgetter("id"))[
            start : start + CATS_PER_PAGE
        ],
        "current_page": page,
        "total_pages": total_pages,
        "total_categories": len(categories),
        "start": start,
        "base_url": request.rel_url,
    }


@routes.get("/jobs/{category_id}", name="job_list")
@aiohttp_jinja2.template("job_list.jinja2")
async def job_list(request: web.Request) -> dict[str, Any]:
    """A page with a list of job postings"""
    try:
        category_id = int(request.match_info["category_id"])
    except ValueError:
        raise web.HTTPNotFound
    category = request.app[JobsDataKey].categories.get(category_id)
    if not category:
        raise web.HTTPNotFound

    try:
        page = int(request.query.get("page", 1))
    except ValueError:
        raise web.HTTPNotFound
    total_pages = len(category.jobs) // JOBS_PER_PAGE + 1
    if page > total_pages:
        raise web.HTTPNotFound

    start = JOBS_PER_PAGE * (page - 1)
    return {
        "category": category,
        "jobs": sorted(
            category.jobs.values(),
            key=operator.attrgetter("date_published"),
            reverse=True,
        )[start : start + JOBS_PER_PAGE],
        "current_page": page,
        "total_pages": total_pages,
        "total_jobs": len(category.jobs),
        "start": start,
        "base_url": request.rel_url,
    }


@routes.get("/job/{job_id}", name="job_detail")
@aiohttp_jinja2.template("job_detail.jinja2")
async def job_detail(request: web.Request) -> dict[str, Any]:
    """A job posting page"""
    try:
        job_id = int(request.match_info["job_id"])
    except ValueError:
        raise web.HTTPNotFound
    job = request.app[JobsDataKey].jobs.get(job_id)
    if not job:
        raise web.HTTPNotFound

    return {"job": job}


@routes.get("/search", name="search")
@aiohttp_jinja2.template("search_results.jinja2")
async def search(request: web.Request) -> dict[str, Any]:
    """A search results page"""
    try:
        page = int(request.query.get("page", 1))
    except ValueError:
        raise web.HTTPNotFound

    q = request.query.get("q")
    if not q:
        return {
            "jobs": [],
            "query": "",
            "current_page": page,
            "total_pages": 1,
            "total_jobs": 0,
            "start": 0,
            "base_url": request.rel_url,
        }

    q = q.lower()
    all_jobs = request.app[JobsDataKey].jobs
    fields = (
        "title",
        "description",
        "company_name",
        "location",
    )
    buckets: defaultdict[str, list[Job]] = defaultdict(list)

    for job in all_jobs.values():
        for field in fields:
            if q in getattr(job, field).lower():
                buckets[field].append(job)
                break

    jobs = []
    for field in fields:
        jobs.extend(
            sorted(
                buckets[field], key=operator.attrgetter("date_published"), reverse=True
            )
        )

    total_pages = len(jobs) // JOBS_PER_PAGE + 1
    if page > total_pages:
        raise web.HTTPNotFound

    start = JOBS_PER_PAGE * (page - 1)
    return {
        "jobs": jobs[start : start + JOBS_PER_PAGE],
        "query": q,
        "current_page": page,
        "total_pages": total_pages,
        "total_jobs": len(jobs),
        "start": start,
        "base_url": request.rel_url,
    }
