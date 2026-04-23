"""Top-level orchestrator for running single or parallel tasks."""

from __future__ import annotations

import concurrent.futures
from typing import Any

from core.dispatcher import dispatch_task
from core.memory_manager import MemoryManager
from core.task_classifier import classify_task
from integrations.external_apps import trigger_external_automation


def _legacy_engine_name(label: str, task_type: str) -> str:
    text = (label or "").replace("_", " ").strip()
    if not text:
        text = task_type.replace("_", " ").strip().capitalize() or "Task"

    parts = text.split()
    if not parts:
        return "Task engine"
    if parts[-1].lower() == "engine":
        parts[-1] = "engine"
    elif "engine" not in text.lower():
        parts.append("engine")
    return " ".join(parts)


def _with_legacy_engine(summary: str, label: str, task_type: str, task: str) -> str:
    text = (summary or "").strip()
    if not text:
        return f"{_legacy_engine_name(label, task_type)} completed task: {task}"
    lower = text.lower()
    if "completed task:" in lower and "engine completed task" not in lower:
        head, tail = text.split("completed task:", 1)
        return f"{_legacy_engine_name(head.strip(), task_type)} completed task:{tail}"
    return text


def _result_summary(result: Any, task_type: str, task: str) -> str:
    """Collapse structured engine payloads into the legacy status-string format."""
    if isinstance(result, str):
        return _with_legacy_engine(result, task_type, task_type, task)

    engine_name = ""
    if isinstance(result, dict):
        label = result.get("label") or result.get("engine") or task_type
        output = result.get("output")
        if isinstance(output, dict):
            nested_result = output.get("result")
            if isinstance(nested_result, str) and nested_result:
                return _with_legacy_engine(nested_result, str(label), task_type, task)

        if isinstance(label, str) and label.strip():
            engine_name = _legacy_engine_name(label, task_type)

        if isinstance(output, str) and output.strip():
            return f"{engine_name or _legacy_engine_name('', task_type)} completed task: {task}"

    if not engine_name:
        engine_name = _legacy_engine_name("", task_type)
    return f"{engine_name} completed task: {task}"


def run_task(task: str) -> str:
    """Run one task through classification, dispatch, storage, and automation."""
    task_type = classify_task(task)
    raw_result = dispatch_task(task)
    result = _result_summary(raw_result, task_type, task)

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
