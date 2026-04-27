from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunStore:
    def __init__(self, runtime_dir: Path | None = None) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        configured_runtime = os.getenv("FOCUS_MASTER_RUNTIME_DIR", "").strip()
        self.runtime_dir = runtime_dir or (
            Path(configured_runtime)
            if configured_runtime
            else repo_root / "FOCUS_MASTER_AI" / "data" / "business_os_runtime"
        )
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.runtime_dir / "engine_runs.json"
        self._lock = RLock()
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _read(self) -> list[dict[str, Any]]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def _write(self, runs: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(runs, indent=2), encoding="utf-8")

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            runs = self._read()
            run = {
                "id": f"run_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
                "created_at": _utc_now(),
                "updated_at": _utc_now(),
                "status": "queued",
                "events": [],
                **payload,
            }
            runs.append(run)
            self._write(runs)
            return run

    def list(self, limit: int | None = None) -> list[dict[str, Any]]:
        runs = list(reversed(self._read()))
        return runs[:limit] if limit else runs

    def get(self, run_id: str) -> dict[str, Any] | None:
        for run in self._read():
            if run.get("id") == run_id:
                return run
        return None

    def update(self, run_id: str, **changes: Any) -> dict[str, Any] | None:
        with self._lock:
            runs = self._read()
            for run in runs:
                if run.get("id") != run_id:
                    continue
                run.update(changes)
                run["updated_at"] = _utc_now()
                self._write(runs)
                return run
        return None

    def append_event(self, run_id: str, kind: str, message: str, **extra: Any) -> dict[str, Any] | None:
        with self._lock:
            runs = self._read()
            for run in runs:
                if run.get("id") != run_id:
                    continue
                event = {
                    "timestamp_utc": _utc_now(),
                    "kind": kind,
                    "message": message,
                }
                if extra:
                    event["data"] = extra
                run.setdefault("events", []).append(event)
                run["updated_at"] = _utc_now()
                self._write(runs)
                return run
        return None
