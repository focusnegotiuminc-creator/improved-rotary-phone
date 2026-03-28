from __future__ import annotations

import concurrent.futures

try:
    from FOCUS_MASTER_AI.core.dispatcher import dispatch_task
except ImportError:
    from core.dispatcher import dispatch_task


def run_parallel(tasks: list[str]) -> list[object]:
    clean_tasks = [task.strip() for task in tasks if task.strip()]

    if not clean_tasks:
        return ["No tasks provided."]

    max_workers = min(8, len(clean_tasks))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(dispatch_task, clean_tasks))

    return results
