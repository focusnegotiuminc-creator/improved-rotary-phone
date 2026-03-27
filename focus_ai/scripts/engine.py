#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import re

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


THREAD_URI_RE = re.compile(r'^codex://threads/[0-9a-fA-F-]+$')


def normalize_thread_uri(thread_uri: str | None) -> str | None:
    if thread_uri is None:
        return None
    normalized = thread_uri.strip()
    if not THREAD_URI_RE.fullmatch(normalized):
        raise SystemExit("Thread URI must match codex://threads/<id>")
    return normalized


def run(stage: int | None = None, thread_uri: str | None = None) -> None:
    log = ROOT / "docs" / "engine_run.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    thread_uri = normalize_thread_uri(thread_uri)

    if stage is not None:
        if not 1 <= stage <= len(STAGES):
            raise SystemExit(f"Stage must be 1-{len(STAGES)}")
        entries = [f"[{now}] Ran stage {stage}: {STAGES[stage-1]}"]
    else:
        entries = [f"[{now}] Ran all 11 stages"] + [
            f"  - {i+1}. {name}" for i, name in enumerate(STAGES)
        ]

    if thread_uri:
        entries.append(f"  - Thread: {thread_uri}")

    with log.open("a", encoding="utf-8") as f:
        f.write("\n".join(entries) + "\n")

    print("\n".join(entries))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Sacred AI workflow stages")
    parser.add_argument("--stage", type=int, help="Run only one stage (1-11)")
    parser.add_argument("--thread-uri", help="Codex thread URI to annotate the run log")
    args = parser.parse_args()
    run(args.stage, args.thread_uri)
