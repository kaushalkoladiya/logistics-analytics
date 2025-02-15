import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import type { TopCostRoute } from '@/types/costs';
import { DataTable } from '../ui/data-table';

interface TopCostRoutesProps {
  routes: TopCostRoute[];
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

export function TopCostRoutes({ routes }: TopCostRoutesProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Top 5 Cost Routes</CardTitle>
      </CardHeader>
      <CardContent>
        <DataTable
          columns={columns}
          data={routes}
          searchKey='origin'
          searchable
        />
      </CardContent>
    </Card>
  );
}