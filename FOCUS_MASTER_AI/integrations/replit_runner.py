from __future__ import annotations

import os
from typing import Any

import requests

try:
    from FOCUS_MASTER_AI.core.runtime_config import bootstrap_runtime_env
except ImportError:  # pragma: no cover
    from core.runtime_config import bootstrap_runtime_env


def trigger_replit(task: str) -> dict[str, Any]:
    bootstrap_runtime_env()
    endpoint = os.getenv("REPLIT_RUNNER_URL", "").strip()
    if not endpoint:
        return {
            "ok": False,
            "status": None,
            "message": "REPLIT_RUNNER_URL is not configured.",
        }

    try:
        response = requests.post(endpoint, json={"task": task}, timeout=20)
        return {
            "ok": response.ok,
            "status": response.status_code,
            "message": response.text[:200] if response.text else "",
        }
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": None,
            "message": f"Replit trigger failed: {exc}",
        }

