from __future__ import annotations

try:
    from FOCUS_MASTER_AI.core.engine_registry import run_engine_by_key
    from FOCUS_MASTER_AI.core.master_machine import run_master_machine
    from FOCUS_MASTER_AI.core.memory_manager import MemoryManager
    from FOCUS_MASTER_AI.core.orchestrator import run_multi_engine_workflow
    from FOCUS_MASTER_AI.core.task_classifier import classify_task
    from FOCUS_MASTER_AI.integrations.openai_client import call_gpt
except ImportError:
    from core.engine_registry import run_engine_by_key
    from core.master_machine import run_master_machine
    from core.memory_manager import MemoryManager
    from core.orchestrator import run_multi_engine_workflow
    from core.task_classifier import classify_task
    from integrations.openai_client import call_gpt


def dispatch_task(task: str) -> object:
    task_type = classify_task(task)
    memory = MemoryManager()
    should_log = True

    if task_type in {"multi", "general"}:
        result = run_master_machine(task)
        should_log = False
    elif task_type == "multi_legacy":
        result = run_multi_engine_workflow(task)
    elif task_type in {
        "research",
        "claims",
        "writing",
        "geometry",
        "construction",
        "compliance",
        "frequency",
        "marketing",
        "ai_twin",
        "publish",
        "automation",
    }:
        result = run_engine_by_key(task_type, task)
    elif task_type == "gpt":
        result = {
            "engine": "gpt",
            "status": "completed",
            "output": call_gpt(task),
        }
    else:
        result = {
            "engine": "general",
            "status": "completed",
            "output": f"Processed task without a specialized engine: {task}",
        }

    if should_log:
        memory.log_task(task, result)
    return result
