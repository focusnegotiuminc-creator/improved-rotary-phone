#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = Path(r"C:\Users\reggi\OneDrive\Desktop\FOCUS_MASTER_MASTER_ARCHIVE")
QUARANTINE = ARCHIVE_ROOT / "quarantine" / f"generated_hygiene_{datetime.now().strftime('%Y-%m-%d')}"
REPORT = ROOT / "docs" / "manifests" / "generated_output_hygiene_report.md"

TRANSIENT_DIRS = [
    ROOT / ".pytest_cache",
    ROOT / "__pycache__",
    ROOT / "FOCUS_MASTER_AI" / "__pycache__",
    ROOT / "FOCUS_MASTER_AI" / "core" / "__pycache__",
    ROOT / "FOCUS_MASTER_AI" / "engines" / "__pycache__",
    ROOT / "FOCUS_MASTER_AI" / "integrations" / "__pycache__",
    ROOT / "focus_ai" / "scripts" / "__pycache__",
    ROOT / "focus_ai" / "tests" / "__pycache__",
    ROOT / "marketing" / "fluxcrave" / "__pycache__",
]

ARCHIVE_CANDIDATES = [
    ROOT / "focus_ai" / "published",
    ROOT / "focus_ai" / "docs" / "engine_run.log",
    ROOT / "focus_ai" / "docs" / "live_stack_report.md",
    ROOT / "memory" / "research_cache.json",
    ROOT / "memory" / "task_history.json",
    ROOT / "FOCUS_MASTER_AI" / "memory" / "research_cache.json",
    ROOT / "FOCUS_MASTER_AI" / "memory" / "task_history.json",
]


def safe_rmtree(path: Path) -> None:
    def on_error(func, value, _exc) -> None:
        os.chmod(value, stat.S_IWRITE)
        func(value)

    if path.exists():
        shutil.rmtree(path, onerror=on_error)


def ensure_quarantine() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)


def copy_candidate(path: Path) -> str:
    if not path.exists():
        return "missing"
    relative = path.relative_to(ROOT)
    target = QUARANTINE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.is_dir():
        if target.exists():
            safe_rmtree(target)
        shutil.copytree(path, target)
    else:
        shutil.copy2(path, target)
    return str(target)


def remove_transient(path: Path) -> str:
    if not path.exists():
        return "missing"
    safe_rmtree(path)
    return "removed"


def write_report(archived: list[tuple[str, str]], removed: list[tuple[str, str]]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Generated Output Hygiene Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Quarantine root: `{QUARANTINE}`",
        "",
        "## Archived generated outputs",
        "",
        "| Path | Result |",
        "| --- | --- |",
    ]
    for path, result in archived:
        lines.append(f"| `{path}` | `{result}` |")
    lines += [
        "",
        "## Removed transient caches",
        "",
        "| Path | Result |",
        "| --- | --- |",
    ]
    for path, result in removed:
        lines.append(f"| `{path}` | `{result}` |")
    lines += [
        "",
        "## Notes",
        "",
        "- This pass archives generated outputs before deleting transient caches.",
        "- It does not delete canonical source files.",
        "- Repo-tracked generated outputs may still appear in git status until a separate source-control policy cleanup is applied.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_quarantine()
    archived: list[tuple[str, str]] = []
    removed: list[tuple[str, str]] = []

    for candidate in ARCHIVE_CANDIDATES:
        archived.append((str(candidate.relative_to(ROOT)), copy_candidate(candidate)))

    for transient in TRANSIENT_DIRS:
        removed.append((str(transient.relative_to(ROOT)), remove_transient(transient)))

    write_report(archived, removed)
    print(
        {
            "ok": True,
            "report": str(REPORT),
            "quarantine": str(QUARANTINE),
            "archived": len(archived),
            "removed": len(removed),
        }
    )


if __name__ == "__main__":
    main()
