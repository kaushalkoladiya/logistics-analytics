from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import text


from app.schemas.vehicles import (
    VehicleMetrics,
    VehicleDetailsResponse,
    VehicleDetailSummary,
    DailyPerformance,
    RoutePerformance,
)


class VehicleService:
    def __init__(self, db: Session = None):
        self.db: Session = db

    def get_vehicle_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> List[VehicleMetrics]:
        params = {"start_date": start_date, "end_date": end_date}

        query = text(
            f"""
            SELECT 
                vehicle_id,
                name,
                SUM(trip_count) as total_trips,
                SUM(daily_mileage) as total_mileage,
                SUM(daily_fuel) as total_fuel,
                CAST(SUM(daily_mileage) / NULLIF(SUM(daily_fuel), 0) AS DECIMAL(10,2)) as fuel_efficiency,
                SUM(daily_shipments) as shipments_delivered,
                CAST(AVG(avg_delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
                CAST(SUM(daily_revenue) AS DECIMAL(10,2)) as total_revenue,
                CAST(SUM(daily_revenue) / NULLIF(SUM(trip_count), 0) AS DECIMAL(10,2)) as revenue_per_trip,
                CAST(SUM(daily_fuel) / NULLIF(SUM(trip_count), 0) AS DECIMAL(10,2)) as fuel_per_trip
            FROM mv_vehicle_daily_metrics
            WHERE metric_date BETWEEN :start_date AND :end_date
            GROUP BY vehicle_id, name
            ORDER BY total_revenue DESC;
            """
        )

        result = self.db.execute(query, params).fetchall()
        return [VehicleMetrics(**dict(row._mapping)) for row in result]

    def get_vehicle_details(
        self, vehicle_id: str, start_date: datetime, end_date: datetime
    ) -> VehicleDetailsResponse:
        # Query 1: Summary
        summary_query = text(
            """
            SELECT 
                vehicle_id,
                name,
                MAX(lifetime_mileage) as lifetime_mileage,
                COUNT(DISTINCT metric_date) as total_trips,
                CAST(SUM(daily_mileage) AS DECIMAL(10,2)) as period_mileage,
                CAST(SUM(daily_fuel) AS DECIMAL(10,2)) as total_fuel,
                CAST(
                    CASE 
                        WHEN SUM(daily_fuel) = 0 THEN 0
                        ELSE SUM(daily_mileage) / SUM(daily_fuel)
                    END 
                    AS DECIMAL(10,2)
                ) as fuel_efficiency,
                SUM(daily_shipments) as deliveries_completed,
                CAST(AVG(avg_delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
                CAST(SUM(daily_revenue) AS DECIMAL(10,2)) as total_revenue,
                CAST(SUM(daily_revenue) / NULLIF(COUNT(DISTINCT metric_date), 0) AS DECIMAL(10,2)) as revenue_per_trip,
                CAST(SUM(daily_fuel) / NULLIF(COUNT(DISTINCT metric_date), 0) AS DECIMAL(10,2)) as fuel_per_trip
            FROM mv_vehicle_daily_metrics
            WHERE vehicle_id = :vehicle_id
            AND metric_date BETWEEN :start_date AND :end_date
            GROUP BY vehicle_id, name;
            """
        )

        # Query 2: Daily Performance
        daily_query = text(
            """
            SELECT 
                metric_date as date,
                COUNT(DISTINCT metric_date) as trips,
                CAST(SUM(daily_mileage) AS DECIMAL(10,2)) as daily_mileage,
                CAST(SUM(daily_fuel) AS DECIMAL(10,2)) as daily_fuel,
                CAST(SUM(daily_revenue) AS DECIMAL(10,2)) as daily_revenue,
                SUM(daily_shipments) as daily_deliveries
            FROM mv_vehicle_daily_metrics
            WHERE vehicle_id = :vehicle_id
            AND metric_date BETWEEN :start_date AND :end_date
            GROUP BY metric_date
            ORDER BY metric_date;
            """
        )

        # Query 3: Route Performance
        route_query = text(
            """
            SELECT 
                origin,
                destination,
                COUNT(*) as route_trips,
                CAST(AVG(avg_delivery_time) AS DECIMAL(10,2)) as avg_route_time,
                CAST(AVG(daily_revenue) AS DECIMAL(10,2)) as avg_route_revenue
            FROM mv_vehicle_daily_metrics
            WHERE vehicle_id = :vehicle_id
            AND metric_date BETWEEN :start_date AND :end_date
            AND origin IS NOT NULL
            AND destination IS NOT NULL
            GROUP BY origin, destination
            ORDER BY route_trips DESC
            LIMIT 5;
            """
        )

        params = {
            "vehicle_id": vehicle_id,
            "start_date": start_date,
            "end_date": end_date,
        }

        summary = self.db.execute(summary_query, params).fetchone()
        daily_perf = self.db.execute(daily_query, params).fetchall()
        top_routes = self.db.execute(route_query, params).fetchall()

        return VehicleDetailsResponse(
            summary=VehicleDetailSummary(**dict(summary._mapping)),
            daily_performance=[
                DailyPerformance(**dict(day._mapping)) for day in daily_perf
            ],
            top_routes=[
                RoutePerformance(**dict(route._mapping)) for route in top_routes
            ],
        )
