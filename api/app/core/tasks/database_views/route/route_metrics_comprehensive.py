from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class RouteMetricsComprehensiveView(MaterializedViewManager):
    VIEW_NAME = "mv_route_metrics_comprehensive"

    VIEW_QUERY = """
        SELECT 
            DATE(vl.trip_date) as metric_date,
            s.origin,
            s.destination,
            vl.vehicle_id,
            COUNT(*) as shipment_count,
            -- Basic metrics
            CAST(AVG(s.delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
            CAST(MIN(s.delivery_time) AS DECIMAL(10,2)) as min_delivery_time,  -- Route performance
            CAST(MAX(s.delivery_time) AS DECIMAL(10,2)) as max_delivery_time,  -- Route performance
            
            CAST(AVG(s.cost) AS DECIMAL(10,2)) as avg_cost,
            CAST(AVG(s.weight) AS DECIMAL(10,2)) as avg_weight,
            CAST(SUM(s.cost) AS DECIMAL(10,2)) as total_cost,
            CAST(SUM(s.weight) AS DECIMAL(10,2)) as total_weight,
            CAST(SUM(s.cost) / COUNT(*) AS DECIMAL(10,2)) as cost_per_trip,
            
            -- Reliability metrics
            CAST(STDDEV(s.delivery_time) AS DECIMAL(10,2)) as delivery_time_stddev,
            -- Value metrics
            CAST(AVG(s.cost/NULLIF(s.weight, 0)) AS DECIMAL(10,2)) as cost_per_kg,
            CAST(AVG(s.cost/NULLIF(s.delivery_time, 0)) AS DECIMAL(10,2)) as value_score
        FROM shipments s
        JOIN vehicle_logs vl ON s.log_id = vl.log_id AND s.trip_date = vl.trip_date
        GROUP BY DATE(vl.trip_date), s.origin, s.destination, vl.vehicle_id;
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index(
            "idx_mv_route_metrics_comp_date", self.VIEW_NAME, "metric_date"
        )
        self.create_index(
            "idx_mv_route_metrics_comp_route", self.VIEW_NAME, "origin, destination"
        )
        self.create_index(
            "idx_mv_route_metrics_comp_cost", self.VIEW_NAME, "total_cost DESC"
        )
        self.create_index(
            "idx_mv_route_metrics_comp_vehicle", self.VIEW_NAME, "vehicle_id"
        )
        self.create_index(
            "idx_mv_route_metrics_comp_origin_search",
            self.VIEW_NAME,
            "origin text_pattern_ops",
        )
        self.create_index(
            "idx_mv_route_metrics_comp_dest_search",
            self.VIEW_NAME,
            "destination text_pattern_ops",
        )
