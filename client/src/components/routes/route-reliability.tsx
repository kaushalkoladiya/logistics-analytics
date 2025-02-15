'use client';

import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DateRangeSelector } from '@/components/shared/date-range-selector';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchRouteReliability } from '@/store/slices/routeSlice';
import { LoadingState } from '@/components/shared/loading-state';
import { ErrorState } from '@/components/shared/error-state';
import { DataTablePagination } from '../ui/data-table-pagination';

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
    key: 'total_deliveries' as const,
    title: 'Total Deliveries',
    sortable: true,
    className: 'text-right',
    render: (value: number) => value.toLocaleString(),
  },
  {
    key: 'reliability_score' as const,
    title: 'Reliability Score',
    sortable: true,
    className: 'text-right',
    render: (value: number) => (
      <Badge variant={value >= 90 ? "success" : value >= 70 ? "warning" : "destructive"}>
        {value}%
      </Badge>
    ),
  },
  {
    key: 'avg_delivery_time' as const,
    title: 'Avg Delivery Time',
    sortable: true,
    className: 'text-right',
  },
  {
    key: 'on_time_delivery_rate' as const,
    title: 'On-Time Rate',
    sortable: true,
    className: 'text-right',
  },
];

export function RouteReliabilityTable() {
  const dispatch = useAppDispatch();
  const { data, loading, error, total } = useAppSelector((state) => state.route.reliability);

  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [sortBy, setSortBy] = useState('reliability_score');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [search, setSearch] = useState('');

  const fetchData = (params: {
    start: string;
    end: string;
    page: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    search?: string;
  }) => {
    if (params.start && params.end) {
      console.log('Fetching data:', params);
      dispatch(fetchRouteReliability({
        ...params
      }));
    }
  };

  const handleDateRangeChange = (range: { start: string; end: string }) => {
    setDateRange(range);
    fetchData({ ...range, page: 1 });
  };

  const handleSort = (key: string) => {
    const newOrder = key === sortBy && sortOrder === 'asc' ? 'desc' : 'asc';
    setSortBy(key);
    setSortOrder(newOrder);
    fetchData({
      ...dateRange,
      page,
      sortBy: key,
      sortOrder: newOrder,
      search
    });
  };

  const handleSearch = (value: string) => {
    setSearch(value);
    setPage(1); // Reset to first page on search
    fetchData({
      ...dateRange,
      page: 1,
      sortBy,
      sortOrder,
      search: value
    });
  };

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
    fetchData({
      ...dateRange,
      page: newPage,
      sortBy,
      sortOrder,
      search
    });
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <CardTitle>Route Reliability Analysis</CardTitle>
          <DateRangeSelector onDateRangeChange={handleDateRangeChange} />
        </div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState message={error} />
        ) : (

          <DataTablePagination
            columns={columns}
            data={data}
            searchable
            onSearch={handleSearch}
            pageSize={pageSize}
            currentPage={page}
            onPageChange={handlePageChange}
            onSort={handleSort}
            total={total}
            sortKey='reliability_score'
            sortOrder='desc'
          />
        )}
      </CardContent>
    </Card>
  );
}
