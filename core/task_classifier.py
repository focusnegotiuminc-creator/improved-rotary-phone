"""Task classification utilities for the multi-agent system."""

from __future__ import annotations


def classify_task(task: str) -> str:
    """Classify a task string into a supported task type."""
    task_lower = task.lower()

    if "research" in task_lower:
        return "research"
    if "claim" in task_lower:
        return "claims"
    if "write" in task_lower or "book" in task_lower:
        return "writing"
    if "geometry" in task_lower or "design" in task_lower:
        return "geometry"
    if "build" in task_lower or "construction" in task_lower:
        return "construction"
    if "legal" in task_lower or "code compliance" in task_lower:
        return "compliance"
    if "chakra" in task_lower or "frequency" in task_lower:
        return "frequency"
    if "marketing" in task_lower or "sales" in task_lower:
        return "marketing"
    if "publish" in task_lower:
        return "publish"
    if "automate" in task_lower or "automation" in task_lower:
        return "automation"

    return "unknown"
