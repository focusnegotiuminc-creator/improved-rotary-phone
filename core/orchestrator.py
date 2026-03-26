"""Top-level orchestrator for running single or parallel tasks."""

from __future__ import annotations

import concurrent.futures

from core.dispatcher import dispatch_task
from core.memory_manager import MemoryManager
from core.task_classifier import classify_task
from integrations.external_apps import trigger_external_automation


def run_task(task: str) -> str:
    """Run one task through classification, dispatch, storage, and automation."""
    task_type = classify_task(task)
    result = dispatch_task(task)

    memory = MemoryManager()
    memory.append_history(task=task, task_type=task_type, result=result)

    if task_type == "research":
        memory.cache_research(query=task, result=result)

    trigger_external_automation(task=task, task_type=task_type, result=result)
    return result


def run_parallel(tasks: list[str]) -> list[str]:
    """Run many tasks concurrently using a thread pool."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(run_task, tasks)
    return list(results)
