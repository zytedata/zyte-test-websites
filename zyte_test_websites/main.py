import sys
from importlib import import_module

from aiohttp import web

if __name__ == "__main__":
    usage_msg = f"Usage: {sys.argv[0]} <articles|ecommerce|jobs> [<port>]"

    if len(sys.argv) < 2:
        print(usage_msg)
        sys.exit(1)

    name = sys.argv[1]
    if name not in {"articles", "ecommerce", "jobs"}:
        print(usage_msg)
        sys.exit(1)

    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80

    app_module = import_module(f"zyte_test_websites.{name}.app")

    app = app_module.make_app()
    web.run_app(app, port=port)
