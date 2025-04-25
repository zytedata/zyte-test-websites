import pytest

from zyte_test_websites.utils import get_total_pages


@pytest.mark.parametrize(
    ("total_items", "per_page", "expected"),
    [
        (0, 10, 1),
        (5, 10, 1),
        (10, 10, 1),
        (11, 10, 2),
        (15, 10, 2),
        (19, 10, 2),
        (20, 10, 2),
        (21, 10, 3),
        (5, 5, 1),
        (6, 5, 2),
    ],
)
def test_get_total_pages(total_items: int, per_page: int, expected: int) -> None:
    assert get_total_pages(total_items, per_page) == expected
