from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Translate this request into a focus/frequency routine. "
        "Return a daily cadence and measurable outcomes.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    return {
        "engine": "frequency",
        "status": "completed",
        "output": output,
    }

