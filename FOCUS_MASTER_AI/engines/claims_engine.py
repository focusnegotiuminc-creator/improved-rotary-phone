from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Extract key claims from the task and suggest how to verify each claim. "
        "Keep it structured and actionable.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    return {
        "engine": "claims",
        "status": "completed",
        "output": output,
    }

