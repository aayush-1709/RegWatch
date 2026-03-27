"use client"

import { useEffect, useState } from "react"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { apiGet } from "@/lib/api"

interface DiffData {
  item?: {
    diff?: {
      additions?: string[]
      removals?: string[]
      added_lines?: string[]
      removed_lines?: string[]
      modified_lines?: string[]
    }
  }
}

export default function DiffPage() {
  const [data, setData] = useState<DiffData["diff"] | null>(null)

  useEffect(() => {
    const load = async () => {
      try {
        const parsed = await apiGet<DiffData>("/api/analyze/latest")
        const next = parsed.item?.diff
        if (!next) {
          setData(null)
          return
        }
        setData({
          additions: next.additions || next.added_lines || [],
          removals: next.removals || next.removed_lines || [],
          modified_lines: next.modified_lines || [],
        })
      } catch {
        setData(null)
      }
    }
    load()
  }, [])

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Policy Diff Viewer</h1>
          <p className="text-sm text-muted-foreground">No predefined diff. Shows backend-generated policy changes only.</p>
        </div>
        {!data && (
          <Card>
            <CardContent className="p-6 text-muted-foreground">No diff data yet. Trigger analysis from UI.</CardContent>
          </Card>
        )}
        {data && (
          <div className="grid gap-6 lg:grid-cols-3">
            <Card>
              <CardHeader><CardTitle>Additions</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {(data.additions || []).length === 0 ? (
                  <p className="text-sm text-muted-foreground">No additions.</p>
                ) : (
                  (data.additions || []).map((line, idx) => <p key={idx} className="text-sm">{line}</p>)
                )}
              </CardContent>
            </Card>
            <Card>
              <CardHeader><CardTitle>Removals</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {(data.removals || []).length === 0 ? (
                  <p className="text-sm text-muted-foreground">No removals.</p>
                ) : (
                  (data.removals || []).map((line, idx) => <p key={idx} className="text-sm">{line}</p>)
                )}
              </CardContent>
            </Card>
            <Card>
              <CardHeader><CardTitle>Modified Lines</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {(data.modified_lines || []).length === 0 ? (
                  <p className="text-sm text-muted-foreground">No modified lines.</p>
                ) : (
                  (data.modified_lines || []).map((line, idx) => <p key={idx} className="text-sm">{line}</p>)
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
