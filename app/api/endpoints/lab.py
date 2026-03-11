from fastapi import APIRouter,  Security
from app.api.deps import get_api_key
from app.services.quant.lab_service import lab_service
from app.schemas.lab import ModelPerformanceResponse, EdgeBucket, CalibrationPoint
from typing import List

# We use security here, it does the same as depends but is specifically for this application
router = APIRouter(
    dependencies=[Security(get_api_key)]
)

# Returns model performance
@router.get("/model-performance", response_model=ModelPerformanceResponse)
async def get_lab_stats():
    return await lab_service.get_model_performance()

# Returns bucketed edge analysis on our model 
@router.get("/edge-analysis", response_model=List[EdgeBucket])
async def get_edge_stats():
    return await lab_service.get_edge_analysis()

# Returns calibration data for plotting in the frontend
@router.get("/calibration", response_model=List[CalibrationPoint])
async def get_calibration_stats():
    return await lab_service.get_calibration()