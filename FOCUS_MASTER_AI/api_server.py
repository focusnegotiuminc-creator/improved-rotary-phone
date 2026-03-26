from __future__ import annotations

from flask import Flask, jsonify, request
from dotenv import load_dotenv

from main import execute_command


load_dotenv()
app = Flask(__name__)


@app.get("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok", "service": "focus_master_ai"}, 200


@app.post("/run")
def run_task():
    payload = request.get_json(silent=True) or {}
    task = str(payload.get("task", "")).strip()
    if not task:
        return jsonify({"ok": False, "error": "task is required"}), 400

    result = execute_command(task)
    return jsonify({"ok": True, "task": task, "result": result}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

