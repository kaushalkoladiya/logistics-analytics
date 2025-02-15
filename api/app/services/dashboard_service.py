from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.dashboard import DashboardResponse


class DashboardService:
    def __init__(self, db: Session = None):
        self.db: Session = db

    def get_dashboard_overview(
        self,
        start_date: datetime,
        end_date: datetime,
        interval_type: str,
        periods_back: int = 1,
    ) -> DashboardResponse:
        query = text(
            """
            WITH current_metrics AS (
                SELECT 
                    date_trunc(:interval_type, metric_date) as period_date,
                    SUM(total_shipments) as total_shipments,
                    AVG(active_vehicles) as active_vehicles,
                    SUM(total_revenue) as total_revenue,
                    AVG(avg_delivery_time) as avg_delivery_time
                FROM mv_daily_metrics
                WHERE metric_date BETWEEN :start_date AND :end_date
                GROUP BY date_trunc(:interval_type, metric_date)
            ),
            comparison_metrics AS (
                SELECT 
                    date_trunc(:interval_type, metric_date) as period_date,
                    SUM(total_shipments) as total_shipments,
                    AVG(active_vehicles) as active_vehicles,
                    SUM(total_revenue) as total_revenue,
                    AVG(avg_delivery_time) as avg_delivery_time
                FROM mv_daily_metrics
                WHERE metric_date BETWEEN 
                    (:start_date - (:periods_back || ' ' || :interval_type)::interval)
                    AND (:end_date - (:periods_back || ' ' || :interval_type)::interval)
                GROUP BY date_trunc(:interval_type, metric_date)
            )
            SELECT 
                c.period_date,
                c.total_shipments,
                c.active_vehicles,
                c.total_revenue,
                c.avg_delivery_time,
                CAST(((c.total_shipments - p.total_shipments)::DECIMAL * 100 / NULLIF(p.total_shipments, 0)) AS DECIMAL(10,1)) as shipment_trend,
                CAST(((c.active_vehicles - p.active_vehicles)::DECIMAL * 100 / NULLIF(p.active_vehicles, 0)) AS DECIMAL(10,1)) as vehicle_trend,
                CAST(((c.total_revenue - p.total_revenue) * 100 / NULLIF(p.total_revenue, 0)) AS DECIMAL(10,1)) as revenue_trend,
                CAST(((c.avg_delivery_time - p.avg_delivery_time) * 100 / NULLIF(p.avg_delivery_time, 0)) AS DECIMAL(10,1)) as delivery_time_trend
            FROM current_metrics c
            LEFT JOIN comparison_metrics p ON c.period_date = p.period_date + (:periods_back || ' ' || :interval_type)::interval
            ORDER BY c.period_date DESC;
        """
        )

        result = self.db.execute(
            query,
            {
                "start_date": start_date,
                "end_date": end_date,
                "interval_type": interval_type,
                "periods_back": periods_back,
            },
        ).fetchone()

        if not result:
            return DashboardResponse(
                total_shipments=0,
                active_vehicles=0,
                total_revenue=0,
                avg_delivery_time=0,
                shipment_trend=0,
                vehicle_trend=0,
                revenue_trend=0,
                delivery_time_trend=0,
            )

        return DashboardResponse(
            total_shipments=result.total_shipments,
            active_vehicles=round(result.active_vehicles, 2),
            total_revenue=float(result.total_revenue),
            avg_delivery_time=round(float(result.avg_delivery_time or 0), 2),
            shipment_trend=float(result.shipment_trend or 0),
            vehicle_trend=float(result.vehicle_trend or 0),
            revenue_trend=float(result.revenue_trend or 0),
            delivery_time_trend=float(result.delivery_time_trend or 0),
        )
