import { MetricCard } from '@/components/shared/metric-card';
import { Package, Timer, DollarSign, Scale, MapPin } from 'lucide-react';
import type { ShipmentOverview as ShipmentOverviewType } from '@/types/shipments';

interface ShipmentOverviewProps {
  data: ShipmentOverviewType;
}

export function ShipmentOverview({ data }: ShipmentOverviewProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <MetricCard
        title="Total Shipments"
        value={data.total_shipments.toLocaleString()}
        icon={<Package className="h-5 w-5 text-sky-500" />}
      />
      <MetricCard
        title="Average Delivery Time"
        value={`${data.avg_delivery_time.toFixed(1)}h`}
        icon={<Timer className="h-5 w-5 text-violet-500" />}
      />
      <MetricCard
        title="Total Cost"
        value={`$${data.total_cost.toLocaleString()}`}
        icon={<DollarSign className="h-5 w-5 text-emerald-500" />}
      />
      <MetricCard
        title="Average Cost/Shipment"
        value={`$${data.avg_cost_per_shipment.toLocaleString()}`}
        icon={<DollarSign className="h-5 w-5 text-amber-500" />}
      />
      <MetricCard
        title="Total Weight"
        value={`${data.total_weight.toLocaleString()} kg`}
        icon={<Scale className="h-5 w-5 text-rose-500" />}
      />
      <MetricCard
        title="Unique Routes"
        value={`${data.unique_origins} → ${data.unique_destinations}`}
        icon={<MapPin className="h-5 w-5 text-blue-500" />}
      />
    </div>
  );
}