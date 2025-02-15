import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  trend?: number;
  icon?: React.ReactNode;
}

export function MetricCard({ title, value, trend, icon }: MetricCardProps) {
  const isTrendPositive = trend && trend > 0;

  return (
    <Card className="transition-all hover:shadow-md">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-slate-700">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-slate-700">{value}</div>
        {trend ? (
          <div className="mt-2 flex items-center text-xs">
            {isTrendPositive ? (
              <TrendingUp className="mr-1 h-4 w-4 text-emerald-500" />
            ) : (
              <TrendingDown className="mr-1 h-4 w-4 text-rose-500" />
            )}
            <span className={isTrendPositive ? 'text-emerald-500' : 'text-rose-500'}>
              {Math.abs(trend)}% from previous
            </span>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}