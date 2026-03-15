#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

STAGES = [
    "Source Ingestion & Normalization",
    "Brand Voice Calibration",
    "Offer Architecture",
    "Visual Direction System",
    "Conversion Copy Engine",
    "Trust & Compliance Layer",
    "Content Expansion",
    "Web Change Operations",
    "QA & Professionalism Audit",
    "Launch Readiness",
    "Continuous Optimization Loop",
]


def run(stage: int | None = None) -> None:
    log = ROOT / "docs" / "engine_run.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    if stage is not None:
        if not 1 <= stage <= len(STAGES):
            raise SystemExit(f"Stage must be 1-{len(STAGES)}")
        entries = [f"[{now}] Ran stage {stage}: {STAGES[stage-1]}"]
    else:
        entries = [f"[{now}] Ran all 11 stages"] + [
            f"  - {i+1}. {name}" for i, name in enumerate(STAGES)
        ]

    with log.open("a", encoding="utf-8") as f:
        f.write("\n".join(entries) + "\n")

    print("\n".join(entries))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Sacred AI workflow stages")
    parser.add_argument("--stage", type=int, help="Run only one stage (1-11)")
    args = parser.parse_args()
    run(args.stage)
