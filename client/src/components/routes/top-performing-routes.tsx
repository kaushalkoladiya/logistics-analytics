'use client';

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { DataTable } from '@/components/ui/data-table';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import type { TopRoutePerformance } from '@/types/routes';
import { useAppDispatch, useAppSelector } from '@/store';
import { LoadingState } from '../shared/loading-state';
import { ErrorState } from '../shared/error-state';
import { DateRangeSelector } from '../shared/date-range-selector';
import { shallowEqual } from 'react-redux';
import { fetchTopPerformingRoutes } from '@/store/slices/routeSlice';

const columns = [
  {
    key: 'origin' as const,
    title: 'Origin',
    sortable: true,
  },
  {
    key: 'destination' as const,
    title: 'Destination',
    sortable: true,
  },
  {
    key: 'overall_score' as const,
    title: 'Performance Score',
    sortable: true,
    className: 'text-center',
    render: (value: number) => (
      <div className="flex items-center gap-2 justify-end">
        <Progress value={value} className="w-20" />
        <span>{value.toFixed(1)}%</span>
      </div>
    ),
  },
  {
    key: 'reliability_score' as const,
    title: 'Reliability',
    sortable: true,
    className: 'text-center',
    render: (value: number) => (
      <Badge variant={value >= 90 ? "success" : value >= 70 ? "warning" : "destructive"}>
        {value.toFixed(1)}%
      </Badge>
    ),
  },
  {
    key: 'performance_metrics' as const,
    title: 'Revenue',
    sortable: true,
    className: 'text-center',
    render: (metrics: TopRoutePerformance['performance_metrics']) =>
      `$${metrics.total_revenue.toLocaleString()}`,
  },
  {
    key: 'total_shipments' as const,
    title: 'Shipments',
    sortable: true,
    className: 'text-center',
    render: (value: number) => value.toLocaleString(),
  },
];

export function TopPerformingRoutes() {
  const dispatch = useAppDispatch();
  const { data, error, loading } = useAppSelector((state) => state.route.topPerforming, shallowEqual);

  const handleDateRangeChange = (range: { start: string; end: string }) => {
    dispatch(fetchTopPerformingRoutes(range));
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <CardTitle>Top Performing Routes</CardTitle>
          <DateRangeSelector onDateRangeChange={handleDateRangeChange} />
        </div>
      </CardHeader>

      <CardContent>
        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState message={error} />
        ) : (
          <DataTable
            columns={columns}
            data={data}
            searchable
            searchKey="origin"
          />
        )}
      </CardContent>
    </Card>
  );
}