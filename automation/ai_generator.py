"""Master orchestration script for the Sacred AI Business Engine."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "automation" / "book_writer.py",
    ROOT / "automation" / "blueprint_generator.py",
    ROOT / "automation" / "business_generator.py",
    ROOT / "automation" / "marketing_engine.py",
]


def run_script(script_path: Path) -> None:
    print(f"[RUN] {script_path.name}")
    subprocess.run(["python", str(script_path)], check=True)


if __name__ == "__main__":
    for script in SCRIPTS:
        run_script(script)
    print("[DONE] Sacred AI Business Engine content generation completed.")
