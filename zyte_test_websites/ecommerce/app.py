from __future__ import annotations

import json
from typing import Any

import aiohttp_jinja2
import jinja2
from aiohttp import web

from ..utils import get_default_data
from .models import Product, ProductCategory, ProductsAppData, ProductsDataKey
from .views import routes


def load_data(data: str) -> ProductsAppData:
    d: dict[str, list[dict[str, Any]]] = json.loads(data)
    categories: dict[int, ProductCategory] = {}
    products: dict[int, Product] = {}
    for cat_dict in d["categories"]:
        category = ProductCategory(
            id=cat_dict["id"],
            name=cat_dict["name"],
            parent_category_id=cat_dict["parent"],
            subcategories={},
            products={},
        )
        categories[cat_dict["id"]] = category
    for category in categories.values():
        if category.parent_category_id is not None:
            categories[category.parent_category_id].subcategories[category.id] = (
                category
            )
    for product_dict in d["products"]:
        category = categories[product_dict["category_id"]]
        product = Product(
            id=product_dict["id"],
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            instock=product_dict["instock"],
            properties=product_dict["properties"],
            rating=product_dict["rating"],
            category=category,
        )
        products[product_dict["id"]] = product
        category.products[product_dict["id"]] = product

    return ProductsAppData(categories=categories, products=products)


def make_app(data: str | None = None) -> web.Application:
    if data is None:
        data = get_default_data("ecommerce")
    app = web.Application()
    app[ProductsDataKey] = load_data(data)
    app.add_routes(routes)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader("zyte_test_websites.ecommerce", "static/templates"),
    )
    return app
