from pydantic import BaseModel
from typing import List

class VehicleCostAnalysis(BaseModel):
    vehicle_id: str
    name: str
    total_trips: int
    total_shipments: int
    total_cost: float
    avg_cost_per_shipment: float
    cost_per_trip: float
    total_fuel_used: float
    cost_per_fuel_unit: float

class PaginatedVehicleCostResponse(BaseModel):
    data: List[VehicleCostAnalysis]
    total: int
    page: int
    page_size: int

class TopCostRoute(BaseModel):
    origin: str
    destination: str
    total_cost: float
    shipment_count: int
    avg_cost: float

class CostOverviewResponse(BaseModel):
    total_cost: float
    avg_cost_per_shipment: float
    total_shipments: int
    cost_per_km: float
    cost_per_kg: float
    vehicles_used: int
    prev_total_cost: float
    prev_avg_cost: float
    cost_growth_percentage: float
    avg_cost_growth_percentage: float
    top_cost_routes: List[TopCostRoute] 