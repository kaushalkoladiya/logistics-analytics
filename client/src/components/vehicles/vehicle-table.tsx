'use client';

import { useState, useMemo } from 'react';
import { Search, ArrowUpDown } from 'lucide-react';
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';

interface VehicleMetric {
  vehicle_id: string;
  name: string;
  total_trips: number;
  total_mileage: number;
  total_fuel: number;
  fuel_efficiency: number;
  shipments_delivered: number;
  avg_delivery_time: number;
  total_revenue: number;
  revenue_per_trip: number;
  fuel_per_trip: number;
}

type SortConfig = {
  key: keyof VehicleMetric;
  direction: 'asc' | 'desc';
} | null;

interface VehicleTableProps {
  data: VehicleMetric[];
}

export function VehicleTable({ data }: VehicleTableProps) {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState<SortConfig>(null);

  // Handle sorting
  const handleSort = (key: keyof VehicleMetric) => {
    setSortConfig(current => {
      if (current?.key === key) {
        return {
          key,
          direction: current.direction === 'asc' ? 'desc' : 'asc'
        };
      }
      return { key, direction: 'asc' };
    });
  };

  // Handle row click for drill-down
  const handleRowClick = (vehicleId: string) => {
    router.push(`/vehicles/${vehicleId}`);
  };

  // Filter and sort data
  const filteredAndSortedData = useMemo(() => {
    let processed = [...data];

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      processed = processed.filter(vehicle => 
        vehicle.name.toLowerCase().includes(term) ||
        vehicle.vehicle_id.toLowerCase().includes(term)
      );
    }

    // Apply sorting
    if (sortConfig) {
      processed.sort((a, b) => {
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];
        
        if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return processed;
  }, [data, searchTerm, sortConfig]);

  return (
    <div className="space-y-4">
      {/* Search Input */}
      <div className="flex w-full max-w-sm items-center space-x-2">
        <Search className="h-4 w-4 text-slate-400" />
        <Input
          placeholder="Search vehicles..."
          value={searchTerm}
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          onChange={(e: any) => setSearchTerm(e.target.value)}
          className="max-w-sm"
        />
      </div>

      {/* Table */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <Button 
                  variant="ghost" 
                  onClick={() => handleSort('name')}
                  className="flex items-center gap-1"
                >
                  Vehicle
                  <ArrowUpDown className="h-4 w-4" />
                </Button>
              </TableHead>
              <TableHead className="text-right">
                <Button 
                  variant="ghost" 
                  onClick={() => handleSort('total_trips')}
                  className="flex items-center gap-1"
                >
                  Total Trips
                  <ArrowUpDown className="h-4 w-4" />
                </Button>
              </TableHead>
              <TableHead className="text-right">
                <Button 
                  variant="ghost" 
                  onClick={() => handleSort('total_mileage')}
                  className="flex items-center gap-1"
                >
                  Mileage
                  <ArrowUpDown className="h-4 w-4" />
                </Button>
              </TableHead>
              <TableHead className="text-right">
                <Button 
                  variant="ghost" 
                  onClick={() => handleSort('fuel_efficiency')}
                  className="flex items-center gap-1"
                >
                  Fuel Efficiency
                  <ArrowUpDown className="h-4 w-4" />
                </Button>
              </TableHead>
              <TableHead className="text-right">
                <Button 
                  variant="ghost" 
                  onClick={() => handleSort('revenue_per_trip')}
                  className="flex items-center gap-1"
                >
                  Revenue/Trip
                  <ArrowUpDown className="h-4 w-4" />
                </Button>
              </TableHead>
              <TableHead className="text-right">
                <Button 
                  variant="ghost" 
                  onClick={() => handleSort('shipments_delivered')}
                  className="flex items-center gap-1"
                >
                  Deliveries
                  <ArrowUpDown className="h-4 w-4" />
                </Button>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredAndSortedData.map((vehicle) => (
              <TableRow 
                key={vehicle.vehicle_id}
                className="cursor-pointer hover:bg-slate-50"
                onClick={() => handleRowClick(vehicle.vehicle_id)}
              >
                <TableCell className="font-medium">{vehicle.name}</TableCell>
                <TableCell className="text-right">{vehicle.total_trips}</TableCell>
                <TableCell className="text-right">
                  {vehicle.total_mileage.toLocaleString()} km
                </TableCell>
                <TableCell className="text-right">
                  {vehicle.fuel_efficiency.toFixed(2)} km/l
                </TableCell>
                <TableCell className="text-right">
                  ${vehicle.revenue_per_trip.toLocaleString()}
                </TableCell>
                <TableCell className="text-right">
                  {vehicle.shipments_delivered}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}