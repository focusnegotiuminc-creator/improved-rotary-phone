#!/usr/bin/env python3
"""Create a Replit-ready bundle of the AI engine + prompts + public site assets."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "published" / "replit_bundle"

INCLUDE = [
    ROOT / "scripts" / "engine.py",
    ROOT / "scripts" / "publish_ebooks.py",
    ROOT / "scripts" / "build_public_site.py",
    ROOT / "prompts" / "stage_prompts.md",
    ROOT / "engine" / "sacred_ai_workflow.md",
    ROOT / "site" / "visual_preview.html",
    ROOT / "site" / "visual_preview.css",
    ROOT / "ebooks",
    ROOT / "published" / "ebooks",
]


def build() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    for src in INCLUDE:
        target = OUT / src.relative_to(ROOT)
        if src.is_dir():
            shutil.copytree(src, target, dirs_exist_ok=True)
        elif src.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)

    (OUT / "README_REPLIT_BUNDLE.md").write_text(
        """# Replit Bundle

This folder contains the Sacred AI engine workflow scripts, prompts, visual theme assets,
and published eBook outputs for running in a Replit app.

Suggested start commands in Replit shell:
- `python3 scripts/publish_ebooks.py`
- `python3 scripts/build_public_site.py`
- `python3 scripts/engine.py`
""",
        encoding="utf-8",
    )
    print(f"Exported Replit bundle to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
