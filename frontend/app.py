from __future__ import annotations

import subprocess
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

ROOT = Path(__file__).resolve().parents[1]
app = Flask(__name__)

TASKS = {
    "books": ROOT / "automation" / "book_writer.py",
    "blueprints": ROOT / "automation" / "blueprint_generator.py",
    "business": ROOT / "automation" / "business_generator.py",
    "marketing": ROOT / "automation" / "marketing_engine.py",
    "all": ROOT / "automation" / "ai_generator.py",
}


def read_file(path: Path) -> str:
    if not path.exists():
        return "No content generated yet."
    return path.read_text(encoding="utf-8")[:5000]


@app.route("/")
def home():
    products = read_file(ROOT / "final_product" / "business_products.md")
    marketing = read_file(ROOT / "marketing" / "marketing_assets.md")
    return render_template("index.html", products=products, marketing=marketing)


@app.route("/run", methods=["POST"])
def run():
    task = request.form.get("task", "")
    script = TASKS.get(task)
    if script:
        subprocess.run(["python", str(script)], check=False)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
