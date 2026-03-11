import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import async_session

# Telling fastapi to look in the headers for my api key, auto_error = false prevents an instant error on lacking it and my function handles the lack of a key
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


# Security trigger the search for the api key, then we check it matches
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == os.getenv("INTERNAL_API_KEY"):
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API Key"
    )


async def get_db() -> (
    AsyncGenerator[AsyncSession, None]
):  # Telling python this yields an async generator, None means we are not sending any data back into the generator
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
