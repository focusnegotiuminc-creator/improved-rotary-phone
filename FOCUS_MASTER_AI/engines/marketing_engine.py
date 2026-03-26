from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Create a marketing execution strategy with channels, message angle, "
        "offer framing, and KPIs.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    return {
        "engine": "marketing",
        "status": "completed",
        "output": output,
    }

