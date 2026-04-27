from __future__ import annotations

from typing import Any

try:
    from FOCUS_MASTER_AI.core.connector_status import build_connector_status
    from FOCUS_MASTER_AI.core.prompt_studio import ENGINE_PROFILES, build_engine_prompt, build_master_task_packet, run_llm_or_fallback
    from FOCUS_MASTER_AI.integrations.external_apps import route_ai
    from FOCUS_MASTER_AI.integrations.make_webhook import trigger_make
    from FOCUS_MASTER_AI.integrations.replit_runner import trigger_replit
except ImportError:
    from core.connector_status import build_connector_status
    from core.prompt_studio import ENGINE_PROFILES, build_engine_prompt, build_master_task_packet, run_llm_or_fallback
    from integrations.external_apps import route_ai
    from integrations.make_webhook import trigger_make
    from integrations.replit_runner import trigger_replit


def run_ai_engine(
    engine_key: str,
    task: str,
    *,
    execute_automation: bool = False,
    preferred_provider: str | None = None,
) -> dict[str, Any]:
    packet = build_master_task_packet(task, preferred_engine=engine_key)
    engine_prompt = build_engine_prompt(packet, engine_key)
    generation = run_llm_or_fallback(
        engine_prompt,
        packet,
        engine_key,
        preferred_provider=preferred_provider,
    )

    result: dict[str, Any] = {
        "engine": engine_key,
        "label": ENGINE_PROFILES[engine_key]["label"],
        "status": "completed",
        "task": task,
        "task_packet": packet,
        "engine_prompt": engine_prompt,
        "output": generation["content"],
        "model_execution": {
            "provider": generation.get("provider", "fallback"),
            "model": generation.get("model", "templated-fallback"),
            "mode": generation.get("mode", "fallback"),
            "attempted": generation.get("attempted", []),
        },
        "connectors": build_connector_status(),
    }
    if generation.get("error"):
        result["model_execution"]["error"] = generation["error"]

    if execute_automation or engine_key == "automation":
        route_hint = route_ai(task)
        result["route_hint"] = route_hint
        result["make"] = trigger_make(
            packet["master_prompt"],
            {
                "route_hint": route_hint,
                "engine": engine_key,
                "raw_task": task,
            },
        )
        result["replit"] = trigger_replit(packet["master_prompt"])

    if engine_key == "ai_twin":
        result["video_stack"] = ENGINE_PROFILES["ai_twin"]["video_stack"]

    return result
