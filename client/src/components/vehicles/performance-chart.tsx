import { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import type { DailyPerformance } from '@/types/vehicles';

interface PerformanceChartProps {
  data: DailyPerformance[];
}

export function PerformanceChart({ data }: PerformanceChartProps) {
  const [metrics] = useState([
    { key: 'daily_revenue', name: 'Revenue', color: '#10B981' },
    { key: 'daily_mileage', name: 'Mileage', color: '#3B82F6' },
    { key: 'daily_deliveries', name: 'Deliveries', color: '#8B5CF6' }
  ]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Daily Performance</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(date) => new Date(date).toLocaleDateString()}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(date) => new Date(date).toLocaleDateString()}
              />
              <Legend />
              {metrics.map(({ key, name, color }) => (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={key}
                  stroke={color}
                  name={name}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}