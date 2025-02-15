'use client';

import { Package, Truck, CreditCard, Timer } from 'lucide-react';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchDashboard } from '@/store/slices/dashboardSlice';
import { MetricCard } from '@/components/shared/metric-card';
import { LoadingState } from '@/components/shared/loading-state';
import { ErrorState } from '@/components/shared/error-state';
import { OnIntervalChangeParams, TrendIntervalSelector } from '../trends/trend-interval-selector';

export function DashboardOverview() {
  const dispatch = useAppDispatch();
  const { data, loading, error } = useAppSelector((state) => state.dashboard);

  const handleDateRangeChange = (range: OnIntervalChangeParams) => {
    dispatch(fetchDashboard(range));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Dashboard Overview</h1>
      </div>
      <div className="mt-2">
        <TrendIntervalSelector onIntervalChange={handleDateRangeChange} />
      </div>

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      {/* Metrics Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Total Shipments"
          value={data?.total_shipments || 0}
          trend={data?.shipment_trend}
          icon={<Package className="h-5 w-5 text-sky-500" />}
        />
        <MetricCard
          title="Active Vehicles"
          value={data?.active_vehicles || 0}
          trend={data?.vehicle_trend}
          icon={<Truck className="h-5 w-5 text-violet-500" />}
        />
        <MetricCard
          title="Total Revenue"
          value={`$${data?.total_revenue?.toLocaleString() || 0}`}
          trend={data?.revenue_trend}
          icon={<CreditCard className="h-5 w-5 text-emerald-500" />}
        />
        <MetricCard
          title="Avg Delivery Time"
          value={`${data?.avg_delivery_time || 0}h`}
          trend={data?.delivery_time_trend}
          icon={<Timer className="h-5 w-5 text-amber-500" />}
        />
      </div>
    </div>
  );
}