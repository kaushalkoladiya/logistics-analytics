from pydantic import BaseModel
from typing import List, Dict

class TopRoutePerformance(BaseModel):
    origin: str
    destination: str
    total_shipments: int
    reliability_score: float
    cost_efficiency_score: float
    delivery_efficiency_score: float
    overall_score: float
    performance_metrics: dict

class RouteReliabilityResponse(BaseModel):
    data: List[Dict]
    total: int
    page: int
    page_size: int

class RouteCostValueResponse(BaseModel):
    data: List[Dict]
    total: int
    page: int
    page_size: int

class RouteOptimizationResponse(BaseModel):
    data: List[Dict]
    total: int
    page: int
    page_size: int 