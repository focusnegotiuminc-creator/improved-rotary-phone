from __future__ import annotations

import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv

try:
    from FOCUS_MASTER_AI.core.business_os import BusinessOperatingSystem
    from FOCUS_MASTER_AI.core.operator_runtime import OperatorRuntime
    from FOCUS_MASTER_AI.main import execute_command
except ImportError:
    from core.business_os import BusinessOperatingSystem
    from core.operator_runtime import OperatorRuntime
    from main import execute_command


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    business_os = BusinessOperatingSystem()
    operator_runtime = OperatorRuntime()
    app.config["BUSINESS_OS"] = business_os
    app.config["OPERATOR_RUNTIME"] = operator_runtime

    @app.get("/")
    def home():
        return app.send_static_file("operator_console.html")

    @app.get("/operator")
    def operator_console():
        return app.send_static_file("operator_console.html")

    @app.get("/private-console")
    def private_console():
        return app.send_static_file("private_console.html")

    @app.get("/health")
    def health():
        return jsonify(business_os.build_status()), 200

    @app.get("/v1/private/runtime")
    def private_runtime_status():
        return jsonify({"ok": True, "runtime": operator_runtime.status()}), 200

    @app.get("/v1/private/runs")
    def private_runs():
        limit = request.args.get("limit", default=20, type=int)
        return jsonify({"ok": True, "runs": operator_runtime.list_runs(limit=limit)}), 200

    @app.get("/v1/private/runs/<run_id>")
    def private_run_detail(run_id: str):
        run = operator_runtime.get_run(run_id)
        if run is None:
            return jsonify({"ok": False, "error": "run not found"}), 404
        return jsonify({"ok": True, "run": run}), 200

    @app.get("/v1/private/runs/<run_id>/artifacts")
    def private_run_artifacts(run_id: str):
        run = operator_runtime.get_run(run_id)
        if run is None:
            return jsonify({"ok": False, "error": "run not found"}), 404
        return jsonify({"ok": True, "artifacts": operator_runtime.list_artifacts(run_id)}), 200

    @app.post("/v1/private/runs")
    def create_private_run():
        payload = request.get_json(silent=True) or {}
        try:
            run = operator_runtime.create_run(payload)
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400
        return jsonify({"ok": True, "run": run}), 201

    @app.post("/v1/private/jobs")
    def create_private_job():
        payload = request.get_json(silent=True) or {}
        try:
            run = operator_runtime.submit_run(payload)
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400
        return jsonify({"ok": True, "run": run}), 202

    @app.get("/v1/private/stacks")
    def private_stacks():
        return jsonify({"ok": True, "stacks": operator_runtime.status()["stacks"]}), 200

    @app.get("/v1/private/tools")
    def private_tools():
        return jsonify({"ok": True, "tools": operator_runtime.status()["tools"]}), 200

    @app.post("/run")
    def run_task():
        payload = request.get_json(silent=True) or {}
        task = str(payload.get("task", "")).strip()
        if not task:
            return jsonify({"ok": False, "error": "task is required"}), 400

        result = execute_command(task)
        return jsonify({"ok": True, "task": task, "result": result}), 200

    @app.get("/v1/offers")
    def offers():
        return jsonify({"offers": business_os.list_offers()}), 200

    @app.get("/v1/workflows")
    def workflows():
        return jsonify({"workflows": business_os.list_workflows()}), 200

    @app.get("/v1/connectors")
    def connectors():
        return jsonify({"connectors": business_os.list_connectors()}), 200

    @app.get("/v1/mobile/config")
    def mobile_config():
        return jsonify(business_os.mobile_config()), 200

    @app.get("/v1/daily-command-mode")
    def daily_command_mode():
        return jsonify(business_os.daily_command_mode()), 200

    @app.get("/v1/knowledge")
    def knowledge():
        limit = request.args.get("limit", type=int)
        return jsonify(business_os.get_knowledge_snapshot(limit=limit)), 200

    @app.post("/v1/tasks")
    def create_task():
        payload = request.get_json(silent=True) or {}
        try:
            task = business_os.create_task(payload)
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400
        return jsonify({"ok": True, "task": task}), 201

    @app.get("/v1/tasks")
    def list_tasks():
        return jsonify({"tasks": business_os.tasks.read()}), 200

    @app.get("/v1/tasks/<task_id>")
    def get_task(task_id: str):
        task = business_os.get_task(task_id)
        if task is None:
            return jsonify({"ok": False, "error": "task not found"}), 404
        return jsonify({"ok": True, "task": task}), 200

    @app.patch("/v1/tasks/<task_id>")
    def update_task(task_id: str):
        payload = request.get_json(silent=True) or {}
        task = business_os.update_task(
            task_id,
            status=payload.get("status"),
            notes=payload.get("notes"),
            result_path=payload.get("result_path"),
            result_summary=payload.get("result_summary"),
        )
        if task is None:
            return jsonify({"ok": False, "error": "task not found"}), 404
        return jsonify({"ok": True, "task": task}), 200

    @app.post("/v1/workflows/<workflow_id>/run")
    def run_workflow(workflow_id: str):
        payload = request.get_json(silent=True) or {}
        try:
            task = business_os.run_workflow(workflow_id, payload)
        except KeyError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 404
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400
        return jsonify({"ok": True, "task": task}), 200

    @app.post("/v1/leads")
    def create_lead():
        payload = request.get_json(silent=True) or {}
        try:
            lead = business_os.register_lead(payload)
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400
        return jsonify({"ok": True, "lead": lead}), 201

    @app.post("/v1/content/generate")
    def generate_content():
        payload = request.get_json(silent=True) or {}
        try:
            job = business_os.create_content_job(payload)
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400
        return jsonify({"ok": True, "job": job}), 201

    @app.post("/v1/readiness/<kind>")
    def readiness(kind: str):
        payload = request.get_json(silent=True) or {}
        if kind not in {"legal", "payroll", "banking"}:
            return jsonify({"ok": False, "error": "unknown readiness pack type"}), 404
        try:
            pack = business_os.create_readiness_pack(kind, payload)
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400
        return jsonify({"ok": True, "readiness_pack": pack}), 201

    @app.get("/v1/readiness")
    def list_readiness():
        return jsonify({"readiness_packs": business_os.readiness_packs.read()}), 200

    return app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("FOCUS_API_HOST", "127.0.0.1").strip() or "127.0.0.1"
    port = int(os.getenv("FOCUS_API_PORT", "8000") or "8000")
    app.run(host=host, port=port, debug=False)
