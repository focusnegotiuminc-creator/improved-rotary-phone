from __future__ import annotations

from engines import construction_engine


def run(task: str) -> dict:
    return construction_engine.run(task)

