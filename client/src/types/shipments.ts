export interface ShipmentOverview {
  total_shipments: number;
  avg_delivery_time: number;
  total_cost: number;
  avg_cost_per_shipment: number;
  total_weight: number;
  unique_origins: number;
  unique_destinations: number;
}

export interface RoutePerformance {
  origin: string;
  destination: string;
  total_trips: number;
  avg_delivery_time: number;
  min_delivery_time: number;
  max_delivery_time: number;
  total_cost: number;
  avg_cost: number;
  total_weight: number;
  unique_vehicles: number;
  cost_per_trip: number;
}

export interface ExpensiveRoute {
  origin: string;
  destination: string;
  total_shipments: number;
  total_cost: number;
  avg_cost_per_shipment: number;
  avg_delivery_time: number;
  vehicles_used: number;
}

export interface ShipmentAnalytics {
  overview: ShipmentOverview;
  expensive_routes: ExpensiveRoute[];
}

export interface ShipmentState {
  analytics: {
    data: ShipmentAnalytics | null;
    loading: boolean;
    error: string | null;
  };
  routes: {
    data: RoutePerformance[];
    total: number;
    page: number;
    pageSize: number;
    loading: boolean;
    error: string | null;
  };
}

export interface RouteParams {
  page: number;
  pageSize: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  search?: string;
}

export interface PaginatedRouteResponse {
  data: RoutePerformance[];
  total: number;
  page: number;
  page_size: number;
}