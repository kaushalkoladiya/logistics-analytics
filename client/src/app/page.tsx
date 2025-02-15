import { DashboardOverview } from "@/components/dashboard/overview";
import { DashboardLayout } from "@/components/layout/dashboard-layout";

export default function Home() {
  return (
    <div>
      <DashboardLayout>
        <DashboardOverview />  
      </DashboardLayout>      
    </div>
  );
}
