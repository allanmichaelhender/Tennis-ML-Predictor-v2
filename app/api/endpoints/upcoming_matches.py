from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_api_key
from app.services.llm_service import LLMService
from app.core.ratelimit import limiter
from app.schemas.upcoming import SyncResponse

router = APIRouter()
llm_service = LLMService()


@router.post("/sync", dependencies=[Security(get_api_key)])
# @limiter.limit("1/minute")
async def sync_live_matches(db: AsyncSession = Depends(get_db)):
     result = await llm_service.sync_upcoming_matches(db)

     return result