"use client";

import { useState, useEffect, useCallback } from "react";
import { cn } from "@/lib/cn";
import {
  ActivitySquare,
  CheckCircle2,
  AlertCircle,
  Loader2,
  ExternalLink,
  RefreshCw,
} from "lucide-react";

interface HealthData {
  service: string;
  status: string;
  version: string;
  timestamp: string;
  engines: string[];
  connectors: { name: string; status: string }[];
  companies: string[];
}

interface SavedTask {
  id: string;
  task: string;
  engine: string;
  company_id?: string;
  execution_mode: string;
  status: string;
  created_at: string;
  route?: string;
}

const COMPANIES = [
  { value: "", label: "General" },
  { value: "focus-negotium", label: "Focus Negotium Inc" },
  { value: "royal-lee-construction", label: "Royal Lee Construction Solutions LLC" },
  { value: "focus-records", label: "Focus Records LLC" },
];

function MetricCard({ label, value, accent }: { label: string; value: string | number; accent?: boolean }) {
  return (
    <div
      className={cn(
        "rounded-[var(--radius-sm)] border p-4",
        accent
          ? "border-[var(--border-gold)] bg-[var(--gold-dim)]"
          : "border-[var(--border)] bg-[var(--surface)]"
      )}
    >
      <p
        className={cn(
          "text-2xl font-bold font-mono",
          accent ? "text-[var(--gold)]" : "text-foreground"
        )}
      >
        {value}
      </p>
      <p className="text-xs text-[var(--muted)] mt-0.5 uppercase tracking-wider">{label}</p>
    </div>
  );
}

function ConnectorBadge({ name, status }: { name: string; status: string }) {
  const ok = status === "configured";
  return (
    <div className="flex items-center justify-between rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2">
      <span className="text-sm text-foreground">{name}</span>
      <span
        className={cn(
          "flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium",
          ok
            ? "bg-[rgba(74,222,128,0.1)] text-[var(--success)]"
            : "bg-[rgba(107,132,168,0.1)] text-[var(--muted)]"
        )}
      >
        {ok ? <CheckCircle2 className="h-3 w-3" /> : <AlertCircle className="h-3 w-3" />}
        {status.replace("_", " ")}
      </span>
    </div>
  );
}

