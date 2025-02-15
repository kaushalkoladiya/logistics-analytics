from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List

from app.utils.logger import get_logger
from app.db.session import get_db
from app.schemas.vehicles import (
    VehicleMetrics,
    VehicleDetailsResponse,
)
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])
logger = get_logger(__name__)


@router.get("/metrics", response_model=List[VehicleMetrics])
async def get_vehicle_metrics(start: str, end: str, db=Depends(get_db)):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return VehicleService(db).get_vehicle_metrics(start_date, end_date)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching vehicle metrics: {str(e)}"
        )


@router.get("/{vehicle_id}/details", response_model=VehicleDetailsResponse)
async def get_vehicle_details(
    vehicle_id: str, start: str, end: str, db=Depends(get_db)
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return VehicleService(db).get_vehicle_details(vehicle_id, start_date, end_date)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching vehicle details: {str(e)}"
        )
