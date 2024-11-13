from aiohttp import web
from .views import HomeView, ListCreateNoteView


routes = [
    web.get('/', HomeView, name='home'),
    web.route('*', '/notes', ListCreateNoteView, name='notes-list-create'),
]
