import sys

from aiohttp import web

if __name__ == "__main__":
    # TODO: when we have >1 website we should make "jobs" not hardcoded

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} jobs <port>")
        sys.exit(1)

    port = int(sys.argv[2])

    from .jobs.app import make_app

    app = make_app()
    web.run_app(app, port=port)
