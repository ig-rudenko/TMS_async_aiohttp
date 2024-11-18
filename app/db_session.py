from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(url="sqlite+aiosqlite:///test.db")

session_maker = async_sessionmaker(bind=engine)
