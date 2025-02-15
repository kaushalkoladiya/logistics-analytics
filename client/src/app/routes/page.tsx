import { DashboardLayout } from '@/components/layout/dashboard-layout'
import RouteAnalytics from '@/components/routes/route-analytics'
import React from 'react'

const RoutesPage = () => {
  return (
    <DashboardLayout>
      <RouteAnalytics />
    </DashboardLayout>
  )
}

export default RoutesPage