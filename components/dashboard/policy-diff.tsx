"use client"

import { useEffect, useMemo, useState } from "react"
import { Check, X, Edit3, GitCompare } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { apiGet } from "@/lib/api"

interface DiffLine {
  type: "added" | "removed" | "unchanged"
  content: string
  lineNumber: number
}

export function PolicyDiff() {
  const [diff, setDiff] = useState<{ additions: string[]; removals: string[] }>({ additions: [], removals: [] })

  useEffect(() => {
    const load = async () => {
      try {
        const data = await apiGet<{
          item?: { diff?: { additions?: string[]; removals?: string[]; added_lines?: string[]; removed_lines?: string[] } }
        }>("/api/analyze/latest")
      setDiff({
          additions: data.item?.diff?.additions || data.item?.diff?.added_lines || [],
          removals: data.item?.diff?.removals || data.item?.diff?.removed_lines || [],
      })
      } catch {
        setDiff({ additions: [], removals: [] })
      }
    }
    load()
  }, [])

  const diffContent = useMemo<DiffLine[]>(() => {
    const lines: DiffLine[] = []
    diff.removals.forEach((line, idx) => lines.push({ type: "removed", content: line, lineNumber: idx + 1 }))
    diff.additions.forEach((line, idx) =>
      lines.push({ type: "added", content: line, lineNumber: diff.removals.length + idx + 1 })
    )
    return lines
  }, [diff])

  return (
    <Card className="border-border/50 bg-card/50 backdrop-blur-sm h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <GitCompare className="h-5 w-5 text-primary" />
            <CardTitle className="text-lg font-semibold">Policy Changes</CardTitle>
          </div>
          <Badge variant="outline" className="text-xs">{diffContent.length} lines</Badge>
        </div>
        <p className="text-sm text-muted-foreground">
          AI-generated diff from latest analysis
        </p>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[300px]">
          <div className="font-mono text-sm px-6 pb-4">
            {diffContent.length === 0 && (
              <div className="rounded-lg border border-dashed border-border/60 p-4 text-sm text-muted-foreground">
                No diff yet. Run analysis from UI input.
              </div>
            )}
            {diffContent.map((line, index) => (
              <div
                key={index}
                className={`flex items-center gap-3 py-1 px-2 rounded ${
                  line.type === "added"
                    ? "bg-success/10 border-l-2 border-success"
                    : line.type === "removed"
                    ? "bg-risk-high/10 border-l-2 border-risk-high"
                    : ""
                }`}
              >
                <span className="w-6 text-right text-xs text-muted-foreground select-none">
                  {line.lineNumber}
                </span>
                <span className="w-4 text-center select-none">
                  {line.type === "added" && (
                    <span className="text-success font-bold">+</span>
                  )}
                  {line.type === "removed" && (
                    <span className="text-risk-high font-bold">-</span>
                  )}
                </span>
                <span
                  className={`flex-1 ${
                    line.type === "added"
                      ? "text-success"
                      : line.type === "removed"
                      ? "text-risk-high line-through opacity-70"
                      : "text-foreground"
                  }`}
                >
                  {line.content || " "}
                </span>
              </div>
            ))}
          </div>
        </ScrollArea>
        
        <div className="border-t border-border/50 p-4 flex items-center gap-2">
          <Button size="sm" className="bg-success hover:bg-success/90 text-white">
            <Check className="h-4 w-4 mr-1.5" />
            Accept
          </Button>
          <Button size="sm" variant="destructive">
            <X className="h-4 w-4 mr-1.5" />
            Reject
          </Button>
          <Button size="sm" variant="outline">
            <Edit3 className="h-4 w-4 mr-1.5" />
            Modify
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
