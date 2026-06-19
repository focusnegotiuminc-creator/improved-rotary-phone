"use client";

import { cn } from "@/lib/cn";
import { type PipelineTask, STATUS_BG, STATUS_COLORS } from "@/lib/engines";
import { Clock, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

interface TaskListProps {
  tasks: PipelineTask[];
  activeTaskId?: string;
  onSelect?: (task: PipelineTask) => void;
}

function StatusIcon({ status }: { status: PipelineTask["status"] }) {
  switch (status) {
    case "running":
      return <Loader2 className="h-3.5 w-3.5 animate-spin text-[var(--running)]" />;
    case "completed":
      return <CheckCircle2 className="h-3.5 w-3.5 text-[var(--success)]" />;
    case "error":
      return <AlertCircle className="h-3.5 w-3.5 text-[var(--error)]" />;
    default:
      return <Clock className="h-3.5 w-3.5 text-[var(--muted)]" />;
  }
}

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const secs = Math.floor(diff / 1000);
  if (secs < 60) return `${secs}s ago`;
  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  return `${hrs}h ago`;
}

export function TaskList({ tasks, activeTaskId, onSelect }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-10 text-center">
        <Clock className="h-8 w-8 text-[var(--muted)] mb-3 opacity-40" />
        <p className="text-sm text-[var(--muted)]">No tasks yet</p>
        <p className="text-xs text-[var(--muted)] mt-1 opacity-60">
          Submit a task above to see it tracked here
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1.5">
      {tasks.map((task) => (
        <button
          key={task.id}
          onClick={() => onSelect?.(task)}
          className={cn(
            "w-full rounded-[var(--radius-sm)] border p-3 text-left transition-all cursor-pointer",
            activeTaskId === task.id
              ? "border-[var(--border-gold)] bg-[var(--gold-dim)]"
              : "border-[var(--border)] bg-[var(--surface)] hover:bg-[var(--surface-elevated)]"
          )}
        >
          <div className="flex items-start justify-between gap-2 mb-1">
            <div className="flex items-center gap-1.5 min-w-0">
              <StatusIcon status={task.status} />
              <span className="text-xs font-medium uppercase tracking-widest text-[var(--muted)] shrink-0">
                {task.engine}
              </span>
            </div>
            <span
              className={cn(
                "shrink-0 rounded-full px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-wider",
                STATUS_BG[task.status],
                STATUS_COLORS[task.status]
              )}
            >
              {task.status}
            </span>
          </div>

          <p className="text-sm text-foreground line-clamp-2 leading-snug">
            {task.task}
          </p>

          <div className="mt-1.5 flex items-center justify-between text-[10px] text-[var(--muted)]">
            <span>{task.execution_mode === "live_ready" ? "LIVE" : "DRY RUN"}</span>
            <span>{timeAgo(task.created_at)}</span>
          </div>
        </button>
      ))}
    </div>
  );
}
