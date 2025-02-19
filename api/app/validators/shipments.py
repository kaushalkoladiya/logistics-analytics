from pydantic import BaseModel

from app.validators.date_range_base import DateRangeBase


class ShipmentAnalyticsValidator(DateRangeBase):
    pass


class ShipmentRouteValidator(BaseModel):
    page: int = 1
    page_size: int = 10
    sort_by: str = "total_trips"
    sort_order: str = "desc"
    search: str = None
