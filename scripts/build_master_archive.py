#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
DESKTOP = HOME / "OneDrive" / "Desktop"
ONEDRIVE_ARCHIVES = HOME / "OneDrive" / "Archives"
DRIVE_EXPORTS = Path(r"G:\My Drive\FOCUS_MASTER_AI_exports")

MASTER_ARCHIVE_ROOT = DESKTOP / "FOCUS_MASTER_MASTER_ARCHIVE"
DESKTOP_ARCHIVE = MASTER_ARCHIVE_ROOT / "current"
DRIVE_ARCHIVE = DRIVE_EXPORTS / "FOCUS_MASTER_MASTER_ARCHIVE"
ONEDRIVE_ARCHIVE = ONEDRIVE_ARCHIVES / "FOCUS_MASTER_MASTER_ARCHIVE"

DESKTOP_LEGACY_REPO = DESKTOP / "FOCUS- AI" / "FOCUS_MASTER_AI"
CODE_REMNANT_ROOTS = [
    DESKTOP / "FOCUS- AI",
    HOME / "OneDrive" / "Documents" / "GitHub",
]
REPO_MIRROR_EXPORT = DRIVE_EXPORTS / "FOCUS_MASTER_AI_live_2026-04-23.bundle"

GITHUB_REPOS = {
    "focusnegotiuminc-creator/improved-rotary-phone": "https://github.com/focusnegotiuminc-creator/improved-rotary-phone.git",
    "thegreatmachevilli/focus": "https://github.com/thegreatmachevilli/focus.git",
    "thegreatmachevilli/Focus-AI": "https://github.com/thegreatmachevilli/Focus-AI.git",
}

IGNORE_NAMES = {
    ".git",
    ".secrets",
    "secrets",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
}
IGNORE_SUFFIXES = {".pyc", ".pyo", ".pem", ".key", ".sqlite-shm", ".sqlite-wal"}
CODE_SUFFIXES = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".md",
    ".html",
    ".css",
    ".scss",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".txt",
    ".sh",
    ".ps1",
    ".bat",
    ".sql",
    ".csv",
    ".svg",
}


@dataclass
class RepoInfo:
    name: str
    path: Path
    branch: str
    head: str
    remotes: list[str]
    canonical: bool


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-").lower() or "item"


def run(command: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=check,
    )


def git_output(args: list[str], *, cwd: Path) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onexc=_rmtree_onexc)
    path.mkdir(parents=True, exist_ok=True)


def _rmtree_onexc(function, path, excinfo) -> None:
    os.chmod(path, stat.S_IWRITE)
    function(path)


def should_skip(path: Path) -> bool:
    if path.name in IGNORE_NAMES:
        return True
    if path.suffix.lower() in IGNORE_SUFFIXES:
        return True
    return False


def copy_tree(src: Path, dst: Path) -> tuple[int, int]:
    files = 0
    dirs = 0
    for root, dirnames, filenames in os.walk(src):
        root_path = Path(root)
        relative = root_path.relative_to(src)
        if any(part in IGNORE_NAMES for part in relative.parts):
            dirnames[:] = []
            continue
        dirnames[:] = [name for name in dirnames if name not in IGNORE_NAMES]
        target_root = dst / relative
        target_root.mkdir(parents=True, exist_ok=True)
        dirs += 1
        for filename in filenames:
            source_file = root_path / filename
            if should_skip(source_file):
                continue
            target_file = target_root / filename
            shutil.copy2(source_file, target_file)
            files += 1
    return files, dirs


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_info(path: Path, *, canonical: bool) -> RepoInfo:
    remotes = git_output(["remote", "-v"], cwd=path).splitlines()
    return RepoInfo(
        name=path.name,
        path=path,
        branch=git_output(["branch", "--show-current"], cwd=path),
        head=git_output(["rev-parse", "HEAD"], cwd=path),
        remotes=remotes,
        canonical=canonical,
    )


