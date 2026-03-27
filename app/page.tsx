import { DashboardLayout } from "@/components/dashboard-layout"
import { KPICards } from "@/components/dashboard/kpi-cards"
import { PulseBar } from "@/components/dashboard/pulse-bar"
import { IntelligenceFeed } from "@/components/dashboard/intelligence-feed"
import { ImpactAnalysis } from "@/components/dashboard/impact-analysis"
import { PolicyDiff } from "@/components/dashboard/policy-diff"

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground">
              Dashboard
            </h1>
            <p className="text-sm text-muted-foreground">
              Real-time regulatory intelligence and compliance monitoring
            </p>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-success animate-pulse" />
            All systems operational
          </div>
        </div>

        {/* KPI Cards */}
        <KPICards />

        {/* Current Pulse Bar */}
        <PulseBar />

        {/* Main Content Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Intelligence Feed - Left Panel */}
          <div className="lg:col-span-1">
            <IntelligenceFeed />
          </div>

          {/* Center & Right Panels */}
          <div className="lg:col-span-2 space-y-6">
            {/* Impact Analysis */}
            <ImpactAnalysis />

            {/* Policy Diff Viewer */}
            <PolicyDiff />
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
