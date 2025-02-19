from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import ProgrammingError

from app.utils.logger import get_logger
from app.db.session import get_db
from app.schemas.shipments import (
    ShipmentAnalytics,
    PaginatedRouteResponse,
)
from app.services.shipment_service import ShipmentService
from app.validators.shipments import ShipmentAnalyticsValidator, ShipmentRouteValidator
from app.utils.validators import ValidatedParams

router = APIRouter(prefix="/api/shipments", tags=["shipments"])
logger = get_logger(__name__)


@router.get("/analytics", response_model=ShipmentAnalytics)
async def get_shipment_analytics(
    req: ShipmentAnalyticsValidator = ValidatedParams(ShipmentAnalyticsValidator),
    db=Depends(get_db),
):
    try:
        return ShipmentService(db).get_shipment_analytics(req.start, req.end)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching shipment analytics: {str(e)}"
        )


@router.get("/routes", response_model=PaginatedRouteResponse)
async def get_route_performance(
    req: ShipmentRouteValidator = ValidatedParams(ShipmentRouteValidator),
    db=Depends(get_db),
):
    try:
        return ShipmentService(db).get_route_performance(
            req.page, req.page_size, req.sort_by, req.sort_order, req.search
        )

    except ProgrammingError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort column. Please provide a valid column name.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching route performance: {str(e)}"
        )
