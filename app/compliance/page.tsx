 "use client"
import { useEffect, useState } from "react"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Card, CardContent } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { apiGet } from "@/lib/api"

interface ComplianceItem {
  regulation_id: string
  title: string
  risk: string
  open_gaps: number
  last_updated: string
}

export default function CompliancePage() {
  const [items, setItems] = useState<ComplianceItem[]>([])

  useEffect(() => {
    const load = async () => {
      try {
        const data = await apiGet<{ items: ComplianceItem[] }>("/api/compliance")
        setItems(data.items || [])
      } catch {
        setItems([])
      }
    }
    load()
  }, [])

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Compliance Register</h1>
          <p className="text-sm text-muted-foreground">No predefined rows. Records come from backend pipeline.</p>
        </div>

        <Card className="border-border/50 bg-card/50 overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent border-border/50">
                <TableHead className="w-[160px]">Regulation ID</TableHead>
                <TableHead>Regulation</TableHead>
                <TableHead>Risk Level</TableHead>
                <TableHead>Open Gaps</TableHead>
                <TableHead>Last Updated</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                    No compliance entries yet. Trigger analysis to generate records.
                  </TableCell>
                </TableRow>
              )}
              {items.map((item) => (
                <TableRow key={item.regulation_id} className="hover:bg-accent/30 border-border/50 transition-colors">
                  <TableCell className="font-mono text-sm text-muted-foreground">{item.regulation_id}</TableCell>
                  <TableCell className="font-medium text-foreground">{item.title}</TableCell>
                  <TableCell>{item.risk}</TableCell>
                  <TableCell>{item.open_gaps}</TableCell>
                  <TableCell>{item.last_updated}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      </div>
    </DashboardLayout>
  )
}