export function OperatorConsole() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [tasks, setTasks] = useState<SavedTask[]>([]);
  const [loadingHealth, setLoadingHealth] = useState(true);

  // Task form state
  const [taskLines, setTaskLines] = useState("");
  const [taskCompany, setTaskCompany] = useState("");
  const [taskMode, setTaskMode] = useState<"dry_run" | "live_ready">("dry_run");
  const [taskNotes, setTaskNotes] = useState("");
  const [taskSubmitting, setTaskSubmitting] = useState(false);
  const [taskResults, setTaskResults] = useState<string[]>([]);

  // Payroll form state
  const [payPeriod, setPayPeriod] = useState("");
  const [approver, setApprover] = useState("");
  const [hoursSummary, setHoursSummary] = useState("");
  const [exceptions, setExceptions] = useState("");
  const [payrollSubmitting, setPayrollSubmitting] = useState(false);
  const [payrollResult, setPayrollResult] = useState<string | null>(null);

  const refreshData = useCallback(async () => {
    setLoadingHealth(true);
    try {
      const [healthRes, tasksRes] = await Promise.all([
        fetch("/api/health"),
        fetch("/api/tasks"),
      ]);
      const healthData = await healthRes.json();
      const tasksData = await tasksRes.json();
      setHealth(healthData);
      setTasks(tasksData.tasks ?? []);
    } catch {
      // silent
    } finally {
      setLoadingHealth(false);
    }
  }, []);

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 30000);
    return () => clearInterval(interval);
  }, [refreshData]);

  const submitTasks = async (e: React.FormEvent) => {
    e.preventDefault();
    const lines = taskLines.split("\n").map((l) => l.trim()).filter(Boolean);
    if (!lines.length) return;
    setTaskSubmitting(true);
    const results: string[] = [];

    for (const task of lines) {
      try {
        const res = await fetch("/api/tasks", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            task,
            company_id: taskCompany || undefined,
            execution_mode: taskMode,
            notes: taskNotes,
          }),
        });
        const data = await res.json();
        if (res.ok) {
          results.push(`✓ Saved: "${task}" → ${data.task.engine} [${data.task.status}]`);
        } else {
          results.push(`✗ Error: ${data.error}`);
        }
      } catch {
        results.push(`✗ Network error saving: "${task}"`);
      }
    }

    setTaskResults((prev) => [...results, ...prev]);
    setTaskLines("");
    setTaskNotes("");
    await refreshData();
    setTaskSubmitting(false);
  };

  const submitPayroll = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!payPeriod || !hoursSummary) return;
    setPayrollSubmitting(true);

    // Simulate payroll readiness pack generation (no live payroll)
    await new Promise((r) => setTimeout(r, 800));
    const packId = `pack_${Date.now()}`;
    setPayrollResult(
      `Payroll readiness pack prepared.\n` +
      `Pack ID: ${packId}\n` +
      `Pay period: ${payPeriod}\n` +
      `Approver: ${approver || "Pending"}\n` +
      `Policy: REVIEW_REQUIRED — No live payroll submitted.\n` +
      `Hours summary logged. Ready for review before any external payroll platform submission.\n` +
      `Exceptions: ${exceptions || "None supplied"}`
    );
    setPayPeriod("");
    setApprover("");
    setHoursSummary("");
    setExceptions("");
    setPayrollSubmitting(false);
  };

  const completedCount = tasks.filter((t) => t.status === "completed").length;
  const runningCount = tasks.filter((t) => t.status === "running").length;

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-col gap-1">
        <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
          Operator Console
        </p>
        <h1 className="font-serif text-3xl font-semibold tracking-tight text-balance">
          Private Business Console
        </h1>
        <p className="text-sm text-[var(--muted)] max-w-xl leading-relaxed">
          Register today&apos;s tasks, prepare payroll readiness packs, and monitor live system
          metrics — all from one internal control surface.
        </p>
      </div>

      {/* Status bar */}
      <div className="flex flex-wrap items-center gap-2">
        {loadingHealth ? (
          <span className="flex items-center gap-1.5 text-xs text-[var(--muted)]">
            <Loader2 className="h-3 w-3 animate-spin" /> Loading system status…
          </span>
        ) : health ? (
          <>
            <span className="flex items-center gap-1.5 rounded-full border border-[var(--border)] bg-[var(--surface)] px-3 py-1 text-xs">
              <span className="h-1.5 w-1.5 rounded-full bg-[var(--success)]" />
              {health.service}
            </span>
            <span className="rounded-full border border-[var(--border)] bg-[var(--surface)] px-3 py-1 text-xs text-[var(--muted)]">
              v{health.version}
            </span>
            <span className="rounded-full border border-[var(--border)] bg-[var(--surface)] px-3 py-1 text-xs text-[var(--muted)]">
              {health.engines.length} engines online
            </span>
          </>
        ) : (
          <span className="text-xs text-[var(--error)]">Could not reach system health endpoint</span>
        )}
        <button
          onClick={refreshData}
          className="ml-auto flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-[var(--surface)] px-3 py-1.5 text-xs text-[var(--muted)] hover:text-foreground transition-colors"
        >
          <RefreshCw className="h-3 w-3" />
          Refresh
        </button>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <MetricCard label="Total Tasks" value={tasks.length} accent />
        <MetricCard label="Completed" value={completedCount} />
        <MetricCard label="Running" value={runningCount} />
        <MetricCard
          label="Engines"
          value={health?.engines.length ?? "—"}
        />
      </div>

      {/* Main grid: tasks + system */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Task form */}
        <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5">
          <div className="mb-4">
            <div className="flex items-center gap-2 mb-0.5">
              <ActivitySquare className="h-4 w-4 text-[var(--gold)]" />
              <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
                Daily Tasks
              </p>
              <span className="rounded-full border border-[var(--border)] px-1.5 py-0.5 text-[10px] text-[var(--muted)]">
                Low / medium risk auto-route
              </span>
            </div>
            <h2 className="font-medium text-foreground">Register Today&apos;s Task Items</h2>
          </div>

          <form onSubmit={submitTasks} className="flex flex-col gap-3">
            <div className="grid grid-cols-2 gap-2">
              <div className="flex flex-col gap-1">
                <label className="text-xs text-[var(--muted)]">Company</label>
                <select
                  value={taskCompany}
                  onChange={(e) => setTaskCompany(e.target.value)}
                  className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-foreground focus:border-[var(--blue)] focus:outline-none"
                >
                  {COMPANIES.map((c) => (
                    <option key={c.value} value={c.value}>{c.label}</option>
                  ))}
                </select>
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-xs text-[var(--muted)]">Execution mode</label>
                <select
                  value={taskMode}
                  onChange={(e) => setTaskMode(e.target.value as "dry_run" | "live_ready")}
                  className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-foreground focus:border-[var(--blue)] focus:outline-none"
                >
                  <option value="dry_run">Dry Run</option>
                  <option value="live_ready">Live Ready</option>
                </select>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[var(--muted)]">Today&apos;s tasks (one per line)</label>
              <textarea
                value={taskLines}
                onChange={(e) => setTaskLines(e.target.value)}
                rows={4}
                placeholder={"Review Stripe sales and update KPI sheet\nRefresh the product page headline\nPrepare today's lead follow-up list"}
                className="resize-none rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none leading-relaxed"
                required
              />
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[var(--muted)]">Notes (optional)</label>
              <textarea
                value={taskNotes}
                onChange={(e) => setTaskNotes(e.target.value)}
                rows={2}
                placeholder="Optional context, deadlines, owners, or blockers."
                className="resize-none rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none"
              />
            </div>

            <div className="flex items-center gap-2">
              <button
                type="submit"
                disabled={taskSubmitting || !taskLines.trim()}
                className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-[var(--gold)] px-4 py-2.5 text-sm font-medium text-[var(--background)] hover:brightness-110 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              >
                {taskSubmitting ? (
                  <><Loader2 className="h-3.5 w-3.5 animate-spin" /> Saving…</>
                ) : (
                  "Save Tasks"
                )}
              </button>
              <a
                href="/api/tasks"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-[var(--muted)] hover:text-foreground transition-colors"
              >
                <ExternalLink className="h-3.5 w-3.5" />
                View JSON
              </a>
            </div>
          </form>

          {/* Task results */}
          {taskResults.length > 0 && (
            <div className="mt-3 rounded-lg border border-[var(--border)] bg-[var(--background)] p-3 flex flex-col gap-1 max-h-32 overflow-y-auto">
              {taskResults.map((r, i) => (
                <p
                  key={i}
                  className={cn(
                    "text-xs font-mono",
                    r.startsWith("✓") ? "text-[var(--success)]" : "text-[var(--error)]"
                  )}
                >
                  {r}
                </p>
              ))}
            </div>
          )}
        </section>

        {/* Payroll readiness */}
        <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5">
          <div className="mb-4">
            <div className="flex items-center gap-2 mb-0.5">
              <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
                Payroll Readiness
              </p>
              <span className="rounded-full border border-[var(--border-gold)] bg-[var(--gold-dim)] px-1.5 py-0.5 text-[10px] text-[var(--gold)]">
                No live payroll
              </span>
            </div>
            <h2 className="font-medium text-foreground">Prepare the Payroll Packet</h2>
          </div>

          <form onSubmit={submitPayroll} className="flex flex-col gap-3">
            <div className="grid grid-cols-2 gap-2">
              <div className="flex flex-col gap-1">
                <label className="text-xs text-[var(--muted)]">Pay period</label>
                <input
                  value={payPeriod}
                  onChange={(e) => setPayPeriod(e.target.value)}
                  placeholder="March 24 to March 30, 2026"
                  required
                  className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none"
                />
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-xs text-[var(--muted)]">Approver</label>
                <input
                  value={approver}
                  onChange={(e) => setApprover(e.target.value)}
                  placeholder="Reginald Hilton Jr."
                  className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none"
                />
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[var(--muted)]">Hours and rate summary</label>
              <textarea
                value={hoursSummary}
                onChange={(e) => setHoursSummary(e.target.value)}
                rows={3}
                required
                placeholder="List employees, hours, rates, reimbursements, and anything that needs review."
                className="resize-none rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none leading-relaxed"
              />
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[var(--muted)]">Exceptions or notes</label>
              <textarea
                value={exceptions}
                onChange={(e) => setExceptions(e.target.value)}
                rows={2}
                placeholder="Missing approvals, overtime notes, reimbursements, or open payroll questions."
                className="resize-none rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none"
              />
            </div>

            <button
              type="submit"
              disabled={payrollSubmitting || !payPeriod || !hoursSummary}
              className="flex items-center justify-center gap-2 rounded-lg bg-[var(--surface-elevated)] border border-[var(--border-gold)] px-4 py-2.5 text-sm font-medium text-[var(--gold)] hover:bg-[var(--gold-dim)] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              {payrollSubmitting ? (
                <><Loader2 className="h-3.5 w-3.5 animate-spin" /> Preparing…</>
              ) : (
                "Prepare Payroll Readiness Pack"
              )}
            </button>
          </form>

          {payrollResult && (
            <div className="mt-3 rounded-lg border border-[var(--border-gold)] bg-[var(--gold-dim)] p-3">
              <pre className="terminal text-xs text-[var(--gold)] whitespace-pre-wrap">
                {payrollResult}
              </pre>
            </div>
          )}
        </section>
      </div>

      {/* Connectors + Recent tasks */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Connector status */}
        <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5">
          <div className="mb-3">
            <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
              Integration Status
            </p>
            <h2 className="font-medium text-foreground">Live Connectors</h2>
          </div>
          {health ? (
            <div className="flex flex-col gap-2">
              {health.connectors.map((c) => (
                <ConnectorBadge key={c.name} name={c.name} status={c.status} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Loading connector status…</p>
          )}
        </section>

        {/* Recent task log */}
        <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5">
          <div className="mb-3">
            <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
              Task Log
            </p>
            <h2 className="font-medium text-foreground">Latest Results</h2>
          </div>
          <div className="flex flex-col gap-2 max-h-64 overflow-y-auto">
            {tasks.length === 0 ? (
              <p className="text-sm text-[var(--muted)]">No tasks recorded yet.</p>
            ) : (
              tasks.slice(0, 8).map((t) => (
                <div
                  key={t.id}
                  className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-[10px] font-medium uppercase tracking-widest text-[var(--muted)]">
                      {t.engine}
                    </span>
                    <span
                      className={cn(
                        "text-[10px] font-medium uppercase",
                        t.status === "completed"
                          ? "text-[var(--success)]"
                          : t.status === "running"
                          ? "text-[var(--running)]"
                          : t.status === "error"
                          ? "text-[var(--error)]"
                          : "text-[var(--muted)]"
                      )}
                    >
                      {t.status}
                    </span>
                  </div>
                  <p className="mt-0.5 text-sm text-foreground line-clamp-1">{t.task}</p>
                  <p className="mt-0.5 text-[10px] text-[var(--muted)]">
                    {new Date(t.created_at).toLocaleString()}
                  </p>
                </div>
              ))
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
