from __future__ import annotations

from engines import claims_engine


def run(task: str) -> dict:
    return claims_engine.run(task)

