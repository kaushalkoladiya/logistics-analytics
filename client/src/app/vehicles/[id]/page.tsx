'use client';

import { DashboardLayout } from '@/components/layout/dashboard-layout';
import VehicleDetails from '@/components/vehicles/vehicle-details';
import React from 'react';

export default function VehicleDetailPage() {
  return (
    <DashboardLayout>
      <VehicleDetails />
    </DashboardLayout>
  );
}