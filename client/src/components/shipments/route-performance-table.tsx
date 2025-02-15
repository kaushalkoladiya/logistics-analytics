'use client';

import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchRoutePerformance } from '@/store/slices/shipmentSlice';
import { LoadingState } from '@/components/shared/loading-state';
import { Search } from 'lucide-react';
import { DataTablePagination } from '../ui/data-table-pagination';
import { useDebounce } from '@/hooks/use-debounce';

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
    key: 'total_trips' as const,
    title: 'Trips',
    sortable: true,
    className: 'text-right',
    render: (value: number) => value.toLocaleString(),
  },
  {
    key: 'avg_delivery_time' as const,
    title: 'Avg Time',
    sortable: true,
    className: 'text-right',
    render: (value: number) => `${value.toFixed(1)}h`,
  },
  {
    key: 'total_cost' as const,
    title: 'Total Cost',
    sortable: true,
    className: 'text-right',
    render: (value: number) => `$${value.toLocaleString()}`,
  },
  {
    key: 'cost_per_trip' as const,
    title: 'Cost/Trip',
    sortable: true,
    className: 'text-right',
    render: (value: number) => `$${value.toLocaleString()}`,
  },
];

export function RoutePerformanceTable() {
  const dispatch = useAppDispatch();
  const { data, total, page, pageSize, loading } = useAppSelector((state) => state.shipments.routes);

  const [search, setSearch] = useState('');
  const [sortConfig, setSortConfig] = useState({
    sortBy: 'total_trips',
    sortOrder: 'desc' as 'asc' | 'desc'
  });

  const debouncedSearchTerm = useDebounce(search, 1000); // 1s delay

  useEffect(() => {
    if (handleSearch) {
      handleSearch(debouncedSearchTerm);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedSearchTerm]);

  const fetchData = () => {
    dispatch(fetchRoutePerformance({
      page,
      pageSize,
      sortBy: sortConfig.sortBy,
      sortOrder: sortConfig.sortOrder,
      search: search || undefined
    }));
  };

  const handleSearch = (value: string) => {
    setSearch(value);
    dispatch(fetchRoutePerformance({
      page: 1,
      pageSize,
      sortBy: sortConfig.sortBy,
      sortOrder: sortConfig.sortOrder,
      search: value || undefined
    }));
  };

  const handleSort = (key: string) => {
    const newOrder = sortConfig.sortBy === key && sortConfig.sortOrder === 'asc' ? 'desc' : 'asc';
    setSortConfig({ sortBy: key, sortOrder: newOrder });
    dispatch(fetchRoutePerformance({
      page,
      pageSize,
      sortBy: key,
      sortOrder: newOrder,
      search: search || undefined
    }));
  };

  const handlePageChange = (newPage: number) => {
    dispatch(fetchRoutePerformance({
      page: newPage,
      pageSize,
      sortBy: sortConfig.sortBy,
      sortOrder: sortConfig.sortOrder,
      search: search || undefined
    }));
  };

  useEffect(() => {
    fetchData();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Route Performance</CardTitle>
          <div className="flex w-full max-w-sm items-center space-x-2">
            <Search className="h-4 w-4 text-slate-400" />
            <Input
              placeholder="Search routes..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="max-w-[200px]"
            />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <LoadingState />
        ) : (
          <DataTablePagination
            columns={columns}
            data={data}
            onSort={handleSort}
            currentPage={page}
            onPageChange={handlePageChange}
            total={total}
            pageSize={pageSize}
          />
        )}
      </CardContent>
    </Card>
  );
}