from __future__ import annotations

from typing import Any

try:
    from FOCUS_MASTER_AI.core.connector_status import build_connector_status
    from FOCUS_MASTER_AI.core.engine_registry import run_engine_by_key
    from FOCUS_MASTER_AI.core.memory_manager import MemoryManager
    from FOCUS_MASTER_AI.core.prompt_studio import build_master_task_packet
except ImportError:
    from core.connector_status import build_connector_status
    from core.engine_registry import run_engine_by_key
    from core.memory_manager import MemoryManager
    from core.prompt_studio import build_master_task_packet


def run_master_machine(task: str) -> dict[str, Any]:
    packet = build_master_task_packet(task)
    results: list[dict[str, Any]] = []
    for engine_key in packet["engine_sequence"]:
        results.append({"engine": engine_key, "result": run_engine_by_key(engine_key, task)})

    outcome = {
        "workflow": "focus_master_ai_powerhouse",
        "status": "completed",
        "task": task,
        "task_packet": packet,
        "connectors": build_connector_status(),
        "results": results,
    }

    MemoryManager().log_task(task, outcome)
    return outcome
