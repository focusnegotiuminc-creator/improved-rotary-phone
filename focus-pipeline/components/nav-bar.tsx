"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/cn";
import { LayoutDashboard, Settings, Terminal, ShieldCheck, ActivitySquare } from "lucide-react";

const LINKS = [
  { href: "/", label: "Pipeline", icon: LayoutDashboard },
  { href: "/operator", label: "Operator", icon: Settings },
  { href: "/private-console", label: "Private Console", icon: ShieldCheck },
];

export function NavBar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-[var(--border)] bg-[var(--background)]/90 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-screen-xl items-center justify-between px-4 md:px-6">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5">
          <span className="flex h-7 w-7 items-center justify-center rounded-md bg-[var(--gold-dim)] border border-[var(--border-gold)]">
            <ActivitySquare className="h-4 w-4 text-[var(--gold)]" />
          </span>
          <span className="font-serif text-lg font-semibold tracking-tight text-foreground">
            FOCUS <span className="text-[var(--gold)]">MASTER AI</span>
          </span>
        </Link>

        {/* Nav links */}
        <nav className="flex items-center gap-1">
          {LINKS.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors",
                pathname === href
                  ? "bg-[var(--surface-elevated)] text-[var(--gold)]"
                  : "text-[var(--muted)] hover:text-foreground hover:bg-[var(--surface)]"
              )}
            >
              <Icon className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">{label}</span>
            </Link>
          ))}
        </nav>

        {/* System badge */}
        <div className="flex items-center gap-2">
          <span className="hidden lg:flex items-center gap-1.5 rounded-full border border-[var(--border)] px-2.5 py-1 text-xs text-[var(--muted)]">
            <Terminal className="h-3 w-3" />
            Pipeline v2
          </span>
          <span className="h-2 w-2 rounded-full bg-[var(--success)] animate-pulse" title="System online" />
        </div>
      </div>
    </header>
  );
}
