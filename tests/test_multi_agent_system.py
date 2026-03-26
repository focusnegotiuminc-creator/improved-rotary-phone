from core.dispatcher import dispatch_task
from core.orchestrator import run_parallel, run_task
from core.task_classifier import classify_task


def test_classify_task_routes_research():
    assert classify_task("Please do research on stone circles") == "research"


def test_dispatch_task_unknown():
    assert dispatch_task("nothing to route here") == "Unknown task"


def test_run_task_persists_and_returns_result():
    result = run_task("write a short chapter")
    assert "Writing engine completed task" in result


def test_run_parallel_returns_results_for_each_task():
    tasks = ["research solar alignment", "marketing funnel optimization"]
    results = run_parallel(tasks)
    assert len(results) == 2
    assert "Research engine completed task" in results[0]
    assert "Marketing engine completed task" in results[1]
