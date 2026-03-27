"use client"

import { useEffect, useState } from "react"
import { ExternalLink } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"
import { apiGet } from "@/lib/api"

interface RegulationItem {
  id: string
  title: string
  source: string
  detected_at: string
}

function getSourceColor(source: string): string {
  switch (source) {
    case "RBI":
      return "bg-blue-500/10 text-blue-500 border-blue-500/20"
    case "SEBI":
      return "bg-purple-500/10 text-purple-500 border-purple-500/20"
    case "GST":
      return "bg-amber-500/10 text-amber-500 border-amber-500/20"
    case "IRDAI":
      return "bg-emerald-500/10 text-emerald-500 border-emerald-500/20"
    default:
      return "bg-muted text-muted-foreground"
  }
}

export function IntelligenceFeed() {
  const [items, setItems] = useState<RegulationItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const data = await apiGet<{ items: Array<{ id: string; title: string; metadata: { source: string; detected_at: string } }> }>("/api/regulations")
        setItems(
          data.items.map((item) => ({
            id: item.id,
            title: item.title,
            source: item.metadata?.source || "Unknown",
            detected_at: item.metadata?.detected_at || "",
          }))
        )
      } catch {
        setItems([])
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <Card className="border-border/50 bg-card/50 backdrop-blur-sm h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">Intelligence Feed</CardTitle>
          <Badge variant="outline" className="gap-1 text-xs">
            {loading ? "Loading..." : `${items.length} items`}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[400px] px-6 pb-6">
          <div className="space-y-3">
            {!loading && items.length === 0 && (
              <div className="rounded-lg border border-dashed border-border/60 p-6 text-sm text-muted-foreground">
                No regulations yet. Run analysis from the UI to populate feed.
              </div>
            )}
            {items.map((item) => (
                <div
                  key={item.id}
                  className="group cursor-pointer rounded-lg border border-border/50 bg-background/50 p-4 transition-all duration-200 hover:border-primary/30 hover:bg-accent/30 hover:shadow-md"
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <h4 className="font-semibold text-sm text-foreground group-hover:text-primary transition-colors line-clamp-1">
                      {item.title}
                    </h4>
                    <ExternalLink className="h-4 w-4 shrink-0 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className={cn("text-[10px] px-2 py-0.5", getSourceColor(item.source))}>
                        {item.source}
                      </Badge>
                    </div>
                    <div className="text-[10px] text-muted-foreground">
                      {item.detected_at ? new Date(item.detected_at).toLocaleString() : "-"}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
