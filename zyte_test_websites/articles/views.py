from __future__ import annotations

import operator
from collections import defaultdict
from typing import Any

import aiohttp_jinja2
from aiohttp import web

from .models import Article, ArticlesDataKey

routes = web.RouteTableDef()


ARTICLES_PER_PAGE = 10
ARTICLES_PER_FEED = 20


@routes.get("/authors", name="authors")
@aiohttp_jinja2.template("authors.jinja2")
async def authors_list(request: web.Request) -> dict[str, Any]:
    authors = request.app[ArticlesDataKey].authors.values()
    return {"authors": sorted(authors, key=operator.attrgetter("name"))}


@routes.get("/about", name="about")
@aiohttp_jinja2.template("about.jinja2")
async def about(request: web.Request) -> dict[str, Any]:
    return {}


@routes.get("/privacy", name="privacy")
@aiohttp_jinja2.template("privacy.jinja2")
async def privacy(request: web.Request) -> dict[str, Any]:
    return {}


@routes.get("/contact", name="contact")
@aiohttp_jinja2.template("contact.jinja2")
async def contact(request: web.Request) -> dict[str, Any]:
    return {}


@routes.get("/", name="index")
@aiohttp_jinja2.template("index.jinja2")
async def index(request: web.Request) -> dict[str, Any]:
    """A home page with a list of categories and top articles."""
    categories = request.app[ArticlesDataKey].categories.values()
    articles = request.app[ArticlesDataKey].articles.values()

    return {
        "articles": sorted(articles, key=operator.attrgetter("date"), reverse=True)[
            :ARTICLES_PER_PAGE
        ],
        "categories": sorted(categories, key=operator.attrgetter("name")),
        "base_url": request.rel_url,
    }


@routes.get("/articles/{category_id}", name="article_list")
@aiohttp_jinja2.template("article_list.jinja2")
async def article_list(request: web.Request) -> dict[str, Any]:
    """A category page with a list of articles."""
    try:
        category_id = int(request.match_info["category_id"])
    except ValueError:
        raise web.HTTPNotFound
    category = request.app[ArticlesDataKey].categories.get(category_id)
    if not category:
        raise web.HTTPNotFound

    try:
        page = int(request.query.get("page", 1))
    except ValueError:
        raise web.HTTPNotFound
    total_pages = len(category.articles) // ARTICLES_PER_PAGE + 1
    if page > total_pages:
        raise web.HTTPNotFound

    articles = category.articles.values()
    start = ARTICLES_PER_PAGE * (page - 1)
    return {
        "category": category,
        "articles": sorted(articles, key=operator.attrgetter("date"), reverse=True)[
            start : start + ARTICLES_PER_PAGE
        ],
        "total_articles": len(articles),
        "start": start,
        "base_url": request.rel_url,
        **get_pagination_args(page, total_pages),
    }


@routes.get("/article/{article_id}", name="article_detail")
@aiohttp_jinja2.template("article_detail.jinja2")
async def article_detail(request: web.Request) -> dict[str, Any]:
    """An article page"""
    try:
        article_id = int(request.match_info["article_id"])
    except ValueError:
        raise web.HTTPNotFound
    article = request.app[ArticlesDataKey].articles.get(article_id)
    if not article:
        raise web.HTTPNotFound

    return {
        "article": article,
    }


@routes.get("/author/{author_id}", name="author")
@aiohttp_jinja2.template("author.jinja2")
async def author(request: web.Request) -> dict[str, Any]:
    """An author page"""
    try:
        author_id = int(request.match_info["author_id"])
    except ValueError:
        raise web.HTTPNotFound
    author = request.app[ArticlesDataKey].authors.get(author_id)
    if not author:
        raise web.HTTPNotFound

    return {
        "author": author,
    }


@routes.get("/rss.xml", name="rss")
async def rss(request: web.Request) -> web.StreamResponse:
    """RSS feed of latest articles."""
    articles = request.app[ArticlesDataKey].articles.values()
    articles_feed = sorted(articles, key=operator.attrgetter("date"), reverse=True)[
        :ARTICLES_PER_FEED
    ]
    context = {
        "articles": articles_feed,
        "base_abs_url": request.url,
    }
    response = aiohttp_jinja2.render_template("rss.jinja2", request, context)
    response.headers["Content-Type"] = "application/rss+xml"
    return response


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
            "articles": [],
            "query": "",
            "total_articles": 0,
            "start": 0,
            "base_url": request.rel_url,
            **get_pagination_args(page, 1),
        }

    q = q.lower()
    all_articles = request.app[ArticlesDataKey].articles
    fields = (
        "title",
        "summary",
        "body",
    )
    buckets: defaultdict[str, list[Article]] = defaultdict(list)

    for article in all_articles.values():
        for field in fields:
            if q in getattr(article, field).lower():
                buckets[field].append(article)
                break

    articles = []
    for field in fields:
        articles.extend(
            sorted(buckets[field], key=operator.attrgetter("date"), reverse=True)
        )

    total_pages = len(articles) // ARTICLES_PER_PAGE + 1
    if page > total_pages:
        raise web.HTTPNotFound

    start = ARTICLES_PER_PAGE * (page - 1)
    return {
        "articles": articles[start : start + ARTICLES_PER_PAGE],
        "query": q,
        "total_articles": len(articles),
        "start": start,
        "base_url": request.rel_url,
        **get_pagination_args(page, total_pages),
    }


def get_pagination_args(page: int, total_pages: int) -> dict[str, Any]:
    # Calculate pagination range
    radius = 2  # Show 2 pages before and after current page
    page_range_start = max(1, page - radius)
    page_range_end = min(total_pages, page + radius)
    # Ensure we always show the first and last pages
    show_start_ellipsis = page_range_start > 1
    show_end_ellipsis = page_range_end < total_pages
    page_range = range(page_range_start, page_range_end + 1)
    return {
        "current_page": page,
        "total_pages": total_pages,
        "page_range": page_range,
        "show_end_ellipsis": show_end_ellipsis,
        "show_start_ellipsis": show_start_ellipsis,
    }
