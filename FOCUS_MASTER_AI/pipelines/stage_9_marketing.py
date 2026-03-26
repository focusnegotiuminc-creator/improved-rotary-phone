from __future__ import annotations

from engines import marketing_engine


def run(task: str) -> dict:
    return marketing_engine.run(task)

