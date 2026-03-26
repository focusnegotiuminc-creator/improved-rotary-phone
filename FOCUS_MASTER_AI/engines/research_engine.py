from __future__ import annotations

from core.memory_manager import MemoryManager
from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    memory = MemoryManager()
    cache_key = task.strip().lower()
    cached = memory.get_research_cache(cache_key)
    if cached:
        return {
            "engine": "research",
            "status": "completed",
            "cached": True,
            "output": cached,
        }

    prompt = (
        "Perform concise research planning for this user request. "
        "Return a practical summary and next actions.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    memory.set_research_cache(cache_key, output)

    return {
        "engine": "research",
        "status": "completed",
        "cached": False,
        "output": output,
    }

