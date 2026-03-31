from __future__ import annotations

import csv
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"


def pdf_from_table(out_path: Path, title: str, rows: list[list[str]]) -> None:
    doc = SimpleDocTemplate(str(out_path), pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    title_style = ParagraphStyle(name="Title", fontSize=14, leading=18, spaceAfter=12)
    elements.append(Paragraph(title, title_style))
    table = Table(rows, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2a33")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#7a7a7a")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    elements.append(table)
    doc.build(elements)


def pdf_from_text(out_path: Path, title: str, text: str) -> None:
    doc = SimpleDocTemplate(str(out_path), pagesize=letter, leftMargin=48, rightMargin=48, topMargin=48, bottomMargin=48)
    elements = []
    title_style = ParagraphStyle(name="Title", fontSize=14, leading=18, spaceAfter=12)
    body_style = ParagraphStyle(name="Body", fontSize=10, leading=14, spaceAfter=6)
    elements.append(Paragraph(title, title_style))
    for line in text.splitlines():
        if not line.strip():
            elements.append(Spacer(1, 6))
        else:
            elements.append(Paragraph(line, body_style))
    doc.build(elements)


def main() -> None:
    material_csv = OUTPUT_DIR / "material_list.csv"
    bid_csv = OUTPUT_DIR / "bid_summary.csv"
    bid_json = OUTPUT_DIR / "bid_summary.json"
    insurance_md = OUTPUT_DIR / "insurance_license_summary.md"

    if material_csv.exists():
        with material_csv.open("r", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
        pdf_from_table(OUTPUT_DIR / "material_list.pdf", "Material List (Public Pricing)", rows)

    if bid_csv.exists():
        with bid_csv.open("r", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
        pdf_from_table(OUTPUT_DIR / "bid_summary.pdf", "Bid Summary", rows)

    if bid_json.exists():
        payload = json.loads(bid_json.read_text(encoding="utf-8"))
        rows = [["Label", "Amount"]]
        for row in payload:
            rows.append([str(row.get("Label", "")), f"${row.get('Amount', 0):,.2f}"])
        pdf_from_table(OUTPUT_DIR / "bid_summary_json.pdf", "Bid Summary (JSON)", rows)

    if insurance_md.exists():
        pdf_from_text(
            OUTPUT_DIR / "insurance_license_summary.pdf",
            "Insurance & License Summary (Draft)",
            insurance_md.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    main()
