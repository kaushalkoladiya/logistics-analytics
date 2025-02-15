import { DataTable } from '@/components/ui/data-table';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import type { RoutePerformance } from '@/types/vehicles';

interface TopRoutesProps {
  routes: RoutePerformance[];
}

export function TopRoutes({ routes }: TopRoutesProps) {
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
      key: 'route_trips' as const,
      title: 'Trips',
      sortable: true,
      className: 'text-right',
      render: (value: number) => value.toLocaleString(),
    },
    {
      key: 'avg_route_time' as const,
      title: 'Avg Time',
      sortable: true,
      className: 'text-right',
      render: (value: number) => `${value.toFixed(1)}h`,
    },
    {
      key: 'avg_route_revenue' as const,
      title: 'Avg Revenue',
      sortable: true,
      className: 'text-right',
      render: (value: number) => `$${value.toLocaleString()}`,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Routes</CardTitle>
      </CardHeader>
      <CardContent>
        <DataTable
          columns={columns}
          data={routes}
          searchable
          searchKey="origin"
        />
      </CardContent>
    </Card>
  );
}