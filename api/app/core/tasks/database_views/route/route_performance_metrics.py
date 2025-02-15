from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class RoutePerformanceMetricsView(MaterializedViewManager):
    VIEW_NAME = "mv_route_performance_metrics"

    VIEW_QUERY = """
        WITH daily_metrics AS (
            SELECT 
                DATE(vl.trip_date) as metric_date,
                s.origin,
                s.destination,
                s.delivery_time,
                s.cost,
                s.weight,
                -- Pre-calculate daily averages for each route
                AVG(s.delivery_time) OVER (PARTITION BY s.origin, s.destination, DATE(vl.trip_date)) as daily_avg_delivery_time,
                COUNT(*) OVER (PARTITION BY s.origin, s.destination, DATE(vl.trip_date)) as daily_shipment_count,
                -- Global min/max for the day
                MIN(s.cost/NULLIF(s.weight, 0)) OVER (PARTITION BY DATE(vl.trip_date)) as daily_min_cost_per_kg,
                MAX(s.cost/NULLIF(s.weight, 0)) OVER (PARTITION BY DATE(vl.trip_date)) as daily_max_cost_per_kg,
                MIN(s.delivery_time) OVER (PARTITION BY DATE(vl.trip_date)) as daily_min_delivery_time,
                MAX(s.delivery_time) OVER (PARTITION BY DATE(vl.trip_date)) as daily_max_delivery_time
            FROM shipments s
            JOIN vehicle_logs vl ON s.log_id = vl.log_id AND s.trip_date = vl.trip_date
        )
        SELECT 
            metric_date,
            origin,
            destination,
            COUNT(*) as total_shipments,
            CAST(AVG(delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
            CAST(STDDEV(delivery_time) AS DECIMAL(10,2)) as delivery_time_variation,
            CAST(AVG(cost) AS DECIMAL(10,2)) as avg_cost,
            CAST(SUM(cost) AS DECIMAL(10,2)) as total_cost,
            CAST(AVG(cost / NULLIF(weight, 0)) AS DECIMAL(10,2)) as cost_per_kg,
            CAST(SUM(weight) AS DECIMAL(10,2)) as total_weight,
            -- On-time delivery calculation
            CAST(COUNT(*) FILTER (WHERE delivery_time <= daily_avg_delivery_time) * 100.0 / 
                NULLIF(COUNT(*), 0) AS DECIMAL(10,2)) as on_time_delivery_rate,
            -- Store daily min/max for normalization
            MIN(daily_min_cost_per_kg) as min_cost_per_kg,
            MAX(daily_max_cost_per_kg) as max_cost_per_kg,
            MIN(daily_min_delivery_time) as min_delivery_time,
            MAX(daily_max_delivery_time) as max_delivery_time
        FROM daily_metrics
        GROUP BY metric_date, origin, destination;
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index(
            "idx_mv_route_perf_date", self.VIEW_NAME, "metric_date"
        )
        self.create_index(
            "idx_mv_route_perf_route", self.VIEW_NAME, "origin, destination"
        )
