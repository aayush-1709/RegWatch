"use client"

import { useEffect, useState } from "react"
import { Radio, Clock, AlertCircle, Zap } from "lucide-react"
import { apiGet } from "@/lib/api"

export function PulseBar() {
  const [lastUpdate, setLastUpdate] = useState("-")
  const [critical, setCritical] = useState(0)
  const [events, setEvents] = useState(0)

  useEffect(() => {
    const load = async () => {
      try {
        const [compliance, logs] = await Promise.all([
          apiGet<{ items: Array<{ risk?: string }> }>("/api/compliance"),
          apiGet<{ items: Array<unknown> }>("/api/audit-logs"),
        ])
        setCritical(compliance.items.filter((x) => (x.risk || "").toUpperCase() === "HIGH").length)
        setEvents(logs.items.length)
        setLastUpdate(new Date().toLocaleTimeString())
      } catch {
        setCritical(0)
        setEvents(0)
        setLastUpdate("-")
      }
    }
    load()
  }, [])

  return (
    <div className="rounded-xl border border-border/50 bg-gradient-to-r from-card via-card to-accent/10 p-4">
      <div className="flex flex-wrap items-center justify-between gap-4">
        {/* Real-time Status */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 animate-ping rounded-full bg-success/30" />
            <div className="relative flex h-10 w-10 items-center justify-center rounded-full bg-success/10 ring-2 ring-success/20">
              <Radio className="h-5 w-5 text-success" />
            </div>
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground">Real-time Monitoring</p>
            <div className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-success animate-pulse" />
              <span className="text-xs font-medium text-success">Active</span>
            </div>
          </div>
        </div>

        <div className="h-8 w-px bg-border/50 hidden sm:block" />

        {/* Last Update */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 ring-2 ring-primary/20">
            <Clock className="h-5 w-5 text-primary" />
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground">Last Update</p>
            <p className="text-xs text-muted-foreground">{lastUpdate}</p>
          </div>
        </div>

        <div className="h-8 w-px bg-border/50 hidden sm:block" />

        {/* Critical Alerts */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 animate-pulse rounded-full bg-risk-high/20" />
            <div className="relative flex h-10 w-10 items-center justify-center rounded-full bg-risk-high/10 ring-2 ring-risk-high/20">
              <AlertCircle className="h-5 w-5 text-risk-high" />
            </div>
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground">Critical Alerts</p>
            <p className="text-xs font-bold text-risk-high">{critical} Require Attention</p>
          </div>
        </div>

        <div className="h-8 w-px bg-border/50 hidden sm:block" />

        {/* AI Processing */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-info/10 ring-2 ring-info/20">
            <Zap className="h-5 w-5 text-info" />
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground">AI Processing</p>
            <p className="text-xs text-muted-foreground">{events} agent events</p>
          </div>
        </div>
      </div>
    </div>
  )
}
