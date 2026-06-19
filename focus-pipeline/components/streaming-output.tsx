"use client";

import { useEffect, useRef } from "react";
import { cn } from "@/lib/cn";
import type { TaskStatus } from "@/lib/engines";
import { Copy, Download } from "lucide-react";

interface StreamingOutputProps {
  output: string;
  status: TaskStatus;
  activeEngine?: string;
  engineSequence?: string[];
  completedEngines?: string[];
}

export function StreamingOutput({
  output,
  status,
  activeEngine,
  engineSequence = [],
  completedEngines = [],
}: StreamingOutputProps) {
  const containerRef = useRef<HTMLPreElement>(null);

  // Auto-scroll to bottom as output streams in
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [output]);

  const copyOutput = async () => {
    if (output) await navigator.clipboard.writeText(output);
  };

  const downloadOutput = () => {
    if (!output) return;
    const blob = new Blob([output], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `focus-pipeline-output-${Date.now()}.md`;
    link.click();
    URL.revokeObjectURL(link.href);
  };

  return (
    <div className="flex flex-col gap-3 h-full">
      {/* Engine pipeline progress */}
      {engineSequence.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5">
          {engineSequence.map((eng, idx) => {
            const isDone = completedEngines.includes(eng);
            const isActive = eng === activeEngine && status === "running";
            return (
              <span
                key={eng}
                className={cn(
                  "flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium border transition-all",
                  isDone
                    ? "border-[rgba(74,222,128,0.3)] bg-[rgba(74,222,128,0.08)] text-[var(--success)]"
                    : isActive
                    ? "border-[rgba(242,201,109,0.4)] bg-[var(--gold-dim)] text-[var(--gold)] pulse-gold"
                    : "border-[var(--border)] bg-transparent text-[var(--muted)]"
                )}
              >
                {isDone ? (
                  <svg className="h-2.5 w-2.5" viewBox="0 0 10 10" fill="none">
                    <path d="M2 5l2.5 2.5L8 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                ) : isActive ? (
                  <span className="h-1.5 w-1.5 rounded-full bg-[var(--gold)] animate-pulse" />
                ) : null}
                {eng}
              </span>
            );
          })}
        </div>
      )}

      {/* Output terminal */}
      <div className="relative flex-1 rounded-[var(--radius-sm)] border border-[var(--border)] bg-[rgba(4,10,22,0.95)] overflow-hidden">
        {/* Header bar */}
        <div className="flex items-center justify-between border-b border-[var(--border)] px-4 py-2">
          <div className="flex items-center gap-2">
            <div className="flex gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full bg-[rgba(248,113,113,0.6)]" />
              <span className="h-2.5 w-2.5 rounded-full bg-[rgba(242,201,109,0.6)]" />
              <span className="h-2.5 w-2.5 rounded-full bg-[rgba(74,222,128,0.6)]" />
            </div>
            <span className="text-xs text-[var(--muted)] font-mono">focus-pipeline :: output</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={copyOutput}
              disabled={!output}
              className="flex items-center gap-1 rounded px-2 py-1 text-xs text-[var(--muted)] hover:text-foreground hover:bg-[var(--surface)] transition-colors disabled:opacity-30"
            >
              <Copy className="h-3 w-3" />
              Copy
            </button>
            <button
              onClick={downloadOutput}
              disabled={!output}
              className="flex items-center gap-1 rounded px-2 py-1 text-xs text-[var(--muted)] hover:text-foreground hover:bg-[var(--surface)] transition-colors disabled:opacity-30"
            >
              <Download className="h-3 w-3" />
              Save
            </button>
          </div>
        </div>

        {/* Content */}
        <pre
          ref={containerRef}
          className={cn(
            "terminal overflow-auto p-4 text-[var(--foreground)] min-h-[400px] max-h-[520px]",
            status === "running" && output && "cursor-blink"
          )}
        >
          {output ||
            (status === "pending"
              ? "// Awaiting task input. Select an engine and enter your task to begin.\n// The pipeline will stream output here in real time."
              : status === "running"
              ? "// Initializing pipeline engines...\n// Streaming output will appear here."
              : "// No output yet.")}
        </pre>
      </div>
    </div>
  );
}
