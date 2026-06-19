"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import { cn } from "@/lib/cn";
import {
  ENGINE_PROFILES,
  ENGINE_SEQUENCES,
  type EngineKey,
  type PipelineTask,
  type TaskStatus,
} from "@/lib/engines";
import { EngineCard } from "@/components/engine-card";
import { StreamingOutput } from "@/components/streaming-output";
import { TaskList } from "@/components/task-list";
import {
  Play,
  Square,
  Zap,
  ChevronDown,
  ChevronUp,
  LayoutGrid,
} from "lucide-react";

const ENGINE_KEYS = Object.keys(ENGINE_PROFILES) as EngineKey[];

const COMPANIES = [
  { value: "", label: "General" },
  { value: "focus-negotium", label: "Focus Negotium Inc" },
  { value: "royal-lee-construction", label: "Royal Lee Construction" },
  { value: "focus-records", label: "Focus Records LLC" },
];

export function PipelineDashboard() {
  const [selectedEngine, setSelectedEngine] = useState<EngineKey>("automation");
  const [executionMode, setExecutionMode] = useState<"dry_run" | "live_ready">("dry_run");
  const [company, setCompany] = useState("");
  const [taskInput, setTaskInput] = useState("");
  const [output, setOutput] = useState("");
  const [status, setStatus] = useState<TaskStatus>("pending");
  const [activeEngine, setActiveEngine] = useState<string | undefined>();
  const [completedEngines, setCompletedEngines] = useState<string[]>([]);
  const [tasks, setTasks] = useState<PipelineTask[]>([]);
  const [activeTask, setActiveTask] = useState<PipelineTask | undefined>();
  const [showAllEngines, setShowAllEngines] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const engineSequence = ENGINE_SEQUENCES[selectedEngine] ?? ["automation"];
  const visibleEngines = showAllEngines ? ENGINE_KEYS : ENGINE_KEYS.slice(0, 8);

  // Load tasks on mount
  useEffect(() => {
    fetch("/api/tasks")
      .then((r) => r.json())
      .then((data) => setTasks(data.tasks ?? []))
      .catch(() => {});
  }, []);

  const stopPipeline = useCallback(() => {
    abortRef.current?.abort();
    setStatus("error");
    setActiveEngine(undefined);
  }, []);

  const runPipeline = useCallback(async () => {
    if (!taskInput.trim() || status === "running") return;

    // Reset
    setOutput("");
    setCompletedEngines([]);
    setActiveEngine(undefined);
    setStatus("running");

    // Save task to store
    const newTask: PipelineTask = {
      id: `task_${Date.now()}`,
      task: taskInput.trim(),
      engine: selectedEngine,
      company_id: company || undefined,
      execution_mode: executionMode,
      status: "running",
      created_at: new Date().toISOString(),
      route: engineSequence.join(" → "),
    };
    setTasks((prev) => [newTask, ...prev]);
    setActiveTask(newTask);

    // Also save to API
    fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        task: taskInput.trim(),
        engine: selectedEngine,
        company_id: company || undefined,
        execution_mode: executionMode,
      }),
    }).catch(() => {});

    const ctrl = new AbortController();
    abortRef.current = ctrl;

    try {
      const resp = await fetch("/api/pipeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: ctrl.signal,
        body: JSON.stringify({
          task: taskInput.trim(),
          engine: selectedEngine,
          execution_mode: executionMode,
        }),
      });

      if (!resp.ok || !resp.body) {
        throw new Error(`Pipeline returned ${resp.status}`);
      }

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        setOutput((prev) => prev + chunk);

        // Parse engine markers
        const startMatches = [...buffer.matchAll(/\[ENGINE_START:(\w+)\]/g)];
        const completeMatches = [...buffer.matchAll(/\[ENGINE_COMPLETE:(\w+)\]/g)];

        for (const m of startMatches) {
          setActiveEngine(m[1]);
        }
        for (const m of completeMatches) {
          setCompletedEngines((prev) =>
            prev.includes(m[1]) ? prev : [...prev, m[1]]
          );
        }

        if (buffer.includes("[PIPELINE_COMPLETE]")) {
          break;
        }
      }

      setStatus("completed");
      setActiveEngine(undefined);
      setTasks((prev) =>
        prev.map((t) =>
          t.id === newTask.id ? { ...t, status: "completed", completed_at: new Date().toISOString() } : t
        )
      );
      setActiveTask((prev) =>
        prev?.id === newTask.id ? { ...prev, status: "completed" } : prev
      );
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        setStatus("error");
        setOutput((prev) => prev + `\n\n[PIPELINE_ERROR: ${(err as Error).message}]`);
        setTasks((prev) =>
          prev.map((t) => (t.id === newTask.id ? { ...t, status: "error" } : t))
        );
      }
    }
  }, [taskInput, selectedEngine, executionMode, company, engineSequence, status]);

  const handleTaskSelect = (task: PipelineTask) => {
    setActiveTask(task);
    setTaskInput(task.task);
    setSelectedEngine(task.engine);
    setExecutionMode(task.execution_mode);
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Page header */}
      <div className="flex flex-col gap-1">
        <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
          AI Master Pipeline
        </p>
        <h1 className="font-serif text-3xl font-semibold tracking-tight text-balance">
          Command &amp; Execute
        </h1>
        <p className="text-sm text-[var(--muted)] max-w-xl leading-relaxed">
          Select an engine, enter your task, and watch the pipeline stream live output
          through each stage in real time. All tasks are tracked and replayable.
        </p>
      </div>

      {/* Main grid: left controls + right output */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[380px_1fr]">
        {/* Left column — controls */}
        <div className="flex flex-col gap-4">
          {/* Engine selector */}
          <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-4">
            <div className="mb-3 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
                  Engine
                </p>
                <h2 className="font-medium text-foreground">Select Primary Engine</h2>
              </div>
              <button
                onClick={() => setShowAllEngines((v) => !v)}
                className="flex items-center gap-1 text-xs text-[var(--muted)] hover:text-foreground transition-colors"
              >
                <LayoutGrid className="h-3.5 w-3.5" />
                {showAllEngines ? (
                  <>Less <ChevronUp className="h-3 w-3" /></>
                ) : (
                  <>More <ChevronDown className="h-3 w-3" /></>
                )}
              </button>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {visibleEngines.map((key) => (
                <EngineCard
                  key={key}
                  profile={ENGINE_PROFILES[key]}
                  selected={selectedEngine === key}
                  onSelect={(k) => setSelectedEngine(k as EngineKey)}
                  running={activeEngine === key}
                  completed={completedEngines.includes(key)}
                />
              ))}
            </div>

            {/* Engine sequence preview */}
            <div className="mt-3 rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2">
              <p className="text-[10px] font-medium uppercase tracking-widest text-[var(--muted)] mb-1">
                Execution sequence
              </p>
              <p className="text-xs font-mono text-[var(--blue)]">
                {engineSequence.join(" → ")}
              </p>
            </div>
          </section>

          {/* Task input form */}
          <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-4 flex flex-col gap-3">
            <div>
              <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
                Task
              </p>
              <h2 className="font-medium text-foreground">Enter Your Task</h2>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div className="flex flex-col gap-1">
                <label className="text-xs text-[var(--muted)]">Company</label>
                <select
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-foreground focus:border-[var(--blue)] focus:outline-none"
                >
                  {COMPANIES.map((c) => (
                    <option key={c.value} value={c.value}>
                      {c.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-xs text-[var(--muted)]">Mode</label>
                <select
                  value={executionMode}
                  onChange={(e) =>
                    setExecutionMode(e.target.value as "dry_run" | "live_ready")
                  }
                  className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-foreground focus:border-[var(--blue)] focus:outline-none"
                >
                  <option value="dry_run">Dry Run</option>
                  <option value="live_ready">Live Ready</option>
                </select>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[var(--muted)]">Task description</label>
              <textarea
                value={taskInput}
                onChange={(e) => setTaskInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) runPipeline();
                }}
                placeholder={`Describe the task for the ${ENGINE_PROFILES[selectedEngine].label}...\n\nExample: Research the top 5 construction materials for sacred geometry-aligned structures and prepare an owner brief.`}
                rows={5}
                className="resize-none rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none leading-relaxed"
              />
              <p className="text-[10px] text-[var(--muted)]">
                Tip: Press ⌘ + Enter to run
              </p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={runPipeline}
                disabled={!taskInput.trim() || status === "running"}
                className={cn(
                  "flex flex-1 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-all",
                  status === "running"
                    ? "bg-[var(--gold-dim)] border border-[var(--border-gold)] text-[var(--gold)] cursor-not-allowed"
                    : "bg-[var(--gold)] text-[var(--background)] hover:brightness-110 disabled:opacity-40 disabled:cursor-not-allowed"
                )}
              >
                {status === "running" ? (
                  <>
                    <span className="h-3.5 w-3.5 rounded-full border-2 border-[var(--gold)] border-t-transparent animate-spin" />
                    Running…
                  </>
                ) : (
                  <>
                    <Play className="h-3.5 w-3.5" />
                    Run Pipeline
                  </>
                )}
              </button>
              {status === "running" && (
                <button
                  onClick={stopPipeline}
                  className="flex items-center gap-1.5 rounded-lg border border-[var(--error)] bg-[rgba(248,113,113,0.08)] px-3 py-2.5 text-sm font-medium text-[var(--error)] hover:bg-[rgba(248,113,113,0.16)] transition-colors"
                >
                  <Square className="h-3.5 w-3.5" />
                  Stop
                </button>
              )}
            </div>
          </section>
        </div>

        {/* Right column — streaming output */}
        <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-4 flex flex-col gap-3 min-h-[600px]">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
                Live Output
              </p>
              <h2 className="font-medium text-foreground">Pipeline Stream</h2>
            </div>
            <div className="flex items-center gap-2">
              {status === "running" && (
                <span className="flex items-center gap-1.5 rounded-full border border-[rgba(242,201,109,0.3)] bg-[var(--gold-dim)] px-2.5 py-1 text-xs text-[var(--gold)]">
                  <span className="h-1.5 w-1.5 rounded-full bg-[var(--gold)] animate-pulse" />
                  Streaming
                </span>
              )}
              {status === "completed" && (
                <span className="flex items-center gap-1.5 rounded-full border border-[rgba(74,222,128,0.3)] bg-[rgba(74,222,128,0.08)] px-2.5 py-1 text-xs text-[var(--success)]">
                  <Zap className="h-3 w-3" />
                  Complete
                </span>
              )}
              {status === "error" && (
                <span className="rounded-full border border-[rgba(248,113,113,0.3)] bg-[rgba(248,113,113,0.08)] px-2.5 py-1 text-xs text-[var(--error)]">
                  Error
                </span>
              )}
            </div>
          </div>

          <div className="flex-1">
            <StreamingOutput
              output={output}
              status={status}
              activeEngine={activeEngine}
              engineSequence={engineSequence}
              completedEngines={completedEngines}
            />
          </div>
        </section>
      </div>

      {/* Task history */}
      <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-4">
        <div className="mb-3 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
              History
            </p>
            <h2 className="font-medium text-foreground">Task Log</h2>
          </div>
          <span className="rounded-full border border-[var(--border)] px-2 py-0.5 text-xs text-[var(--muted)]">
            {tasks.length} task{tasks.length !== 1 ? "s" : ""}
          </span>
        </div>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {tasks.length === 0 ? (
            <p className="col-span-full py-6 text-center text-sm text-[var(--muted)]">
              No tasks yet. Run the pipeline to get started.
            </p>
          ) : (
            tasks.slice(0, 9).map((task) => (
              <button
                key={task.id}
                onClick={() => handleTaskSelect(task)}
                className={cn(
                  "rounded-lg border p-3 text-left transition-all cursor-pointer",
                  activeTask?.id === task.id
                    ? "border-[var(--border-gold)] bg-[var(--gold-dim)]"
                    : "border-[var(--border)] bg-[var(--background)] hover:bg-[var(--surface-elevated)]"
                )}
              >
                <div className="flex items-center justify-between gap-1 mb-1">
                  <span className="text-[10px] font-medium uppercase tracking-widest text-[var(--muted)]">
                    {task.engine}
                  </span>
                  <span
                    className={cn(
                      "text-[10px] font-medium uppercase rounded-full px-1.5 py-0.5",
                      task.status === "completed"
                        ? "bg-[rgba(74,222,128,0.1)] text-[var(--success)]"
                        : task.status === "running"
                        ? "bg-[rgba(96,165,250,0.1)] text-[var(--running)]"
                        : task.status === "error"
                        ? "bg-[rgba(248,113,113,0.1)] text-[var(--error)]"
                        : "bg-[rgba(107,132,168,0.1)] text-[var(--muted)]"
                    )}
                  >
                    {task.status}
                  </span>
                </div>
                <p className="text-sm text-foreground line-clamp-2 leading-snug">
                  {task.task}
                </p>
                <p className="mt-1.5 text-[10px] text-[var(--muted)]">
                  {task.execution_mode === "live_ready" ? "LIVE" : "DRY RUN"} ·{" "}
                  {new Date(task.created_at).toLocaleTimeString()}
                </p>
              </button>
            ))
          )}
        </div>
      </section>
    </div>
  );
}
