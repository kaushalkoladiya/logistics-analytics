from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.routes import (
    TopRoutePerformance,
    RouteReliabilityResponse,
    RouteCostValueResponse,
    RouteOptimizationResponse,
)


class RouteService:
    def __init__(self, db: Session = None):
        self.db: Session = db

    def get_route_reliability(
        self,
        start_date: datetime,
        end_date: datetime,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "reliability_score",
        sort_order: str = "desc",
        search: str = None,
    ) -> RouteReliabilityResponse:
        where_clause = "WHERE metric_date BETWEEN :start_date AND :end_date"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }

        if search:
            where_clause += " AND (:search IS NULL OR (origin ILIKE :search OR destination ILIKE :search))"
            params["search"] = f"%{search}%"

        query = text(
            f"""
            WITH filtered_routes AS (
                SELECT DISTINCT
                    origin,
                    destination,
                    route_delivery_count as total_deliveries,
                    CAST(route_avg_delivery_time AS DECIMAL(10,2)) as avg_delivery_time,
                    CAST(route_stddev AS DECIMAL(10,2)) as delivery_time_variation,
                    CAST(
                        100 * (1 - COALESCE(route_stddev / NULLIF(route_avg_delivery_time, 0), 0))
                        AS DECIMAL(10,2)
                    ) as reliability_score,
                    CAST(
                        100 * COUNT(CASE 
                            WHEN delivery_time <= route_avg_delivery_time + 1 
                            THEN 1 
                        END)::float / NULLIF(route_delivery_count, 0)
                        AS DECIMAL(10,2)
                    ) as on_time_delivery_rate
                FROM mv_route_reliability
                {where_clause}
                GROUP BY 
                    origin, destination, route_delivery_count, 
                    route_avg_delivery_time, route_stddev
                HAVING route_delivery_count >= 5
            ),
            total_count AS (
                SELECT COUNT(*) as total FROM filtered_routes
            )
            SELECT 
                fr.*,
                tc.total as total_count
            FROM filtered_routes fr, total_count tc
            ORDER BY {sort_by} {sort_order}
            LIMIT :limit OFFSET :offset;
            """
        )

        result = self.db.execute(query, params).fetchall()

        if not result:
            return RouteReliabilityResponse(
                data=[], total=0, page=page, page_size=page_size
            )

        total_count = result[0].total_count
        data = [
            {k: v for k, v in row._mapping.items() if k != "total_count"}
            for row in result
        ]

        return RouteReliabilityResponse(
            data=data,
            total=total_count,
            page=page,
            page_size=page_size,
        )

    def get_route_cost_value(
        self,
        start_date: datetime,
        end_date: datetime,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "value_score",
        sort_order: str = "desc",
        search: str = None,
    ) -> RouteCostValueResponse:
        where_clause = "WHERE metric_date BETWEEN :start_date AND :end_date"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }

        if search:
            where_clause += " AND (:search IS NULL OR (origin ILIKE :search OR destination ILIKE :search))"
            params["search"] = f"%{search}%"

        query = text(
            f"""
                WITH filtered_routes AS (
                    SELECT 
                        origin,
                        destination,
                        SUM(shipment_count) as total_shipments,
                        CAST(AVG(avg_shipment_weight) AS DECIMAL(10,2)) as avg_shipment_weight,
                        CAST(AVG(avg_cost) AS DECIMAL(10,2)) as avg_cost,
                        CAST(AVG(cost_per_kg) AS DECIMAL(10,2)) as cost_per_kg,
                        CAST(AVG(value_score) AS DECIMAL(10,2)) as value_score
                    FROM mv_route_value_metrics
                    {where_clause}
                    GROUP BY origin, destination
                    HAVING SUM(shipment_count) >= 5
                ),
                percentiles AS (
                    SELECT
                        percentile_cont(0.33) WITHIN GROUP (ORDER BY value_score) as p33,
                        percentile_cont(0.66) WITHIN GROUP (ORDER BY value_score) as p66
                    FROM filtered_routes
                ),
                route_value AS (
                    SELECT 
                        fr.*,
                        CASE 
                            WHEN fr.value_score <= p.p33 THEN 'High Value'
                            WHEN fr.value_score <= p.p66 THEN 'Medium Value'
                            ELSE 'Low Value'
                        END as value_category
                    FROM filtered_routes fr, percentiles p
                ),
                total_count AS (
                    SELECT COUNT(*) as total FROM route_value
                )
                SELECT 
                    rv.*,
                    tc.total as total_count
                FROM route_value rv, total_count tc
                ORDER BY {sort_by} {sort_order}
                LIMIT :limit OFFSET :offset;          
        """
        )

        result = self.db.execute(query, params).fetchall()

        if not result:
            return {"data": [], "total": 0, "page": page, "page_size": page_size}

        total_count = result[0].total_count
        data = [
            {k: v for k, v in row._mapping.items() if k != "total_count"}
            for row in result
        ]

        return RouteReliabilityResponse(
            data=data,
            total=total_count,
            page=page,
            page_size=page_size,
        )

    def get_route_optimization(
        self,
        start_date: datetime,
        end_date: datetime,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "cost_time_efficiency",
        sort_order: str = "desc",
        search: str = None,
    ) -> RouteOptimizationResponse:
        where_clause = "WHERE metric_date BETWEEN :start_date AND :end_date"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }

        if search:
            where_clause += " AND (:search IS NULL OR (origin ILIKE :search OR destination ILIKE :search))"
            params["search"] = f"%{search}%"

        query = text(
            f"""
                WITH filtered_routes AS (
                    SELECT 
                        origin,
                        destination,
                        SUM(shipment_count) as total_shipments,
                        CAST(AVG(avg_delivery_time) AS DECIMAL(10,2)) as avg_delivery_time,
                        CAST(AVG(avg_cost) AS DECIMAL(10,2)) as avg_cost,
                        CAST(AVG(avg_weight) AS DECIMAL(10,2)) as avg_weight,
                        CAST(SUM(total_cost) AS DECIMAL(10,2)) as total_cost,
                        CAST(SUM(total_weight) AS DECIMAL(10,2)) as total_weight
                    FROM mv_route_metrics_comprehensive
                    {where_clause}
                    GROUP BY origin, destination
                    HAVING SUM(shipment_count) >= 5
                ),
                route_averages AS (
                    SELECT
                        AVG(avg_delivery_time) as global_avg_delivery_time,
                        AVG(avg_cost) as global_avg_cost,
                        AVG(total_cost/NULLIF(total_weight, 0)) as global_cost_per_weight
                    FROM filtered_routes
                ),
                route_optimization AS (
                    SELECT 
                        fr.*,
                        CAST((fr.total_cost / NULLIF(fr.total_weight, 0)) / NULLIF(fr.avg_delivery_time, 0) 
                            AS DECIMAL(10,2)) as cost_time_efficiency,
                        CASE
                            WHEN fr.avg_delivery_time > ra.global_avg_delivery_time * 1.2 
                                THEN 'High delivery time - Consider route optimization'
                            WHEN (fr.total_cost/NULLIF(fr.total_weight, 0)) > ra.global_cost_per_weight * 1.2 
                                THEN 'High cost per weight - Review pricing strategy'
                            WHEN fr.total_shipments < 10 AND fr.total_cost > ra.global_cost_per_weight * fr.total_weight * 1.5 
                                THEN 'Low volume, high cost - Consider consolidation'
                            ELSE 'Performing within normal parameters'
                        END as optimization_recommendation
                    FROM filtered_routes fr, route_averages ra
                ),
                total_count AS (
                    SELECT COUNT(*) as total FROM route_optimization
                )
                SELECT 
                    ro.*,
                    tc.total as total_count
                FROM route_optimization ro, total_count tc
                ORDER BY {sort_by} {sort_order}
                LIMIT :limit OFFSET :offset;
        """
        )

        result = self.db.execute(query, params).fetchall()

        if not result:
            return {"data": [], "total": 0, "page": page, "page_size": page_size}

        total_count = result[0].total_count
        data = [
            {k: v for k, v in row._mapping.items() if k != "total_count"}
            for row in result
        ]

        return RouteReliabilityResponse(
            data=data,
            total=total_count,
            page=page,
            page_size=page_size,
        )

    def get_top_performing_routes(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 10,
    ) -> List[TopRoutePerformance]:
        query = text(
            """
            WITH route_metrics AS (
                SELECT 
                    origin,
                    destination,
                    SUM(total_shipments) as total_shipments,
                    AVG(avg_delivery_time) as avg_delivery_time,
                    AVG(delivery_time_variation) as delivery_time_variation,
                    AVG(avg_cost) as avg_cost,
                    SUM(total_cost) as total_cost,
                    AVG(cost_per_kg) as cost_per_kg,
                    SUM(total_weight) as total_weight,
                    AVG(on_time_delivery_rate) as on_time_delivery_rate,
                    MIN(min_cost_per_kg) as min_cost_per_kg,
                    MAX(max_cost_per_kg) as max_cost_per_kg,
                    MIN(min_delivery_time) as min_delivery_time,
                    MAX(max_delivery_time) as max_delivery_time
                FROM mv_route_performance_metrics
                WHERE metric_date BETWEEN :start_date AND :end_date
                GROUP BY origin, destination
                HAVING SUM(total_shipments) >= 5
            )
            SELECT 
                origin,
                destination,
                total_shipments,
                CAST(
                    100 * (1 - COALESCE(delivery_time_variation / NULLIF(avg_delivery_time, 0), 0))
                    AS DECIMAL(10,2)
                ) AS reliability_score,
                CAST(
                    100 * (1 - (cost_per_kg - min_cost_per_kg) / 
                    NULLIF(max_cost_per_kg - min_cost_per_kg, 1))
                    AS DECIMAL(10,2)
                ) AS cost_efficiency_score,
                CAST(
                    100 * (1 - (avg_delivery_time - min_delivery_time) / 
                    NULLIF(max_delivery_time - min_delivery_time, 1))
                    AS DECIMAL(10,2)
                ) AS delivery_efficiency_score,
                CAST(
                    (100 * (1 - COALESCE(delivery_time_variation / NULLIF(avg_delivery_time, 0), 0))) * 0.4 + 
                    (100 * (1 - (cost_per_kg - min_cost_per_kg) / NULLIF(max_cost_per_kg - min_cost_per_kg, 1))) * 0.3 + 
                    (100 * (1 - (avg_delivery_time - min_delivery_time) / NULLIF(max_delivery_time - min_delivery_time, 1))) * 0.3
                    AS DECIMAL(10,2)
                ) AS overall_score,
                jsonb_build_object(
                    'on_time_delivery_rate', on_time_delivery_rate,
                    'avg_cost_per_shipment', avg_cost,
                    'total_revenue', total_cost,
                    'total_weight_shipped', total_weight
                ) AS performance_metrics
            FROM route_metrics
            ORDER BY overall_score DESC
            LIMIT :limit;
            """
        )

        result = self.db.execute(
            query,
            {
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit,
            },
        ).fetchall()

        return [TopRoutePerformance(**dict(row._mapping)) for row in result]
