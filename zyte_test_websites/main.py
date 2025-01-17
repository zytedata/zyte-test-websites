import sys

from aiohttp import web

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} jobs <port>")
        sys.exit(1)

    port = int(sys.argv[2])

    from .jobs.app import app

    web.run_app(app, port=port)
