from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import aiohttp_jinja2
import jinja2
from aiohttp import web

from ..utils import get_default_data
from .models import Job, JobCategory, JobsAppData, JobsDataKey
from .views import routes


def load_data(data: str) -> JobsAppData:
    d: dict[str, list[dict[str, Any]]] = json.loads(data)
    categories: dict[int, JobCategory] = {}
    jobs: dict[int, Job] = {}
    for cat_dict in d["categories"]:
        category = JobCategory(id=cat_dict["id"], name=cat_dict["name"], jobs={})
        categories[cat_dict["id"]] = category
    for job_dict in d["jobs"]:
        category = categories[job_dict["category_id"]]
        job = Job(
            id=job_dict["id"],
            title=job_dict["title"],
            date_published=datetime.fromisoformat(job_dict["date_published"]),
            description=job_dict["description"],
            salary=job_dict["salary"],
            experience=job_dict["experience"],
            work_type=job_dict["work_type"],
            contact_name=job_dict["contact_name"],
            contact_phone=job_dict["contact_phone"],
            benefits=job_dict["benefits"],
            responsibilities=job_dict["responsibilities"],
            company_name=job_dict["company_name"],
            location=job_dict["location"],
            category=category,
        )
        jobs[job_dict["id"]] = job
        category.jobs[job_dict["id"]] = job

    return JobsAppData(categories=categories, jobs=jobs)


def make_app(data: str | None = None) -> web.Application:
    if data is None:
        data = get_default_data("jobs")
    app = web.Application()
    app[JobsDataKey] = load_data(data)
    app.add_routes(routes)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader("zyte_test_websites.jobs", "static/templates"),
    )
    return app
