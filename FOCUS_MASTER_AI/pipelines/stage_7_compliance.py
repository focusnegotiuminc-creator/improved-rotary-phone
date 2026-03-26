from __future__ import annotations

from engines import compliance_engine


def run(task: str) -> dict:
    return compliance_engine.run(task)

