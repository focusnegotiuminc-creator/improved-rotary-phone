from __future__ import annotations

try:
    from FOCUS_MASTER_AI.core.engine_runtime import run_ai_engine
    from FOCUS_MASTER_AI.integrations.github_api import GitHubClient
except ImportError:
    from core.engine_runtime import run_ai_engine
    from integrations.github_api import GitHubClient


def run(task: str) -> dict:
    client = GitHubClient()
    result = run_ai_engine("publish", task)
    result["github"] = client.healthcheck()
    return result

