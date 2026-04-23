from __future__ import annotations

import os
from typing import Any

import requests

try:
    from FOCUS_MASTER_AI.core.runtime_config import bootstrap_runtime_env
except ImportError:  # pragma: no cover
    from core.runtime_config import bootstrap_runtime_env

_LAST_REPLIT_STATUS = {
    "state": "unknown",
    "message": "Replit runner has not been exercised in this runtime yet.",
}


def get_replit_runtime_status() -> dict[str, str]:
    return dict(_LAST_REPLIT_STATUS)


def trigger_replit(task: str) -> dict[str, Any]:
    bootstrap_runtime_env()
    endpoint = os.getenv("REPLIT_RUNNER_URL", "").strip()
    if not endpoint:
        _LAST_REPLIT_STATUS.update(
            {
                "state": "attention",
                "message": "REPLIT_RUNNER_URL is not configured.",
            }
        )
        return {
            "ok": False,
            "status": None,
            "message": "REPLIT_RUNNER_URL is not configured.",
        }

    try:
        response = requests.post(endpoint, json={"task": task}, timeout=20)
        _LAST_REPLIT_STATUS.update(
            {
                "state": "ready" if response.ok else "attention",
                "message": response.text[:200] if response.text else f"Replit returned HTTP {response.status_code}.",
            }
        )
        return {
            "ok": response.ok,
            "status": response.status_code,
            "message": response.text[:200] if response.text else "",
        }
    except requests.RequestException as exc:
        _LAST_REPLIT_STATUS.update(
            {
                "state": "attention",
                "message": f"Replit trigger failed: {exc}",
            }
        )
        return {
            "ok": False,
            "status": None,
            "message": f"Replit trigger failed: {exc}",
        }

