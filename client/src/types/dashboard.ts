export interface AnalyticsState {
  data: DashboardOverview | null;
  loading: boolean;
  error: string | null;
}

export interface DashboardOverview {
  total_shipments: number;
  active_vehicles: number;
  total_revenue: number;
  avg_delivery_time: number;
  shipment_trend: number;
  vehicle_trend: number;
  revenue_trend: number;
  delivery_time_trend: number;
}