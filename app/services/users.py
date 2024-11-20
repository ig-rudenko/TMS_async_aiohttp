from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def create_user(session: AsyncSession, email: str, username: str, password: str) -> User:
    # TODO: Добавить шифрование пароля.
    user = User(email=email, username=username, password=password)
    session.add(user)
    # print("User id:", user.id)
    await session.commit()
    await session.refresh(user)
    # print("User id:", user.id)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int | None) -> User | None:
    if user_id is None:
        return None
    query = select(User).where(User.id == user_id)
    return await session.scalar(query)


async def is_username_exists(session: AsyncSession, username: str) -> bool:
    query = select(User.id).where(User.username == username)

    print(query)
    user_id = await session.scalar(query)

    return bool(user_id)


async def get_user_by_credentials(session: AsyncSession, username: str, password: str) -> User | None:
    # TODO: Добавить шифрование пароля и проверку с базой.
    query = select(User).where(User.username == username, User.password == password)
    return await session.scalar(query)
