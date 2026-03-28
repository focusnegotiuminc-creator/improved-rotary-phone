#!/usr/bin/env python3
"""Configure GitHub Actions secrets and variables for Focus Master deployment."""

from __future__ import annotations

import argparse
import base64
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[2]

SECRET_NAMES = [
    "INFINITYFREE_FTP_HOST",
    "INFINITYFREE_FTP_USER",
    "INFINITYFREE_FTP_PASS",
    "INFINITYFREE_REMOTE_DIR",
    "REPLIT_DEPLOY_HOOK_URL",
    "REPLIT_DEPLOY_WEBHOOK_URL",
    "REPLIT_DEPLOY_TOKEN",
]

SUGGESTED_DEPLOY_PATH = "thefocuscorp.com/htdocs"
SUGGESTED_DEPLOY_PATH_CANDIDATES = (
    "thefocuscorp.com/htdocs,htdocs,domains/thefocuscorp.com/public_html"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set GitHub Actions secrets/variables for Focus Master deployments."
    )
    parser.add_argument(
        "--repo",
        help="Repository in owner/name format. Defaults to origin remote.",
    )
    parser.add_argument(
        "--env-file",
        default=str(ROOT / "focus_ai" / ".env"),
        help="Optional .env file to load values from (default: focus_ai/.env).",
    )
    parser.add_argument(
        "--suggested-deploy-path",
        default=SUGGESTED_DEPLOY_PATH,
        help="Used when INFINITYFREE_REMOTE_DIR is not provided (default: thefocuscorp.com/htdocs).",
    )
    parser.add_argument(
        "--deploy-path-candidates",
        default=SUGGESTED_DEPLOY_PATH_CANDIDATES,
        help="Default value for INFINITYFREE_REMOTE_DIR_CANDIDATES repository variable.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be configured without changing repository settings.",
    )
    return parser.parse_args()


def _run_git(args: list[str], stdin_text: str | None = None) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        input=stdin_text,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout.strip()


def _parse_repo_slug(remote_url: str) -> str:
    url = remote_url.strip()
    if url.startswith("git@github.com:"):
        slug = url.split("git@github.com:", 1)[1]
    elif "github.com/" in url:
        slug = url.split("github.com/", 1)[1]
    else:
        raise ValueError(f"Unsupported remote URL format: {remote_url}")
    return slug.removesuffix(".git").strip("/")


def resolve_repo_slug(repo_arg: str | None) -> str:
    if repo_arg:
        return repo_arg.strip()
    remote = _run_git(["config", "--get", "remote.origin.url"])
    return _parse_repo_slug(remote)


def _token_from_git_credentials() -> str:
    payload = "protocol=https\nhost=github.com\n\n"
    proc = subprocess.run(
        ["git", "credential", "fill"],
        cwd=ROOT,
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return ""
    for line in proc.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    return ""


def resolve_token() -> tuple[str, str]:
    for env_name in ("GH_TOKEN", "GITHUB_TOKEN"):
        token = os.getenv(env_name, "").strip()
        if token:
            return token, env_name
    from_credentials = _token_from_git_credentials()
    if from_credentials:
        return from_credentials, "git-credential"
    return "", ""


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    loaded: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        loaded[key.strip()] = value.strip().strip("'").strip('"')
    return loaded


def encrypt_secret(public_key: str, value: str) -> str:
    try:
        import nacl.encoding
        import nacl.public
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency PyNaCl. Install with: pip install pynacl"
        ) from exc

    key = nacl.public.PublicKey(public_key.encode("utf-8"), nacl.encoding.Base64Encoder())
    sealed_box = nacl.public.SealedBox(key)
    encrypted = sealed_box.encrypt(value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def _request_error(response: requests.Response) -> str:
    try:
        body: Any = response.json()
    except ValueError:
        body = response.text
    if isinstance(body, dict):
        message = body.get("message", "")
        if message:
            return str(message)
    return str(body)


class GitHubRepoActionsConfigurator:
    def __init__(self, token: str, repo_slug: str, dry_run: bool = False) -> None:
        self.token = token
        self.repo_slug = repo_slug
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )
        self._public_key: dict[str, str] | None = None

    def _api(self, suffix: str) -> str:
        return f"https://api.github.com/repos/{self.repo_slug}{suffix}"

    def _load_public_key(self) -> dict[str, str]:
        if self._public_key:
            return self._public_key
        response = self.session.get(self._api("/actions/secrets/public-key"), timeout=30)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to read Actions public key: {_request_error(response)}")
        self._public_key = response.json()
        return self._public_key

    def set_secret(self, name: str, value: str) -> bool:
        if self.dry_run:
            print(f"[dry-run] Secret {name} would be configured.")
            return True

        key_payload = self._load_public_key()
        encrypted_value = encrypt_secret(key_payload["key"], value)
        response = self.session.put(
            self._api(f"/actions/secrets/{name}"),
            json={"encrypted_value": encrypted_value, "key_id": key_payload["key_id"]},
            timeout=30,
        )
        if response.status_code not in {201, 204}:
            print(f"Failed to set secret {name}: {_request_error(response)}", file=sys.stderr)
            return False
        print(f"Configured secret: {name}")
        return True

    def set_variable(self, name: str, value: str) -> bool:
        if self.dry_run:
            print(f"[dry-run] Variable {name}={value} would be configured.")
            return True

        update_response = self.session.patch(
            self._api(f"/actions/variables/{name}"),
            json={"name": name, "value": value},
            timeout=30,
        )
        if update_response.status_code in {201, 204}:
            print(f"Configured variable: {name}")
            return True
        if update_response.status_code != 404:
            print(
                f"Failed to update variable {name}: {_request_error(update_response)}",
                file=sys.stderr,
            )
            return False

        create_response = self.session.post(
            self._api("/actions/variables"),
            json={"name": name, "value": value},
            timeout=30,
        )
        if create_response.status_code not in {201, 204}:
            print(
                f"Failed to create variable {name}: {_request_error(create_response)}",
                file=sys.stderr,
            )
            return False

        print(f"Configured variable: {name}")
        return True


