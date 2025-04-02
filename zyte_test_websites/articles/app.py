from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import aiohttp_jinja2
import jinja2
from aiohttp import web

from ..utils import get_default_data
from .models import Article, ArticleCategory, ArticlesAppData, ArticlesDataKey, Author
from .views import routes


def load_data(data: str) -> ArticlesAppData:
    d: dict[str, list[dict[str, Any]]] = json.loads(data)
    articles: dict[int, Article] = {}
    categories: dict[int, ArticleCategory] = {}
    authors: dict[int, Author] = {}
    for author_dict in d["authors"]:
        author = Author(
            id=author_dict["id"],
            name=author_dict["name"],
            bio=author_dict["bio"],
        )
        authors[author.id] = author
    for category_dict in d["categories"]:
        category = ArticleCategory(
            id=category_dict["id"],
            name=category_dict["name"],
            articles={},
        )
        categories[category.id] = category
    for article_dict in d["articles"]:
        author = authors[article_dict["author_id"]]
        category = categories[article_dict["category_id"]]
        article = Article(
            id=article_dict["id"],
            category=category,
            author=author,
            title=article_dict["title"],
            summary=article_dict["summary"],
            body=article_dict["body"],
            date=datetime.fromisoformat(article_dict["date"]),
        )
        articles[article.id] = article
        category.articles[article_dict["id"]] = article

    return ArticlesAppData(articles=articles, authors=authors, categories=categories)


def make_app(data: str | None = None) -> web.Application:
    if data is None:
        data = get_default_data("articles")
    app = web.Application()
    app[ArticlesDataKey] = load_data(data)
    app.add_routes(routes)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader("zyte_test_websites.articles", "static/templates"),
    )
    return app
