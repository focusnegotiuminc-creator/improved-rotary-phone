#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SyncTargets:
    cloudflare_public_dir: Path
    dest_dir: Path  # typically cloudflare/.../public/archives

    @property
    def ensure_dirs(self) -> list[Path]:
        return [self.cloudflare_public_dir, self.dest_dir]


def _copy_file(src: Path, dest: Path, *, dry_run: bool) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Required file missing: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return
    shutil.copy2(src, dest)


def _safe_iter_dirs(root: Path, names: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    for n in names:
        p = root / n
        if p.exists() and p.is_dir():
            out.append(p)
    return out


def _zip_dir(source_dir: Path, zip_path: Path, *, dry_run: bool) -> None:
    if not source_dir.exists() or not source_dir.is_dir():
        raise FileNotFoundError(f"Cannot zip missing directory: {source_dir}")

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return

    # Create a deterministic-ish zip by walking sorted paths.
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        all_paths: list[Path] = []
        for p in source_dir.rglob("*"):
            all_paths.append(p)
        all_paths.sort(key=lambda x: str(x).lower())

        for p in all_paths:
            rel = p.relative_to(source_dir)
            # Ensure we store paths without leading separators
            arcname = str(rel).replace("\\", "/")
            if p.is_dir():
                # Skip directories (zip will infer via files)
                continue
            zf.write(p, arcname=arcname)


def _load_consolidation_manifest(manifests_dir: Path) -> dict[str, object]:
    manifest_path = manifests_dir / "consolidation_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing consolidation manifest: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _default_paths() -> tuple[Path, Path]:
    """
    Defaults mirror scripts/build_master_archive.py.
    Note: these are Windows-specific local paths; in tests we override via CLI.
    """
    # Local imports avoided to keep script standalone
    # We compute via environment approximations rather than importing build_master_archive.
    # Users can always override via CLI flags.
    import os

    home = Path.home()
    desktop = home / "OneDrive" / "Desktop"
    master_archive_root = desktop / "FOCUS_MASTER_MASTER_ARCHIVE"
    archive_root = master_archive_root / "current"
    manifests_dir = archive_root / "docs" / "manifests"
    return archive_root, manifests_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy build_master_archive outputs into Cloudflare workbench public/assets for deployment."
    )
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=None,
        help="Root of the consolidated archive (default matches scripts/build_master_archive.py local paths).",
    )
    parser.add_argument(
        "--manifests-dir",
        type=Path,
        default=None,
        help="Directory containing consolidation_manifest.json, repo_inventory.md, etc.",
    )
    parser.add_argument(
        "--cloudflare-public-dir",
        type=Path,
        default=Path("cloudflare/focus-mobile-workbench/public"),
        help="Cloudflare wrangler assets directory (default: cloudflare/focus-mobile-workbench/public).",
    )
    parser.add_argument(
        "--dest-subdir",
        type=str,
        default="archives",
        help="Subdirectory under cloudflare-public-dir to store outputs.",
    )
    parser.add_argument(
        "--include-zip",
        action="store_true",
        help="If export_bundle is missing, zip apps/ and sites/ directories into Cloudflare.",
    )
    parser.add_argument(
        "--apps-dir-name",
        type=str,
        default="apps",
        help="Directory name under archive root to zip/copy for local code storage.",
    )
    parser.add_argument(
        "--sites-dir-name",
        type=str,
        default="sites",
        help="Directory name under archive root to zip/copy for local code storage.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be copied without writing.",
    )

    args = parser.parse_args()

    if args.archive_root is None or args.manifests_dir is None:
        default_archive_root, default_manifests_dir = _default_paths()
        archive_root = args.archive_root or default_archive_root
        manifests_dir = args.manifests_dir or default_manifests_dir
    else:
        archive_root = args.archive_root
        manifests_dir = args.manifests_dir

    targets = SyncTargets(
        cloudflare_public_dir=args.cloudflare_public_dir,
        dest_dir=args.cloudflare_public_dir / args.dest_subdir,
    )

    # Ensure destination dirs
    for d in targets.ensure_dirs:
        if not d.exists() and not args.dry_run:
            d.mkdir(parents=True, exist_ok=True)

    manifest = _load_consolidation_manifest(manifests_dir)

    export_bundle_str = str(manifest.get("export_bundle", "") or "")
    export_bundle_path = Path(export_bundle_str) if export_bundle_str else None

    # Required metadata files
    required_manifest_files = [
        manifests_dir / "consolidation_manifest.json",
        manifests_dir / "repo_inventory.md",
        manifests_dir / "storage_sync_report.md",
        manifests_dir / "local_cleanup_report.md",
    ]

    # Optional archive README
    readme_path = archive_root / "README_ARCHIVE.md"
    optional = [readme_path]

    # Copy required files
    for src in required_manifest_files:
        dest = targets.dest_dir / src.name
        _copy_file(src, dest, dry_run=args.dry_run)

    # Copy optional
    for src in optional:
        if src.exists():
            dest = targets.dest_dir / src.name
            _copy_file(src, dest, dry_run=args.dry_run)

    # Copy bundle if available
    if export_bundle_path and export_bundle_path.exists():
        dest = targets.dest_dir / export_bundle_path.name
        _copy_file(export_bundle_path, dest, dry_run=args.dry_run)
    else:
        if export_bundle_path:
            # export_bundle key exists but file missing
            raise FileNotFoundError(
                f"Manifest reports export_bundle but file is missing: {export_bundle_path}"
            )
        # export_bundle is empty string or missing
        if args.include_zip:
            # Create a zip artifact so the local code snapshot is still stored on Cloudflare.
            # We zip apps/ and sites/ directories if present.
            apps_dir = archive_root / args.apps_dir_name
            sites_dir = archive_root / args.sites_dir_name

            archives: list[Path] = []
            if apps_dir.exists() and apps_dir.is_dir():
                archives.append(apps_dir)
            if sites_dir.exists() and sites_dir.is_dir():
                archives.append(sites_dir)

            if not archives:
                raise FileNotFoundError(
                    f"include-zip enabled but neither {apps_dir} nor {sites_dir} exist."
                )

            if apps_dir.exists() and apps_dir.is_dir():
                _zip_dir(
                    apps_dir,
                    targets.dest_dir / f"{apps_dir.name}.zip",
                    dry_run=args.dry_run,
                )
            if sites_dir.exists() and sites_dir.is_dir():
                _zip_dir(
                    sites_dir,
                    targets.dest_dir / f"{sites_dir.name}.zip",
                    dry_run=args.dry_run,
                )

    # Also store the (possibly updated) manifest itself under dest_dir for easy retrieval
    # (already copied above, but we keep this step explicit for clarity)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
