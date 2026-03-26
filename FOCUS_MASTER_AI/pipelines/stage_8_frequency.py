from __future__ import annotations

from engines import frequency_engine


def run(task: str) -> dict:
    return frequency_engine.run(task)

