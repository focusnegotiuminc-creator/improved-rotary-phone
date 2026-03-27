from __future__ import annotations

import json
import sys
from typing import Any

from dotenv import load_dotenv

try:
    from FOCUS_MASTER_AI.core.business_os import BusinessOperatingSystem
    from FOCUS_MASTER_AI.core.dispatcher import dispatch_task
    from FOCUS_MASTER_AI.core.parallel import run_parallel
except ImportError:
    from core.business_os import BusinessOperatingSystem
    from core.dispatcher import dispatch_task
    from core.parallel import run_parallel


def _format_output(data: Any) -> str:
    if isinstance(data, (dict, list)):
        return json.dumps(data, indent=2)
    return str(data)


def execute_command(task: str) -> Any:
    cleaned = task.strip()
    if not cleaned:
        return "No command provided."

    business_os = BusinessOperatingSystem()
    normalized = cleaned.lower()

    if "," in cleaned:
        tasks = [item.strip() for item in cleaned.split(",") if item.strip()]
        return run_parallel(tasks)

    if normalized in {"offers", "show offers", "list offers"}:
        return {"offers": business_os.list_offers()}
    if normalized in {"connectors", "connector status", "show connectors"}:
        return {"connectors": business_os.list_connectors()}
    if normalized in {"daily command mode", "status", "business status"}:
        return business_os.daily_command_mode()
    if normalized in {"knowledge", "knowledge snapshot"}:
        return business_os.get_knowledge_snapshot(limit=40)

    return dispatch_task(cleaned)


def _banner() -> None:
    print("🔥 FOCUS MASTER AI ENGINE LIVE 🔥")
    print("Type a command, comma-separate multiple tasks, or type 'exit' to quit.")


def main() -> None:
    load_dotenv()

    if len(sys.argv) > 1:
        cli_task = " ".join(sys.argv[1:])
        print(_format_output(execute_command(cli_task)))
        return

    _banner()
    while True:
        task = input("\nEnter command: ").strip()
        if task.lower() == "exit":
            print("Shutting down FOCUS MASTER AI.")
            break
        print(_format_output(execute_command(task)))


if __name__ == "__main__":
    main()
