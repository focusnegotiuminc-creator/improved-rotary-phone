"""External automation hooks."""

from __future__ import annotations


def trigger_external_automation(task: str, task_type: str, result: str) -> None:
    _ = (task, task_type, result)
    return None
