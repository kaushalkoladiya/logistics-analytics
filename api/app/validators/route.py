from app.validators.date_range_base import DateRangeBase


class CostOverviewValidator(DateRangeBase):
    pass


class RouteReliabilityValidator(DateRangeBase):
    page: int = 1
    page_size: int = 10
    sort_by: str = "reliability_score"
    sort_order: str = "desc"
    search: str = None


class RouteCostValueValidator(DateRangeBase):
    page: int = 1
    page_size: int = 10
    sort_by: str = "value_score"
    sort_order: str = "desc"
    search: str = None


class RouteOptimizationValidator(DateRangeBase):
    page: int = 1
    page_size: int = 10
    sort_by: str = "cost_time_efficiency"
    sort_order: str = "desc"
    search: str = None


class RouteTopPerformingValidator(DateRangeBase):
    limit: int = 10
