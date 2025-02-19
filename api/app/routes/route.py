from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
from app.validators.route import (
    RouteReliabilityValidator,
    RouteOptimizationValidator,
    RouteCostValueValidator,
    RouteTopPerformingValidator,
)
from app.utils.validators import ValidatedParams


router = APIRouter(prefix="/api/route", tags=["route"])
logger = get_logger(__name__)


@router.get("/reliability", response_model=RouteReliabilityResponse)
async def get_route_reliability(
    req: RouteReliabilityValidator = ValidatedParams(RouteReliabilityValidator),
    db: Session = Depends(get_db),
):
    try:
        return RouteService(db).get_route_reliability(
            req.start,
            req.end,
            req.page,
            req.page_size,
            req.sort_by,
            req.sort_order,
            req.search,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching route reliability: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching route reliability: {str(e)}"
        )


@router.get("/cost-value", response_model=RouteCostValueResponse)
async def get_route_cost_value(
    req: RouteCostValueValidator = ValidatedParams(RouteCostValueValidator),
    db: Session = Depends(get_db),
):
    try:
        return RouteService(db).get_route_cost_value(
            req.start,
            req.end,
            req.page,
            req.page_size,
            req.sort_by,
            req.sort_order,
            req.search,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching route cost value: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching route cost value: {str(e)}"
        )


@router.get("/optimization", response_model=RouteOptimizationResponse)
async def get_route_optimization(
    req: RouteOptimizationValidator = ValidatedParams(RouteOptimizationValidator),
    db: Session = Depends(get_db),
):
    try:
        return RouteService(db).get_route_optimization(
            req.start,
            req.end,
            req.page,
            req.page_size,
            req.sort_by,
            req.sort_order,
            req.search,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching route optimization: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching route optimization: {str(e)}"
        )


@router.get("/top-performing", response_model=List[TopRoutePerformance])
async def get_top_performing_routes(
    req: RouteTopPerformingValidator = ValidatedParams(RouteTopPerformingValidator),
    db: Session = Depends(get_db),
):
    try:
        return RouteService(db).get_top_performing_routes(req.start, req.end, req.limit)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching top performing routes: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching top performing routes: {str(e)}"
        )
