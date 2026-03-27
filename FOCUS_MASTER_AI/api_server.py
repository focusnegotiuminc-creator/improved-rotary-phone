from __future__ import annotations

from flask import Flask, jsonify, request
from dotenv import load_dotenv

try:
    from FOCUS_MASTER_AI.core.business_os import BusinessOperatingSystem
    from FOCUS_MASTER_AI.main import execute_command
except ImportError:
    from core.business_os import BusinessOperatingSystem
    from main import execute_command


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    business_os = BusinessOperatingSystem()
    app.config["BUSINESS_OS"] = business_os

    @app.get("/")
    def home():
        return app.send_static_file("operator_console.html")

    @app.get("/operator")
    def operator_console():
        return app.send_static_file("operator_console.html")

    @app.get("/health")
    def health():
        return jsonify(business_os.build_status()), 200

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
    app.run(host="0.0.0.0", port=8000, debug=False)
