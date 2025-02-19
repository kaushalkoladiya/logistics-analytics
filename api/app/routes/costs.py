from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.cost_service import CostAnalysisService
from app.schemas.costs import CostOverviewResponse
from app.utils.logger import get_logger
from app.db.session import get_db
from app.validators.route import CostOverviewValidator
from app.utils.validators import ValidatedParams

router = APIRouter(prefix="/api/costs", tags=["costs"])
logger = get_logger(__name__)


@router.get("/overview", response_model=CostOverviewResponse)
async def get_cost_overview(
    req: CostOverviewValidator = ValidatedParams(CostOverviewValidator),
    db: Session = Depends(get_db),
):
    try:
        result = CostAnalysisService(db).get_cost_analysis(req.start, req.end)

        if not result:
            raise HTTPException(
                status_code=404, detail="No data found for the given period"
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching cost overview: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching cost overview: {str(e)}"
        )
