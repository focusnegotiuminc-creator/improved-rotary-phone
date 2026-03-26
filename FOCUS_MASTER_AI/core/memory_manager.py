from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MemoryManager:
    def __init__(self, memory_dir: str = "memory") -> None:
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.task_history_path = self.memory_dir / "task_history.json"
        self.research_cache_path = self.memory_dir / "research_cache.json"
        self._ensure_json_file(self.task_history_path, [])
        self._ensure_json_file(self.research_cache_path, {})

    @staticmethod
    def _ensure_json_file(path: Path, default_value: Any) -> None:
        if not path.exists():
            path.write_text(json.dumps(default_value, indent=2), encoding="utf-8")

    @staticmethod
    def _read_json(path: Path, fallback: Any) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return fallback

    @staticmethod
    def _write_json(path: Path, data: Any) -> None:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def log_task(self, task: str, result: Any) -> None:
        history = self._read_json(self.task_history_path, [])
        history.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "task": task,
                "result": result,
            }
        )
        self._write_json(self.task_history_path, history)

    def recent_tasks(self, limit: int = 10) -> list[dict[str, Any]]:
        history = self._read_json(self.task_history_path, [])
        return history[-limit:]

    def get_research_cache(self, key: str) -> Any:
        cache = self._read_json(self.research_cache_path, {})
        return cache.get(key)

    def set_research_cache(self, key: str, value: Any) -> None:
        cache = self._read_json(self.research_cache_path, {})
        cache[key] = value
        self._write_json(self.research_cache_path, cache)

