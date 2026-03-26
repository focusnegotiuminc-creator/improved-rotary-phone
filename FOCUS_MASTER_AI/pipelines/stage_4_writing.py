from __future__ import annotations

from engines import writing_engine


def run(task: str) -> dict:
    return writing_engine.run(task)

