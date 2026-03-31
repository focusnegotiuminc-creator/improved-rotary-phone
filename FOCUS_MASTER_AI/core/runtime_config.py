from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
_BOOTSTRAPPED = False
_LOADED_FILES: list[str] = []


def _candidate_env_files() -> list[Path]:
    home = Path.home()
    return [
        REPO_ROOT / ".env",
        REPO_ROOT / ".secrets" / "focus_master.env",
        REPO_ROOT.parent / ".secrets" / "focus_master.env",
        REPO_ROOT.parent / "GitHub" / "Focus--Master" / ".secrets" / "focus_master.env",
        home / "OneDrive" / "Documents" / "GitHub" / "Focus--Master" / ".secrets" / "focus_master.env",
    ]


def _first_nonempty(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def _extract_openai_key() -> str:
    direct = _first_nonempty("OPENAI_API_KEY_PRIMARY", "OPENAI_API_KEY")
    if direct:
        return direct

    multi_key_block = os.getenv("OPENAI_API_KEYS", "").strip()
    if not multi_key_block:
        return ""

    for token in re.split(r"[\s,;]+", multi_key_block):
        cleaned = token.strip().strip("'").strip('"')
        if cleaned.startswith("sk-"):
            return cleaned
    return ""


def _detect_github_repo() -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""

    remote = result.stdout.strip()
    if not remote:
        return ""

    match = re.search(r"github\.com[:/](?P<repo>[^/\s]+/[^/\s]+?)(?:\.git)?$", remote)
    return match.group("repo") if match else ""


def git_remote_healthcheck() -> dict[str, Any]:
    bootstrap_runtime_env()
    repo = os.getenv("GITHUB_REPO", "").strip() or _detect_github_repo()
    if not repo:
        return {
            "reachable": False,
            "repo": "",
            "message": "Git origin is not configured as a GitHub repository.",
        }

    try:
        result = subprocess.run(
            ["git", "ls-remote", "origin", "-h", "refs/heads/main"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=12,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "reachable": False,
            "repo": repo,
            "message": f"Git remote check failed: {exc}",
        }

    if result.returncode == 0:
        return {
            "reachable": True,
            "repo": repo,
            "message": f"Git remote is reachable for {repo}.",
        }

    detail = (result.stderr or result.stdout or "").strip()
    return {
        "reachable": False,
        "repo": repo,
        "message": detail[:180] or "Git remote could not be reached.",
    }


def bootstrap_runtime_env() -> dict[str, Any]:
    global _BOOTSTRAPPED
    if _BOOTSTRAPPED:
        return {
            "loaded_files": list(_LOADED_FILES),
            "github_repo": os.getenv("GITHUB_REPO", "").strip(),
        }

    loaded_files: list[str] = []
    for env_file in _candidate_env_files():
        if env_file.exists():
            load_dotenv(env_file, override=False)
            loaded_files.append(str(env_file))

    if not os.getenv("OPENAI_API_KEY", "").strip():
        openai_key = _extract_openai_key()
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key

    if not os.getenv("DEFAULT_OPENAI_MODEL", "").strip():
        selected_model = _first_nonempty("OPENAI_MODEL", "DEFAULT_OPENAI_MODEL")
        if selected_model:
            os.environ["DEFAULT_OPENAI_MODEL"] = selected_model

    if not os.getenv("MAKE_WEBHOOK_URL", "").strip():
        make_url = _first_nonempty("MAKE_MCP_SERVER_URL", "MAKE_WEBHOOK_URL")
        if make_url:
            os.environ["MAKE_WEBHOOK_URL"] = make_url

    if not os.getenv("REPLIT_RUNNER_URL", "").strip():
        replit_url = _first_nonempty(
            "REPLIT_RUNNER_URL",
            "REPLIT_ENDPOINT",
            "REPLIT_DEPLOY_HOOK_URL",
            "REPLIT_DEPLOY_WEBHOOK_URL",
        )
        if replit_url:
            os.environ["REPLIT_RUNNER_URL"] = replit_url

    if not os.getenv("GITHUB_REPO", "").strip():
        repo = _detect_github_repo()
        if repo:
            os.environ["GITHUB_REPO"] = repo

    _LOADED_FILES[:] = loaded_files
    _BOOTSTRAPPED = True
    return {
        "loaded_files": list(_LOADED_FILES),
        "github_repo": os.getenv("GITHUB_REPO", "").strip(),
    }
