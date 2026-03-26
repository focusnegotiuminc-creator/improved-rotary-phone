"""Task orchestration for FOCUS MASTER AI."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict


@dataclass(frozen=True)
class TaskResult:
    task_type: str
    module: str
    action: str
    timestamp_utc: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "task_type": self.task_type,
            "module": self.module,
            "action": self.action,
            "timestamp_utc": self.timestamp_utc,
        }


TASK_MAP = {
    "build": ("BUILD", "core.automation_engine", "Routing to build module"),
    "automate": (
        "AUTOMATE",
        "workflows.make_scenarios",
        "Triggering Make webhook",
    ),
    "create": ("CREATE", "core.content_engine", "Routing to content engine"),
    "deploy": ("DEPLOY", "core.api_router", "Sending to Replit"),
    "market": ("MARKET", "modules.marketing", "Launching marketing engine"),
}


def classify_task(task: str) -> TaskResult:
    normalized = task.lower()
    now = datetime.now(timezone.utc).isoformat()
    for keyword, (task_type, module, action) in TASK_MAP.items():
        if keyword in normalized:
            return TaskResult(task_type, module, action, now)
    return TaskResult("UNKNOWN", "core.orchestration", "Task not recognized", now)


def run_task(task: str) -> str:
    """Route commands by intent and return a concise status string."""
    result = classify_task(task)
    return (
        f"[{result.timestamp_utc}] task_type={result.task_type} "
        f"module={result.module} action={result.action}"
    )
