from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp import web


@dataclass(frozen=True)
class ProductCategory:
    id: int
    name: str
    parent_category_id: int | None
    subcategories: dict[int, ProductCategory]
    products: dict[int, Product]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "parent": self.parent_category_id,
        }


@dataclass(frozen=True)
class Product:
    id: int
    category: ProductCategory
    name: str
    description: str
    price: str
    instock: bool
    properties: dict[str, str]
    rating: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category_id": self.category.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "instock": self.instock,
            "properties": self.properties,
            "rating": self.rating,
        }


@dataclass(frozen=True)
class ProductsAppData:
    categories: dict[int, ProductCategory]
    products: dict[int, Product]


ProductsDataKey = web.AppKey("data", ProductsAppData)
