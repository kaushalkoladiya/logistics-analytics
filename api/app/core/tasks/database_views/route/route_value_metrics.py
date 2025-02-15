from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class RouteValueMetricsView(MaterializedViewManager):
    VIEW_NAME = "mv_route_value_metrics"
    INDEX_NAME = "idx_mv_route_value_date"
    COLUMN_NAME = "metric_date"

    VIEW_QUERY = """
        SELECT 
            DATE(vl.trip_date) as metric_date,
            s.origin,
            s.destination,
            COUNT(*) as shipment_count,
            CAST(AVG(s.weight) AS DECIMAL(10,2)) as avg_shipment_weight,
            CAST(AVG(s.cost) AS DECIMAL(10,2)) as avg_cost,
            CAST(AVG(s.cost/NULLIF(s.weight, 0)) AS DECIMAL(10,2)) as cost_per_kg,
            CAST(AVG(s.cost/(NULLIF(s.delivery_time, 0))) AS DECIMAL(10,2)) as value_score
        FROM shipments s
        JOIN vehicle_logs vl ON s.log_id = vl.log_id AND s.trip_date = vl.trip_date
        GROUP BY DATE(vl.trip_date), s.origin, s.destination;
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index(self.INDEX_NAME, self.VIEW_NAME, self.COLUMN_NAME)
        self.create_index(
            "idx_mv_route_value_route", self.VIEW_NAME, "origin, destination"
        )
