#!/usr/bin/env python3
"""Trigger a Replit deployment webhook/hook from CI or local shell.

Required env vars:
- REPLIT_DEPLOY_HOOK_URL (or REPLIT_DEPLOY_WEBHOOK_URL)

Optional env vars:
- REPLIT_DEPLOY_TOKEN (Bearer token)
- REPLIT_DEPLOY_TIMEOUT (seconds, default: 30)
- REPLIT_DEPLOY_METHOD (POST or GET, default: POST)
- FOCUS_APP_URL (used only in payload metadata)
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

import requests


def _truthy(value: str | None) -> bool:
    if not value:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _build_payload() -> dict[str, Any]:
    return {
        "source": "github-actions",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "github_sha": os.getenv("GITHUB_SHA", ""),
        "github_ref": os.getenv("GITHUB_REF", ""),
        "repository": os.getenv("GITHUB_REPOSITORY", ""),
        "target_url": os.getenv("FOCUS_APP_URL", "https://thefocuscorp.com"),
        "deploy_scope": "focus_ai_public_site",
    }


def main() -> int:
    hook_url = (
        os.getenv("REPLIT_DEPLOY_HOOK_URL", "").strip()
        or os.getenv("REPLIT_DEPLOY_WEBHOOK_URL", "").strip()
    )
    if not hook_url:
        print("Missing REPLIT_DEPLOY_HOOK_URL/REPLIT_DEPLOY_WEBHOOK_URL.")
        print("Strict deploy mode requires deploy credentials for every run.")
        return 1

    method = os.getenv("REPLIT_DEPLOY_METHOD", "POST").strip().upper() or "POST"
    timeout = int(os.getenv("REPLIT_DEPLOY_TIMEOUT", "30"))
    token = os.getenv("REPLIT_DEPLOY_TOKEN", "").strip()

    headers = {"User-Agent": "FocusAI-ReplitDeploy/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = _build_payload()
    verify_tls = not _truthy(os.getenv("FOCUS_SKIP_TLS_VERIFY"))

    try:
        if method == "GET":
            response = requests.get(
                hook_url,
                params=payload,
                headers=headers,
                timeout=timeout,
                verify=verify_tls,
            )
        else:
            headers["Content-Type"] = "application/json"
            response = requests.post(
                hook_url,
                data=json.dumps(payload),
                headers=headers,
                timeout=timeout,
                verify=verify_tls,
            )
    except requests.RequestException as exc:
        print(f"Replit deploy trigger failed: {exc}")
        return 1

    snippet = (response.text or "").strip()[:240]
    print(f"Replit deploy hook response: status={response.status_code} ok={response.ok}")
    if snippet:
        print(f"Response snippet: {snippet}")

    return 0 if response.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
