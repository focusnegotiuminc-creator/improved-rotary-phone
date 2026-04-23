from __future__ import annotations

try:
    from FOCUS_MASTER_AI.core.master_machine import run_master_machine
except ImportError:
    from core.master_machine import run_master_machine


def run_multi_engine_workflow(task: str) -> dict:
    return run_master_machine(task)
