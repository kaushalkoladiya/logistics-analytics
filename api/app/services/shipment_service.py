from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.shipments import (
    ShipmentAnalytics,
    ShipmentOverview,
    ExpensiveRoute,
    PaginatedRouteResponse,
)


class ShipmentService:
    def __init__(self, db: Session = None):
        self.db: Session = db

    def get_shipment_analytics(
        self, start_date: datetime, end_date: datetime
    ) -> ShipmentAnalytics:
        overview_query = text(
            """
            SELECT 
                SUM(shipment_count) as total_shipments,
                CAST(AVG(avg_delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
                CAST(SUM(total_cost) AS DECIMAL(10,2)) as total_cost,
                CAST(AVG(avg_cost) AS DECIMAL(10,2)) as avg_cost_per_shipment,
                CAST(SUM(total_weight) AS DECIMAL(10,2)) as total_weight,
                COUNT(DISTINCT origin) as unique_origins,
                COUNT(DISTINCT destination) as unique_destinations
            FROM mv_route_metrics_comprehensive
            WHERE metric_date BETWEEN :start_date AND :end_date;
            """
        )

        expensive_routes_query = text(
            """
            SELECT 
                origin,
                destination,
                SUM(shipment_count) as total_shipments,
                CAST(SUM(total_cost) AS DECIMAL(10,2)) as total_cost,
                CAST(AVG(avg_cost) AS DECIMAL(10,2)) as avg_cost_per_shipment,
                CAST(AVG(avg_delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
                COUNT(DISTINCT vehicle_id) as vehicles_used
            FROM mv_route_metrics_comprehensive
            WHERE metric_date BETWEEN :start_date AND :end_date
            GROUP BY origin, destination
            HAVING SUM(shipment_count) >= 5
            ORDER BY avg_cost_per_shipment DESC
            LIMIT 5;
            """
        )

        overview = self.db.execute(
            overview_query, {"start_date": start_date, "end_date": end_date}
        ).fetchone()

        expensive_routes = self.db.execute(
            expensive_routes_query, {"start_date": start_date, "end_date": end_date}
        ).fetchall()

        return ShipmentAnalytics(
            overview=ShipmentOverview(**dict(overview._mapping)),
            expensive_routes=[
                ExpensiveRoute(**dict(route._mapping)) for route in expensive_routes
            ],
        )

    def get_route_performance(
        self,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "total_trips",
        sort_order: str = "desc",
        search: str = None,
    ) -> PaginatedRouteResponse:
        where_clause = ""
        params = {
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }

        if search:
            where_clause += "WHERE (:search IS NULL OR (origin ILIKE :search OR destination ILIKE :search))"
            params["search"] = f"%{search}%"

        query = text(
            f"""
            WITH route_metrics AS (
                SELECT 
                    origin,
                    destination,
                    SUM(shipment_count) as total_trips,
                    CAST(AVG(avg_delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
                    CAST(MIN(min_delivery_time) AS DECIMAL(10,2)) as min_delivery_time,
                    CAST(MAX(max_delivery_time) AS DECIMAL(10,2)) as max_delivery_time,
                    CAST(SUM(total_cost) AS DECIMAL(10,2)) as total_cost,
                    CAST(AVG(avg_cost) AS DECIMAL(10,2)) as avg_cost,
                    CAST(SUM(total_weight) AS DECIMAL(10,2)) as total_weight,
                    COUNT(DISTINCT vehicle_id) as unique_vehicles,
                    CAST(AVG(cost_per_trip) AS DECIMAL(10,2)) as cost_per_trip
                FROM mv_route_metrics_comprehensive
                {where_clause}
                GROUP BY origin, destination
            ),
            total_count AS (
                SELECT COUNT(*) as total FROM route_metrics
            )
            SELECT 
                *,
                (SELECT total FROM total_count) as total_count
            FROM route_metrics
            ORDER BY {sort_by} {sort_order}
            LIMIT :limit OFFSET :offset;
            """
        )

        result = self.db.execute(query, params).fetchall()

        if not result:
            return PaginatedRouteResponse(
                data=[], total=0, page=page, page_size=page_size
            )

        total_count = result[0].total_count
        data = [
            {k: v for k, v in row._mapping.items() if k != "total_count"}
            for row in result
        ]

        return PaginatedRouteResponse(
            data=data,
            total=total_count,
            page=page,
            page_size=page_size,
        )
