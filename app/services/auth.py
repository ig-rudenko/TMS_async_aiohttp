from aiohttp_session import get_session

from .users import get_user_by_credentials
from app.db_session import session_maker


class AuthError(Exception):
    pass


class UserNotFoundError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


async def login(request, username, password) -> None:
    async with session_maker() as session:
        user = await get_user_by_credentials(session, username, password)
        print("Пользователь", user)
        if user is not None:
            print("Нашли пользователя", user)
            session = await get_session(request)
            session["user_id"] = user.id
            print("Залогинились", session["user_id"])
        else:
            raise InvalidCredentialsError("Неправильный логин или пароль")
