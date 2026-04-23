from __future__ import annotations

import os
from typing import Any

import requests

try:
    from FOCUS_MASTER_AI.core.runtime_config import bootstrap_runtime_env
except ImportError:  # pragma: no cover
    from core.runtime_config import bootstrap_runtime_env

_LAST_MAKE_STATUS = {
    "state": "unknown",
    "message": "Make webhook has not been exercised in this runtime yet.",
}


def get_make_runtime_status() -> dict[str, str]:
    return dict(_LAST_MAKE_STATUS)


def trigger_make(task: str, extra_payload: dict[str, Any] | None = None) -> dict:
    bootstrap_runtime_env()
    webhook = os.getenv("MAKE_WEBHOOK_URL", "").strip()
    if not webhook:
        _LAST_MAKE_STATUS.update(
            {
                "state": "attention",
                "message": "MAKE_WEBHOOK_URL is not configured.",
            }
        )
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
        _LAST_MAKE_STATUS.update(
            {
                "state": "ready" if response.ok else "attention",
                "message": response.text[:200] if response.text else f"Make returned HTTP {response.status_code}.",
            }
        )
        return {
            "ok": response.ok,
            "status": response.status_code,
            "message": response.text[:200] if response.text else "",
        }
    except requests.RequestException as exc:
        _LAST_MAKE_STATUS.update(
            {
                "state": "attention",
                "message": f"Make webhook call failed: {exc}",
            }
        )
        return {
            "ok": False,
            "status": None,
            "message": f"Make webhook call failed: {exc}",
        }

