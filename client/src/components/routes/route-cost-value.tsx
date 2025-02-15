import { useAppDispatch, useAppSelector } from "@/store";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { shallowEqual } from "react-redux";
import { Badge } from "../ui/badge";
import { LoadingState } from "../shared/loading-state";
import { ErrorState } from "../shared/error-state";
import { fetchRouteCostValue } from "@/store/slices/routeSlice";
import { useState } from "react";
import { DataTablePagination } from "../ui/data-table-pagination";
import { DateRangeSelector } from "../shared/date-range-selector";

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
    key: 'cost_per_kg' as const,
    title: 'Cost/kg',
    sortable: true,
    className: 'text-right'
  },
  {
    key: 'value_category' as const,
    title: 'Value Category',
    sortable: true,
    render: (value: string) => (
      <Badge
        variant={
          value === 'High Value'
            ? "success"
            : value === 'Medium Value'
              ? "warning"
              : "destructive"
        }
      >
        {value}
      </Badge>
    ),
  },
];

export function RouteCostValueTable() {
  const dispatch = useAppDispatch();
  const { data, loading, error, total } = useAppSelector((state) => state.route.costValue, shallowEqual);

  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [sortBy, setSortBy] = useState('value_score');
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
      dispatch(fetchRouteCostValue({
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
          <CardTitle>Route Cost-Value Analysis</CardTitle>
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