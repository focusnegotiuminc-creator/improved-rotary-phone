#!/usr/bin/env python3
"""Build a single final package for the Focus Master AI system."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import shutil
import stat
import subprocess
import sys
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[2]
FOCUS_ROOT = REPO_ROOT / "focus_ai"
SACRED_ROOT = REPO_ROOT / "sacred-geometry-ai-engine"

OUT_ROOT = FOCUS_ROOT / "published"
FINAL_DIR = OUT_ROOT / "final_system"
ZIP_PATH = OUT_ROOT / "focus_master_ai_final_system.zip"


def run_cmd(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, cwd=REPO_ROOT, check=False, text=True, capture_output=True)
    if proc.returncode != 0:
        details = (proc.stderr or proc.stdout).strip() or "Command failed with no output."
        raise RuntimeError(f"{' '.join(cmd)}\n{details}")


def ensure_fresh_outputs() -> None:
    run_cmd([sys.executable, str(FOCUS_ROOT / "scripts" / "engine.py")])
    run_cmd([sys.executable, str(FOCUS_ROOT / "scripts" / "publish_ebooks.py")])
    run_cmd([sys.executable, str(FOCUS_ROOT / "scripts" / "build_public_site.py")])


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _on_rmtree_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onerror=_on_rmtree_error)


def build_master_manuscript() -> Path:
    ebooks_dir = FOCUS_ROOT / "ebooks"
    out_path = FINAL_DIR / "final_product" / "focus_master_ai_master_manuscript.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    parts: list[str] = []
    timestamp = datetime.now(timezone.utc).isoformat()
    parts.append("# Focus Master AI Master Manuscript")
    parts.append("")
    parts.append(f"- Generated: {timestamp}")
    parts.append("- Source: focus_ai/ebooks/*.md")
    parts.append("")
    parts.append("## Combined Content")
    parts.append("")

    for md_file in sorted(ebooks_dir.glob("*.md")):
        title = md_file.stem.replace("_", " ").title()
        parts.append(f"## {title}")
        parts.append("")
        parts.append(md_file.read_text(encoding="utf-8").strip())
        parts.append("")

    out_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return out_path


def write_readme(manuscript_path: Path) -> None:
    readme = FINAL_DIR / "README_FINAL_SYSTEM.md"
    generated = datetime.now(timezone.utc).isoformat()
    readme.write_text(
        (
            "# Focus Master AI Final System\n\n"
            "This bundle contains the complete generated outputs and operating assets for the Focus Master AI project.\n\n"
            f"- Generated: {generated}\n"
            "- Build source: local repository pipeline\n\n"
            "## Primary Launch Entry\n"
            "- `public_site/index.html`\n"
            "- `public_site/landing.html`\n"
            "- `public_site/ebooks/index.html`\n\n"
            "## Included System Assets\n"
            "- `public_site/` final web and funnel pages\n"
            "- `ebooks/` published HTML eBooks\n"
            "- `docs/` 11-stage workflow documentation and launch reports\n"
            "- `system/` workflow + prompt architecture\n"
            "- `sacred_geometry_engine/` long-form engine assets\n"
            f"- `{manuscript_path.relative_to(FINAL_DIR).as_posix()}` combined master manuscript\n\n"
            "## Rebuild Command\n"
            "- `python focus_ai/scripts/build_final_system.py`\n"
        ),
        encoding="utf-8",
    )


def write_manifest(manuscript_path: Path) -> None:
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "bundle": "Focus Master AI Final System",
        "paths": {
            "public_site": "public_site",
            "ebooks": "ebooks",
            "docs": "docs",
            "system": "system",
            "sacred_geometry_engine": "sacred_geometry_engine",
            "master_manuscript": str(manuscript_path.relative_to(FINAL_DIR).as_posix()),
        },
    }
    (FINAL_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def make_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in FINAL_DIR.rglob("*"):
            if item.is_file():
                archive.write(item, Path("final_system") / item.relative_to(FINAL_DIR))


def build() -> int:
    ensure_fresh_outputs()

    remove_tree(FINAL_DIR)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    copy_tree(FOCUS_ROOT / "published" / "public_site", FINAL_DIR / "public_site")
    copy_tree(FOCUS_ROOT / "published" / "ebooks", FINAL_DIR / "ebooks")
    copy_tree(FOCUS_ROOT / "docs", FINAL_DIR / "docs")

    copy_file(FOCUS_ROOT / "engine" / "sacred_ai_workflow.md", FINAL_DIR / "system" / "sacred_ai_workflow.md")
    copy_file(FOCUS_ROOT / "prompts" / "stage_prompts.md", FINAL_DIR / "system" / "stage_prompts.md")

    if SACRED_ROOT.exists():
        copy_file(SACRED_ROOT / "automation_engine.md", FINAL_DIR / "sacred_geometry_engine" / "automation_engine.md")
        copy_file(SACRED_ROOT / "book" / "book_outline.md", FINAL_DIR / "sacred_geometry_engine" / "book_outline.md")
        copy_file(SACRED_ROOT / "book" / "manuscript.md", FINAL_DIR / "sacred_geometry_engine" / "manuscript.md")
        copy_file(SACRED_ROOT / "final_product" / "final_book_manuscript.md", FINAL_DIR / "sacred_geometry_engine" / "final_book_manuscript.md")
        copy_file(SACRED_ROOT / "research" / "research_database.md", FINAL_DIR / "sacred_geometry_engine" / "research_database.md")
        copy_file(SACRED_ROOT / "claims" / "verified_claims.md", FINAL_DIR / "sacred_geometry_engine" / "verified_claims.md")
        copy_file(SACRED_ROOT / "compliance" / "compliance_report.md", FINAL_DIR / "sacred_geometry_engine" / "compliance_report.md")
        copy_file(SACRED_ROOT / "geometry" / "geometry_diagrams.md", FINAL_DIR / "sacred_geometry_engine" / "geometry_diagrams.md")
        copy_file(SACRED_ROOT / "construction" / "construction_optimization.md", FINAL_DIR / "sacred_geometry_engine" / "construction_optimization.md")
        copy_file(SACRED_ROOT / "alignment" / "frequency_alignment.md", FINAL_DIR / "sacred_geometry_engine" / "frequency_alignment.md")
        copy_file(SACRED_ROOT / "marketing" / "marketing_automation.md", FINAL_DIR / "sacred_geometry_engine" / "marketing_automation.md")

    manuscript_path = build_master_manuscript()
    write_readme(manuscript_path)
    write_manifest(manuscript_path)
    make_zip()

    print(f"Built final system folder: {FINAL_DIR}")
    print(f"Built final system zip: {ZIP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
