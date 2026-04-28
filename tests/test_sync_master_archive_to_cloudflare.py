from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_sync(script_path: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(script_path), *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def test_sync_copies_required_files_and_bundle(tmp_path: Path) -> None:
    # Arrange
    archive_root = tmp_path / "archive_root"
    manifests_dir = archive_root / "docs" / "manifests"
    cloudflare_public_dir = tmp_path / "cloudflare_public"

    manifests_dir.mkdir(parents=True, exist_ok=True)
    archive_root.mkdir(parents=True, exist_ok=True)

    # Required manifest files
    (manifests_dir / "repo_inventory.md").write_text("inventory", encoding="utf-8")
    (manifests_dir / "storage_sync_report.md").write_text("report", encoding="utf-8")
    (manifests_dir / "local_cleanup_report.md").write_text("cleanup", encoding="utf-8")

    export_bundle = archive_root / "FOCUS_MASTER_AI_live_test.bundle"
    export_bundle.write_text("bundle-bytes", encoding="utf-8")

    consolidation_manifest = {
        "generated_at_utc": "2026-01-01T00:00:00Z",
        "canonical_repo": ".",
        "archive_root": str(archive_root),
        "source_repos": [],
        "copies": [],
        "raw_repo_mirrors": [],
        "export_bundle": str(export_bundle),
        "duplicate_summary": {},
        "remnants": [],
    }
    (manifests_dir / "consolidation_manifest.json").write_text(
        json.dumps(consolidation_manifest, indent=2),
        encoding="utf-8",
    )

    (archive_root / "README_ARCHIVE.md").write_text("readme", encoding="utf-8")

    script_path = ROOT / "scripts" / "sync_master_archive_to_cloudflare.py"
    assert script_path.exists(), f"Missing {script_path}"

    # Act
    result = _run_sync(
        script_path,
        [
            "--archive-root",
            archive_root,
            "--manifests-dir",
            manifests_dir,
            "--cloudflare-public-dir",
            cloudflare_public_dir,
            "--dest-subdir",
            "archives",
        ],
    )

    # Assert
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

    dest_dir = cloudflare_public_dir / "archives"
    assert (dest_dir / "consolidation_manifest.json").exists()
    assert (dest_dir / "repo_inventory.md").exists()
    assert (dest_dir / "storage_sync_report.md").exists()
    assert (dest_dir / "local_cleanup_report.md").exists()

    # Optional readme
    assert (dest_dir / "README_ARCHIVE.md").exists()

    # Bundle copied
    assert (dest_dir / export_bundle.name).exists()


def test_sync_include_zip_when_no_export_bundle(tmp_path: Path) -> None:
    # Arrange
    archive_root = tmp_path / "archive_root"
    manifests_dir = archive_root / "docs" / "manifests"
    cloudflare_public_dir = tmp_path / "cloudflare_public"

    manifests_dir.mkdir(parents=True, exist_ok=True)
    archive_root.mkdir(parents=True, exist_ok=True)

    (manifests_dir / "repo_inventory.md").write_text("inventory", encoding="utf-8")
    (manifests_dir / "storage_sync_report.md").write_text("report", encoding="utf-8")
    (manifests_dir / "local_cleanup_report.md").write_text("cleanup", encoding="utf-8")

    # export_bundle intentionally missing/empty
    consolidation_manifest = {
        "generated_at_utc": "2026-01-01T00:00:00Z",
        "canonical_repo": ".",
        "archive_root": str(archive_root),
        "source_repos": [],
        "copies": [],
        "raw_repo_mirrors": [],
        "export_bundle": "",
        "duplicate_summary": {},
        "remnants": [],
    }
    (manifests_dir / "consolidation_manifest.json").write_text(
        json.dumps(consolidation_manifest, indent=2),
        encoding="utf-8",
    )

    # Provide apps/ and sites/ so include_zip has something to zip
    (archive_root / "apps").mkdir(parents=True, exist_ok=True)
    (archive_root / "apps" / "app.txt").write_text("app", encoding="utf-8")

    (archive_root / "sites").mkdir(parents=True, exist_ok=True)
    (archive_root / "sites" / "site.txt").write_text("site", encoding="utf-8")

    (archive_root / "README_ARCHIVE.md").write_text("readme", encoding="utf-8")

    script_path = ROOT / "scripts" / "sync_master_archive_to_cloudflare.py"
    assert script_path.exists(), f"Missing {script_path}"

    # Act
    result = _run_sync(
        script_path,
        [
            "--archive-root",
            archive_root,
            "--manifests-dir",
            manifests_dir,
            "--cloudflare-public-dir",
            cloudflare_public_dir,
            "--dest-subdir",
            "archives",
            "--include-zip",
            "--apps-dir-name",
            "apps",
            "--sites-dir-name",
            "sites",
        ],
    )

    # Assert
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

    dest_dir = cloudflare_public_dir / "archives"
    assert (dest_dir / "consolidation_manifest.json").exists()

    # zips created
    assert (dest_dir / "apps.zip").exists()
    assert (dest_dir / "sites.zip").exists()
