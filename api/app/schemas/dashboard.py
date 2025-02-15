from pydantic import BaseModel
from typing import Literal

class DashboardResponse(BaseModel):
    total_shipments: int
    active_vehicles: float
    total_revenue: float
    avg_delivery_time: float
    shipment_trend: float
    vehicle_trend: float
    revenue_trend: float
    delivery_time_trend: float 