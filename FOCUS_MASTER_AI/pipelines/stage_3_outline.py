from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Create a concise project outline with phases and deliverables "
        "for the task below.\n\n"
        f"Task: {task}"
    )
    return {
        "engine": "outline",
        "status": "completed",
        "output": call_gpt(prompt),
    }

