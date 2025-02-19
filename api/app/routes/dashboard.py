from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.utils.logger import get_logger
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService
from app.validators.dashboard import DashboardValidator
from app.utils.validators import ValidatedParams


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
logger = get_logger(__name__)


@router.get("", response_model=DashboardResponse)
async def get_dashboard_overview(
    req: DashboardValidator = ValidatedParams(DashboardValidator),
    db: Session = Depends(get_db),
):
    try:
        return DashboardService(db).get_dashboard_overview(
            req.start, req.end, req.interval_type, req.periods_back
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching dashboard overview: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching dashboard overview: {str(e)}"
        )
