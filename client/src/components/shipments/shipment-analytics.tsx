'use client';

import { useAppDispatch, useAppSelector } from '@/store';
import { fetchShipmentAnalytics } from '@/store/slices/shipmentSlice';
import { DateRangeSelector } from '@/components/shared/date-range-selector';
import { LoadingState } from '@/components/shared/loading-state';
import { ErrorState } from '@/components/shared/error-state';
import { ShipmentOverview } from './shipment-overview';
import { ExpensiveRoutesTable } from './expensive-routes-table';
import { RoutePerformanceTable } from './route-performance-table';

export function ShipmentAnalytics() {
  const dispatch = useAppDispatch();
  const { data, loading, error } = useAppSelector((state) => state.shipments.analytics);

  const handleDateRangeChange = (range: { start: string; end: string }) => {
    dispatch(fetchShipmentAnalytics(range));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Shipment Analytics</h1>
        <DateRangeSelector onDateRangeChange={handleDateRangeChange} />
      </div>

      {loading ? (
        <LoadingState />
      ) : error ? (
        <ErrorState message={error} />
      ) : data ? (
        <>
          <ShipmentOverview data={data.overview} />
          <div className="grid gap-6 lg:grid-cols-2">
            <ExpensiveRoutesTable data={data.expensive_routes} />
            <RoutePerformanceTable/>
          </div>
        </>
      ) : null}
    </div>
  );
}