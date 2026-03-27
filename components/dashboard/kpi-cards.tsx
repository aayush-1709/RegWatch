"use client"

import { useEffect, useMemo, useState } from "react"
import { Activity, AlertTriangle, FileText, Shield, TrendingDown, TrendingUp } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { apiGet } from "@/lib/api"

interface KPICardProps {
  title: string
  value: string
  change: string
  trend: "up" | "down" | "neutral"
  icon: React.ReactNode
  accentColor: string
}

function KPICard({ title, value, change, trend, icon, accentColor }: KPICardProps) {
  return (
    <Card className="relative overflow-hidden border-border/50 bg-card/50 backdrop-blur-sm transition-all duration-300 hover:shadow-lg hover:shadow-primary/5 hover:border-primary/20">
      <div className={cn("absolute inset-x-0 top-0 h-1", accentColor)} />
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="text-3xl font-bold tracking-tight text-foreground">{value}</p>
            <div className="flex items-center gap-1.5">
              {trend === "up" && (
                <TrendingUp className="h-4 w-4 text-success" />
              )}
              {trend === "down" && (
                <TrendingDown className="h-4 w-4 text-risk-high" />
              )}
              <span
                className={cn(
                  "text-sm font-medium",
                  trend === "up" && "text-success",
                  trend === "down" && "text-risk-high",
                  trend === "neutral" && "text-muted-foreground"
                )}
              >
                {change}
              </span>
            </div>
          </div>
          <div className={cn("rounded-xl p-3", accentColor.replace("bg-", "bg-opacity-10 bg-"))}>
            {icon}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export function KPICards() {
  const [regulationsCount, setRegulationsCount] = useState(0)
  const [complianceCount, setComplianceCount] = useState(0)
  const [highRiskCount, setHighRiskCount] = useState(0)

  useEffect(() => {
    const load = async () => {
      try {
        const [regs, comp] = await Promise.all([
          apiGet<{ items: Array<unknown> }>("/api/regulations"),
          apiGet<{ items: Array<{ risk?: string }> }>("/api/compliance"),
        ])
        setRegulationsCount(regs.items.length)
        setComplianceCount(comp.items.length)
        setHighRiskCount(comp.items.filter((x) => (x.risk || "").toUpperCase() === "HIGH").length)
      } catch {
        setRegulationsCount(0)
        setComplianceCount(0)
        setHighRiskCount(0)
      }
    }
    load()
  }, [])

  const kpis = useMemo(
    () => [
    {
      title: "Compliance Score",
      value: complianceCount > 0 ? "Active" : "N/A",
      change: complianceCount > 0 ? `${complianceCount} tracked items` : "No tracked items yet",
      trend: "neutral" as const,
      icon: <Shield className="h-6 w-6 text-success" />,
      accentColor: "bg-success",
    },
    {
      title: "Active Regulations",
      value: String(regulationsCount),
      change: regulationsCount > 0 ? "Fetched from backend" : "No regulations detected",
      trend: "neutral" as const,
      icon: <Activity className="h-6 w-6 text-primary" />,
      accentColor: "bg-primary",
    },
    {
      title: "High Risk Alerts",
      value: String(highRiskCount),
      change: highRiskCount > 0 ? "Requires action" : "No high-risk items",
      trend: highRiskCount > 0 ? ("down" as const) : ("up" as const),
      icon: <AlertTriangle className="h-6 w-6 text-risk-high" />,
      accentColor: "bg-risk-high",
    },
    {
      title: "Total Regulations",
      value: String(regulationsCount),
      change: "Based on live feed",
      trend: "neutral" as const,
      icon: <FileText className="h-6 w-6 text-info" />,
      accentColor: "bg-info",
    },
  ],
    [complianceCount, highRiskCount, regulationsCount]
  )

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {kpis.map((kpi) => (
        <KPICard key={kpi.title} {...kpi} />
      ))}
    </div>
  )
}
