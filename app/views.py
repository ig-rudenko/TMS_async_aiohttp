from datetime import datetime
from uuid import uuid4

from aiohttp import web
from aiohttp_jinja2 import template

from .cache import cache


class HomeView(web.View):
    @template('home.html')
    async def get(self):
        return {}


class ListCreateNoteView(web.View):

    @template('list_create_note.html')
    async def get(self):
        all_notes = cache.get('notes')
        return {"notes": all_notes or []}

    @template('list_create_note.html')
    async def post(self):
        # Получаем данные от пользователя.
        data = await self.request.post()

        title = data.get('title')
        content = data.get('content')

        note = {
            'id': str(uuid4()),
            'title': title,
            'content': content,
            'created_at': datetime.now()
        }
        cache.set(note['id'], note)

        all_notes = cache.get('notes') or []
        all_notes.append(note)
        cache.set('notes', all_notes)

        return web.HTTPMovedPermanently("/notes")
