from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class DailyShipmentTotalsView(MaterializedViewManager):
    VIEW_NAME = "mv_daily_shipment_totals"

    VIEW_QUERY = """
        SELECT 
            DATE(vl.trip_date) as metric_date,
            COUNT(DISTINCT s.shipment_id) as total_shipments,
            CAST(AVG(s.delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
            CAST(SUM(s.cost) AS DECIMAL(10,2)) as total_cost,
            CAST(AVG(s.cost) AS DECIMAL(10,2)) as avg_cost_per_shipment,
            CAST(SUM(s.weight) AS DECIMAL(10,2)) as total_weight,
            COUNT(DISTINCT s.origin) as unique_origins,
            COUNT(DISTINCT s.destination) as unique_destinations
        FROM shipments s
        JOIN vehicle_logs vl ON s.log_id = vl.log_id AND s.trip_date = vl.trip_date
        GROUP BY DATE(vl.trip_date);
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index("idx_mv_daily_shipment_totals_date", self.VIEW_NAME, "metric_date")
