from __future__ import annotations

from importlib.resources import files
from typing import Any


def get_default_data(site_name: str) -> str:
    return files(f"zyte_test_websites.{site_name}").joinpath("data.json").read_text()


def get_total_pages(total_items: int, per_page: int) -> int:
    """Calculate the total number of pages based on total items and items per page."""
    if total_items == 0:
        return 1
    return (total_items - 1) // per_page + 1


def get_pagination_args(page: int, total_pages: int, radius: int = 2) -> dict[str, Any]:
    # Calculate pagination range
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
