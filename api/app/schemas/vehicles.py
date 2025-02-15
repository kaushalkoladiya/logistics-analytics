from pydantic import BaseModel
from typing import List
from datetime import date

class VehicleMetrics(BaseModel):
    vehicle_id: str
    name: str
    total_trips: int
    total_mileage: float
    total_fuel: float
    fuel_efficiency: float
    shipments_delivered: int
    avg_delivery_time: float
    total_revenue: float
    revenue_per_trip: float
    fuel_per_trip: float

class RoutePerformance(BaseModel):
    origin: str
    destination: str
    route_trips: int
    avg_route_time: float
    avg_route_revenue: float

class DailyPerformance(BaseModel):
    date: date
    trips: int
    daily_mileage: float | None
    daily_fuel: float | None
    daily_revenue: float | None
    daily_deliveries: int

class VehicleDetailSummary(BaseModel):
    vehicle_id: str
    name: str
    lifetime_mileage: float
    total_trips: int
    period_mileage: float
    total_fuel: float
    fuel_efficiency: float
    deliveries_completed: int
    avg_delivery_time: float
    total_revenue: float
    revenue_per_trip: float
    fuel_per_trip: float

class VehicleDetailsResponse(BaseModel):
    summary: VehicleDetailSummary
    daily_performance: List[DailyPerformance]
    top_routes: List[RoutePerformance] 