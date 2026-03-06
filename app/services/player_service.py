import os
import json
import httpx  # For fast, async API calls to The-Odds-API
import google.generativeai as genai
from datetime import datetime, timedelta
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

# Models
from app.models.player import Player

async def get_elite_players(session: AsyncSession):
    # Get Top 100 by Elo, active in last 12 months
    twelve_months_ago = datetime.now() - timedelta(days=365)
    
    stmt = (
        select(Player.id, Player.name, Player.elo)
        .where(Player.last_played_date >= twelve_months_ago)
        .order_by(Player.elo.desc())
        .limit(100)
    )
    result = await session.execute(stmt)
    return result.all()
