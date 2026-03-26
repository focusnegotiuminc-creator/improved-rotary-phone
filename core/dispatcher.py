"""Task dispatcher that routes tasks to specialized engines."""

from __future__ import annotations

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


def dispatch_task(task: str) -> str:
    """Dispatch a task to the proper specialized engine."""
    task_type = classify_task(task)

    if task_type == "research":
        return research_engine.run(task)
    if task_type == "claims":
        return claims_engine.run(task)
    if task_type == "writing":
        return writing_engine.run(task)
    if task_type == "geometry":
        return geometry_engine.run(task)
    if task_type == "construction":
        return construction_engine.run(task)
    if task_type == "compliance":
        return compliance_engine.run(task)
    if task_type == "frequency":
        return frequency_engine.run(task)
    if task_type == "marketing":
        return marketing_engine.run(task)
    if task_type == "publish":
        return publishing_engine.run(task)
    if task_type == "automation":
        return automation_engine.run(task)

    return "Unknown task"
