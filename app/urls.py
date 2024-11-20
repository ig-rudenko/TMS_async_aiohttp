from aiohttp import web
from .views import HomeView, ListCreateNoteView, LoginView


routes = [
    web.get("/", HomeView, name="home"),
    web.route("*", "/notes", ListCreateNoteView, name="notes-list-create"),
    web.route("*", "/login", LoginView, name="login"),
]
