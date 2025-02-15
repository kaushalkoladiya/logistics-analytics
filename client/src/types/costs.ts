export interface TopCostRoute {
  origin: string;
  destination: string;
  total_cost: number;
  shipment_count: number;
  avg_cost: number;
}

export interface CostOverview {
  total_cost: number;
  avg_cost_per_shipment: number;
  total_shipments: number;
  cost_per_km: number;
  cost_per_kg: number;
  vehicles_used: number;
  prev_total_cost: number;
  prev_avg_cost: number;
  cost_growth_percentage: number;
  avg_cost_growth_percentage: number;
  top_cost_routes: TopCostRoute[];
}

export interface CostState {
  overview: {
    data: CostOverview | null;
    loading: boolean;
    error: string | null;
  };
}