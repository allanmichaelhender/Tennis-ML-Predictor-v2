import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# we use asyncpg to allow asyncio to work with
DATABASE_URL = os.getenv(
    "DATABASE_URL")

# The engine manages connection sessions, we have a max number of sessions of 20
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20
)

# Async Session Factory
# expire_on_commit=False prevents 'detached instance' errors in Asyncio
async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

 # FastAPI Dependency
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
