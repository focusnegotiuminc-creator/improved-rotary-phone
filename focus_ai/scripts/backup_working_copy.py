#!/usr/bin/env python3
"""Create a timestamped backup archive of the focus_ai working tree."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BACKUPS = ROOT / "backups"
SOURCE_DIRS = [
    ROOT / "docs",
    ROOT / "ebooks",
    ROOT / "engine",
    ROOT / "prompts",
    ROOT / "published",
    ROOT / "scripts",
    ROOT / "site",
    ROOT / "tests",
]


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    BACKUPS.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive = BACKUPS / f"focus_ai_backup_{timestamp}.tar.gz"

    with tarfile.open(archive, "w:gz") as tar:
        for src in SOURCE_DIRS:
            if src.exists():
                tar.add(src, arcname=src.relative_to(ROOT))

    checksum = _sha256(archive)
    checksum_file = archive.with_suffix(archive.suffix + ".sha256")
    checksum_file.write_text(f"{checksum}  {archive.name}\n", encoding="utf-8")

    print(f"Created backup: {archive}")
    print(f"Checksum file: {checksum_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
