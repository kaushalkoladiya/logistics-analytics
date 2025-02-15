import { Car, Fuel, Timer, DollarSign, Package, Route } from 'lucide-react';
import { MetricCard } from '@/components/shared/metric-card';
import type { VehicleDetailSummary } from '@/types/vehicles';

interface VehicleSummaryProps {
  summary: VehicleDetailSummary;
}

export function VehicleSummary({ summary }: VehicleSummaryProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <MetricCard
        title="Total Trips"
        value={summary.total_trips.toLocaleString()}
        icon={<Route className="h-5 w-5 text-sky-500" />}
      />
      <MetricCard
        title="Lifetime Mileage"
        value={`${summary.lifetime_mileage.toLocaleString()} km`}
        icon={<Car className="h-5 w-5 text-violet-500" />}
      />
      <MetricCard
        title="Fuel Efficiency"
        value={`${summary.fuel_efficiency.toFixed(2)} km/l`}
        icon={<Fuel className="h-5 w-5 text-emerald-500" />}
      />
      <MetricCard
        title="Revenue Per Trip"
        value={`$${summary.revenue_per_trip.toLocaleString()}`}
        icon={<DollarSign className="h-5 w-5 text-amber-500" />}
      />
      <MetricCard
        title="Deliveries Completed"
        value={summary.deliveries_completed.toLocaleString()}
        icon={<Package className="h-5 w-5 text-rose-500" />}
      />
      <MetricCard
        title="Avg Delivery Time"
        value={`${summary.avg_delivery_time.toFixed(1)}h`}
        icon={<Timer className="h-5 w-5 text-blue-500" />}
      />
    </div>
  );
}