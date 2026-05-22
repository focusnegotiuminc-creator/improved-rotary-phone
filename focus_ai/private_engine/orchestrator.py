"""Focus Private AI Engine multi-agent orchestrator.

Default mode does not call remote models. It creates a run packet that can be
sent to local/open/provider endpoints once configured.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(__file__).resolve().parent / "config"
RUNS_DIR = Path("D:/TheFocusFiles/AI-Pipeline/runs")

HIGH_IMPACT_TERMS = {
    "deploy", "post", "publish", "send", "outreach", "email", "sms", "payment", "purchase",
    "contract", "legal", "tax", "credit", "loan", "funding", "property", "permit", "zoning",
    "medical", "health", "hr", "employment", "franchise", "credential", "password", "token",
}

BUSINESS_LANES = {
    "flux": "Flux & Crave",
    "crave": "Flux & Crave",
    "records": "Focus Records LLC",
    "music": "Focus Records LLC",
    "construction": "Royal Lee Construction Solutions LLC",
    "royal lee": "Royal Lee Construction Solutions LLC",
    "rlc": "Royal Lee Construction Solutions LLC",
    "negotium": "Focus Negotium Inc",
    "focus corp": "The Focus Corporation",
    "the focus": "The Focus Corporation",
}


@dataclasses.dataclass
class EngineRun:
    task: str
    lane: str
    risk: str
    approval_required: bool
    stages: list[dict[str, Any]]
    recommended_next_action: str
    created_at: str = dataclasses.field(default_factory=lambda: dt.datetime.now(dt.UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


def load_json(name: str) -> dict[str, Any]:
    return json.loads((CONFIG_DIR / name).read_text(encoding="utf-8-sig"))


def classify_lane(task: str) -> str:
    lower = task.lower()
    for key, lane in BUSINESS_LANES.items():
        if key in lower:
            return lane
    return "The Focus Corporation / General Focus Engine"


def classify_risk(task: str) -> tuple[str, bool]:
    lower = task.lower()
    hits = sorted(term for term in HIGH_IMPACT_TERMS if term in lower)
    if hits:
        return f"high-impact terms detected: {', '.join(hits)}", True
    return "local planning/drafting risk", False


def build_stage(agent: dict[str, Any], task: str, lane: str, risk: str) -> dict[str, Any]:
    prompt = f"""You are {agent['id']} for the Focus Private AI Engine.
Voice: {agent['voice']}
Mission: {agent['mission']}

Business lane: {lane}
Risk classification: {risk}

User task:
{task}

Return:
1. What you would do next.
2. Files/data you need.
3. Risks or approval gates.
4. Concrete output you would produce.
""".strip()
    return {
        "agent_id": agent["id"],
        "model_lane": agent["lane"],
        "prompt": prompt,
        "status": "prompt_packet_ready",
    }


def create_run(task: str) -> EngineRun:
    board = load_json("agent_board.json")
    lane = classify_lane(task)
    risk, approval_required = classify_risk(task)
    stages = [build_stage(agent, task, lane, risk) for agent in board["agents"]]
    next_action = "Run local drafts/analysis now; request approval before external action." if approval_required else "Safe for local drafting, code edits, and internal QA."
    return EngineRun(task=task, lane=lane, risk=risk, approval_required=approval_required, stages=stages, recommended_next_action=next_action)


def save_run(run: EngineRun) -> Path:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    path = RUNS_DIR / f"focus-engine-run-{stamp}.json"
    path.write_text(json.dumps(run.to_dict(), indent=2), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Focus Private AI Engine multi-agent run packet.")
    parser.add_argument("task", nargs="*", help="Task to route through the Focus engine.")
    parser.add_argument("--save", action="store_true", help="Save run packet to D:/TheFocusFiles/AI-Pipeline/runs")
    args = parser.parse_args(argv)
    task = " ".join(args.task).strip() or "Build a Focus-tailored AI task execution system."
    run = create_run(task)
    payload = run.to_dict()
    if args.save:
        payload["saved_to"] = str(save_run(run))
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
