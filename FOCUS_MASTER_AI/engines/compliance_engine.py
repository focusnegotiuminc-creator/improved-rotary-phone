from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Review this task with a compliance mindset. "
        "List regulatory concerns, policy risks, and suggested safeguards.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    return {
        "engine": "compliance",
        "status": "completed",
        "output": output,
    }

