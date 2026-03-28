from __future__ import annotations

from importlib import import_module


def run_multi_engine_workflow(task: str) -> dict:
    pipeline = [
        ("stage_1_research", "stage_1_research"),
        ("stage_2_claims", "stage_2_claims"),
        ("stage_3_outline", "stage_3_outline"),
        ("stage_4_writing", "stage_4_writing"),
        ("stage_5_geometry", "stage_5_geometry"),
        ("stage_6_construction", "stage_6_construction"),
        ("stage_7_compliance", "stage_7_compliance"),
        ("stage_8_frequency", "stage_8_frequency"),
        ("stage_9_marketing", "stage_9_marketing"),
        ("stage_10_publish", "stage_10_publish"),
    ]

    results: list[dict] = []
    for stage_name, module_name in pipeline:
        try:
            try:
                module = import_module(f"FOCUS_MASTER_AI.pipelines.{module_name}")
            except ImportError:
                module = import_module(f"pipelines.{module_name}")
            stage_result = module.run(task)
        except Exception as exc:
            stage_result = {
                "status": "degraded",
                "output": f"Stage import or execution failed: {exc}",
            }
        results.append({"stage": stage_name, "result": stage_result})

    return {
        "workflow": "focus_master_multi_engine",
        "task": task,
        "status": "completed",
        "steps": results,
    }
