from fastapi import APIRouter
from app.services.calculation_status import CalculationStatusService

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/status")
async def get_system_status():
    return CalculationStatusService().get_system_status()
