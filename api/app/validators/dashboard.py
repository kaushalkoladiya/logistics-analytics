from typing import Literal

from app.validators.date_range_base import DateRangeBase


class DashboardValidator(DateRangeBase):
    interval_type: Literal["week", "month", "year"]
    periods_back: int = 1
