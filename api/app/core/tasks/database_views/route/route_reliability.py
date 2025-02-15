from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class RouteReliabilityView(MaterializedViewManager):
    VIEW_NAME = "mv_route_reliability"
    INDEX_NAME = "idx_mv_route_reliability_date"
    COLUMN_NAME = "metric_date"

    VIEW_QUERY = """
        SELECT 
            DATE(vl.trip_date) as metric_date,
            s.origin,
            s.destination,
            s.delivery_time,
            COUNT(*) OVER (PARTITION BY s.origin, s.destination) as route_delivery_count,
            AVG(s.delivery_time) OVER (PARTITION BY s.origin, s.destination) as route_avg_delivery_time,
            AVG(s.delivery_time) OVER () as global_avg_delivery_time,
            STDDEV(s.delivery_time) OVER (PARTITION BY s.origin, s.destination) as route_stddev
        FROM shipments s
        JOIN vehicle_logs vl ON s.log_id = vl.log_id AND s.trip_date = vl.trip_date;
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index(self.INDEX_NAME, self.VIEW_NAME, self.COLUMN_NAME)
        self.create_index(
            "idx_mv_route_reliability_route", self.VIEW_NAME, "origin, destination"
        )
