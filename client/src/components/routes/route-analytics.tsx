'use client';

import { TopPerformingRoutes } from './top-performing-routes';
import { RouteReliabilityTable } from './route-reliability';
import { RouteCostValueTable } from './route-cost-value';
import { RouteOptimizationTable } from './route-optimization';

export default function RoutesPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Route Analytics</h1>
      </div>

      <div className="space-y-6">
        <RouteReliabilityTable />
        <RouteCostValueTable />
        <RouteOptimizationTable />
        <TopPerformingRoutes />
      </div>
    </div>
  );
}