import { DollarSign, Package, Truck, Scale, Route } from 'lucide-react';
import { MetricCard } from '@/components/shared/metric-card';
import type { CostOverview } from '@/types/costs';

interface CostMetricsProps {
  data: CostOverview;
}

export function CostMetrics({ data }: CostMetricsProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <MetricCard
        title="Total Cost"
        value={`$${data.total_cost.toLocaleString()}`}
        trend={data.cost_growth_percentage}
        icon={<DollarSign className="h-5 w-5 text-sky-500" />}
      />
      <MetricCard
        title="Average Cost/Shipment"
        value={`$${data.avg_cost_per_shipment.toLocaleString()}`}
        trend={data.avg_cost_growth_percentage}
        icon={<Package className="h-5 w-5 text-violet-500" />}
      />
      <MetricCard
        title="Cost per KM"
        value={`$${data.cost_per_km.toFixed(2)}`}
        icon={<Route className="h-5 w-5 text-emerald-500" />}
      />
      <MetricCard
        title="Cost per KG"
        value={`$${data.cost_per_kg.toFixed(2)}`}
        icon={<Scale className="h-5 w-5 text-amber-500" />}
      />
      <MetricCard
        title="Total Shipments"
        value={data.total_shipments.toLocaleString()}
        icon={<Package className="h-5 w-5 text-rose-500" />}
      />
      <MetricCard
        title="Vehicles Used"
        value={data.vehicles_used.toLocaleString()}
        icon={<Truck className="h-5 w-5 text-blue-500" />}
      />
    </div>
  );
}