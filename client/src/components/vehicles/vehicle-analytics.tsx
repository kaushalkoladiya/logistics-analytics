'use client';

import { Car, Fuel, Timer, DollarSign } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchVehicleMetrics } from '@/store/slices/vehicleSlice';
import { MetricCard } from '@/components/shared/metric-card';
import { LoadingState } from '@/components/shared/loading-state';
import { ErrorState } from '@/components/shared/error-state';
import { DateRangeSelector } from '@/components/shared/date-range-selector';
import { DataTable } from '@/components/ui/data-table';
import { VehicleMetric } from '@/types/vehicles';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';

const columns = [
    {
      key: 'name' as const,
      title: 'Vehicle',
      sortable: true,
    },
    {
      key: 'total_trips' as const,
      title: 'Total Trips',
      sortable: true,
      className: 'text-center',
      render: (value: number) => value.toLocaleString(),
    },
    {
      key: 'total_mileage' as const,
      title: 'Mileage',
      sortable: true,
      className: 'text-center',
      render: (value: number) => `${value.toLocaleString()} km`,
    },
    {
      key: 'fuel_efficiency' as const,
      title: 'Fuel Efficiency',
      sortable: true,
      className: 'text-center',
      render: (value: number) => `${value.toFixed(2)} km/l`,
    },
    {
      key: 'revenue_per_trip' as const,
      title: 'Revenue/Trip',
      sortable: true,
      className: 'text-center',
      render: (value: number) => `$${value.toLocaleString()}`,
    },
    {
      key: 'shipments_delivered' as const,
      title: 'Deliveries',
      sortable: true,
      className: 'text-center',
      render: (value: number) => value.toLocaleString(),
    },
  ];

export function VehicleAnalytics() {
  const router = useRouter();
  const dispatch = useAppDispatch();
  const { data, loading, error } = useAppSelector((state) => state.vehicles.metrics);

  const handleDateRangeChange = (range: { start: string; end: string }) => {
    dispatch(fetchVehicleMetrics(range));
  };

  const handleRowClick = (vehicle: VehicleMetric) => {
    router.push(`/vehicles/${vehicle.vehicle_id}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Vehicle Analytics</h1>
        <DateRangeSelector onDateRangeChange={handleDateRangeChange} />
      </div>

      {loading ? (
        <LoadingState />
      ) : error ? (
        <ErrorState message={error} />
      ) : (
        <div className="space-y-6">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              title="Total Vehicles"
              value={data?.length || 0}
              icon={<Car className="h-5 w-5 text-sky-500" />}
            />
            <MetricCard
              title="Average Fuel Efficiency"
              value={`${data ? (data.reduce((acc, v) => acc + v.fuel_efficiency, 0) / data.length).toFixed(2) : 0} km/l`}
              icon={<Fuel className="h-5 w-5 text-violet-500" />}
            />
            <MetricCard
              title="Avg Delivery Time"
              value={`${data ? (data.reduce((acc, v) => acc + v.avg_delivery_time, 0) / data.length).toFixed(1) : 0}h`}
              icon={<Timer className="h-5 w-5 text-emerald-500" />}
            />
            <MetricCard
              title="Total Revenue"
              value={`$${data ? data.reduce((acc, v) => acc + v.total_revenue, 0).toLocaleString() : 0}`}
              icon={<DollarSign className="h-5 w-5 text-amber-500" />}
            />
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Vehicle Metrics</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable
                columns={columns}
                data={data || []}
                searchable
                searchKey="name"
                onRowClick={handleRowClick}
              />
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}