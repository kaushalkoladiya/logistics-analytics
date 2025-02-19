from datetime import datetime, timedelta
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text


class CostAnalysisService:
    def __init__(self, db: Session = None):
        self.db: Session = db

    def get_period_totals(self, start_date: datetime, end_date: datetime):
        query = """
            SELECT 
                CAST(SUM(daily_total_cost) AS DECIMAL(10,2)) as total_cost,
                CAST(AVG(daily_avg_cost) AS DECIMAL(10,2)) as avg_cost_per_shipment,
                SUM(daily_shipments) as total_shipments,
                CAST(SUM(daily_total_cost) / NULLIF(SUM(daily_mileage), 0) AS DECIMAL(10,2)) as cost_per_km,
                CAST(SUM(daily_total_cost) / NULLIF(SUM(daily_weight), 0) AS DECIMAL(10,2)) as cost_per_kg,
                MAX(vehicle_count) as vehicles_used
            FROM mv_daily_cost_metrics
            WHERE metric_date BETWEEN :start_date AND :end_date
        """

        result = self.db.execute(
            text(query), {"start_date": start_date, "end_date": end_date}
        ).fetchone()

        return result._mapping

    def get_top_routes(
        self, start_date: datetime, end_date: datetime, limit: int = 5
    ) -> List:
        query = """
            SELECT 
                origin,
                destination,
                CAST(SUM(total_cost) AS DECIMAL(10,2)) as total_cost,
                SUM(shipment_count) as shipment_count,
                CAST(AVG(avg_cost) AS DECIMAL(10,2)) as avg_cost
            FROM mv_route_metrics
            WHERE metric_date BETWEEN :start_date AND :end_date
            GROUP BY origin, destination
            ORDER BY SUM(total_cost) DESC
            LIMIT :limit
        """
        results = self.db.execute(
            text(query),
            {"start_date": start_date, "end_date": end_date, "limit": limit},
        ).fetchall()

        return [row._mapping for row in results]

    def calculate_growth_percentage(
        self, current: Decimal, previous: Decimal
    ) -> Decimal:
        if not previous or previous == 0:
            return Decimal("0.00")
        return ((current - previous) / previous * 100).quantize(Decimal("0.01"))

    def get_comparison_period_dates(
        self, start_date: datetime, end_date: datetime
    ) -> tuple:
        """Calculate the previous period based on the date range length."""
        period_length = (end_date - start_date).days
        prev_end = start_date - timedelta(days=1)
        prev_start = prev_end - timedelta(days=period_length)
        return prev_start, prev_end

    def get_cost_analysis(self, start_date: datetime, end_date: datetime):
        prev_start, prev_end = self.get_comparison_period_dates(start_date, end_date)

        # Get metrics for both periods
        current_metrics = self.get_period_totals(start_date, end_date)
        previous_metrics = self.get_period_totals(prev_start, prev_end)

        # Calculate growth percentages
        cost_growth = self.calculate_growth_percentage(
            current_metrics.total_cost, previous_metrics.total_cost
        )
        avg_cost_growth = self.calculate_growth_percentage(
            current_metrics.avg_cost_per_shipment,
            previous_metrics.avg_cost_per_shipment,
        )

        # Get top routes for the current period
        top_routes = self.get_top_routes(start_date, end_date)

        return {
            "total_cost": current_metrics["total_cost"],
            "avg_cost_per_shipment": current_metrics["avg_cost_per_shipment"],
            "total_shipments": current_metrics["total_shipments"],
            "cost_per_km": current_metrics["cost_per_km"],
            "cost_per_kg": current_metrics["cost_per_kg"],
            "vehicles_used": current_metrics["vehicles_used"],
            "prev_total_cost": previous_metrics["total_cost"],
            "prev_avg_cost": previous_metrics["avg_cost_per_shipment"],
            "cost_growth_percentage": cost_growth,
            "avg_cost_growth_percentage": avg_cost_growth,
            "top_cost_routes": top_routes,
        }
