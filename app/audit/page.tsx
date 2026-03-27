 "use client"
import { useEffect, useState } from "react"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { RefreshCw } from "lucide-react"
import { apiGet } from "@/lib/api"

interface AuditLog {
  agent_name: string
  action: string
  timestamp: string
  confidence_score: number
}

export default function AuditPage() {
  const [items, setItems] = useState<AuditLog[]>([])

  const load = async () => {
    try {
      const data = await apiGet<{ items: AuditLog[] }>("/api/audit-logs")
      setItems(data.items || [])
    } catch {
      setItems([])
    }
  }

  useEffect(() => {
    load()
  }, [])

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground">
              Audit Logs
            </h1>
            <p className="text-sm text-muted-foreground">
              No predefined log rows. Data is read from backend audit pipeline.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" onClick={load}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
        </div>

        {/* Logs Table */}
        <Card className="border-border/50 bg-card/50 overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent border-border/50">
                <TableHead className="w-[180px]">Timestamp</TableHead>
                <TableHead className="w-[200px]">Agent</TableHead>
                <TableHead>Action</TableHead>
                <TableHead className="w-[140px] text-center">Confidence</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
                    No logs yet. Run an analysis to generate audit trail.
                  </TableCell>
                </TableRow>
              )}
              {items.map((log, idx) => (
                <TableRow
                  key={`${log.agent_name}-${idx}`}
                  className="cursor-pointer hover:bg-accent/30 border-border/50 transition-colors"
                >
                  <TableCell className="font-mono text-xs text-muted-foreground">
                    {new Date(log.timestamp).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <span className="text-sm font-medium text-foreground">{log.agent_name}</span>
                  </TableCell>
                  <TableCell>
                    <p className="text-sm font-medium text-foreground">{log.action}</p>
                  </TableCell>
                  <TableCell className="text-center">{Math.round(log.confidence_score * 100)}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      </div>
    </DashboardLayout>
  )
}
