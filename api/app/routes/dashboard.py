from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Literal

from app.db.session import get_db
from app.utils.logger import get_logger
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
logger = get_logger(__name__)


@router.get("", response_model=DashboardResponse)
async def get_dashboard_overview(
    start: str,
    end: str,
    interval_type: Literal["week", "month", "year"],
    periods_back: int = 1,
    db: Session = Depends(get_db),
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        return DashboardService(db).get_dashboard_overview(
            start_date, end_date, interval_type, periods_back
        )

    except Exception as e:
        logger.error(f"Error fetching dashboard overview: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching dashboard overview: {str(e)}"
        )
