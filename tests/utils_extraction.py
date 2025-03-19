from __future__ import annotations

from typing import TYPE_CHECKING, Any

from web_poet import HttpResponse

if TYPE_CHECKING:
    from aiohttp.test_utils import TestClient


async def get_web_poet_response(client: TestClient[Any, Any], url: str) -> HttpResponse:
    response = await client.get(url)
    body = await response.read()
    return HttpResponse(str(response.url), body)
