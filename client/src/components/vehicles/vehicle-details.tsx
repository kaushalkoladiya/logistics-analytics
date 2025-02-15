"use client";

import React, { useEffect } from 'react'
import { LoadingState } from '../shared/loading-state';
import { ErrorState } from '../shared/error-state';
import { DateRangeSelector } from '../shared/date-range-selector';
import { VehicleSummary } from './vehicle-summary';
import { PerformanceChart } from './performance-chart';
import { TopRoutes } from './top-routes';
import { clearVehicleDetails, fetchVehicleDetails } from '@/store/slices/vehicleSlice';
import { useAppDispatch, useAppSelector } from '@/store';
import { useParams } from 'next/navigation';
import { shallowEqual } from 'react-redux';

const VehicleDetails = () => {
  const { id } = useParams();
  const dispatch = useAppDispatch();
  const { data: detail, error, loading } = useAppSelector((state) => state.vehicles.detail, shallowEqual);

  useEffect(() => {
    if (id) {
      const end = new Date();
      const start = new Date();
      start.setMonth(start.getMonth() - 1);

      dispatch(
        fetchVehicleDetails({
          id: id as string,
          start: start.toISOString().split('T')[0],
          end: end.toISOString().split('T')[0]
        })
      );
    }

    return () => {
      dispatch(clearVehicleDetails());
    };
  }, [id, dispatch]);

  const handleDateRangeChange = (range: { start: string; end: string }) => {
    if (id) {
      dispatch(fetchVehicleDetails({ id: id as string, ...range }));
    } else {
      console.log("No vehicle id found");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">{detail?.summary?.name || ''}</h1>
        <DateRangeSelector onDateRangeChange={handleDateRangeChange} />
      </div>

      {loading ? <LoadingState /> :
        error ? <ErrorState message={error} /> :
          detail ? (
            <>
              <VehicleSummary summary={detail.summary} />
              <PerformanceChart data={detail.daily_performance} />
              <TopRoutes routes={detail.top_routes} />
            </>
          ) : null}
    </div>
  );
}

export default VehicleDetails