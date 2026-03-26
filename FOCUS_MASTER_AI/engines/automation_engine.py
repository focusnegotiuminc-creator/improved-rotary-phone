from __future__ import annotations

from integrations.external_apps import route_ai
from integrations.make_webhook import trigger_make
from integrations.replit_runner import trigger_replit


def run(task: str) -> dict:
    task_lower = task.lower().strip()
    if task_lower == "initialize system and wait for commands":
        return {
            "engine": "automation",
            "status": "completed",
            "state": "waiting",
            "output": "FOCUS MASTER AI initialized and waiting for commands.",
        }

    route_hint = route_ai(task)
    make_result = trigger_make(task, {"route_hint": route_hint})
    replit_result = trigger_replit(task)

    return {
        "engine": "automation",
        "status": "completed",
        "route_hint": route_hint,
        "make": make_result,
        "replit": replit_result,
    }

