"use client"

import { useEffect, useState } from "react"
import { TrendingDown, TrendingUp } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function ImpactAnalysis() {
  const [inactionCost, setInactionCost] = useState("-")
  const [complianceCost, setComplianceCost] = useState("-")

  useEffect(() => {
    try {
      const raw = localStorage.getItem("regwatch:lastAnalysis")
      if (!raw) {
        setInactionCost("-")
        setComplianceCost("-")
        return
      }
      const data = JSON.parse(raw) as { impact?: { cost_of_inaction?: string; cost_of_compliance?: string } }
      setInactionCost(data.impact?.cost_of_inaction || "-")
      setComplianceCost(data.impact?.cost_of_compliance || "-")
    } catch {
      setInactionCost("-")
      setComplianceCost("-")
    }
  }, [])

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {/* Cost of Inaction */}
      <Card className="relative overflow-hidden border-risk-high/30 bg-gradient-to-br from-risk-high/5 to-risk-high/10">
        <div className="absolute inset-x-0 top-0 h-1 bg-risk-high" />
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-risk-high/10">
              <TrendingDown className="h-5 w-5 text-risk-high" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-foreground">Cost of Inaction</CardTitle>
              <p className="text-xs text-muted-foreground">Projected impact if non-compliant</p>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="rounded-lg bg-background/50 p-4">
            <p className="text-sm text-muted-foreground mb-1">Total Potential Impact</p>
            <p className="text-3xl font-bold text-risk-high">{inactionCost}</p>
          </div>
        </CardContent>
      </Card>

      {/* Cost of Action */}
      <Card className="relative overflow-hidden border-success/30 bg-gradient-to-br from-success/5 to-success/10">
        <div className="absolute inset-x-0 top-0 h-1 bg-success" />
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-success/10">
              <TrendingUp className="h-5 w-5 text-success" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-foreground">Cost of Action</CardTitle>
              <p className="text-xs text-muted-foreground">Investment for full compliance</p>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="rounded-lg bg-background/50 p-4">
            <p className="text-sm text-muted-foreground mb-1">Total Investment Required</p>
            <p className="text-3xl font-bold text-success">{complianceCost}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
