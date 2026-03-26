from __future__ import annotations

from core.memory_manager import MemoryManager
from core.orchestrator import run_multi_engine_workflow
from core.task_classifier import classify_task
from engines import (
    automation_engine,
    claims_engine,
    compliance_engine,
    construction_engine,
    frequency_engine,
    geometry_engine,
    marketing_engine,
    publishing_engine,
    research_engine,
    writing_engine,
)
from integrations.openai_client import call_gpt


def dispatch_task(task: str) -> object:
    task_type = classify_task(task)
    memory = MemoryManager()

    if task_type == "multi":
        result = run_multi_engine_workflow(task)
    elif task_type == "research":
        result = research_engine.run(task)
    elif task_type == "claims":
        result = claims_engine.run(task)
    elif task_type == "writing":
        result = writing_engine.run(task)
    elif task_type == "geometry":
        result = geometry_engine.run(task)
    elif task_type == "construction":
        result = construction_engine.run(task)
    elif task_type == "compliance":
        result = compliance_engine.run(task)
    elif task_type == "frequency":
        result = frequency_engine.run(task)
    elif task_type == "marketing":
        result = marketing_engine.run(task)
    elif task_type == "publish":
        result = publishing_engine.run(task)
    elif task_type == "automation":
        result = automation_engine.run(task)
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

