#!/usr/bin/env python3
"""Launch and verify the full Focus Master live stack from one command."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import os
import subprocess
import sys

import requests


REPO_ROOT = Path(__file__).resolve().parents[2]
FOCUS_ROOT = REPO_ROOT / "focus_ai"
SECRETS_FILE = REPO_ROOT / ".secrets" / "focus_master.env"
REPORT_FILE = FOCUS_ROOT / "docs" / "live_stack_report.md"
LOCAL_GH = REPO_ROOT / "tools" / "gh" / "bin" / "gh.exe"
FALLBACK_GH = REPO_ROOT.parent / "tools" / "gh" / "bin" / "gh.exe"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def mask_secret(value: str) -> str:
    if len(value) <= 10:
        return "***"
    return f"{value[:6]}...{value[-4:]}"


def run_cmd(cmd: list[str], env: dict[str, str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=env,
            check=False,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:
        return 127, str(exc)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output.strip()


def openai_probe(
    key: str, model: str, mcp_label: str, mcp_url: str, timeout: int = 60
) -> tuple[str, bool, str]:
    payload = {
        "model": model,
        "input": "List all available tools.",
        "tools": [
            {
                "type": "mcp",
                "server_label": mcp_label,
                "server_url": mcp_url,
            }
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            json=payload,
            headers=headers,
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover
        return mask_secret(key), False, f"request_error: {exc}"

    if response.ok:
        return mask_secret(key), True, f"http_{response.status_code}"
    return mask_secret(key), False, f"http_{response.status_code}"


def run_engine_smoke() -> tuple[bool, str]:
    sys.path.insert(0, str(REPO_ROOT))
    from core.orchestrator import run_parallel

    tasks = [
        "research sacred geometry market demand",
        "claim verification for legacy build narratives",
        "write a conversion chapter for the sacred system",
        "geometry design for golden ratio layout",
        "construction optimization for modular build",
        "legal code compliance pass",
        "chakra frequency alignment for rooms",
        "marketing funnel optimization for high ticket leads",
        "publish the latest system outputs",
        "automation handoff for recurrent generation",
    ]
    results = run_parallel(tasks)
    ok = len(results) == len(tasks) and all("completed task" in r for r in results)
    return ok, f"processed={len(results)}"


def main() -> int:
    file_env = load_env_file(SECRETS_FILE)
    env = os.environ.copy()
    env.update(file_env)

    lines: list[str] = []
    lines.append("# Live Stack Report")
    lines.append("")
    lines.append(f"- Timestamp (UTC): {now_utc()}")
    lines.append(f"- Secrets file loaded: {'yes' if file_env else 'no'}")
    lines.append("")

    steps = [
        ("go_live", [sys.executable, str(FOCUS_ROOT / "scripts" / "github_ops.py"), "go-live"]),
        ("verify_visuals", [sys.executable, str(FOCUS_ROOT / "scripts" / "verify_visuals.py")]),
        ("build_final_system", [sys.executable, str(FOCUS_ROOT / "scripts" / "build_final_system.py")]),
        ("export_replit_bundle", [sys.executable, str(FOCUS_ROOT / "scripts" / "export_replit_bundle.py")]),
    ]

    lines.append("## Core Pipeline")
    core_ok = True
    for name, cmd in steps:
        code, output = run_cmd(cmd, env)
        ok = code == 0
        if not ok:
            core_ok = False
        lines.append(f"- {name}: {'ok' if ok else f'failed ({code})'}")
        if not ok and output:
            lines.append(f"  - detail: {output.splitlines()[-1]}")
    lines.append("")

    lines.append("## Engine Smoke")
    try:
        smoke_ok, smoke_detail = run_engine_smoke()
        lines.append(f"- orchestrator_parallel: {'ok' if smoke_ok else 'failed'} ({smoke_detail})")
    except Exception as exc:  # pragma: no cover
        smoke_ok = False
        lines.append(f"- orchestrator_parallel: failed ({exc})")
    lines.append("")

    lines.append("## API Probe")
    model = env.get("OPENAI_MODEL", "gpt-4.1")
    mcp_label = env.get("MAKE_MCP_SERVER_LABEL", "make")
    mcp_url = env.get("MAKE_MCP_SERVER_URL", "")
    raw_keys = [k.strip() for k in env.get("OPENAI_API_KEYS", "").split(",") if k.strip()]
    if raw_keys and mcp_url:
        with ThreadPoolExecutor(max_workers=min(6, len(raw_keys))) as pool:
            futures = [pool.submit(openai_probe, key, model, mcp_label, mcp_url) for key in raw_keys]
            for fut in as_completed(futures):
                masked_key, ok, detail = fut.result()
                lines.append(f"- {masked_key}: {'ok' if ok else 'failed'} ({detail})")
    else:
        lines.append("- skipped (missing OPENAI_API_KEYS or MAKE_MCP_SERVER_URL)")
    lines.append("")

    lines.append("## GitHub PR Merge")
    if LOCAL_GH.exists():
        gh_bin = str(LOCAL_GH)
    elif FALLBACK_GH.exists():
        gh_bin = str(FALLBACK_GH)
    else:
        gh_bin = "gh"
    gh_check_code, _ = run_cmd([gh_bin, "--version"], env)
    if gh_check_code != 0:
        lines.append("- merge_prs: blocked (gh not available)")
    else:
        auth_code, auth_out = run_cmd([gh_bin, "auth", "status"], env)
        if auth_code != 0:
            lines.append("- merge_prs: blocked (gh not authenticated)")
            if auth_out:
                lines.append(f"  - detail: {auth_out.splitlines()[-1]}")
        else:
            code, output = run_cmd(
                [
                    sys.executable,
                    str(FOCUS_ROOT / "scripts" / "github_ops.py"),
                    "merge-prs",
                    "--repo",
                    "thegreatmachevilli/Focus--Master",
                ],
                {**env, "PATH": f"{str(Path(gh_bin).parent)};{env.get('PATH', '')}"},
            )
            lines.append(f"- merge_prs: {'ok' if code == 0 else f'failed ({code})'}")
            if code != 0 and output:
                lines.append(f"  - detail: {output.splitlines()[-1]}")
    lines.append("")

    lines.append("## Deployment")
    deploy_code, deploy_out = run_cmd(
        [sys.executable, str(FOCUS_ROOT / "scripts" / "deploy_infinityfree.py")], env
    )
    lines.append(f"- infinityfree_deploy: {'ok' if deploy_code == 0 else f'failed ({deploy_code})'}")
    if deploy_out:
        lines.append(f"  - detail: {deploy_out.splitlines()[-1]}")
    lines.append("")

    lines.append("## Summary")
    if core_ok and smoke_ok:
        lines.append("- Core stack is live locally and deployment artifacts are refreshed.")
    else:
        lines.append("- Core stack has failures; inspect details above.")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote report: {REPORT_FILE}")
    return 0 if core_ok and smoke_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
