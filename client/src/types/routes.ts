export interface RouteReliability {
  origin: string;
  destination: string;
  total_deliveries: number;
  avg_delivery_time: number;
  delivery_time_variation: number;
  reliability_score: number;
  on_time_delivery_rate: number;
}

export interface RouteCostValue {
  origin: string;
  destination: string;
  total_shipments: number;
  avg_shipment_weight: number;
  avg_cost: number;
  cost_per_kg: number;
  value_score: number;
  value_category: string;
}

export interface RouteOptimization {
  origin: string;
  destination: string;
  total_shipments: number;
  avg_delivery_time: number;
  avg_cost: number;
  avg_weight: number;
  cost_time_efficiency: number;
  optimization_recommendation: string;
}

export interface TopRoutePerformance {
  origin: string;
  destination: string;
  total_shipments: number;
  reliability_score: number;
  cost_efficiency_score: number;
  delivery_efficiency_score: number;
  overall_score: number;
  performance_metrics: {
    on_time_delivery_rate: number;
    avg_cost_per_shipment: number;
    total_revenue: number;
    total_weight_shipped: number;
  };
}

export interface RouteState {
  reliability: {
    data: RouteReliability[];
    loading: boolean;
    error: string | null;
    page: number;
    pageSize: number;
    total: number;
  };
  costValue: {
    data: RouteCostValue[];
    loading: boolean;
    error: string | null;
    page: number;
    pageSize: number;
    total: number;
  };
  optimization: {
    data: RouteOptimization[];
    loading: boolean;
    error: string | null;
    page: number;
    pageSize: number;
    total: number;
  };
  topPerforming: {
    data: TopRoutePerformance[];
    loading: boolean;
    error: string | null;
    page: number;
    pageSize: number;
    total: number;
  };
}

export interface RouteAPIRequest {
  start: string;
  end: string;
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  search?: string;
};

export interface RouteReliabilityResponse {
  data: RouteReliability[];
  page: number;
  pageSize: number;
  total: number;
}

export interface RouteCostValueResponse {
  data: RouteCostValue[];
  page: number;
  pageSize: number;
  total: number;
}

export interface RouteOptimizationResponse {
  data: RouteOptimization[];
  page: number;
  pageSize: number;
  total: number;
}

export interface RoutePerformanceResponse {
  data: TopRoutePerformance[];
  page: number;
  pageSize: number;
  total: number;
}
