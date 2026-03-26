from core.dispatcher import dispatch_task

def run(task: str) -> str:
    return dispatch_task(f"write: {task}")
