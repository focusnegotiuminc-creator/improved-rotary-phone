from __future__ import annotations

try:
    from FOCUS_MASTER_AI.core.engine_runtime import run_ai_engine
except ImportError:
    from core.engine_runtime import run_ai_engine


def run(task: str) -> dict:
    return run_ai_engine("frequency", task)

