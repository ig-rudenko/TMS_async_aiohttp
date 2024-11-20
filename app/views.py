from aiohttp import web
from aiohttp_jinja2 import template

from .filters import get_note_filter
from .services.auth import UserNotFoundError, login, AuthError
from .services.notes import create_note, get_filtered_notes


class HomeView(web.View):
    async def get(self):
        return web.HTTPMovedPermanently("/notes")


class ListCreateNoteView(web.View):

    @template("list_create_note.html")
    async def get(self):
        note_filters = get_note_filter(self.request)
        notes = await get_filtered_notes(self.request.user_id, note_filters)
        return {"notes": notes}

    @template("list_create_note.html")
    async def post(self):
        # Получаем данные от пользователя.
        data = await self.request.post()

        title = data.get("title")
        content = data.get("content")
        tags = data.getall("tags")

        try:
            await create_note(title, content, self.request.user_id, tags=tags)
        except UserNotFoundError:
            return web.HTTPFound("/login")

        return web.HTTPMovedPermanently("/notes")


class LoginView(web.View):
    @template("login.html")
    async def get(self):
        return {}

    @template("login.html")
    async def post(self):
        user_data = await self.request.post()

        # TODO: добавить проверку входных данных.

        try:
            await login(self.request, user_data["usernameInput"], user_data["passwordInput"])
        except AuthError as exc:
            return {"error": str(exc)}


# TODO: Добавить регистрацию пользователей.
# TODO: Добавить страницу отображения одной записи.
