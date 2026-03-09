from pydantic import BaseModel
from typing import List

class PerformanceSummary(BaseModel):
    roi: float            # e.g., 0.042 (4.2%)
    total_profit: float   # Net units (+/-)
    win_rate: float       # % of bets won
    brier_score: float    # Probability accuracy (lower is better)
    total_bets: int       # Sample size

class WeeklyPoint(BaseModel):
    date: str             # e.g., "2025-01-12"
    balance: float        # The closing balance of that week

class MonthlyStat(BaseModel):
    month: str            # e.g., "Jan 2025"
    roi: float            # ROI specifically for that month
    profit: float         # Profit specifically for that month

class ModelPerformanceResponse(BaseModel):
    summary: PerformanceSummary
    equity_curve: List[WeeklyPoint]
    monthly_breakdown: List[MonthlyStat]

class EdgeBucket(BaseModel):
    bucket: str
    roi: float
    brier_score: float
    match_count: int
    avg_edge: float

class CalibrationPoint(BaseModel):
    prob_bucket: str
    avg_predicted: float
    actual_win_rate: float
    match_count: int

