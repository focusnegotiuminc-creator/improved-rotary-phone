#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = Path(r"C:\Users\reggi\OneDrive\Documents\GitHub\_cloudflare_build\focus-mobile-workbench")
DEV_VARS = RUNNER / ".dev.vars"
REPORT = ROOT / "docs" / "manifests" / "focus_mobile_workbench_qa_report.md"
BASE_URL = "http://127.0.0.1:8787"


def load_dev_vars(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return values


def request_json(
    opener: urllib.request.OpenerDirector,
    path: str,
    *,
    method: str = "GET",
    payload: dict[str, object] | None = None,
) -> tuple[int, dict[str, object]]:
    body = None
    headers = {"content-type": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        urllib.parse.urljoin(BASE_URL, path),
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def write_report(lines: list[str]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    values = load_dev_vars(DEV_VARS)
    cookies = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))

    checks: list[tuple[str, bool, str]] = []

    status_code, status_payload = request_json(opener, "/api/status")
    checks.append(
        (
            "unauthenticated status gate",
            status_code == 401 and status_payload.get("ok") is False,
            f"status={status_code}",
        )
    )

    login_code, login_payload = request_json(
        opener,
        "/api/session",
        method="POST",
        payload={"password": values.get("PRIVATE_APP_PASSWORD", "")},
    )
    checks.append(
        (
            "session login",
            login_code == 200 and login_payload.get("ok") is True,
            f"status={login_code}",
        )
    )

    auth_status_code, auth_status_payload = request_json(opener, "/api/status")
    stacks = auth_status_payload.get("stacks", []) if isinstance(auth_status_payload, dict) else []
    bridges = auth_status_payload.get("toolBridges", []) if isinstance(auth_status_payload, dict) else []
    checks.append(
        (
            "authenticated status payload",
            auth_status_code == 200
            and auth_status_payload.get("ok") is True
            and len(stacks) >= 6
            and len(bridges) >= 6,
            f"status={auth_status_code}, stacks={len(stacks)}, bridges={len(bridges)}",
        )
    )

    run_code, run_payload = request_json(
        opener,
        "/api/run",
        method="POST",
        payload={
            "stackId": "website_delivery_stack",
            "provider": "fallback",
            "toolIds": ["github_workspace", "artifact_archive"],
            "prompt": "Create a private execution plan for a storefront update and summarize next actions.",
            "documentText": "Keep the public site business-facing and list a clean operator follow-up sequence.",
        },
    )
    run = run_payload.get("run", {}) if isinstance(run_payload, dict) else {}
    checks.append(
        (
            "fallback run execution",
            run_code == 200
            and run_payload.get("ok") is True
            and run.get("provider") == "fallback"
            and "Website Delivery Stack" in str(run.get("output", "")),
            f"status={run_code}, provider={run.get('provider', 'n/a')}",
        )
    )

    timestamp = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Focus Mobile Workbench QA Report",
        "",
        f"Generated: {timestamp}",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    for label, ok, detail in checks:
        lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |")
    write_report(lines)

    if not all(ok for _, ok, _ in checks):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
