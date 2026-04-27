from __future__ import annotations

from typing import Any

try:
    from FOCUS_MASTER_AI.integrations.github_api import GitHubClient
    from FOCUS_MASTER_AI.integrations.make_webhook import trigger_make
    from FOCUS_MASTER_AI.integrations.replit_runner import trigger_replit
except ImportError:  # pragma: no cover
    from integrations.github_api import GitHubClient
    from integrations.make_webhook import trigger_make
    from integrations.replit_runner import trigger_replit


TOOL_CATALOG: dict[str, dict[str, Any]] = {
    "knowledge_base": {
        "label": "Knowledge Base Router",
        "role": "Stages research, notes, claims, and operating knowledge into structured storage.",
        "analogs": ["Notion", "GitHub", "Airtable"],
        "execution_mode": "planned",
    },
    "github_workspace": {
        "label": "GitHub Workspace",
        "role": "Repo state, issues, pull requests, and publish handoff.",
        "analogs": ["GitHub"],
        "execution_mode": "connector",
    },
    "automation_router": {
        "label": "Automation Router",
        "role": "Webhook-ready automation continuation for follow-up tasks.",
        "analogs": ["Make", "Zapier"],
        "execution_mode": "connector",
    },
    "creative_studio": {
        "label": "Creative Studio",
        "role": "Campaign visual direction, PDF packets, layouts, and design prompts.",
        "analogs": ["Adobe CC", "Canva", "Figma"],
        "execution_mode": "planned",
    },
    "figma_canvas": {
        "label": "Interface Canvas",
        "role": "Interface diagrams, component planning, and design-system translation.",
        "analogs": ["Figma"],
        "execution_mode": "planned",
    },
    "stripe_catalog": {
        "label": "Offer and Checkout Catalog",
        "role": "Service offers, pricing ladders, and checkout routing.",
        "analogs": ["Stripe"],
        "execution_mode": "planned",
    },
    "geometry_lab": {
        "label": "Geometry Lab",
        "role": "Geometry studies, drafting instructions, proportions, and layout logic.",
        "analogs": ["GeoGebra", "Desmos", "CAD tooling"],
        "execution_mode": "planned",
    },
    "construction_specs": {
        "label": "Construction Specs",
        "role": "Owner packets, build sequencing, and implementation notes.",
        "analogs": ["Construction documentation stack"],
        "execution_mode": "planned",
    },
    "publishing_router": {
        "label": "Publishing Router",
        "role": "Manuscript packaging, digital publishing, and release distribution prep.",
        "analogs": ["Amazon KDP", "Gumroad", "Google Drive"],
        "execution_mode": "planned",
    },
    "media_pipeline": {
        "label": "Media Pipeline",
        "role": "Video, music, rollout assets, and catalog packaging.",
        "analogs": ["Suno", "HeyGen", "Canva"],
        "execution_mode": "planned",
    },
    "task_hub": {
        "label": "Task Hub",
        "role": "Task prioritization, work queues, and operator planning overlays.",
        "analogs": ["Notion", "Trello", "Monday", "ClickUp"],
        "execution_mode": "planned",
    },
    "calendar_optimizer": {
        "label": "Calendar Optimizer",
        "role": "Scheduling, priority windows, and follow-up timing.",
        "analogs": ["Clockwise", "Calendar automation"],
        "execution_mode": "planned",
    },
    "crm_bridge": {
        "label": "CRM Bridge",
        "role": "Lead routing, sales notes, and enrichment follow-up.",
        "analogs": ["Salesforce", "Clay", "Mailchimp"],
        "execution_mode": "planned",
    },
    "artifact_archive": {
        "label": "Artifact Archive",
        "role": "Structured storage for generated run outputs and delivery bundles.",
        "analogs": ["GitHub", "Drive", "Airtable"],
        "execution_mode": "planned",
    },
    "remote_runner": {
        "label": "Remote Runner",
        "role": "Pushes remote code-execution handoffs for long-running jobs.",
        "analogs": ["Replit", "Railway"],
        "execution_mode": "connector",
    },
}


INTEGRATION_TOOLS = {
    "github": ["github_workspace"],
    "airtable": ["knowledge_base"],
    "stripe": ["stripe_catalog"],
    "figma": ["figma_canvas"],
    "adobe": ["creative_studio"],
    "media": ["media_pipeline"],
    "make": ["automation_router"],
    "replit": ["remote_runner"],
}


def list_tools() -> list[dict[str, Any]]:
    return [{"id": tool_id, **definition} for tool_id, definition in TOOL_CATALOG.items()]


def build_tool_plan(workflow_stack: dict[str, Any], integrations: list[str]) -> list[dict[str, Any]]:
    ordered_tools = list(workflow_stack.get("tools", []))
    for key in integrations:
        ordered_tools.extend(INTEGRATION_TOOLS.get(key, []))

    plan: list[dict[str, Any]] = []
    for tool_id in dict.fromkeys(ordered_tools):
        definition = TOOL_CATALOG.get(tool_id)
        if not definition:
            continue
        plan.append(
            {
                "tool_id": tool_id,
                "label": definition["label"],
                "role": definition["role"],
                "analogs": definition["analogs"],
                "execution_mode": definition["execution_mode"],
                "status": "planned",
            }
        )
    return plan


def execute_tool_plan(
    run_id: str,
    tool_plan: list[dict[str, Any]],
    *,
    automation_allowed: bool,
    task_prompt: str,
) -> list[dict[str, Any]]:
    executions: list[dict[str, Any]] = []
    for item in tool_plan:
        tool_id = item["tool_id"]
        result = dict(item)
        if not automation_allowed or item["execution_mode"] != "connector":
            result["status"] = "planned"
            executions.append(result)
            continue

        if tool_id == "automation_router":
            result["status"] = "executed"
            result["result"] = trigger_make(task_prompt, {"run_id": run_id, "tool_id": tool_id})
        elif tool_id == "remote_runner":
            result["status"] = "executed"
            result["result"] = trigger_replit(task_prompt)
        elif tool_id == "github_workspace":
            result["status"] = "checked"
            result["result"] = GitHubClient().healthcheck()
        else:
            result["status"] = "planned"
        executions.append(result)
    return executions
