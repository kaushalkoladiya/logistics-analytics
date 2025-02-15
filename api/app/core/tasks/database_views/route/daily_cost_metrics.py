from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class DailyCostMetricsView(MaterializedViewManager):
    VIEW_NAME = "mv_daily_cost_metrics"
    INDEX_NAME = "idx_mv_daily_cost_metrics_date"
    COLUMN_NAME = "metric_date"

    VIEW_QUERY = """
        SELECT 
            metric_date,
            SUM(total_cost) as daily_total_cost,
            SUM(shipment_count) as daily_shipments,
            SUM(total_weight) as daily_weight,
            SUM(total_mileage) as daily_mileage,
            COUNT(DISTINCT CONCAT(origin, ':', destination)) as route_count,
            COUNT(DISTINCT vehicle_id) as vehicle_count,
            AVG(avg_cost) as daily_avg_cost
        FROM mv_route_metrics
        GROUP BY metric_date;
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_unique_index(self.INDEX_NAME, self.VIEW_NAME, self.COLUMN_NAME)
