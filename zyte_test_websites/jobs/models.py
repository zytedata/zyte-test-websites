from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from aiohttp import web

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class JobCategory:
    id: int
    name: str
    jobs: dict[int, Job]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
        }


@dataclass(frozen=True)
class Job:
    id: int
    category: JobCategory
    title: str
    date_published: datetime
    description: str
    salary: str
    experience: str
    work_type: str
    contact_name: str
    contact_phone: str
    benefits: list[str]
    responsibilities: str
    company_name: str
    location: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category_id": self.category.id,
            "title": self.title,
            "date_published": self.date_published.isoformat(),
            "description": self.description,
            "salary": self.salary,
            "experience": self.experience,
            "work_type": self.work_type,
            "contact_name": self.contact_name,
            "contact_phone": self.contact_phone,
            "benefits": self.benefits,
            "responsibilities": self.responsibilities,
            "company_name": self.company_name,
            "location": self.location,
        }


@dataclass(frozen=True)
class JobsAppData:
    categories: dict[int, JobCategory]
    jobs: dict[int, Job]


JobsDataKey = web.AppKey("data", JobsAppData)
