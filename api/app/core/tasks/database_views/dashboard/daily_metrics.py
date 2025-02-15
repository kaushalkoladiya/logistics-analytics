from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class DailyMetricsView(MaterializedViewManager):
    VIEW_NAME = "mv_daily_metrics"
    INDEX_NAME = "idx_mv_daily_metrics_date"
    COLUMN_NAME = "metric_date"

    VIEW_QUERY = """
        SELECT 
            DATE(vl.trip_date) as metric_date,
            COUNT(DISTINCT s.shipment_id) as total_shipments,
            COUNT(DISTINCT vl.vehicle_id) as active_vehicles,
            SUM(s.cost) as total_revenue,
            AVG(s.delivery_time) as avg_delivery_time
        FROM vehicle_logs vl
        JOIN shipments s ON vl.log_id = s.log_id AND vl.trip_date = s.trip_date
        WHERE vl.mileage IS NOT NULL 
            AND vl.fuel_used IS NOT NULL
        GROUP BY DATE(vl.trip_date);
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index(self.INDEX_NAME, self.VIEW_NAME, self.COLUMN_NAME)
