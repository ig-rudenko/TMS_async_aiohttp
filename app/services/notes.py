from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import array_agg

from app.db_session import session_maker
from app.filters import filter_notes
from app.models import User, Note, Tag, NoteTag
from .users import get_user_by_id
from .auth import UserNotFoundError


async def get_filtered_notes(user_id: int, filters: dict):
    notes = []
    async with session_maker() as db_session:
        user = await get_user_by_id(db_session, user_id)
        print("USER:", user)
        if user is not None:
            notes = await get_user_notes(db_session, user.id, filters)
            print(notes)

    return notes


async def get_user_notes(session: AsyncSession, user_id: int, filters: dict | None = None) -> list[dict]:

    # DJANGO
    # qs = Note.objects.filter(author_id=user_id, tags__name__in=tags)
    # .order_by('-created_at')
    # .select_related('author')
    # .prefetch_related('tags')
    # .only("id", "title", "author__username", "tags")

    query = (
        select(Note.id, Note.title, User.username, array_agg(Tag.name).label("tags"), Note.created_at)
        .where(Note.author_id == user_id)
        .join(User, Note.author_id == User.id)
        .join(NoteTag, Note.id == NoteTag.note_id)
        .join(Tag, NoteTag.tag_id == Tag.id)
        .group_by(Note.id, User.username)
        .order_by(Note.created_at.desc())
    )

    if filters is not None:
        query = filter_notes(query, filters)

    result = await session.execute(query)

    return [
        {
            "id": row[0],
            "title": row[1],
            "username": row[2],
            "tags": row[3],
            "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S"),
        }
        for row in result
    ]


async def create_note(title: str, content: str, user_id: int, tags: list[tuple[str, str]]):
    # Создаем новую запись.
    async with session_maker() as db_session:
        user = await get_user_by_id(db_session, user_id)
        if user is None:
            raise UserNotFoundError("Пользователь не найден")

        # Создаем теги
        # TODO: Убрать явно прописанные теги.
        tags = [
            ("python", "Язык программирования"),
            ("django", "Фреймворк для создания веб-приложений"),
            ("flask", "Фреймворк для создания веб-приложений"),
        ]

        await create_note(db_session, title, content, user_id, tags)


async def create_note(
    session: AsyncSession, title: str, content: str, user_id: int, tags: list[tuple[str, str]]
) -> Note:

    tags = await get_or_create_tags(session, tags)
    note = Note(title=title, content=content, author_id=user_id, tags=tags)

    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note


async def get_or_create_tags(
    session: AsyncSession, tags: list[tuple[str, str]], commit: bool = False
) -> list[Tag]:
    result = []

    for tag_name, tag_description in tags:
        stored_tag_result = await session.execute(select(Tag).where(Tag.name.ilike(tag_name)))
        stored_tag: Tag | None = stored_tag_result.scalar_one_or_none()
        print("def get_or_create_tags | stored_tag:", stored_tag)

        if stored_tag is not None:
            result.append(stored_tag)
        else:
            tag = Tag(name=tag_name, description=tag_description)
            session.add(tag)
            result.append(tag)

    if commit:
        await session.commit()
        for tag in result:
            await session.refresh(tag)

    return result
