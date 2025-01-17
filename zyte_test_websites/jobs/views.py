from aiohttp import web


async def index(request: web.Request) -> web.Response:
    return web.Response(text="Hello Aiohttp!")
