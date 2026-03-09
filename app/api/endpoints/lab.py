from fastapi import APIRouter, Depends, Security
from app.api.deps import get_api_key
from app.services.quant.lab_service import lab_service
from app.schemas.lab import ModelPerformanceResponse, EdgeBucket, CalibrationPoint
from typing import List

# 🔒 Apply Security to the entire Lab section
router = APIRouter(
    dependencies=[Security(get_api_key)]
)

@router.get("/model-performance", response_model=ModelPerformanceResponse)
async def get_lab_stats():
    """
    Returns aggregated ROI, weekly equity curve, and monthly performance.
    Requires X-API-KEY in header.
    """
    return await lab_service.get_model_performance()

@router.get("/edge-analysis", response_model=List[EdgeBucket])
async def get_edge_stats():
    return await lab_service.get_edge_analysis()


@router.get("/calibration", response_model=List[CalibrationPoint])
async def get_calibration_stats():
    """
    High-fidelity (0.05 bins) calibration analysis.
    Maps Predicted Probability vs. Actual Win Rate to find the 'Ego Cliff'.
    """
    return await lab_service.get_calibration()