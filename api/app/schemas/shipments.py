from pydantic import BaseModel
from typing import List

class ShipmentOverview(BaseModel):
    total_shipments: int
    avg_delivery_time: float
    total_cost: float
    avg_cost_per_shipment: float
    total_weight: float
    unique_origins: int
    unique_destinations: int

class RoutePerformance(BaseModel):
    origin: str
    destination: str
    total_trips: int
    avg_delivery_time: float
    min_delivery_time: float
    max_delivery_time: float
    total_cost: float
    avg_cost: float
    total_weight: float
    unique_vehicles: int
    cost_per_trip: float

class ExpensiveRoute(BaseModel):
    origin: str
    destination: str
    total_shipments: int
    total_cost: float
    avg_cost_per_shipment: float
    avg_delivery_time: float
    vehicles_used: int

class ShipmentAnalytics(BaseModel):
    overview: ShipmentOverview
    expensive_routes: List[ExpensiveRoute]

class PaginatedRouteResponse(BaseModel):
    data: List[RoutePerformance]
    total: int
    page: int
    page_size: int 