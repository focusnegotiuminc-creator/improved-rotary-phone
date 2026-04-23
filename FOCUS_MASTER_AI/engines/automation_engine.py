from __future__ import annotations

try:
    from FOCUS_MASTER_AI.core.engine_runtime import run_ai_engine
except ImportError:
    from core.engine_runtime import run_ai_engine


def run(task: str) -> dict:
    task_lower = task.lower().strip()
    if task_lower == "initialize system and wait for commands":
        return {
            "engine": "automation",
            "status": "completed",
            "state": "waiting",
            "output": "FOCUS MASTER AI initialized and waiting for commands.",
        }

    return run_ai_engine("automation", task, execute_automation=True)

