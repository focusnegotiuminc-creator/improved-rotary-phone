from __future__ import annotations

import importlib.util
import os
from typing import Any

try:
    from FOCUS_MASTER_AI.integrations.github_api import GitHubClient
except ImportError:
    from integrations.github_api import GitHubClient


def _state_tone(state: str) -> str:
    return {"ready": "ready", "partial": "partial", "fallback": "fallback"}.get(state, "attention")


def build_connector_status() -> dict[str, Any]:
    openai_key = bool(os.getenv("OPENAI_API_KEY", "").strip())
    openai_package = importlib.util.find_spec("openai") is not None
    make_ready = bool(os.getenv("MAKE_WEBHOOK_URL", "").strip())
    replit_ready = bool(os.getenv("REPLIT_RUNNER_URL", "").strip())
    github = GitHubClient().healthcheck()

    items = [
        {
            "id": "openai",
            "label": "OpenAI Reasoning Core",
            "state": "ready" if openai_key and openai_package else "attention",
            "tone": _state_tone("ready" if openai_key and openai_package else "attention"),
            "message": "Live model access available." if openai_key and openai_package else "Missing API key or package install.",
        },
        {
            "id": "make",
            "label": "Make Automation Webhook",
            "state": "ready" if make_ready else "attention",
            "tone": _state_tone("ready" if make_ready else "attention"),
            "message": "Webhook is configured for remote automations." if make_ready else "Configure MAKE_WEBHOOK_URL for live automation runs.",
        },
        {
            "id": "replit",
            "label": "Replit Remote Runner",
            "state": "ready" if replit_ready else "attention",
            "tone": _state_tone("ready" if replit_ready else "attention"),
            "message": "Remote runner endpoint is configured." if replit_ready else "Configure REPLIT_RUNNER_URL for live remote execution.",
        },
        {
            "id": "github",
            "label": "GitHub Publish Surface",
            "state": "ready" if github.get("ok") else "attention",
            "tone": _state_tone("ready" if github.get("ok") else "attention"),
            "message": github.get("message", "GitHub integration status unavailable."),
        },
        {
            "id": "ai_twin",
            "label": "AI Twin Video Stack",
            "state": "ready" if openai_key and openai_package else "fallback",
            "tone": _state_tone("ready" if openai_key and openai_package else "fallback"),
            "message": "Live reasoning available for scene and avatar prompt generation." if openai_key and openai_package else "Running in high-quality templated fallback mode until OpenAI is configured.",
        },
    ]

    ready_count = sum(1 for item in items if item["state"] == "ready")
    return {
        "items": items,
        "ready_count": ready_count,
        "attention_count": len(items) - ready_count,
        "total": len(items),
    }
