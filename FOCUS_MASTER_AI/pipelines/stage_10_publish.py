from __future__ import annotations

from engines import publishing_engine


def run(task: str) -> dict:
    return publishing_engine.run(task)

