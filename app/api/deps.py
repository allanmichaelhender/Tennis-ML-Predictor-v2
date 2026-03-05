import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# The header name React will send
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == os.getenv("INTERNAL_API_KEY"):
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid or missing API Key"
    )
