from __future__ import annotations

import importlib.util
import os
from typing import Any

try:
    from FOCUS_MASTER_AI.integrations.github_api import GitHubClient
    from FOCUS_MASTER_AI.integrations.make_webhook import get_make_runtime_status
    from FOCUS_MASTER_AI.integrations.openai_client import get_openai_runtime_status
    from FOCUS_MASTER_AI.integrations.replit_runner import get_replit_runtime_status
    from FOCUS_MASTER_AI.core.runtime_config import bootstrap_runtime_env
except ImportError:
    from integrations.github_api import GitHubClient
    from integrations.make_webhook import get_make_runtime_status
    from integrations.openai_client import get_openai_runtime_status
    from integrations.replit_runner import get_replit_runtime_status
    from core.runtime_config import bootstrap_runtime_env


def _state_tone(state: str) -> str:
    return {"ready": "ready", "partial": "partial", "fallback": "fallback"}.get(state, "attention")


def build_connector_status() -> dict[str, Any]:
    bootstrap_runtime_env()
    openai_key = bool(os.getenv("OPENAI_API_KEY", "").strip())
    openai_package = importlib.util.find_spec("openai") is not None
    openai_runtime = get_openai_runtime_status()
    make_ready = bool(os.getenv("MAKE_WEBHOOK_URL", "").strip())
    make_runtime = get_make_runtime_status()
    replit_ready = bool(os.getenv("REPLIT_RUNNER_URL", "").strip())
    replit_runtime = get_replit_runtime_status()
    github = GitHubClient().healthcheck()
    if openai_key and openai_package:
        if openai_runtime["state"] == "ready":
            openai_state = "ready"
            openai_message = openai_runtime["message"]
            ai_twin_state = "ready"
            ai_twin_message = "Live reasoning is available for scene, avatar, and voice prompt generation."
        elif openai_runtime["state"] == "attention":
            openai_state = "attention"
            openai_message = openai_runtime["message"]
            ai_twin_state = "fallback"
            ai_twin_message = "OpenAI is configured but not currently generating, so the AI twin stack is running in fallback mode."
        else:
            openai_state = "partial"
            openai_message = "OpenAI is configured locally, but live generation has not been verified in this runtime."
            ai_twin_state = "partial"
            ai_twin_message = "AI twin prompts can compile locally now and will switch to live reasoning once OpenAI generation succeeds."
    else:
        openai_state = "attention"
        openai_message = "Missing API key or package install."
        ai_twin_state = "fallback"
        ai_twin_message = "Running in high-quality templated fallback mode until OpenAI is configured."

    if make_ready:
        if make_runtime["state"] == "ready":
            make_state = "ready"
            make_message = "Make webhook is responding and ready for remote automations."
        elif make_runtime["state"] == "attention":
            make_state = "attention"
            make_message = make_runtime["message"]
        else:
            make_state = "partial"
            make_message = "Make webhook is configured locally, but has not been verified in this runtime."
    else:
        make_state = "attention"
        make_message = "Configure MAKE_WEBHOOK_URL for live automation runs."

    if replit_ready:
        if replit_runtime["state"] == "ready":
            replit_state = "ready"
            replit_message = "Remote runner endpoint is responding."
        elif replit_runtime["state"] == "attention":
            replit_state = "attention"
            replit_message = replit_runtime["message"]
        else:
            replit_state = "partial"
            replit_message = "Remote runner is configured locally, but has not been verified in this runtime."
    else:
        replit_state = "attention"
        replit_message = "Configure REPLIT_RUNNER_URL for live remote execution."

    items = [
        {
            "id": "openai",
            "label": "OpenAI Reasoning Core",
            "state": openai_state,
            "tone": _state_tone(openai_state),
            "message": openai_message,
        },
        {
            "id": "make",
            "label": "Make Automation Webhook",
            "state": make_state,
            "tone": _state_tone(make_state),
            "message": make_message,
        },
        {
            "id": "replit",
            "label": "Replit Remote Runner",
            "state": replit_state,
            "tone": _state_tone(replit_state),
            "message": replit_message,
        },
        {
            "id": "github",
            "label": "GitHub Publish Surface",
            "state": github.get("state", "ready" if github.get("ok") else "attention"),
            "tone": _state_tone(github.get("state", "ready" if github.get("ok") else "attention")),
            "message": github.get("message", "GitHub integration status unavailable."),
        },
        {
            "id": "ai_twin",
            "label": "AI Twin Video Stack",
            "state": ai_twin_state,
            "tone": _state_tone(ai_twin_state),
            "message": ai_twin_message,
        },
    ]

    ready_count = sum(1 for item in items if item["state"] == "ready")
    attention_count = sum(1 for item in items if item["state"] == "attention")
    return {
        "items": items,
        "ready_count": ready_count,
        "attention_count": attention_count,
        "total": len(items),
    }
