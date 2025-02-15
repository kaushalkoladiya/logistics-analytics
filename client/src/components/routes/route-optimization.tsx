import { useAppDispatch, useAppSelector } from "@/store";
import { Badge } from "../ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { shallowEqual } from "react-redux";
import { LoadingState } from "../shared/loading-state";
import { ErrorState } from "../shared/error-state";
import { DateRangeSelector } from "../shared/date-range-selector";
import { DataTablePagination } from "../ui/data-table-pagination";
import { fetchRouteOptimization } from "@/store/slices/routeSlice";
import { useState } from "react";

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
    key: 'total_shipments' as const,
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
  {
    key: 'cost_time_efficiency' as const,
    title: 'Efficiency Score',
    sortable: true,
    className: 'text-right',
  },
  {
    key: 'optimization_recommendation' as const,
    title: 'Recommendation',
    render: (value: string) => (
      <div className="max-w-md text-sm">
        <Badge
          variant={
            value.includes('High delivery time')
              ? "destructive"
              : value.includes('High cost')
                ? "warning"
                : "success"
          }
        >
          {value}
        </Badge>
      </div>
    ),
  },
];

export function RouteOptimizationTable() {
  const dispatch = useAppDispatch();
  const { data, loading, error, total } = useAppSelector((state) => state.route.optimization, shallowEqual);

  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [sortBy, setSortBy] = useState('total_shipments');
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
      dispatch(fetchRouteOptimization({
        ...params
      }));
    }
  };

  const handleDateRangeChange = (range: { start: string; end: string }) => {
    setDateRange(range);
    fetchData({ ...range, page: 1 });
  };

  const handleSort = (key: string, order: "asc" | "desc") => {
    setSortBy(key);
    setSortOrder(order);
    fetchData({
      ...dateRange,
      page: 1,
      sortBy: key,
      sortOrder: order,
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
          <CardTitle>Route Optimization Opportunities</CardTitle>
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
            data={data || []}
            total={total || 0}
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