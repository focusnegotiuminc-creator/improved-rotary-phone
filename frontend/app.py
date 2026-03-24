from __future__ import annotations

import csv
import subprocess
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "final_product"
LEADS_FILE = DATA_DIR / "leads.csv"
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
    return path.read_text(encoding="utf-8")[:6000]


def append_lead(email: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_exists = LEADS_FILE.exists()
    with LEADS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email"])
        writer.writerow([email.strip().lower()])


@app.route("/")
def home():
    products = read_file(ROOT / "final_product" / "business_products.md")
    marketing = read_file(ROOT / "marketing" / "marketing_assets.md")
    return render_template("index.html", products=products, marketing=marketing)


@app.route("/landing")
def landing():
    return render_template("landing.html")


@app.route("/capture", methods=["POST"])
def capture():
    email = request.form.get("email", "").strip()
    if email and "@" in email:
        append_lead(email)
    return redirect(url_for("delivery"))


@app.route("/delivery")
def delivery():
    return render_template("delivery.html")


@app.route("/upsell")
def upsell():
    return render_template("upsell.html")


@app.route("/high-ticket")
def high_ticket():
    return render_template("high_ticket.html")


@app.route("/run", methods=["POST"])
def run():
    task = request.form.get("task", "")
    script = TASKS.get(task)
    if script:
        subprocess.run(["python", str(script)], check=False)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
