from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.utils.logger import get_logger
from app.db.session import get_db
from app.schemas.routes import (
    TopRoutePerformance,
    RouteReliabilityResponse,
    RouteCostValueResponse,
    RouteOptimizationResponse,
)
from app.services.route_service import RouteService


router = APIRouter(prefix="/api/route", tags=["route"])
logger = get_logger(__name__)


@router.get("/reliability", response_model=RouteReliabilityResponse)
async def get_route_reliability(
    start: str,
    end: str,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "reliability_score",
    sort_order: str = "desc",
    search: str = None,
    db: Session = Depends(get_db),
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return RouteService(db).get_route_reliability(
            start_date, end_date, page, page_size, sort_by, sort_order, search
        )

    except Exception as e:
        logger.error(f"Error fetching route reliability: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching route reliability: {str(e)}"
        )


@router.get("/cost-value", response_model=RouteCostValueResponse)
async def get_route_cost_value(
    start: str,
    end: str,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "value_score",
    sort_order: str = "desc",
    search: str = None,
    db: Session = Depends(get_db),
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return RouteService(db).get_route_cost_value(
            start_date, end_date, page, page_size, sort_by, sort_order, search
        )

    except Exception as e:
        logger.error(f"Error fetching route cost value: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching route cost value: {str(e)}"
        )


@router.get("/optimization", response_model=RouteOptimizationResponse)
async def get_route_optimization(
    start: str,
    end: str,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "cost_time_efficiency",
    sort_order: str = "desc",
    search: str = None,
    db: Session = Depends(get_db),
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return RouteService(db).get_route_optimization(
            start_date, end_date, page, page_size, sort_by, sort_order, search
        )

    except Exception as e:
        logger.error(f"Error fetching route optimization: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching route optimization: {str(e)}"
        )


@router.get("/top-performing", response_model=List[TopRoutePerformance])
async def get_top_performing_routes(
    start: str,
    end: str,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return RouteService(db).get_top_performing_routes(start_date, end_date, limit)

    except Exception as e:
        logger.error(f"Error fetching top performing routes: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching top performing routes: {str(e)}"
        )
