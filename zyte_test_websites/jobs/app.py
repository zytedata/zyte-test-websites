from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import aiohttp_jinja2
import jinja2
from aiohttp import web

from .items import Job, JobCategory, JobsAppData, JobsDataKey
from .views import routes


def load_data(data_path: Path) -> JobsAppData:
    d: dict[str, list[dict[str, Any]]] = json.loads(data_path.read_bytes())
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
            category=category,
        )
        jobs[job_dict["id"]] = job
        category.jobs[job_dict["id"]] = job

    return JobsAppData(categories=categories, jobs=jobs)


def make_app(data_path: Path) -> web.Application:
    app = web.Application()
    app[JobsDataKey] = load_data(data_path)
    app.add_routes(routes)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(Path(__file__).parent / "static" / "templates"),
    )
    return app
