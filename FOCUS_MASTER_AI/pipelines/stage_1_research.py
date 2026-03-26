from __future__ import annotations

from engines import research_engine


def run(task: str) -> dict:
    return research_engine.run(task)

