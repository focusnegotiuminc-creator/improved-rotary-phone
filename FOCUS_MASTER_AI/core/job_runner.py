from __future__ import annotations

import os
from concurrent.futures import Future, ThreadPoolExecutor
from threading import RLock
from typing import Callable


class BackgroundRunExecutor:
    def __init__(self) -> None:
        self.max_workers = int(os.getenv("FOCUS_MASTER_MAX_WORKERS", "4"))
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="focus-master-run")
        self._lock = RLock()
        self._jobs: dict[str, Future] = {}

    def submit(self, run_id: str, fn: Callable[[], object]) -> None:
        future = self._executor.submit(fn)
        with self._lock:
            self._jobs[run_id] = future
        future.add_done_callback(lambda _future, key=run_id: self._forget(key))

    def _forget(self, run_id: str) -> None:
        with self._lock:
            self._jobs.pop(run_id, None)

    def status_snapshot(self) -> dict[str, object]:
        with self._lock:
            active = list(self._jobs.keys())
        return {
            "active_jobs": active,
            "active_count": len(active),
            "max_workers": self.max_workers,
        }


EXECUTOR = BackgroundRunExecutor()
