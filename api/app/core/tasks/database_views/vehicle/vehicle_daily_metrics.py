from app.core.tasks.database_views.materialized_view_manager import (
    MaterializedViewManager,
)
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class VehicleDailyMetricsView(MaterializedViewManager):
    VIEW_NAME = "mv_vehicle_daily_metrics"

    VIEW_QUERY = """
        SELECT 
            DATE(vl.trip_date) as metric_date,
            v.vehicle_id,
            v.name,
            v.total_mileage as lifetime_mileage,
            COUNT(DISTINCT vl.log_id) as trip_count,
            SUM(vl.mileage) as daily_mileage,
            SUM(vl.fuel_used) as daily_fuel,
            CAST(SUM(vl.mileage) / NULLIF(SUM(vl.fuel_used), 0) AS DECIMAL(10,2)) as daily_fuel_efficiency,
            COUNT(DISTINCT s.shipment_id) as daily_shipments,
            CAST(AVG(s.delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
            CAST(SUM(s.cost) AS DECIMAL(10,2)) as daily_revenue,
            s.origin,
            s.destination
        FROM vehicles v
        LEFT JOIN vehicle_logs vl ON v.vehicle_id = vl.vehicle_id
        LEFT JOIN shipments s ON vl.log_id = s.log_id
        WHERE vl.mileage IS NOT NULL 
            AND vl.fuel_used IS NOT NULL
        GROUP BY DATE(vl.trip_date), v.vehicle_id, v.name, s.origin, s.destination;
    """

    def __init__(self, db: Session = None):
        self.db: Session = db or SessionLocal()
        super().__init__(self.db)

    def setup(self):
        """Creates the view and its index."""
        self.create_view(self.VIEW_NAME, self.VIEW_QUERY)
        self.create_index("idx_mv_vehicle_metrics_date", self.VIEW_NAME, "metric_date")
        self.create_index("idx_mv_vehicle_metrics_id", self.VIEW_NAME, "vehicle_id")
        self.create_index(
            "idx_mv_vehicle_metrics_revenue", self.VIEW_NAME, "daily_revenue DESC"
        )
        self.create_index(
            "idx_mv_vehicle_metrics_route", self.VIEW_NAME, "origin, destination"
        )
