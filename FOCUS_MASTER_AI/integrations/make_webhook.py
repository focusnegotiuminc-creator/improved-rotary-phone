from __future__ import annotations

import os
from typing import Any

import requests


def trigger_make(task: str, extra_payload: dict[str, Any] | None = None) -> dict:
    webhook = os.getenv("MAKE_WEBHOOK_URL", "").strip()
    if not webhook:
        return {
            "ok": False,
            "status": None,
            "message": "MAKE_WEBHOOK_URL is not configured.",
        }

    payload: dict[str, Any] = {"task": task}
    if extra_payload:
        payload.update(extra_payload)

    try:
        response = requests.post(webhook, json=payload, timeout=20)
        return {
            "ok": response.ok,
            "status": response.status_code,
            "message": response.text[:200] if response.text else "",
        }
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": None,
            "message": f"Make webhook call failed: {exc}",
        }

