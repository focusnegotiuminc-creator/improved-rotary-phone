from __future__ import annotations

from pathlib import Path

c = Path("scripts/build_master_archive.py").read_text(encoding="utf-8")

tokens = [
    "REPO_MIRROR_EXPORT",
    "consolidation_manifest",
    "repo_inventory",
    "write_repo_inventory",
    "manifests_dir",
    "DESKTOP_ARCHIVE",
    "DRIVE_EXPORTS",
    "FOCUS_MASTER_AI_live_",
    "templates_only",
    "templates_only",
    "DRIVE_ARCHIVE",
    "ONEDRIVE_ARCHIVE",
    "MASTER_ARCHIVE_ROOT",
]

for t in tokens:
    idx = c.find(t)
    if idx == -1:
        continue
    start = max(0, idx - 300)
    end = min(len(c), idx + 800)
    print(f"\n--- {t} @ {idx} ---\n")
    print(c[start:end])
