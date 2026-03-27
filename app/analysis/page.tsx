"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { apiPost } from "@/lib/api"

interface AnalysisData {
  title: string
  summary: string
  risk: string
  timeline: string[]
  gaps: Array<{ clause: string; gap: string; severity: string }>
  actions: Array<{ step: string; team: string; deadline: string }>
  diff?: { additions?: string[]; removals?: string[]; modified_lines?: string[] }
}

export default function AnalysisPage() {
  const [regulationText, setRegulationText] = useState("")
  const [policyText, setPolicyText] = useState("")
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<AnalysisData | null>(null)

  const runAnalysis = async () => {
    setLoading(true)
    try {
      const result = await apiPost<AnalysisData>("/api/analyze", {
        regulation_text: regulationText || undefined,
        company_policy_text: policyText || undefined,
      })
      setData(result)
      localStorage.setItem("regwatch:lastAnalysis", JSON.stringify(result))
    } finally {
      setLoading(false)
    }
  }

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Regulation Analysis</h1>
          <p className="text-sm text-muted-foreground">Clean input-first flow. No predefined UI data.</p>
        </div>

        <Card>
          <CardHeader><CardTitle>Input</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder="Paste regulation text..."
              value={regulationText}
              onChange={(e) => setRegulationText(e.target.value)}
              className="min-h-28"
            />
            <Textarea
              placeholder="Paste company policy text..."
              value={policyText}
              onChange={(e) => setPolicyText(e.target.value)}
              className="min-h-28"
            />
            <Button onClick={runAnalysis} disabled={loading}>
              {loading ? "Running..." : "Run Analysis"}
            </Button>
          </CardContent>
        </Card>

        {!data && (
          <Card>
            <CardContent className="p-6 text-muted-foreground">
              Submit input to generate analysis.
            </CardContent>
          </Card>
        )}

        {data && (
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader><CardTitle>{data.title}</CardTitle></CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground">{data.summary}</p>
                <p className="text-sm"><span className="font-semibold">Risk:</span> {data.risk}</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader><CardTitle>Timeline</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {data.timeline.map((item, idx) => <p key={idx} className="text-sm">{item}</p>)}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
