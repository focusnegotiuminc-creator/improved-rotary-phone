from __future__ import annotations

try:
    from FOCUS_MASTER_AI.core.memory_manager import MemoryManager
    from FOCUS_MASTER_AI.core.orchestrator import run_multi_engine_workflow
    from FOCUS_MASTER_AI.core.task_classifier import classify_task
    from FOCUS_MASTER_AI.integrations.openai_client import call_gpt
except ImportError:
    from core.memory_manager import MemoryManager
    from core.orchestrator import run_multi_engine_workflow
    from core.task_classifier import classify_task
    from integrations.openai_client import call_gpt


def dispatch_task(task: str) -> object:
    task_type = classify_task(task)
    memory = MemoryManager()

    if task_type == "multi":
        result = run_multi_engine_workflow(task)
    elif task_type == "research":
        result = _run_engine("research_engine", task)
    elif task_type == "claims":
        result = _run_engine("claims_engine", task)
    elif task_type == "writing":
        result = _run_engine("writing_engine", task)
    elif task_type == "geometry":
        result = _run_engine("geometry_engine", task)
    elif task_type == "construction":
        result = _run_engine("construction_engine", task)
    elif task_type == "compliance":
        result = _run_engine("compliance_engine", task)
    elif task_type == "frequency":
        result = _run_engine("frequency_engine", task)
    elif task_type == "marketing":
        result = _run_engine("marketing_engine", task)
    elif task_type == "publish":
        result = _run_engine("publishing_engine", task)
    elif task_type == "automation":
        result = _run_engine("automation_engine", task)
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

    memory.log_task(task, result)
    return result


def _run_engine(module_name: str, task: str) -> dict:
    try:
        from importlib import import_module

        try:
            module = import_module(f"FOCUS_MASTER_AI.engines.{module_name}")
        except ImportError:
            module = import_module(f"engines.{module_name}")
        return module.run(task)
    except Exception as exc:
        return {
            "engine": module_name,
            "status": "degraded",
            "output": f"Engine import or execution failed: {exc}",
        }
