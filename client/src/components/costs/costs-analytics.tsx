'use client';

import { useAppDispatch, useAppSelector } from '@/store';
import { DateRangeSelector } from '@/components/shared/date-range-selector';
import { LoadingState } from '@/components/shared/loading-state';
import { ErrorState } from '@/components/shared/error-state';
import { CostMetrics } from './cost-metrics';
import { TopCostRoutes } from './top-cost-routes';
import { fetchCostOverview } from '@/store/slices/costSlice';

export default function CostsAnalytics() {
  const dispatch = useAppDispatch();
  const { data, loading, error } = useAppSelector((state) => state.costs.overview);

  const handleDateRangeChange = (range: { start: string; end: string }) => {
    dispatch(fetchCostOverview(range));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Cost Analytics</h1>
        <DateRangeSelector onDateRangeChange={handleDateRangeChange} />
      </div>

      {loading ? (
        <LoadingState />
      ) : error ? (
        <ErrorState message={error} />
      ) : data ? (
        <div className="space-y-6">
          <CostMetrics data={data} />
          <TopCostRoutes routes={data.top_cost_routes} />
        </div>
      ) : null}
    </div>
  );
}