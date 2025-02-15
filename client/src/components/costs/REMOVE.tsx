import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { DataTablePagination } from '@/components/ui/data-table-pagination';
import { DateRangeSelector } from '@/components/shared/date-range-selector';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchTopCostRoutes } from '@/store/slices/costSlice';
import { LoadingState } from '@/components/shared/loading-state';
import { ErrorState } from '@/components/shared/error-state';

export function TopCostRoutes() {
  const dispatch = useAppDispatch();
  const { data, total, loading, error } = useAppSelector((state) => state.costs.topRoutes);
  
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [sortBy, setSortBy] = useState('total_cost');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [search, setSearch] = useState('');

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
      key: 'total_cost' as const,
      title: 'Total Cost',
      sortable: true,
      className: 'text-right',
      render: (value: number) => `$${value.toLocaleString()}`,
    },
    {
      key: 'shipment_count' as const,
      title: 'Shipments',
      sortable: true,
      className: 'text-right',
      render: (value: number) => value.toLocaleString(),
    },
    {
      key: 'avg_cost' as const,
      title: 'Avg Cost',
      sortable: true,
      className: 'text-right',
      render: (value: number) => `$${value.toLocaleString()}`,
    },
  ];

  const fetchData = (params: {
    start: string;
    end: string;
    page: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    search?: string;
  }) => {
    if (params.start && params.end) {
      dispatch(fetchTopCostRoutes({
        ...params,
        pageSize
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
          <CardTitle>Top Cost Routes</CardTitle>
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
            total={total}
            currentPage={page}
            pageSize={pageSize}
            sortKey={sortBy}
            sortOrder={sortOrder}
            searchable
            onPageChange={handlePageChange}
            onSort={handleSort}
            onSearch={handleSearch}
          />
        )}
      </CardContent>
    </Card>
  );
}