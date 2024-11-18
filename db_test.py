import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.models import User, Base


async def create_user(session: AsyncSession, email: str, username: str, password: str) -> User:
    user = User(email=email, username=username, password=password)
    session.add(user)
    print("User id:", user.id)
    await session.commit()
    await session.refresh(user)
    print("User id:", user.id)
    return user


engine = create_async_engine(url="sqlite+aiosqlite:///test.db")

session_maker = async_sessionmaker(bind=engine)


# session: AsyncSession = session_maker()

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()

    async with session_maker() as session:
        user = await create_user(session=session, email="test@test.com", username="test", password="test")
        print("Создан пользователь:", user.id, user.email, user.username, user.password)


if __name__ == '__main__':
    asyncio.run(main())
