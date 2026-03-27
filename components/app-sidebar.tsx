"use client"

import Link from "next/link"
import Image from "next/image"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  Radio,
  FileSearch,
  GitCompare,
  ClipboardList,
  Network,
  ScrollText,
  Sparkles,
} from "lucide-react"
import { cn } from "@/lib/utils"
import logoImage from "@/logo.png"
import nameImage from "@/name.png"

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Intelligence Feed", href: "/intelligence", icon: Radio },
  { name: "Regulation Analysis", href: "/analysis", icon: FileSearch },
  { name: "Policy Diff Viewer", href: "/diff", icon: GitCompare },
  { name: "Compliance Register", href: "/compliance", icon: ClipboardList },
  { name: "Conflict Map", href: "/conflicts", icon: Network },
  { name: "Audit Logs", href: "/audit", icon: ScrollText },
]

export function AppSidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-sidebar-border bg-sidebar">
      {/* Logo Section */}
      <div className="flex h-16 items-center gap-3 border-b border-sidebar-border px-6">
        <div className="flex h-9 w-9 items-center justify-center overflow-hidden rounded-lg bg-white/10 shadow-lg">
          <Image
            src={logoImage}
            alt="RegWatch logo"
            className="h-full w-full object-contain p-1"
            priority
          />
        </div>
        <div className="flex min-w-0 flex-1 items-center">
          <Image
            src={nameImage}
            alt="RegWatch"
            className="h-7 w-auto max-w-[140px] object-contain"
            priority
          />
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        <div className="mb-2 px-3">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
            Main Menu
          </span>
        </div>
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-sidebar-accent text-sidebar-primary shadow-sm"
                  : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
              )}
            >
              <item.icon
                className={cn(
                  "h-4.5 w-4.5 shrink-0 transition-colors",
                  isActive
                    ? "text-sidebar-primary"
                    : "text-muted-foreground group-hover:text-sidebar-foreground"
                )}
              />
              {item.name}
              {isActive && (
                <Sparkles className="ml-auto h-3 w-3 text-sidebar-primary animate-pulse" />
              )}
            </Link>
          )
        })}
      </nav>

      {/* Bottom Section */}
      <div className="border-t border-sidebar-border p-4">
        <div className="rounded-lg bg-gradient-to-br from-primary/10 to-info/10 p-4">
          <div className="flex items-center gap-2 mb-2">
            <div className="h-2 w-2 rounded-full bg-success animate-pulse" />
            <span className="text-xs font-medium text-foreground">AI Engine Active</span>
          </div>
          <p className="text-[11px] text-muted-foreground leading-relaxed">
            Real-time monitoring across 50+ regulatory sources
          </p>
        </div>
      </div>
    </aside>
  )
}