def scan_repo_files(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for file in path.rglob("*"):
        if not file.is_file():
            continue
        if should_skip(file) or any(part in IGNORE_NAMES for part in file.relative_to(path).parts):
            continue
        rows.append(
            {
                "relative_path": file.relative_to(path).as_posix(),
                "sha256": sha256(file),
            }
        )
    return rows


def build_duplicate_summary(source_repos: list[RepoInfo]) -> dict[str, object]:
    by_hash: dict[str, list[dict[str, str]]] = {}
    for repo in source_repos:
        for row in scan_repo_files(repo.path):
            by_hash.setdefault(row["sha256"], []).append(
                {
                    "repo": repo.name,
                    "repo_path": str(repo.path),
                    "relative_path": row["relative_path"],
                }
            )
    duplicates = {digest: items for digest, items in by_hash.items() if len(items) > 1}
    return {
        "unique_hashes": len(by_hash),
        "duplicate_hashes": len(duplicates),
        "duplicates": duplicates,
    }


def write_env_template(source_env: Path, destination: Path) -> None:
    lines: list[str] = []
    for raw in source_env.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or "=" not in raw:
            continue
        key, _value = raw.split("=", 1)
        key = key.strip()
        lines.append(f"{key}=replace_me")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def classify_remnant(path: Path) -> str:
    if path.name in {"edge_flux_profile", "edge_flux_user_data", "wix_remote_debug_profile", "_tmp_flux"}:
        return "non-code/browser-profile"
    if path.suffix.lower() in CODE_SUFFIXES:
        return "code-file"
    if path.is_dir():
        child_suffixes = {child.suffix.lower() for child in path.rglob("*") if child.is_file()}
        if child_suffixes.intersection(CODE_SUFFIXES):
            return "code-directory"
    return "uncertain/manual-review"


def write_repo_inventory(destination: Path, repos: list[RepoInfo]) -> None:
    lines = [
        "# Repo Inventory",
        "",
        f"Generated: {utc_now()}",
        "",
        "| Repo | Canonical | Branch | HEAD | Path |",
        "| --- | --- | --- | --- | --- |",
    ]
    for repo in repos:
        lines.append(
            f"| {repo.name} | {'yes' if repo.canonical else 'no'} | {repo.branch} | `{repo.head}` | `{repo.path}` |"
        )
        for remote in repo.remotes:
            lines.append(f"|  |  |  |  | `{remote}` |")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_cleanup_report(destination: Path, remnant_rows: list[dict[str, str]]) -> None:
    lines = [
        "# Local Cleanup Report",
        "",
        f"Generated: {utc_now()}",
        "",
        "This report inventories local remnants and defers destructive cleanup until archive and cloud sync verification are complete.",
        "",
        "| Path | Classification |",
        "| --- | --- |",
    ]
    for row in remnant_rows:
        lines.append(f"| `{row['path']}` | {row['classification']} |")
    lines.extend(
        [
            "",
            "## Action posture",
            "",
            "- Canonical code remains in the Drive-backed workspace.",
            "- The master archive was created before any duplicate pruning.",
            "- No final destructive duplicate removal has been performed yet.",
        ]
    )
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def mirror_repo(source: str, destination: Path, *, local_path: Path | None = None) -> dict[str, str]:
    if destination.exists():
        shutil.rmtree(destination)
    if local_path and local_path.exists():
        run(["git", "clone", "--mirror", str(local_path), str(destination)])
    else:
        run(["git", "clone", "--mirror", source, str(destination)])
    return {"source": source, "destination": str(destination)}


def build_archive() -> dict[str, object]:
    source_repos = [repo_info(ROOT, canonical=True)]
    if DESKTOP_LEGACY_REPO.exists():
        source_repos.append(repo_info(DESKTOP_LEGACY_REPO, canonical=False))

    ensure_clean_dir(DESKTOP_ARCHIVE)
    for path in [
        DESKTOP_ARCHIVE / "apps",
        DESKTOP_ARCHIVE / "sites",
        DESKTOP_ARCHIVE / "private_console",
        DESKTOP_ARCHIVE / "engines",
        DESKTOP_ARCHIVE / "integrations",
        DESKTOP_ARCHIVE / "archives" / "raw_repo_mirrors",
        DESKTOP_ARCHIVE / "artifacts" / "published_outputs",
        DESKTOP_ARCHIVE / "docs" / "manifests",
        DESKTOP_ARCHIVE / "secrets" / "templates_only",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    copies: list[dict[str, object]] = []
    targets = [
        ("apps/focus_master_ai_live", ROOT),
        ("private_console/FOCUS_MASTER_AI", ROOT / "FOCUS_MASTER_AI"),
        ("sites/fluxcrave", ROOT / "marketing" / "fluxcrave"),
        ("engines/focus_master_engines", ROOT / "FOCUS_MASTER_AI" / "engines"),
        ("integrations/focus_master_integrations", ROOT / "FOCUS_MASTER_AI" / "integrations"),
        ("artifacts/published_outputs/focus_ai_published", ROOT / "focus_ai" / "published"),
    ]
    for relative, source in targets:
        destination = DESKTOP_ARCHIVE / relative
        files, dirs = copy_tree(source, destination)
        copies.append({"source": str(source), "destination": str(destination), "files": files, "dirs": dirs})

    raw_root = DESKTOP_ARCHIVE / "archives" / "raw_repo_mirrors"
    mirrors = [
        mirror_repo(str(ROOT), raw_root / "focus_master_ai_live.git", local_path=ROOT),
    ]
    if DESKTOP_LEGACY_REPO.exists():
        mirrors.append(mirror_repo(str(DESKTOP_LEGACY_REPO), raw_root / "focus_master_ai_legacy_desktop.git", local_path=DESKTOP_LEGACY_REPO))
    for repo_name, remote_url in GITHUB_REPOS.items():
        mirrors.append(mirror_repo(remote_url, raw_root / f"{slugify(repo_name)}.git"))

    if REPO_MIRROR_EXPORT.exists():
        shutil.copy2(REPO_MIRROR_EXPORT, raw_root / REPO_MIRROR_EXPORT.name)

    env_templates = DESKTOP_ARCHIVE / "secrets" / "templates_only"
    shutil.copy2(ROOT / "FOCUS_MASTER_AI" / ".env.example", env_templates / ".env.example")
    for env_name in ("focus_master.env", "fluxcrave.env"):
        source_env = ROOT / ".secrets" / env_name
        if source_env.exists():
            write_env_template(source_env, env_templates / f"{env_name}.template")

    manifests_dir = DESKTOP_ARCHIVE / "docs" / "manifests"
    write_repo_inventory(manifests_dir / "repo_inventory.md", source_repos)

    remnant_rows: list[dict[str, str]] = []
    for remnant_root in CODE_REMNANT_ROOTS:
        if not remnant_root.exists():
            continue
        for child in remnant_root.iterdir():
            remnant_rows.append(
                {
                    "path": str(child),
                    "classification": classify_remnant(child),
                }
            )

    consolidation_manifest = {
        "generated_at_utc": utc_now(),
        "canonical_repo": str(ROOT),
        "archive_root": str(DESKTOP_ARCHIVE),
        "source_repos": [
            {
                "name": repo.name,
                "path": str(repo.path),
                "branch": repo.branch,
                "head": repo.head,
                "canonical": repo.canonical,
                "remotes": repo.remotes,
            }
            for repo in source_repos
        ],
        "copies": copies,
        "raw_repo_mirrors": mirrors,
        "export_bundle": str(REPO_MIRROR_EXPORT) if REPO_MIRROR_EXPORT.exists() else "",
        "duplicate_summary": build_duplicate_summary(source_repos),
        "remnants": remnant_rows,
    }
    (manifests_dir / "consolidation_manifest.json").write_text(
        json.dumps(consolidation_manifest, indent=2),
        encoding="utf-8",
    )
    write_cleanup_report(manifests_dir / "local_cleanup_report.md", remnant_rows)

    readme = DESKTOP_ARCHIVE / "README_ARCHIVE.md"
    readme.write_text(
        "\n".join(
            [
                "# Focus Master Master Archive",
                "",
                "This folder is the consolidated, sanitized code and artifact archive for the Focus platform.",
                "",
                "## Top-level labels",
                "- `apps/`: canonical workspace snapshot",
                "- `sites/`: public-facing site code and assets",
                "- `private_console/`: internal operator console",
                "- `engines/`: engine modules",
                "- `integrations/`: external/local adapters",
                "- `archives/raw_repo_mirrors/`: git mirrors and historical bundle exports",
                "- `artifacts/published_outputs/`: generated deliverables and site/book outputs",
                "- `docs/manifests/`: inventory, dedupe, sync, cleanup, and QA reports",
                "- `secrets/templates_only/`: sanitized environment templates only",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return consolidation_manifest


def sync_archive_tree(source: Path, destination: Path) -> tuple[int, int]:
    if destination.exists():
        shutil.rmtree(destination, onexc=_rmtree_onexc)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return copy_tree(source, destination)


def write_storage_sync_report(destination: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Storage Sync Report",
        "",
        f"Generated: {utc_now()}",
        "",
        "| Target | Status | Files | Directories | Path |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['target']} | {row['status']} | {row['files']} | {row['dirs']} | `{row['path']}` |"
        )
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    manifest = build_archive()

    manifests_dir = DESKTOP_ARCHIVE / "docs" / "manifests"
    sync_rows: list[dict[str, object]] = [
        {
            "target": "Desktop master archive",
            "status": "created",
            "files": 0,
            "dirs": 0,
            "path": str(DESKTOP_ARCHIVE),
        }
    ]
    write_storage_sync_report(manifests_dir / "storage_sync_report.md", sync_rows)

    desktop_files = sum(1 for path in DESKTOP_ARCHIVE.rglob("*") if path.is_file())
    desktop_dirs = sum(1 for path in DESKTOP_ARCHIVE.rglob("*") if path.is_dir())
    sync_rows[0]["files"] = desktop_files
    sync_rows[0]["dirs"] = desktop_dirs
    write_storage_sync_report(manifests_dir / "storage_sync_report.md", sync_rows)

    for label, target in [
        ("Google Drive archive", DRIVE_ARCHIVE),
        ("OneDrive archive", ONEDRIVE_ARCHIVE),
    ]:
        files, dirs = sync_archive_tree(DESKTOP_ARCHIVE, target)
        sync_rows.append({"target": label, "status": "synced", "files": files, "dirs": dirs, "path": str(target)})

    write_storage_sync_report(manifests_dir / "storage_sync_report.md", sync_rows)
    sync_archive_tree(DESKTOP_ARCHIVE, DRIVE_ARCHIVE)
    sync_archive_tree(DESKTOP_ARCHIVE, ONEDRIVE_ARCHIVE)

    print(json.dumps({"ok": True, "manifest": manifest["archive_root"], "sync_targets": sync_rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
