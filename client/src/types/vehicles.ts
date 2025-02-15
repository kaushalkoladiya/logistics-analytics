export interface VehicleDetailsRequest {
  id: string;
  start: string;
  end: string;
}

export interface VehicleMetric {
  vehicle_id: string;
  name: string;
  total_trips: number;
  total_mileage: number;
  total_fuel: number;
  fuel_efficiency: number;
  shipments_delivered: number;
  avg_delivery_time: number;
  total_revenue: number;
  revenue_per_trip: number;
  fuel_per_trip: number;
}

export interface VehicleDetailSummary {
  vehicle_id: string;
  name: string;
  lifetime_mileage: number;
  total_trips: number;
  period_mileage: number;
  total_fuel: number;
  fuel_efficiency: number;
  deliveries_completed: number;
  avg_delivery_time: number;
  total_revenue: number;
  revenue_per_trip: number;
  fuel_per_trip: number;
}

export interface DailyPerformance {
  date: string;
  trips: number;
  daily_mileage: number;
  daily_fuel: number;
  daily_revenue: number;
  daily_deliveries: number;
}

export interface RoutePerformance {
  origin: string;
  destination: string;
  route_trips: number;
  avg_route_time: number;
  avg_route_revenue: number;
}

export interface VehicleDetail {
  summary: VehicleDetailSummary;
  daily_performance: DailyPerformance[];
  top_routes: RoutePerformance[];
}

export interface VehicleState {
  metrics: {
    data: VehicleMetric[] | null;
    loading: boolean;
    error: string | null;
  };
  detail: {
    data: VehicleDetail | null;
    loading: boolean;
    error: string | null;
  }
}