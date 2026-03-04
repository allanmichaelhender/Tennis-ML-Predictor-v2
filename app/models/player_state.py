from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import date
from app.models.base import Base


class PlayerState(Base):
    __tablename__ = "player_states"

    player_id: Mapped[str] = mapped_column(ForeignKey("players.id"), primary_key=True)

    # Elo Snapshots
    current_elo: Mapped[float] = mapped_column(Float, default=1500.0)
    current_hard_elo: Mapped[float] = mapped_column(Float, default=1500.0)
    current_clay_elo: Mapped[float] = mapped_column(Float, default=1500.0)
    current_grass_elo: Mapped[float] = mapped_column(Float, default=1500.0)

    # Timing Features (The "Rust" Trackers)
    last_match_date: Mapped[date | None] = mapped_column(Date)
    last_hard_match_date: Mapped[date | None] = mapped_column(Date)
    last_clay_match_date: Mapped[date | None] = mapped_column(Date)
    last_grass_match_date: Mapped[date | None] = mapped_column(Date)

    # ... (Elo and Timing fields) ...

    # 1. Match Win % (e.g., 0.8 means 8 wins in last 10)
    rolling_match_win_pct: Mapped[float] = mapped_column(Float, default=0.0)
    
    # 2. Game Win % (e.g., 0.54 means they won 54% of all games in last 10)
    rolling_game_win_pct: Mapped[float] = mapped_column(Float, default=0.50)
    
    # 3. The raw "buffer" to calculate the above (Stored as JSONB)
    # Stored as list of dicts: [{"w": 1, "gp": 0.55}, {"w": 0, "gp": 0.48}, ...]
    performance_buffer: Mapped[list] = mapped_column(JSONB, default=list)
