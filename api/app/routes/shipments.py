from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from app.utils.logger import get_logger
from app.db.session import get_db
from app.schemas.shipments import (
    ShipmentAnalytics,
    PaginatedRouteResponse,
)
from app.services.shipment_service import ShipmentService

router = APIRouter(prefix="/api/shipments", tags=["shipments"])
logger = get_logger(__name__)


@router.get("/analytics", response_model=ShipmentAnalytics)
async def get_shipment_analytics(start: str, end: str, db=Depends(get_db)):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return ShipmentService(db).get_shipment_analytics(start_date, end_date)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching shipment analytics: {str(e)}"
        )


@router.get("/routes", response_model=PaginatedRouteResponse)
async def get_route_performance(
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "total_trips",
    sort_order: str = "desc",
    search: str = None,
    db=Depends(get_db),
):
    try:
        return ShipmentService(db).get_route_performance(
            page, page_size, sort_by, sort_order, search
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching route performance: {str(e)}"
        )
