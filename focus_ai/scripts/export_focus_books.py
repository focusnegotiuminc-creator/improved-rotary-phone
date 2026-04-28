#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from site_catalog import BOOK_BY_SOURCE

ROOT = Path(__file__).resolve().parents[1]
EBOOKS = ROOT / "ebooks"
PUBLISHED_PDFS = ROOT / "published" / "ebooks" / "pdfs"
CONFIG = ROOT / "config" / "business_os.json"
DESKTOP = Path.home() / "Desktop"
DESKTOP_OUT = DESKTOP / "Focus Books"


def load_contact_phone() -> str:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    return "".join(char for char in data["portal"]["primary_contact"]["phone"] if char.isdigit())


def build_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "FocusBookTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#c68e19"),
            spaceAfter=18,
        ),
        "heading": ParagraphStyle(
            "FocusBookHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1b2c4a"),
            spaceBefore=14,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "FocusBookBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#1f2430"),
            spaceAfter=8,
        ),
        "meta": ParagraphStyle(
            "FocusBookMeta",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#3b597f"),
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "FocusBookBullet",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=16,
            leftIndent=16,
            bulletIndent=4,
            textColor=colors.HexColor("#1f2430"),
            spaceAfter=5,
        ),
    }


def paragraphs_from_markdown(markdown: str, title: str, tag: str, price: float, phone: str):
    styles = build_styles()
    story = [
        Paragraph(title, styles["title"]),
        Paragraph(f"{tag} | Suggested digital price {price:,.2f} USD", styles["meta"]),
        Paragraph(f"Published for TheFocusCorp.com | Routing line {phone}", styles["meta"]),
        Spacer(1, 0.16 * inch),
    ]

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            story.append(Paragraph(line[3:], styles["heading"]))
            continue
        if line.startswith("### "):
            story.append(Paragraph(line[4:], styles["heading"]))
            continue
        if line.startswith("- "):
            story.append(Paragraph(line[2:], styles["bullet"], bulletText="•"))
            continue
        if line[:2].isdigit() and line[1:3] == ". ":
            story.append(Paragraph(line[3:], styles["bullet"], bulletText="•"))
            continue
        story.append(Paragraph(line, styles["body"]))
    return story


def export_pdf(source_path: Path, out_path: Path, phone: str) -> None:
    meta = BOOK_BY_SOURCE.get(source_path.name, {
        "title": source_path.stem.replace("_", " ").title(),
        "tag": "Published title",
        "price_usd": 14.99,
    })
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        author="The Focus Corporation",
        title=meta["title"],
    )
    story = paragraphs_from_markdown(
        source_path.read_text(encoding="utf-8"),
        meta["title"],
        meta["tag"],
        float(meta["price_usd"]),
        phone,
    )
    doc.build(story)


def main() -> int:
    phone = load_contact_phone()
    markdown_files = sorted(EBOOKS.glob("*.md"))
    if not markdown_files:
        print("No book manuscripts found.")
        return 1

    DESKTOP_OUT.mkdir(parents=True, exist_ok=True)
    PUBLISHED_PDFS.mkdir(parents=True, exist_ok=True)

    for source_path in markdown_files:
        meta = BOOK_BY_SOURCE.get(source_path.name, {"slug": source_path.stem})
        file_name = f"{meta['slug']}.pdf"
        export_pdf(source_path, DESKTOP_OUT / file_name, phone)
        export_pdf(source_path, PUBLISHED_PDFS / file_name, phone)

    print(f"Exported {len(markdown_files)} PDFs to {DESKTOP_OUT}")
    print(f"Exported {len(markdown_files)} PDFs to {PUBLISHED_PDFS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