def build_value_map(env_file: Path) -> dict[str, str]:
    values = load_env_file(env_file)
    for key, value in os.environ.items():
        if value:
            values[key] = value
    return values


def main() -> int:
    args = parse_args()
    try:
        repo_slug = resolve_repo_slug(args.repo)
    except Exception as exc:  # noqa: BLE001
        print(f"Unable to determine repository slug: {exc}", file=sys.stderr)
        return 1

    token, source = resolve_token()
    if not token and not args.dry_run:
        print(
            "Missing GitHub token. Set GH_TOKEN/GITHUB_TOKEN or login with git credentials first.",
            file=sys.stderr,
        )
        return 1

    values = build_value_map(Path(args.env_file))
    if source:
        print(f"Using GitHub token source: {source}")
    elif args.dry_run:
        print("No GitHub token found; continuing in dry-run mode.")
    print(f"Configuring repository: {repo_slug}")

    configurator = GitHubRepoActionsConfigurator(
        token=token or "dry-run-token",
        repo_slug=repo_slug,
        dry_run=args.dry_run,
    )

    success = True
    configured = 0
    skipped = 0

    for secret_name in SECRET_NAMES:
        value = values.get(secret_name, "").strip()
        if secret_name == "INFINITYFREE_REMOTE_DIR" and not value:
            value = args.suggested_deploy_path.strip().strip("/")

        if not value:
            print(f"Skipping secret {secret_name}: no value found.")
            skipped += 1
            continue

        if configurator.set_secret(secret_name, value):
            configured += 1
        else:
            success = False

    variable_defaults = {
        "INFINITYFREE_REMOTE_DIR_CANDIDATES": args.deploy_path_candidates.strip(),
        "REPLIT_DEPLOY_METHOD": "POST",
        "REPLIT_DEPLOY_TIMEOUT": "30",
        "FOCUS_APP_URL": "https://thefocuscorp.com",
        "FOCUS_APP_PATHS": "/,/booking.html,/services.html,/products.html,/ebooks/index.html",
        "FOCUS_REQUIRE_ALL_PATHS": "0",
        "FOCUS_SKIP_TLS_VERIFY": "1",
        "INFINITYFREE_STRICT": "0",
    }

    for variable_name, default_value in variable_defaults.items():
        value = values.get(variable_name, default_value).strip()
        if not value:
            continue
        if configurator.set_variable(variable_name, value):
            configured += 1
        else:
            success = False

    print(
        f"Configuration complete: configured={configured}, skipped_secrets={skipped}, success={success}"
    )
    if not args.dry_run:
        print(
            "Next step: run the workflow 'Deploy TheFocusCorp Site' from GitHub Actions to deploy live changes."
        )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
