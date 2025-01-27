from __future__ import annotations

import operator
from typing import Any

import aiohttp_jinja2
from aiohttp import web

from .items import JobsDataKey

routes = web.RouteTableDef()


@routes.get("/")
@aiohttp_jinja2.template("index.jinja2")
async def index(request: web.Request) -> dict[str, Any]:
    """Home page with a list of categories."""
    # TODO: pagination
    categories = request.app[JobsDataKey].categories
    return {
        "categories": sorted(categories.values(), key=operator.attrgetter("id")),
        "total_categories": len(categories),
    }


@routes.get("/jobs/{category_id}")
@aiohttp_jinja2.template("job_list.jinja2")
async def job_list(request: web.Request) -> dict[str, Any]:
    """A page with a list of job postings"""
    # TODO: pagination
    category = request.app[JobsDataKey].categories[
        int(request.match_info["category_id"])
    ]
    return {
        "category": category,
        "jobs": category.jobs.values(),
        "total_jobs": len(category.jobs),
    }


@routes.get("/job/{job_id}")
@aiohttp_jinja2.template("job_detail.jinja2")
async def job_detail(request: web.Request) -> dict[str, Any]:
    """A job posting page"""
    return {"job": request.app[JobsDataKey].jobs[int(request.match_info["job_id"])]}
