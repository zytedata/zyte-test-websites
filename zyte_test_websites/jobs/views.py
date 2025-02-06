from __future__ import annotations

import operator
from typing import Any

import aiohttp_jinja2
from aiohttp import web

from .items import JobsDataKey

routes = web.RouteTableDef()


CATS_PER_PAGE = 10
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
    if page >= total_pages:
        raise web.HTTPNotFound

    return {
        "categories": sorted(categories.values(), key=operator.attrgetter("id"))[
            CATS_PER_PAGE * (page - 1) : CATS_PER_PAGE * page
        ],
        "current_page": page,
        "total_pages": total_pages,
        "total_categories": len(categories),
        "base_url": request.path,
    }


@routes.get("/jobs/{category_id}")
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

    return {
        "category": category,
        "jobs": sorted(
            category.jobs.values(),
            key=operator.attrgetter("date_published"),
            reverse=True,
        )[JOBS_PER_PAGE * (page - 1) : JOBS_PER_PAGE * page],
        "current_page": page,
        "total_pages": total_pages,
        "total_jobs": len(category.jobs),
        "base_url": request.path,
    }


@routes.get("/job/{job_id}")
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
