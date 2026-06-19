import { NextRequest, NextResponse } from "next/server";
import type { PipelineTask, EngineKey, TaskStatus } from "@/lib/engines";
import { ENGINE_PROFILES, ENGINE_SEQUENCES } from "@/lib/engines";

// In-memory store — persists for the server process lifetime
const taskStore: PipelineTask[] = [];

function generateId(): string {
  return `task_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

function classifyEngine(task: string): EngineKey {
  const t = task.toLowerCase();
  if (t.includes("research") || t.includes("investigate") || t.includes("find")) return "research";
  if (t.includes("claim") || t.includes("verify") || t.includes("evidence")) return "claims";
  if (t.includes("write") || t.includes("draft") || t.includes("copy")) return "writing";
  if (t.includes("layout") || t.includes("geometry") || t.includes("spatial")) return "geometry";
  if (t.includes("build") || t.includes("construct") || t.includes("renovation")) return "construction";
  if (t.includes("legal") || t.includes("comply") || t.includes("compliance")) return "compliance";
  if (t.includes("schedule") || t.includes("cadence") || t.includes("routine")) return "frequency";
  if (t.includes("market") || t.includes("campaign") || t.includes("offer")) return "marketing";
  if (t.includes("video") || t.includes("avatar") || t.includes("twin")) return "ai_twin";
  if (t.includes("publish") || t.includes("release") || t.includes("deploy")) return "publish";
  return "automation";
}

export async function GET() {
  return NextResponse.json({ tasks: taskStore });
}

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}));
  const {
    task,
    company_id,
    execution_mode = "dry_run",
    notes,
    engine,
  } = body as {
    task?: string;
    company_id?: string;
    execution_mode?: "dry_run" | "live_ready";
    notes?: string;
    engine?: EngineKey;
  };

  if (!task || typeof task !== "string" || !task.trim()) {
    return NextResponse.json({ ok: false, error: "task is required" }, { status: 400 });
  }

  const resolvedEngine: EngineKey =
    engine && ENGINE_PROFILES[engine] ? engine : classifyEngine(task);

  const newTask: PipelineTask = {
    id: generateId(),
    task: task.trim(),
    engine: resolvedEngine,
    company_id,
    execution_mode,
    status: "pending",
    created_at: new Date().toISOString(),
    route: ENGINE_SEQUENCES[resolvedEngine]?.join(" → ") ?? resolvedEngine,
  };

  taskStore.unshift(newTask);

  return NextResponse.json({ ok: true, task: newTask }, { status: 201 });
}
