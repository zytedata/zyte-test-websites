from aiohttp import web

from .views import index


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", index)
