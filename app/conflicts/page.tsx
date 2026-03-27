"use client"

import { useEffect, useMemo, useState } from "react"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface GapItem {
  clause: string
  gap: string
  severity: string
}

export default function ConflictMapPage() {
  const [gaps, setGaps] = useState<GapItem[]>([])

  useEffect(() => {
    try {
      const raw = localStorage.getItem("regwatch:lastAnalysis")
      if (!raw) {
        setGaps([])
        return
      }
      const parsed = JSON.parse(raw) as { gaps?: GapItem[] }
      setGaps(parsed.gaps || [])
    } catch {
      setGaps([])
    }
  }, [])

  const grouped = useMemo(() => {
    return {
      HIGH: gaps.filter((g) => g.severity.toUpperCase() === "HIGH"),
      MEDIUM: gaps.filter((g) => g.severity.toUpperCase() === "MEDIUM"),
      LOW: gaps.filter((g) => g.severity.toUpperCase() === "LOW"),
    }
  }, [gaps])

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Conflict Map</h1>
          <p className="text-sm text-muted-foreground">No mock conflict graph. Conflicts are derived from real compliance gaps.</p>
        </div>
        {gaps.length === 0 ? (
          <Card>
            <CardContent className="p-6 text-muted-foreground">
              No conflicts yet. Run analysis to generate gap-based conflict signals.
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6 lg:grid-cols-3">
            <Card>
              <CardHeader><CardTitle>High Severity</CardTitle></CardHeader>
              <CardContent className="space-y-3">{grouped.HIGH.map((g, i) => <p key={i} className="text-sm">{g.gap}</p>)}</CardContent>
            </Card>
            <Card>
              <CardHeader><CardTitle>Medium Severity</CardTitle></CardHeader>
              <CardContent className="space-y-3">{grouped.MEDIUM.map((g, i) => <p key={i} className="text-sm">{g.gap}</p>)}</CardContent>
            </Card>
            <Card>
              <CardHeader><CardTitle>Low Severity</CardTitle></CardHeader>
              <CardContent className="space-y-3">{grouped.LOW.map((g, i) => <p key={i} className="text-sm">{g.gap}</p>)}</CardContent>
            </Card>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
