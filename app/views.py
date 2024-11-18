from aiohttp import web
from aiohttp_jinja2 import template
from aiohttp_session import get_session

from .db_session import session_maker
from .filters import get_note_filter
from .services import get_user_by_credentials, get_user_notes, get_user_by_id, create_note


class HomeView(web.View):
    async def get(self):
        return web.HTTPMovedPermanently("/notes")


class ListCreateNoteView(web.View):

    @template('list_create_note.html')
    async def get(self):

        user_session = await get_session(self.request)
        print("USER SESSION:", user_session)
        user_id = user_session.get('user_id')

        notes = []
        async with session_maker() as db_session:
            user = await get_user_by_id(db_session, user_id)
            print("USER:", user)
            if user is not None:
                note_filters = get_note_filter(self.request)
                notes = await get_user_notes(db_session, user.id, note_filters)

        print("NOTES:", notes)

        return {"notes": notes}

    @template('list_create_note.html')
    async def post(self):
        # Получаем данные от пользователя.
        data = await self.request.post()

        user_session = await get_session(self.request)
        print("USER SESSION:", user_session)
        user_id = user_session.get('user_id')

        title = data.get('title')
        content = data.get('content')

        # Создаем новую запись.
        async with session_maker() as db_session:
            user = await get_user_by_id(db_session, user_id)
            if user is None:
                return web.HTTPFound("/login")

            await create_note(db_session, title, content, user_id)

        return web.HTTPMovedPermanently("/notes")


class LoginView(web.View):
    @template('login.html')
    async def get(self):
        return {}

    @template('login.html')
    async def post(self):
        user_data = await self.request.post()

        # TODO: добавить проверку входных данных.

        print(user_data)

        async with session_maker() as session:

            user = await get_user_by_credentials(session, user_data["usernameInput"], user_data["passwordInput"])
            print("Пользователь", user)
            if user is not None:
                print("Нашли пользователя", user)
                session = await get_session(self.request)
                session['user_id'] = user.id
                print("Залогинились", session['user_id'])
                return web.HTTPFound("/notes")
            else:
                return {"error": "Неверный логин или пароль"}


# TODO: Добавить регистрацию пользователей.
# TODO: Добавить страницу отображения одной записи.
