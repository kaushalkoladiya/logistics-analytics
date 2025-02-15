from app.db.session import get_context_db
from app.core.tasks.database_views.dashboard.daily_metrics import DailyMetricsView
from app.core.tasks.database_views.route.daily_cost_metrics import DailyCostMetricsView
from app.core.tasks.database_views.route.route_metrics import RouteMetricsView
from app.core.tasks.database_views.route.route_reliability import RouteReliabilityView
from app.core.tasks.database_views.route.route_value_metrics import (
    RouteValueMetricsView,
)
from app.core.tasks.database_views.route.route_metrics_comprehensive import (
    RouteMetricsComprehensiveView,
)
from app.core.tasks.database_views.route.route_performance_metrics import (
    RoutePerformanceMetricsView,
)
from app.core.tasks.database_views.shipment.daily_shipment_totals import (
    DailyShipmentTotalsView,
)
from app.core.tasks.database_views.vehicle.vehicle_daily_metrics import (
    VehicleDailyMetricsView,
)


class ViewExecutor:
    def execute(self):
        with get_context_db() as db:
            # Dashboard views
            DailyMetricsView(db).setup()

            # Routes views
            RouteMetricsView(db).setup()
            DailyCostMetricsView(db).setup()
            RouteReliabilityView(db).setup()
            RouteValueMetricsView(db).setup()
            RouteMetricsComprehensiveView(db).setup()
            RoutePerformanceMetricsView(db).setup()

            # shipments views
            DailyShipmentTotalsView(db).setup()

            # vehicle views
            VehicleDailyMetricsView(db).setup()
