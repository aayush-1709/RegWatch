import { DashboardLayout } from "@/components/dashboard-layout"
import { IntelligenceFeed } from "@/components/dashboard/intelligence-feed"

export default function IntelligencePage() {
  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Intelligence Feed</h1>
          <p className="text-sm text-muted-foreground">No predefined data. Feed is populated from backend only.</p>
        </div>
        <IntelligenceFeed />
      </div>
    </DashboardLayout>
  )
}
