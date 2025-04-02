from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from aiohttp.pytest_plugin import AiohttpClient
    from aiohttp.test_utils import TestClient
    from aiohttp.web import Application, Request


def configure_itemadapter() -> None:
    try:
        from itemadapter import ItemAdapter
        from zyte_common_items import ZyteItemAdapter
    except ImportError:
        return
    ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)


configure_itemadapter()


@pytest.fixture
async def ecommerce_client(
    aiohttp_client: AiohttpClient,
) -> TestClient[Request, Application]:
    from zyte_test_websites.ecommerce.app import make_app

    app = make_app()
    return await aiohttp_client(app)


@pytest.fixture
async def jobs_client(
    aiohttp_client: AiohttpClient,
) -> TestClient[Request, Application]:
    from zyte_test_websites.jobs.app import make_app

    app = make_app()
    return await aiohttp_client(app)


@pytest.fixture
async def articles_client(
    aiohttp_client: AiohttpClient,
) -> TestClient[Request, Application]:
    from zyte_test_websites.articles.app import make_app

    app = make_app()
    return await aiohttp_client(app)
