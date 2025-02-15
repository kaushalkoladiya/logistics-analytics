"use client";

import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { ShipmentAnalytics } from '@/components/shipments/shipment-analytics';
import React from 'react'

const ShipmentsPage = () => {
  return (
    <DashboardLayout>
      <ShipmentAnalytics />
    </DashboardLayout>
  )
}

export default ShipmentsPage