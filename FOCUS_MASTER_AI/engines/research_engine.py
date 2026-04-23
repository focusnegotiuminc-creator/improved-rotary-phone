from __future__ import annotations

try:
    from FOCUS_MASTER_AI.core.engine_runtime import run_ai_engine
    from FOCUS_MASTER_AI.core.memory_manager import MemoryManager
except ImportError:
    from core.engine_runtime import run_ai_engine
    from core.memory_manager import MemoryManager


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

    result = run_ai_engine("research", task)
    memory.set_research_cache(cache_key, result["output"])
    result["cached"] = False
    return result

