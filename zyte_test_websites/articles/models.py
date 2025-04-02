from __future__ import annotations

from dataclasses import dataclass
from email.utils import format_datetime
from typing import TYPE_CHECKING, Any

from aiohttp import web

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class ArticleCategory:
    id: int
    name: str
    articles: dict[int, Article]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
        }


@dataclass(frozen=True)
class Article:
    id: int
    category: ArticleCategory
    author: Author
    title: str
    summary: str
    body: str
    date: datetime

    def get_rss_date(self) -> str:
        return format_datetime(self.date)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category_id": self.category.id,
            "author_id": self.author.id,
            "title": self.title,
            "summary": self.summary,
            "body": self.body,
            "date": self.date.isoformat(),
        }


@dataclass(frozen=True)
class Author:
    id: int
    name: str
    bio: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
        }


@dataclass(frozen=True)
class ArticlesAppData:
    articles: dict[int, Article]
    authors: dict[int, Author]
    categories: dict[int, ArticleCategory]


ArticlesDataKey = web.AppKey("data", ArticlesAppData)
