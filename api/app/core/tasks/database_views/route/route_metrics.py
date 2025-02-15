from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class RouteMetricsView(MaterializedViewManager):
    VIEW_NAME = "mv_route_metrics"
    INDEX_NAME = "idx_mv_route_metrics_date"
    COLUMN_NAME = "metric_date"

    VIEW_QUERY = """
        SELECT 
            DATE(vl.trip_date) as metric_date,
            s.origin,
            s.destination,
            vl.vehicle_id,
            COUNT(*) as shipment_count,
            SUM(s.cost) as total_cost,
            AVG(s.cost) as avg_cost,
            SUM(s.weight) as total_weight,
            SUM(vl.mileage) as total_mileage
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
        self.create_index(self.INDEX_NAME, self.VIEW_NAME, self.COLUMN_NAME)
        self.create_index(
            "idx_mv_route_metrics_cost", self.VIEW_NAME, "total_cost DESC"
        )
