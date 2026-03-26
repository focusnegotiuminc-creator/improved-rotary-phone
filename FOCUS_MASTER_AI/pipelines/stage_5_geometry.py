from __future__ import annotations

from engines import geometry_engine


def run(task: str) -> dict:
    return geometry_engine.run(task)

