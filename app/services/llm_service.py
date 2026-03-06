import os
import json
import httpx  # For the-odds-api requests
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Database imports
from sqlalchemy import select, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession

# Models (Make sure these match your actual file names)
from app.models.player_state import PlayerState


class LLMService:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.odds_key = os.getenv("THE_ODDS_API_KEY")
        genai.configure(api_key=self.gemini_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def get_elite_100(self, session: AsyncSession):
        """Fetch top 100 active players from Postgres"""
        one_year_ago = datetime.now() - timedelta(days=365)
        stmt = (
            select(PlayerState.player_id, PlayerState.current_elo)
            .where(PlayerState.last_match_date >= one_year_ago) # Ensure your column name matches
            .order_by(desc(PlayerState.current_elo))
            .limit(100)
        )
        result = await session.execute(stmt)
        rows = result.all()
        # return [{"name": p.name, "id": p.id, "elo": p.elo} for p in result.scalars().all()]
        return [{"id": p.player_id, "elo": p.current_elo} for p in rows]

    async def get_raw_markets(self):
        """Fetch current ATP markets from The-Odds-API"""
        url = f"https://api.the-odds-api.com{self.odds_key}&regions=eu&markets=h2h"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
        

    async def sync_upcoming_matches(self, session: AsyncSession):
        elite_100 = await self.get_elite_100(session)
        raw_markets = await self.get_raw_markets()


        print(elite_100)
        print(raw_markets)

        prompt = f"""
<context>
You are a professional tennis quant analyst. I have two datasets: 
1. ELITE_LIST: The top 100 players from my database based on Elo ratings.
2. LIVE_MARKETS: Current ATP betting markets from The-Odds-API.
</context>

<task>
Cross-reference the LIVE_MARKETS against the ELITE_LIST. 
Select the top 20 most significant matches based on these priority rules:
1. Priority 1: Matches where BOTH players are in the ELITE_LIST (High-tier matchups).
2. Priority 2: Matches where at least ONE player is in the ELITE_LIST (Rising stars vs Elites).
3. Priority 3: Matches with the most competitive/sharp odds (Pinnacle/Bet365 spreads).

Discard any WTA (Women's) matches if they accidentally appear in the data.
</task>

<input_data>
ELITE_LIST: {None}

LIVE_MARKETS: {None}
</input_data>

<output_requirement>
Return ONLY a valid JSON object. 
Map the players from the LIVE_MARKETS to their corresponding 'id' from the ELITE_LIST where possible.
If a player in a market is NOT in the Elite List, provide their name but set the id to null.

Format:
{{
  "featured_matches": [
    {{
      "p1_name": "string",
      "p1_id": "string_or_null",
      "p2_name": "string",
      "p2_id": "string_or_null",
      "b365_p1": float,
      "b365_p2": float,
      "pin_p1": float,
      "pin_p2": float,
      "tournament": "string",
      "commence_time": "ISO_TIMESTAMP"
    }}
  ]
}}
</output_requirement>
"""
        return None