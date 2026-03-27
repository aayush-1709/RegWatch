"use client"

import { useEffect, useState } from "react"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { apiGet } from "@/lib/api"

interface SourceUpdate {
  source: string
  last_seen: string | null
  latest_title: string
  published: string | null
  url: string | null
}

export default function UpdatesPage() {
  const [items, setItems] = useState<SourceUpdate[]>([])
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const data = await apiGet<{ items: SourceUpdate[] }>("/api/regulations/last-updates")
      setItems(data.items || [])
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground">Regulator Last Updates</h1>
            <p className="text-sm text-muted-foreground">
              Latest RBI, SEBI, and GST updates with last refresh timestamps.
            </p>
          </div>
          <Button variant="outline" onClick={load} disabled={loading}>
            {loading ? "Refreshing..." : "Refresh"}
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {items.map((item) => (
            <Card key={item.source} className="border-border/50 bg-card/50">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>{item.source}</CardTitle>
                  <Badge variant="outline">Live</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-xs text-muted-foreground">Last Seen</p>
                  <p className="text-sm font-medium">
                    {item.last_seen ? new Date(item.last_seen).toLocaleString() : "Not available"}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Published</p>
                  <p className="text-sm">{item.published || "Not available"}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Latest Update</p>
                  <p className="text-sm line-clamp-3">{item.latest_title}</p>
                </div>
                {item.url && (
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sm text-primary underline underline-offset-2"
                  >
                    Open source link
                  </a>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </DashboardLayout>
  )
}
