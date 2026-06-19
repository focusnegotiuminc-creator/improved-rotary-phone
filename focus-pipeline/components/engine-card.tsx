"use client";

import { cn } from "@/lib/cn";
import type { EngineProfile } from "@/lib/engines";

interface EngineCardProps {
  profile: EngineProfile;
  selected: boolean;
  onSelect: (key: string) => void;
  running?: boolean;
  completed?: boolean;
}

export function EngineCard({ profile, selected, onSelect, running, completed }: EngineCardProps) {
  return (
    <button
      onClick={() => onSelect(profile.key)}
      className={cn(
        "relative w-full rounded-[var(--radius-sm)] border p-3 text-left transition-all duration-200 cursor-pointer",
        selected
          ? "border-[var(--border-gold)] bg-[var(--gold-dim)] shadow-[0_0_0_1px_rgba(242,201,109,0.2)]"
          : "border-[var(--border)] bg-[var(--surface)] hover:border-[rgba(129,201,255,0.3)] hover:bg-[var(--surface-elevated)]",
        running && "pulse-gold"
      )}
    >
      {/* Status dot */}
      {(running || completed) && (
        <span
          className={cn(
            "absolute top-2.5 right-2.5 h-1.5 w-1.5 rounded-full",
            running ? "bg-[var(--running)] animate-pulse" : "bg-[var(--success)]"
          )}
        />
      )}

      <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)] mb-1">
        {profile.key}
      </p>
      <h3
        className={cn(
          "font-medium text-sm leading-snug",
          selected ? "text-[var(--gold)]" : "text-foreground"
        )}
      >
        {profile.label}
      </h3>
      <p className="mt-1 text-xs text-[var(--muted)] line-clamp-2 leading-relaxed">
        {profile.focus}
      </p>
    </button>
  );
}
