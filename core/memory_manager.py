"""Simple JSON-backed memory manager for task history and cache."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class MemoryManager:
    root: Path = Path("memory")

    def __post_init__(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.task_history_path = self.root / "task_history.json"
        self.research_cache_path = self.root / "research_cache.json"
        self.vector_store_path = self.root / "vector_store"
        self.vector_store_path.mkdir(parents=True, exist_ok=True)

        self._init_json_file(self.task_history_path, [])
        self._init_json_file(self.research_cache_path, {})

    @staticmethod
    def _init_json_file(path: Path, default: Any) -> None:
        if not path.exists():
            path.write_text(json.dumps(default, indent=2), encoding="utf-8")

    def append_history(self, task: str, task_type: str, result: str) -> None:
        history = self.read_json(self.task_history_path, [])
        history.append(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "task": task,
                "task_type": task_type,
                "result": result,
            }
        )
        self.task_history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def cache_research(self, query: str, result: str) -> None:
        cache = self.read_json(self.research_cache_path, {})
        cache[query] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "result": result,
        }
        self.research_cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")

    @staticmethod
    def read_json(path: Path, default: Any) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return default
