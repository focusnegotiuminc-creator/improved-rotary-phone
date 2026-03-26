from __future__ import annotations

from pipelines import (
    stage_10_publish,
    stage_1_research,
    stage_2_claims,
    stage_3_outline,
    stage_4_writing,
    stage_5_geometry,
    stage_6_construction,
    stage_7_compliance,
    stage_8_frequency,
    stage_9_marketing,
)


def run_multi_engine_workflow(task: str) -> dict:
    pipeline = [
        ("stage_1_research", stage_1_research.run),
        ("stage_2_claims", stage_2_claims.run),
        ("stage_3_outline", stage_3_outline.run),
        ("stage_4_writing", stage_4_writing.run),
        ("stage_5_geometry", stage_5_geometry.run),
        ("stage_6_construction", stage_6_construction.run),
        ("stage_7_compliance", stage_7_compliance.run),
        ("stage_8_frequency", stage_8_frequency.run),
        ("stage_9_marketing", stage_9_marketing.run),
        ("stage_10_publish", stage_10_publish.run),
    ]

    results: list[dict] = []
    for stage_name, stage_runner in pipeline:
        stage_result = stage_runner(task)
        results.append(
            {
                "stage": stage_name,
                "result": stage_result,
            }
        )

    return {
        "workflow": "focus_master_multi_engine",
        "task": task,
        "status": "completed",
        "steps": results,
    }

