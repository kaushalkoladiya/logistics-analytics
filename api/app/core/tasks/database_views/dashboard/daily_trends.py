from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class DailyTrendsView(MaterializedViewManager):
    VIEW_NAME = "mv_daily_trends"
    INDEX_NAME = "idx_mv_daily_trends_date"
    COLUMN_NAME = "metric_date"

    VIEW_QUERY = """
        SELECT 
          m1.metric_date,
          m1.total_shipments,
          m1.active_vehicles,
          m1.total_revenue,
          m1.avg_delivery_time,
          CAST(
              CASE 
                  WHEN m2.total_shipments = 0 THEN 0 
                  ELSE ((m1.total_shipments - m2.total_shipments)::DECIMAL * 100 / m2.total_shipments)
              END AS DECIMAL(10,1)
          ) as shipment_trend,
          CAST(
              CASE 
                  WHEN m2.active_vehicles = 0 THEN 0 
                  ELSE ((m1.active_vehicles - m2.active_vehicles)::DECIMAL * 100 / m2.active_vehicles)
              END AS DECIMAL(10,1)
          ) as vehicle_trend,
          CAST(
              CASE 
                  WHEN m2.total_revenue = 0 THEN 0 
                  ELSE ((m1.total_revenue - m2.total_revenue) * 100 / m2.total_revenue)
              END AS DECIMAL(10,1)
          ) as revenue_trend,
          CAST(
              CASE 
                  WHEN m2.avg_delivery_time = 0 THEN 0 
                  ELSE ((m1.avg_delivery_time - m2.avg_delivery_time) * 100 / m2.avg_delivery_time)
              END AS DECIMAL(10,1)
          ) as delivery_time_trend
      FROM mv_daily_metrics m1
      LEFT JOIN mv_daily_metrics m2 ON m2.metric_date = m1.metric_date - INTERVAL '1 day';     
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index(self.INDEX_NAME, self.VIEW_NAME, self.COLUMN_NAME)
