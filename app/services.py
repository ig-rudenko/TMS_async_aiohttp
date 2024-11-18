from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters import filter_notes
from app.models import User, Note


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


async def get_user_notes(session: AsyncSession, user_id: int, filters: dict | None = None) -> list[dict]:
    query = select(Note.id, Note.title).where(Note.author_id == user_id)

    if filters is not None:
        query = filter_notes(query, filters)

    # {"search": Note.title or Note.content}

    result = await session.execute(query)

    return [{'id': row[0], 'title': row[1]} for row in result]


async def create_note(session: AsyncSession, title: str, content: str, user_id: int) -> Note:
    note = Note(title=title, content=content, author_id=user_id)

    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note
