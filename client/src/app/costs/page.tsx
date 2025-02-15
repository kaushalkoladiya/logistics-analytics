import CostsAnalytics from '@/components/costs/costs-analytics'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import React from 'react'

const CostsPage = () => {
  return (
    <DashboardLayout>
      <CostsAnalytics />
    </DashboardLayout>
  )
}

export default CostsPage