import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { DataTable } from '@/components/ui/data-table';
import type { ExpensiveRoute } from '@/types/shipments';

interface ExpensiveRoutesTableProps {
  data: ExpensiveRoute[];
}

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
    key: 'avg_cost_per_shipment' as const,
    title: 'Avg Cost',
    sortable: true,
    className: 'text-right',
    render: (value: number) => `$${value.toLocaleString()}`,
  },
  {
    key: 'avg_delivery_time' as const,
    title: 'Avg Time',
    sortable: true,
    className: 'text-right',
    render: (value: number) => `${value.toFixed(1)}h`,
  },
];

export function ExpensiveRoutesTable({ data }: ExpensiveRoutesTableProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Top 5 Most Expensive Routes</CardTitle>
      </CardHeader>
      <CardContent>
        <DataTable
          columns={columns}
          data={data}
          searchable
          searchKey="origin"
        />
      </CardContent>
    </Card>
  );
}