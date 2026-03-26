from __future__ import annotations

import os
from typing import Any

import requests


def trigger_replit(task: str) -> dict[str, Any]:
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

