from aiohttp import web
from jinja2 import FileSystemLoader
import aiohttp_jinja2

from app.urls import routes
from app.middlewares import redis_session_middleware


app = web.Application(
    middlewares=[redis_session_middleware],
)


aiohttp_jinja2.setup(
    app,
    loader=FileSystemLoader('templates'),
    context_processors=[
        aiohttp_jinja2.request_processor,
    ]
)

app.router.add_routes(routes)

web.run_app(app, host='0.0.0.0', port=8080)
