"use client"

import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { VehicleAnalytics } from '@/components/vehicles/vehicle-analytics'
import React from 'react'

const Vehicles = () => {
  return (
    <DashboardLayout>
      <VehicleAnalytics />
    </DashboardLayout>
  )
}

export default Vehicles