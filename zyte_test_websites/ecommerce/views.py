from __future__ import annotations

import operator
from collections import defaultdict
from typing import TYPE_CHECKING, Any

import aiohttp_jinja2
from aiohttp import web

from ..utils import get_total_pages
from .models import Product, ProductCategory, ProductsDataKey

if TYPE_CHECKING:
    from yarl import URL

routes = web.RouteTableDef()


CATS_PER_PAGE = 10
PRODUCTS_PER_PAGE = 10


def _make_breadcrumbs(
    app: web.Application, category: ProductCategory
) -> list[dict[str, str | URL]]:
    breadcrumbs: list[dict[str, str | URL]] = []
    while True:
        breadcrumbs.append(
            {
                "name": category.name,
                "url": app.router["category"].url_for(category_id=str(category.id)),
            }
        )
        if category.parent_category_id is None:
            break
        category = app[ProductsDataKey].categories[category.parent_category_id]
    breadcrumbs.reverse()
    return breadcrumbs


@routes.get("/", name="index")
@aiohttp_jinja2.template("index.jinja2")
async def index(request: web.Request) -> dict[str, Any]:
    """Home page with a list of categories."""
    # only top-level categories
    categories = [
        cat
        for cat in request.app[ProductsDataKey].categories.values()
        if cat.parent_category_id is None
    ]

    try:
        page = int(request.query.get("page", 1))
    except ValueError:
        raise web.HTTPNotFound
    total_pages = get_total_pages(len(categories), CATS_PER_PAGE)
    if page > total_pages:
        raise web.HTTPNotFound

    start = CATS_PER_PAGE * (page - 1)
    return {
        "categories": sorted(categories, key=operator.attrgetter("name"))[
            start : start + CATS_PER_PAGE
        ],
        "current_page": page,
        "total_pages": total_pages,
        "total_categories": len(categories),
        "start": start,
        "base_url": request.rel_url,
    }


@routes.get("/category/{category_id}", name="category")
@aiohttp_jinja2.template("category.jinja2")
async def category_detail(request: web.Request) -> dict[str, Any]:
    """A page with a list of subcategories and/or products"""
    try:
        category_id = int(request.match_info["category_id"])
    except ValueError:
        raise web.HTTPNotFound
    category = request.app[ProductsDataKey].categories.get(category_id)
    if not category:
        raise web.HTTPNotFound

    try:
        page = int(request.query.get("page", 1))
    except ValueError:
        raise web.HTTPNotFound
    total_pages = get_total_pages(len(category.products), PRODUCTS_PER_PAGE)
    if page > total_pages:
        raise web.HTTPNotFound

    breadcrumbs = _make_breadcrumbs(request.app, category)
    start = PRODUCTS_PER_PAGE * (page - 1)
    return {
        "category": category,
        "products": sorted(
            category.products.values(),
            key=operator.attrgetter("name"),
        )[start : start + PRODUCTS_PER_PAGE],
        "subcategories": sorted(
            category.subcategories.values(),
            key=operator.attrgetter("name"),
        ),
        "current_page": page,
        "total_pages": total_pages,
        "total_products": len(category.products),
        "start": start,
        "base_url": request.rel_url,
        "breadcrumbs": breadcrumbs,
    }


@routes.get("/product/{product_id}", name="product_detail")
@aiohttp_jinja2.template("product_detail.jinja2")
async def product_detail(request: web.Request) -> dict[str, Any]:
    """A product page"""
    try:
        product_id = int(request.match_info["product_id"])
    except ValueError:
        raise web.HTTPNotFound
    product = request.app[ProductsDataKey].products.get(product_id)
    if not product:
        raise web.HTTPNotFound

    breadcrumbs = _make_breadcrumbs(request.app, product.category)
    breadcrumbs.append({"name": product.name, "url": request.rel_url})
    return {
        "product": product,
        "breadcrumbs": breadcrumbs,
    }


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
            "products": [],
            "query": "",
            "current_page": page,
            "total_pages": 1,
            "total_products": 0,
            "start": 0,
            "base_url": request.rel_url,
        }

    q = q.lower()
    all_products = request.app[ProductsDataKey].products
    fields = (
        "name",
        "description",
    )
    buckets: defaultdict[str, list[Product]] = defaultdict(list)

    for product in all_products.values():
        for field in fields:
            if q in getattr(product, field).lower():
                buckets[field].append(product)
                break

    products = []
    for field in fields:
        products.extend(sorted(buckets[field], key=operator.attrgetter("name")))

    total_pages = get_total_pages(len(products), PRODUCTS_PER_PAGE)
    if page > total_pages:
        raise web.HTTPNotFound

    start = PRODUCTS_PER_PAGE * (page - 1)
    return {
        "products": products[start : start + PRODUCTS_PER_PAGE],
        "query": q,
        "current_page": page,
        "total_pages": total_pages,
        "total_products": len(products),
        "start": start,
        "base_url": request.rel_url,
    }
