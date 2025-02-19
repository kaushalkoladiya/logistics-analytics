from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.utils.logger import get_logger
from app.db.session import get_db
from app.schemas.vehicles import (
    VehicleMetrics,
    VehicleDetailsResponse,
)
from app.services.vehicle_service import VehicleService
from app.validators.vehicles import VehicleMetricsValidator, VehicleDetailsValidator
from app.utils.validators import ValidatedParams

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])
logger = get_logger(__name__)


@router.get("/metrics", response_model=List[VehicleMetrics])
async def get_vehicle_metrics(
    req: VehicleMetricsValidator = ValidatedParams(VehicleMetricsValidator),
    db=Depends(get_db),
):
    try:
        return VehicleService(db).get_vehicle_metrics(req.start, req.end)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching vehicle metrics: {str(e)}"
        )


@router.get("/{vehicle_id}/details", response_model=VehicleDetailsResponse)
async def get_vehicle_details(
    vehicle_id: str,
    req: VehicleDetailsValidator = ValidatedParams(VehicleDetailsValidator),
    db=Depends(get_db),
):
    try:
        result = VehicleService(db).get_vehicle_details(vehicle_id, req.start, req.end)

        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Vehicle not found")

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching vehicle details: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching vehicle details: {str(e)}"
        )
