from __future__ import annotations

from dataclasses import dataclass

from aiohttp import web


@dataclass(frozen=True)
class JobCategory:
    id: int
    name: str
    jobs: dict[int, Job]

    @property
    def url(self) -> str:
        return f"/jobs/{self.id}"


@dataclass(frozen=True)
class Job:
    id: int
    title: str
    category: JobCategory

    @property
    def url(self) -> str:
        return f"/job/{self.id}"


@dataclass(frozen=True)
class JobsAppData:
    categories: dict[int, JobCategory]
    jobs: dict[int, Job]


JobsDataKey = web.AppKey("data", JobsAppData)
