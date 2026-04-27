from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-").lower()
    return cleaned or "artifact"


class ArtifactStore:
    def __init__(self, runtime_dir: Path | None = None) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        configured_runtime = os.getenv("FOCUS_MASTER_RUNTIME_DIR", "").strip()
        self.runtime_dir = runtime_dir or (
            Path(configured_runtime)
            if configured_runtime
            else repo_root / "FOCUS_MASTER_AI" / "data" / "business_os_runtime"
        )
        self.base_dir = self.runtime_dir / "artifacts"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()

    def _run_dir(self, run_id: str) -> Path:
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def _manifest_path(self, run_id: str) -> Path:
        return self._run_dir(run_id) / "manifest.json"

    def _read_manifest(self, run_id: str) -> list[dict[str, Any]]:
        path = self._manifest_path(run_id)
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def _write_manifest(self, run_id: str, items: list[dict[str, Any]]) -> None:
        self._manifest_path(run_id).write_text(json.dumps(items, indent=2), encoding="utf-8")

    def create(
        self,
        run_id: str,
        *,
        name: str,
        content: str,
        kind: str = "text",
        extension: str = ".md",
        content_type: str = "text/markdown",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        filename = f"{_slugify(name)}{extension}"
        path = self._run_dir(run_id) / filename
        path.write_text(content, encoding="utf-8")
        item = {
            "name": name,
            "kind": kind,
            "path": str(path),
            "filename": filename,
            "content_type": content_type,
            "created_at": _utc_now(),
        }
        if metadata:
            item["metadata"] = metadata

        with self._lock:
            manifest = self._read_manifest(run_id)
            manifest.append(item)
            self._write_manifest(run_id, manifest)
        return item

    def create_json(self, run_id: str, *, name: str, payload: Any, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.create(
            run_id,
            name=name,
            content=json.dumps(payload, indent=2),
            kind="json",
            extension=".json",
            content_type="application/json",
            metadata=metadata,
        )

    def list(self, run_id: str) -> list[dict[str, Any]]:
        return self._read_manifest(run_id)
