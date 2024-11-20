from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(
    url="postgresql+asyncpg://aiohttp_test:aiohttp_test@localhost:5432/aiohttp_test", echo=True
)

session_maker = async_sessionmaker(bind=engine)
