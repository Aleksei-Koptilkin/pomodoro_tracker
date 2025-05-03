from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import Settings


settings = Settings()
db_url = settings.db_url


engine = create_async_engine(url=db_url, future=True, echo=True, pool_pre_ping=True)


AsyncSessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()
