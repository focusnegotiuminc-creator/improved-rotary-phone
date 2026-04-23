from __future__ import annotations

from importlib import import_module
from typing import Any


ENGINE_MODULES = {
    "research": "research_engine",
    "claims": "claims_engine",
    "writing": "writing_engine",
    "geometry": "geometry_engine",
    "construction": "construction_engine",
    "compliance": "compliance_engine",
    "frequency": "frequency_engine",
    "marketing": "marketing_engine",
    "ai_twin": "ai_twin_engine",
    "publish": "publishing_engine",
    "automation": "automation_engine",
}


def run_engine_by_key(engine_key: str, task: str) -> dict[str, Any]:
    module_name = ENGINE_MODULES.get(engine_key)
    if not module_name:
        return {
            "engine": engine_key,
            "status": "degraded",
            "output": f"Unknown engine '{engine_key}'.",
        }

    try:
        try:
            module = import_module(f"FOCUS_MASTER_AI.engines.{module_name}")
        except ImportError:
            module = import_module(f"engines.{module_name}")
        return module.run(task)
    except Exception as exc:
        return {
            "engine": engine_key,
            "status": "degraded",
            "output": f"Engine import or execution failed: {exc}",
        }
