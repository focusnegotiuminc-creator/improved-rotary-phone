from __future__ import annotations

import csv
import json
import math
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DUMPSTER_ALLOWANCE = 450.0
INSURANCE_FEE = 300.0


def parse_feet(value: str) -> float:
    """Parse a dimension like 13' 4 3/4 into decimal feet."""
    value = value.replace('"', "").strip()
    if "'" not in value:
        inches = 0.0
        for part in value.split():
            if "/" in part:
                num, den = part.split("/")
                inches += float(num) / float(den)
            else:
                inches += float(part)
        return inches / 12.0
    feet_str, inches_str = value.split("'")
    feet = float(feet_str.strip() or 0)
    inches_str = inches_str.strip()
    if not inches_str:
        return feet
    inches = 0.0
    parts = inches_str.split()
    for part in parts:
        if "/" in part:
            num, den = part.split("/")
            inches += float(num) / float(den)
        else:
            inches += float(part)
    return feet + inches / 12.0


def feet_to_str(value: float) -> str:
    total_inches = value * 12
    feet = int(total_inches // 12)
    inches = total_inches - feet * 12
    return f"{feet}'-{inches:.2f}\""


@dataclass
class FloorAssumptions:
    name: str
    height_ft: float
    perimeter_ft: float
    interior_partition_ft: float
    door_count: int
    floor_area_sqft: float

    @property
    def wall_area_sqft(self) -> float:
        # Perimeter gets one side of drywall, partitions get two sides.
        base_area = self.perimeter_ft * self.height_ft + 2 * self.interior_partition_ft * self.height_ft
        door_area = self.door_count * (3.0 * 7.0)
        return max(base_area - door_area, 0.0)


def ceiling_grid_takeoff(length_ft: float, width_ft: float) -> dict[str, int]:
    # Simple 2x4 grid takeoff.
    main_spacing = 4.0
    module = 4.0

    main_runs = math.ceil(width_ft / main_spacing) + 1
    modules_along = math.ceil(length_ft / module)
    main_length_total = main_runs * length_ft
    main_pieces = math.ceil(main_length_total / 12.0)

    cross_4ft = main_runs - 1
    total_4ft = cross_4ft * modules_along
    total_2ft = total_4ft

    hanger_wires = main_runs * math.ceil(length_ft / 4.0)

    wall_angle = math.ceil((2 * (length_ft + width_ft)) / 12.0)

    return {
        "main_tee_12ft": main_pieces,
        "cross_tee_4ft": total_4ft,
        "cross_tee_2ft": total_2ft,
        "wall_angle_12ft": wall_angle,
        "hanger_wire_12ft": hanger_wires,
    }


def drywall_sheet_count(area_sqft: float, waste: float = 0.1) -> int:
    return math.ceil(area_sqft * (1 + waste) / 32.0)


def paint_gallons(area_sqft: float, coats: int = 2, coverage_sqft_per_gal: int = 350) -> int:
    return math.ceil((area_sqft * coats) / coverage_sqft_per_gal)


def compound_buckets(area_sqft: float, coverage_sqft: int = 500) -> int:
    return math.ceil(area_sqft / coverage_sqft)


def tape_rolls(sheet_count: int, roll_ft: int = 500) -> int:
    # Approximate 12 linear feet of tape per sheet.
    total_ft = sheet_count * 12 * 1.1
    return math.ceil(total_ft / roll_ft)


def screw_boxes(sheet_count: int, sheets_per_box: int = 34) -> int:
    return math.ceil(sheet_count / sheets_per_box)


def baseboard_lineal_ft(perimeter_ft: float, interior_partition_ft: float, door_count: int) -> float:
    door_width_total = door_count * 3.0
    total = perimeter_ft + 2 * interior_partition_ft - door_width_total
    return max(total, 0.0)


def build_dimension_schedule() -> dict[str, list[tuple[str, str]]]:
    return {
        "First Floor": [
            ("A", "13' 4 3/4\" (overall interior width)"),
            ("B", "28' 3 1/2\""),
            ("C", "8' 4\""),
            ("D", "10' 0\""),
            ("E", "14' 4 7/8\""),
            ("F", "6' 9 1/2\""),
            ("G", "8 3/4\" (bump-out)"),
            ("H", "13' 10 1/2\""),
            ("I", "12' 11 1/2\""),
        ],
        "Second Floor": [
            ("A", "13' 11\""),
            ("B", "10' 4 3/4\""),
            ("C", "8' 4\""),
            ("D", "10' 7\""),
            ("E", "7' 0\""),
            ("F", "9' 7 1/4\""),
            ("G", "16 3/8\""),
            ("H", "11' 1 3/8\""),
            ("I", "9' 4\""),
            ("J", "13' 8 1/2\""),
            ("K", "11' 11\""),
            ("L", "12' 0\""),
            ("M", "13' 8 1/4\""),
            ("N", "8' 7\""),
            ("O", "12 7/8\""),
            ("P", "8' 7\""),
        ],
    }


def build_floor_assumptions() -> tuple[FloorAssumptions, FloorAssumptions]:
    # Assumptions derived from the provided sketch values.
    first_width = parse_feet("13' 4 3/4\"")
    first_length = parse_feet("28' 3 1/2\"")
    bump_out = parse_feet("8 3/4\"")
    bump_height = parse_feet("6' 9 1/2\"")
    floor1_area = first_width * first_length + bump_out * bump_height

    # Interior partition length sum (based on provided dimensions).
    first_partitions = sum(
        parse_feet(value)
        for value in ["8' 4\"", "10' 0\"", "14' 4 7/8\"", "6' 9 1/2\"", "13' 10 1/2\"", "12' 11 1/2\""]
    )

    first_perimeter = 2 * (first_width + first_length)

    floor1 = FloorAssumptions(
        name="First Floor",
        height_ft=9.5,
        perimeter_ft=first_perimeter,
        interior_partition_ft=first_partitions,
        door_count=3,
        floor_area_sqft=floor1_area,
    )

    second_width = parse_feet("10' 7\"") + parse_feet("8' 4\"")
    second_length = parse_feet("13' 11\"")
    floor2_area = second_width * second_length

    second_partitions = sum(
        parse_feet(value)
        for value in [
            "7' 0\"",
            "9' 7 1/4\"",
            "11' 1 3/8\"",
            "9' 4\"",
            "11' 11\"",
            "12' 0\"",
            "13' 8 1/4\"",
            "8' 7\"",
            "8' 7\"",
        ]
    )

    second_perimeter = 2 * (second_width + second_length)

    floor2 = FloorAssumptions(
        name="Second Floor",
        height_ft=8.5,
        perimeter_ft=second_perimeter,
        interior_partition_ft=second_partitions,
        door_count=2,
        floor_area_sqft=floor2_area,
    )

    return floor1, floor2


def write_materials(materials: list[dict[str, object]], path: Path) -> None:
    headers = [
        "Category",
        "Item",
        "Supplier",
        "Quantity",
        "Unit",
        "Unit Price (USD)",
        "Line Total (USD)",
        "Notes",
        "Source",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in materials:
            writer.writerow(row)


def draw_floor_plan(
    c: canvas.Canvas,
    origin_x: float,
    origin_y: float,
    width_ft: float,
    length_ft: float,
    walls: list[list[tuple[float, float]]],
    labels: list[tuple[str, float, float]],
    title: str,
) -> None:
    # Scale to fit into a 500x320pt box.
    max_w = 500.0
    max_h = 320.0
    scale = min(max_w / width_ft, max_h / length_ft)

    def tx(x: float) -> float:
        return origin_x + x * scale

    def ty(y: float) -> float:
        return origin_y + y * scale

    c.setStrokeColor(colors.HexColor("#111111"))
    c.setLineWidth(2)
    for path in walls:
        for idx in range(len(path) - 1):
            x1, y1 = path[idx]
            x2, y2 = path[idx + 1]
            c.line(tx(x1), ty(y1), tx(x2), ty(y2))

    c.setFont("Helvetica-Bold", 12)
    c.drawString(origin_x, origin_y + max_h + 20, title)
    c.setFont("Helvetica", 9)
    for label, x, y in labels:
        c.drawString(tx(x), ty(y), label)


def draw_floor_plan_scaled(
    c: canvas.Canvas,
    origin_x: float,
    origin_y: float,
    scale: float,
    walls: list[list[tuple[float, float]]],
    labels: list[tuple[str, float, float]],
    title: str,
) -> None:
    def tx(x: float) -> float:
        return origin_x + x * scale

    def ty(y: float) -> float:
        return origin_y + y * scale

    c.setStrokeColor(colors.HexColor("#0d0d0d"))
    c.setLineWidth(2)
    for path in walls:
        for idx in range(len(path) - 1):
            x1, y1 = path[idx]
            x2, y2 = path[idx + 1]
            c.line(tx(x1), ty(y1), tx(x2), ty(y2))

    c.setFont("Helvetica-Bold", 14)
    c.drawString(origin_x, origin_y + 540, title)
    c.setFont("Helvetica", 10)
    for label, x, y in labels:
        c.drawString(tx(x), ty(y), label)


def draw_dim_line(
    c: canvas.Canvas,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str,
) -> None:
    c.setStrokeColor(colors.HexColor("#3a3a3a"))
    c.setLineWidth(1)
    c.line(x1, y1, x2, y2)
    if abs(y2 - y1) < 0.1:
        # horizontal
        c.line(x1, y1 - 6, x1, y1 + 6)
        c.line(x2, y2 - 6, x2, y2 + 6)
        c.setFont("Helvetica", 9)
        c.drawCentredString((x1 + x2) / 2, y1 + 8, label)
    else:
        c.line(x1 - 6, y1, x1 + 6, y1)
        c.line(x2 - 6, y2, x2 + 6, y2)
        c.setFont("Helvetica", 9)
        c.drawCentredString(x1 + 14, (y1 + y2) / 2, label)


def build_blueprint_svg(path: Path, floor: FloorAssumptions, dimensions: list[tuple[str, str]]) -> None:
    # Build a stylized floor plan diagram with dimension labels.
    width = 900
    height = 650
    margin = 60
    rect_w = width - margin * 2
    rect_h = height - margin * 2

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#f7f3ea"/>',
        f'<rect x="{margin}" y="{margin}" width="{rect_w}" height="{rect_h}" fill="none" stroke="#111" stroke-width="3"/>',
        f'<text x="{width/2}" y="40" font-family="Helvetica" font-size="22" text-anchor="middle">{floor.name} Plan (Schematic)</text>',
        f'<text x="{width/2}" y="{height-15}" font-family="Helvetica" font-size="12" text-anchor="middle">Dimensions provided by owner; verify field before fabrication.</text>',
    ]
    # Place dimension labels on right side.
    start_y = margin + 20
    for label, value in dimensions:
        svg_lines.append(
            f'<text x="{width-20}" y="{start_y}" font-family="Helvetica" font-size="12" text-anchor="end">{label}: {value}</text>'
        )
        start_y += 18

    svg_lines.append('</svg>')
    path.write_text("\n".join(svg_lines), encoding="utf-8")


def build_report(
    output_pdf: Path,
    floor1: FloorAssumptions,
    floor2: FloorAssumptions,
    materials: list[dict[str, object]],
    bid_summary: list[dict[str, object]],
    permit_text: str,
    contract_text: str,
    certificate_text: str,
    dimension_schedule: dict[str, list[tuple[str, str]]],
) -> None:
    c = canvas.Canvas(str(output_pdf), pagesize=letter)
    width, height = letter
    logo_path = ROOT / "assets" / "logos" / "clean" / "rlc_clean.png"

    def draw_watermark() -> None:
        c.saveState()
        c.setFillColor(colors.Color(0.7, 0.65, 0.5, alpha=0.12))
        c.setFont("Helvetica-Bold", 48)
        c.translate(width / 2, height / 2)
        c.rotate(30)
        c.drawCentredString(0, 0, "ROYAL LEE CONSTRUCTION SOLUTIONS")
        c.restoreState()

    def header(title: str) -> None:
        draw_watermark()
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, height - 50, title)
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 65, f"Prepared: {datetime.now().strftime('%B %d, %Y')}")
        if logo_path.exists():
            c.drawImage(ImageReader(str(logo_path)), width - 140, height - 90, width=90, height=60, mask="auto")

    def new_page(title: str) -> None:
        c.showPage()
        header(title)

    header("Royal Lee Construction Solutions | Office Renovation Package")
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 90, "Project: Office Renovation - Steven Bunch")
    c.drawString(40, height - 105, "Jobsite: 522 Vermont St, Quincy, IL")
    c.drawString(40, height - 120, "Scope: Demo + replace drywall, ceiling grid, base, repaint")
    c.drawString(40, height - 135, "Note: This package is based on provided sketches and measurements.")
    c.drawString(40, height - 150, "Pricing basis: Existing material stack retained from the prior package, with only missing allowances added.")

    y = height - 170
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Floor Area Summary")
    y -= 18
    c.setFont("Helvetica", 11)
    for floor in [floor1, floor2]:
        c.drawString(40, y, f"{floor.name}: {floor.floor_area_sqft:.1f} sq ft")
        y -= 15
    c.drawString(40, y, f"Total: {floor1.floor_area_sqft + floor2.floor_area_sqft:.1f} sq ft")

    # Insert dimension schedule
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Dimension Schedule (Owner Provided)")
    y -= 18
    c.setFont("Helvetica", 10)
    for floor_name, items in dimension_schedule.items():
        c.drawString(40, y, floor_name)
        y -= 14
        for label, value in items:
            c.drawString(60, y, f"{label}: {value}")
            y -= 12
        y -= 6

    new_page("Floor Plan Diagrams")
    # Draw first floor plan
    first_width = parse_feet("13' 4 3/4\"")
    first_length = parse_feet("28' 3 1/2\"")
    bump_depth = parse_feet("8 3/4\"")
    bump_height = parse_feet("6' 9 1/2\"")
    bath_width = parse_feet("4' 4 3/8\"")
    bath_depth = parse_feet("10' 0\"")
    stair_width = parse_feet("4' 5\"")
    stair_depth = parse_feet("13' 10 1/2\"")

    outer = [
        (0, 0),
        (first_width, 0),
        (first_width + bump_depth, 0),
        (first_width + bump_depth, bump_height),
        (first_width, bump_height),
        (first_width, first_length),
        (0, first_length),
        (0, 0),
    ]
    bath = [
        (0, 0),
        (bath_width, 0),
        (bath_width, bath_depth),
        (0, bath_depth),
        (0, 0),
    ]
    stairs = [
        (first_width - stair_width, first_length - stair_depth),
        (first_width, first_length - stair_depth),
        (first_width, first_length),
        (first_width - stair_width, first_length),
        (first_width - stair_width, first_length - stair_depth),
    ]
    labels = [
        ("Entry bump-out", first_width + bump_depth * 0.2, bump_height * 0.2),
        ("Bath/Closet", bath_width * 0.2, bath_depth * 0.4),
        ("Stairs", first_width - stair_width * 0.8, first_length - stair_depth * 0.4),
    ]

    draw_floor_plan(
        c,
        origin_x=40,
        origin_y=200,
        width_ft=first_width + bump_depth,
        length_ft=first_length,
        walls=[outer, bath, stairs],
        labels=labels,
        title="First Floor Plan (scaled from provided dimensions)",
    )

    c.setFont("Helvetica", 10)
    c.drawString(40, 180, "Doors: 3 (1 entry + 2 sliding plastic doorways indicated on sketch).")
    c.showPage()

    # Draw second floor plan
    second_width = parse_feet("10' 7\"") + parse_feet("8' 4\"")
    second_length = parse_feet("13' 11\"")
    hall_height = parse_feet("2' 6\"")
    hall_y = second_length / 2 - hall_height / 2
    top_left_width = parse_feet("10' 7\"")
    top_left_depth = parse_feet("7' 0\"")
    top_right_width = parse_feet("8' 4\"")
    top_right_depth = parse_feet("10' 4 3/4\"")

    outer2 = [
        (0, 0),
        (second_width, 0),
        (second_width, second_length),
        (0, second_length),
        (0, 0),
    ]
    hall = [
        (0, hall_y),
        (second_width, hall_y),
        (second_width, hall_y + hall_height),
        (0, hall_y + hall_height),
        (0, hall_y),
    ]
    top_left = [
        (0, second_length - top_left_depth),
        (top_left_width, second_length - top_left_depth),
        (top_left_width, second_length),
        (0, second_length),
        (0, second_length - top_left_depth),
    ]
    top_right = [
        (second_width - top_right_width, second_length - top_right_depth),
        (second_width, second_length - top_right_depth),
        (second_width, second_length),
        (second_width - top_right_width, second_length),
        (second_width - top_right_width, second_length - top_right_depth),
    ]

    labels2 = [
        ("Stair Hall", second_width * 0.4, hall_y + hall_height * 0.3),
        ("Upper Left", top_left_width * 0.2, second_length - top_left_depth * 0.5),
        ("Upper Right", second_width - top_right_width * 0.8, second_length - top_right_depth * 0.5),
    ]

    draw_floor_plan(
        c,
        origin_x=40,
        origin_y=200,
        width_ft=second_width,
        length_ft=second_length,
        walls=[outer2, hall, top_left, top_right],
        labels=labels2,
        title="Second Floor Plan (scaled from provided dimensions)",
    )

    c.setFont("Helvetica", 10)
    c.drawString(40, 180, "Doorways: 1 near stairwell + 1 sliding plastic doorway (per sketch).")

    new_page("Material Takeoff Summary")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 90, "Materials (Key Items)")
    c.setFont("Helvetica", 9)
    c.drawString(40, height - 104, "Use this as an owner-review draft and confirm the final cart against current Menards store pricing before issue.")
    y = height - 122
    for row in materials:
        line = f"{row['Item']} | Qty {row['Quantity']} {row['Unit']} | ${row['Unit Price (USD)']}"
        c.drawString(40, y, line[:110])
        y -= 11
        if y < 60:
            c.showPage()
            y = height - 60

    new_page("Bid Summary")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 90, "Bid Summary (Labor Reduced by 2/3)")
    c.setFont("Helvetica", 10)
    y = height - 110
    for row in bid_summary:
        c.drawString(40, y, f"{row['Label']}: ${row['Amount']:.2f}")
        y -= 14

    new_page("Contract Draft")
    c.setFont("Helvetica", 9)
    y = height - 90
    for line in contract_text.splitlines():
        c.drawString(40, y, line[:110])
        y -= 11
        if y < 60:
            c.showPage()
            y = height - 60

    new_page("Warranty Certificate")
    # Sacred geometric border
    c.setStrokeColor(colors.HexColor("#c9a227"))
    c.setLineWidth(2)
    c.rect(30, 40, width - 60, height - 80)
    # border triangles
    for x in range(40, int(width - 60), 30):
        c.line(x, height - 60, x + 15, height - 40)
        c.line(x + 15, height - 40, x + 30, height - 60)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 90, "Royal Lee Construction Solutions")
    c.setFont("Helvetica", 10)
    y = height - 120
    for line in certificate_text.splitlines():
        c.drawString(50, y, line[:110])
        y -= 12

    new_page("Permit Application Draft")
    c.setFont("Helvetica", 9)
    y = height - 90
    for line in permit_text.splitlines():
        c.drawString(40, y, line[:110])
        y -= 11
        if y < 60:
            c.showPage()
            y = height - 60

    c.save()


def main() -> None:
    dimension_schedule = build_dimension_schedule()
    floor1, floor2 = build_floor_assumptions()

    # Ceiling grid takeoff based on overall floor areas (approximate rectangles).
    grid_floor1 = ceiling_grid_takeoff(parse_feet("28' 3 1/2\""), parse_feet("13' 4 3/4\""))
    grid_floor2 = ceiling_grid_takeoff(parse_feet("13' 11\""), parse_feet("18' 11 1/2\""))

    total_wall_area = floor1.wall_area_sqft + floor2.wall_area_sqft
    sheet_count = drywall_sheet_count(total_wall_area)

    paint_gal = paint_gallons(total_wall_area, coats=2)
    primer_gal = paint_gallons(total_wall_area, coats=1)

    materials = [
        {
            "Category": "Drywall",
            "Item": "5/8 in. x 4 ft. x 8 ft. Type X gypsum board",
            "Supplier": "Lowe's (Public)",
            "Quantity": sheet_count,
            "Unit": "sheets",
            "Unit Price (USD)": 19.98,
            "Line Total (USD)": round(sheet_count * 19.98, 2),
            "Notes": "Type X per owner request.",
            "Source": "https://www.lowes.com/pd/Gold-Bond-Brand-1-2-in-x-4-ft-x-8-ft-Drywall/5200101",
        },
        {
            "Category": "Ceiling",
            "Item": "2 ft. x 4 ft. acoustic ceiling tiles (64 sq ft/case)",
            "Supplier": "Home Depot (Public)",
            "Quantity": math.ceil((floor1.floor_area_sqft + floor2.floor_area_sqft) / 64.0),
            "Unit": "cases",
            "Unit Price (USD)": 59.88,
            "Line Total (USD)": round(math.ceil((floor1.floor_area_sqft + floor2.floor_area_sqft) / 64.0) * 59.88, 2),
            "Notes": "Basic 2x4 mineral fiber tile.",
            "Source": "https://www.homedepot.com/b/Ceiling-Tiles/N-5yc1vZc5kq",
        },
        {
            "Category": "Ceiling",
            "Item": "Main tee 12 ft (ceil grid)",
            "Supplier": "American Builder Supply (pricing ref)",
            "Quantity": grid_floor1["main_tee_12ft"] + grid_floor2["main_tee_12ft"],
            "Unit": "pieces",
            "Unit Price (USD)": 15.54,
            "Line Total (USD)": round((grid_floor1["main_tee_12ft"] + grid_floor2["main_tee_12ft"]) * 15.54, 2),
            "Notes": "Pricing referenced from public supplier, verify ABS.",
            "Source": "https://cardinalwarehouseinc.com/products/armstrong-7300xl-main-tee-12",
        },
        {
            "Category": "Ceiling",
            "Item": "Cross tee 4 ft",
            "Supplier": "American Builder Supply (pricing ref)",
            "Quantity": grid_floor1["cross_tee_4ft"] + grid_floor2["cross_tee_4ft"],
            "Unit": "pieces",
            "Unit Price (USD)": 4.78,
            "Line Total (USD)": round((grid_floor1["cross_tee_4ft"] + grid_floor2["cross_tee_4ft"]) * 4.78, 2),
            "Notes": "Pricing referenced from public supplier, verify ABS.",
            "Source": "https://cardinalwarehouseinc.com/products/armstrong-7300xl-4ft-cross-tee",
        },
        {
            "Category": "Ceiling",
            "Item": "Cross tee 2 ft (case of 60)",
            "Supplier": "American Builder Supply (pricing ref)",
            "Quantity": math.ceil((grid_floor1["cross_tee_2ft"] + grid_floor2["cross_tee_2ft"]) / 60.0),
            "Unit": "cases",
            "Unit Price (USD)": 141.00,
            "Line Total (USD)": round(math.ceil((grid_floor1["cross_tee_2ft"] + grid_floor2["cross_tee_2ft"]) / 60.0) * 141.00, 2),
            "Notes": "Case pricing, verify ABS.",
            "Source": "https://hdsupplysolutions.com/p/hg-grid-2ft-white-intermediate-tees-box-of-60-p243158",
        },
        {
            "Category": "Ceiling",
            "Item": "Wall angle 12 ft",
            "Supplier": "American Builder Supply (pricing ref)",
            "Quantity": grid_floor1["wall_angle_12ft"] + grid_floor2["wall_angle_12ft"],
            "Unit": "pieces",
            "Unit Price (USD)": 10.25,
            "Line Total (USD)": round((grid_floor1["wall_angle_12ft"] + grid_floor2["wall_angle_12ft"]) * 10.25, 2),
            "Notes": "Pricing referenced from public supplier, verify ABS.",
            "Source": "https://aorweb.com/product/armstrong-m7/"
        },
        {
            "Category": "Ceiling",
            "Item": "12-gauge hanger wire 12 ft",
            "Supplier": "American Builder Supply (pricing ref)",
            "Quantity": grid_floor1["hanger_wire_12ft"] + grid_floor2["hanger_wire_12ft"],
            "Unit": "pieces",
            "Unit Price (USD)": 2.20,
            "Line Total (USD)": round((grid_floor1["hanger_wire_12ft"] + grid_floor2["hanger_wire_12ft"]) * 2.20, 2),
            "Notes": "Pricing referenced from public supplier, verify ABS.",
            "Source": "https://turkstralumber.com/products/12-gauge-hanger-wire-12-ft"
        },
        {
            "Category": "Drywall Finishing",
            "Item": "All-purpose joint compound, 4.5 gal",
            "Supplier": "Walmart Business (Public)",
            "Quantity": compound_buckets(total_wall_area),
            "Unit": "buckets",
            "Unit Price (USD)": 74.99,
            "Line Total (USD)": round(compound_buckets(total_wall_area) * 74.99, 2),
            "Notes": "Ready-mix.",
            "Source": "https://business.walmart.com/ip/USG-SHEETROCK-Brand-All-Purpose-Joint-Compound-4-5-Gal-Blue-Cap/1171831039",
        },
        {
            "Category": "Drywall Finishing",
            "Item": "Paper joint tape 2\" x 500 ft",
            "Supplier": "Home Depot (Public)",
            "Quantity": tape_rolls(sheet_count),
            "Unit": "rolls",
            "Unit Price (USD)": 15.48,
            "Line Total (USD)": round(tape_rolls(sheet_count) * 15.48, 2),
            "Notes": "Standard paper tape.",
            "Source": "https://www.homedepot.com/p/USG-Sheetrock-Brand-2-1-16-in-x-500-ft-Paper-Drywall-Joint-Tape-382175/100321608",
        },
        {
            "Category": "Drywall Finishing",
            "Item": "10 ft metal corner bead",
            "Supplier": "Lenco Supplies (Public)",
            "Quantity": math.ceil((floor1.perimeter_ft + floor2.perimeter_ft) / 10.0),
            "Unit": "pieces",
            "Unit Price (USD)": 3.19,
            "Line Total (USD)": round(math.ceil((floor1.perimeter_ft + floor2.perimeter_ft) / 10.0) * 3.19, 2),
            "Notes": "Outside corners allowance.",
            "Source": "https://lencosupplies.com/products/ammow-wall-corner-bead-10ft-metal-1-1-4-expansion",
        },
        {
            "Category": "Drywall Finishing",
            "Item": "1-5/8 in. drywall screws (5 lb)",
            "Supplier": "Ace Hardware (Public)",
            "Quantity": screw_boxes(sheet_count),
            "Unit": "boxes",
            "Unit Price (USD)": 27.99,
            "Line Total (USD)": round(screw_boxes(sheet_count) * 27.99, 2),
            "Notes": "Fine thread, 5/8 Type X.",
            "Source": "https://www.acehardware.com/departments/hardware/screws-and-anchors/sheet-metal-screws/5356130",
        },
        {
            "Category": "Baseboard",
            "Item": "4 in. vinyl cove base (120 ft/case)",
            "Supplier": "Home Depot (Public)",
            "Quantity": math.ceil(baseboard_lineal_ft(floor1.perimeter_ft + floor2.perimeter_ft, floor1.interior_partition_ft + floor2.interior_partition_ft, floor1.door_count + floor2.door_count) / 120.0),
            "Unit": "cases",
            "Unit Price (USD)": 85.57,
            "Line Total (USD)": round(math.ceil(baseboard_lineal_ft(floor1.perimeter_ft + floor2.perimeter_ft, floor1.interior_partition_ft + floor2.interior_partition_ft, floor1.door_count + floor2.door_count) / 120.0) * 85.57, 2),
            "Notes": "Standard base, neutral color.",
            "Source": "https://www.homedepot.com/p/ROPPE-4-in-x-120-ft-Black-Premier-Rubber-Wall-Base-Cove-Base-Coil-HB-40P-110/100180026",
        },
        {
            "Category": "Baseboard",
            "Item": "Wall base adhesive (1 gal)",
            "Supplier": "Tools4Flooring (Public)",
            "Quantity": math.ceil(baseboard_lineal_ft(floor1.perimeter_ft + floor2.perimeter_ft, floor1.interior_partition_ft + floor2.interior_partition_ft, floor1.door_count + floor2.door_count) / 500.0),
            "Unit": "gallons",
            "Unit Price (USD)": 32.99,
            "Line Total (USD)": round(math.ceil(baseboard_lineal_ft(floor1.perimeter_ft + floor2.perimeter_ft, floor1.interior_partition_ft + floor2.interior_partition_ft, floor1.door_count + floor2.door_count) / 500.0) * 32.99, 2),
            "Notes": "Approx 500 LF per gallon.",
            "Source": "https://www.tools4flooring.com/ntb-f-66-wall-base-adhesive-1-gallon.html",
        },
        {
            "Category": "Paint",
            "Item": "Interior paint, 5 gal, eggshell",
            "Supplier": "Home Depot (Public)",
            "Quantity": math.ceil(paint_gal / 5.0),
            "Unit": "buckets",
            "Unit Price (USD)": 158.00,
            "Line Total (USD)": round(math.ceil(paint_gal / 5.0) * 158.00, 2),
            "Notes": "Walls, two coats, neutral tone.",
            "Source": "https://www.homedepot.com/p/BEHR-PREMIUM-PLUS-5-gal-ULTRA-PURE-WHITE-EGGshell-Enamel-Low-Odor-Interior-Paint-Primer-105005/100144907",
        },
        {
            "Category": "Paint",
            "Item": "Interior primer, 5 gal",
            "Supplier": "Home Depot (Public)",
            "Quantity": math.ceil(primer_gal / 5.0),
            "Unit": "buckets",
            "Unit Price (USD)": 158.00,
            "Line Total (USD)": round(math.ceil(primer_gal / 5.0) * 158.00, 2),
            "Notes": "Prime new drywall.",
            "Source": "https://www.homedepot.com/p/BEHR-PREMIUM-PLUS-5-gal-ULTRA-PURE-WHITE-EGGshell-Enamel-Low-Odor-Interior-Paint-Primer-105005/100144907",
        },
        {
            "Category": "Equipment",
            "Item": "Self-leveling cross-line laser (40 ft)",
            "Supplier": "Home Depot (Public)",
            "Quantity": 1,
            "Unit": "each",
            "Unit Price (USD)": 119.00,
            "Line Total (USD)": 119.00,
            "Notes": "Ceiling grid installation.",
            "Source": "https://www.homedepot.com/p/DEWALT-40-ft-Red-Self-Leveling-Cross-Line-Laser-Level-DW088K/203141212",
        },
        {
            "Category": "Protection",
            "Item": "Zip wall dust barrier kit",
            "Supplier": "Home Depot (Public)",
            "Quantity": 2,
            "Unit": "kits",
            "Unit Price (USD)": 52.98,
            "Line Total (USD)": 105.96,
            "Notes": "Sliding plastic doorway openings.",
            "Source": "https://www.homedepot.com/p/ZipWall-Barrier-Wrap-10-ft-x-100-ft-Dust-Barrier-Wrap-2-Pack-ZPBW12/207197034",
        },
        {
            "Category": "Waste",
            "Item": "Construction dumpster allowance",
            "Supplier": "Big River Disposal (allowance)",
            "Quantity": 1,
            "Unit": "allowance",
            "Unit Price (USD)": DUMPSTER_ALLOWANCE,
            "Line Total (USD)": DUMPSTER_ALLOWANCE,
            "Notes": "Provisional allowance for debris haul-off and dump handling; confirm vendor quote before issue.",
            "Source": "Vendor quote required",
        },
    ]

    for row in materials:
        row["Notes"] = f"{row['Notes']} Existing material scope retained; verify current supplier pricing before formal issue."

    material_total = sum(float(row["Line Total (USD)"]) for row in materials)

    labor_base = material_total * 0.85
    labor_reduced = labor_base / 3.0
    subtotal = material_total + labor_reduced + INSURANCE_FEE
    overhead = subtotal * 0.08
    total_bid = subtotal + overhead

    bid_summary = [
        {"Label": "Materials Total", "Amount": material_total},
        {"Label": "Labor (Reduced by 2/3)", "Amount": labor_reduced},
        {"Label": "Insurance Fee", "Amount": INSURANCE_FEE},
        {"Label": "Subtotal", "Amount": subtotal},
        {"Label": "Overhead (8%)", "Amount": overhead},
        {"Label": "Total Bid", "Amount": total_bid},
    ]

    permit_text = textwrap.dedent(
        f"""
        CITY OF QUINCY, ILLINOIS - PERMIT APPLICATION DRAFT (NOT OFFICIAL)
        Applicant/Contractor: Royal Lee Construction Solutions LLC
        Address: 3930 New London Gravel Rd, Hannibal, MO 63401
        Phone: (217) 257-6222
        Email: rlcsolutions@proton.me
        License: Hannibal, MO General Contracting License #7411
        MO Registration: LC014481759

        Owner: Steven Bunch
        Jobsite Address: 522 Vermont St, Quincy, IL

        Scope of Work: Interior demolition and replacement of drywall, drop ceiling grid, baseboard,
        repaint, and debris haul-off. No structural modifications proposed. All work to comply with AHJ requirements.

        Estimated Project Value: ${total_bid:,.2f}

        NOTE: This is a draft application for owner review. Official permits must be issued
        by the City of Quincy Building & Inspection Department.
        """
    ).strip()

    contract_text = textwrap.dedent(
        """
        CONSTRUCTION AGREEMENT (DRAFT)
        Parties: Royal Lee Construction Solutions LLC ("Contractor") and Steven Bunch ("Owner")
        Project Address: 522 Vermont St, Quincy, IL

        Scope: Demo and replacement of interior drywall, 2x4 drop ceiling grid, ceiling tiles,
        baseboard, and repainting as outlined in the attached takeoff and material list.

        Price: See attached bid summary.
        Schedule: Work to begin upon permit approval and material delivery.
        Payment: 50% deposit to secure materials, 40% progress payment, 10% upon completion.

        Warranty: See attached 20-year workmanship certificate for covered scope.
        Exclusions: Unforeseen structural issues, electrical/plumbing rework unless written change order.
        Compliance: Work performed to current code requirements and AHJ directives.

        Signatures:
        Contractor Representative: ____________________  Date: ____________
        Owner: ____________________  Date: ____________
        """
    ).strip()

    certificate_text = textwrap.dedent(
        """
        CERTIFICATE OF WORKMANSHIP - 20 YEAR GUARANTEE

        Customer: Steven Bunch
        Jobsite: 522 Vermont St, Quincy, IL

        Royal Lee Construction Solutions LLC guarantees, for a period of twenty (20) years from
        completion, to repair or replace holes and workmanship discrepancies directly related to
        the drywall, ceiling grid, baseboard, and paint scope delivered under this agreement.

        This certificate applies only to the scope of work performed by Royal Lee Construction Solutions LLC.
        """
    ).strip()

    # Build SVGs
    build_blueprint_svg(OUTPUT_DIR / "first_floor.svg", floor1, dimension_schedule["First Floor"])
    build_blueprint_svg(OUTPUT_DIR / "second_floor.svg", floor2, dimension_schedule["Second Floor"])

    write_materials(materials, OUTPUT_DIR / "material_list.csv")
    with (OUTPUT_DIR / "bid_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(bid_summary, handle, indent=2)
    with (OUTPUT_DIR / "bid_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Label", "Amount"])
        writer.writeheader()
        for row in bid_summary:
            writer.writerow(row)

    report_path = OUTPUT_DIR / "RLC_Quincy_Office_Package.pdf"
    build_report(
        report_path,
        floor1,
        floor2,
        materials,
        bid_summary,
        permit_text,
        contract_text,
        certificate_text,
        dimension_schedule,
    )

    # Full-scale blueprint package (24x36, 1/4" = 1'-0")
    blueprint_path = OUTPUT_DIR / "RLC_Quincy_Blueprints_24x36.pdf"
    build_blueprint_pdf(blueprint_path, floor1, floor2)
    build_blueprint_floor_pdf(OUTPUT_DIR / "RLC_Quincy_Blueprint_FirstFloor_24x36.pdf", "first")
    build_blueprint_floor_pdf(OUTPUT_DIR / "RLC_Quincy_Blueprint_SecondFloor_24x36.pdf", "second")


def build_blueprint_pdf(path: Path, floor1: FloorAssumptions, floor2: FloorAssumptions) -> None:
    width_pt = 36 * inch
    height_pt = 24 * inch
    c = canvas.Canvas(str(path), pagesize=(width_pt, height_pt))

    logo_path = ROOT / "assets" / "logos" / "clean" / "rlc_clean.png"

    def title_block(sheet: str, title: str, notes: list[str] | None = None) -> None:
        c.setStrokeColor(colors.black)
        c.rect(24, 24, width_pt - 48, height_pt - 48, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, height_pt - 40, title)
        c.setFont("Helvetica", 10)
        c.drawString(40, height_pt - 56, "Royal Lee Construction Solutions LLC")
        c.drawString(40, height_pt - 70, "Jobsite: 522 Vermont St, Quincy, IL")
        c.drawString(40, height_pt - 84, "Scale: 1/4\" = 1'-0\" (print at 100%)")
        c.drawRightString(width_pt - 40, height_pt - 56, f"Sheet: {sheet}")
        c.drawRightString(width_pt - 40, height_pt - 70, datetime.now().strftime("%B %d, %Y"))
        if logo_path.exists():
            c.drawImage(ImageReader(str(logo_path)), width_pt - 210, height_pt - 130, width=160, height=90, mask='auto')
        if notes:
            c.setFont("Helvetica", 8)
            y = 110
            for line in notes:
                c.drawString(40, y, line)
                y += 10

    scale = 18.0  # 1/4" per foot => 18 pts

    # First floor geometry
    first_width = parse_feet("13' 4 3/4\"")
    first_length = parse_feet("28' 3 1/2\"")
    bump_depth = parse_feet("8 3/4\"")
    bump_height = parse_feet("6' 9 1/2\"")
    bath_width = parse_feet("4' 4 3/8\"")
    bath_depth = parse_feet("10' 0\"")
    stair_width = parse_feet("4' 5\"")
    stair_depth = parse_feet("13' 10 1/2\"")

    outer = [
        (0, 0),
        (first_width, 0),
        (first_width + bump_depth, 0),
        (first_width + bump_depth, bump_height),
        (first_width, bump_height),
        (first_width, first_length),
        (0, first_length),
        (0, 0),
    ]
    bath = [
        (0, 0),
        (bath_width, 0),
        (bath_width, bath_depth),
        (0, bath_depth),
        (0, 0),
    ]
    stairs = [
        (first_width - stair_width, first_length - stair_depth),
        (first_width, first_length - stair_depth),
        (first_width, first_length),
        (first_width - stair_width, first_length),
        (first_width - stair_width, first_length - stair_depth),
    ]

    # Draw first floor
    title_block(
        "A1",
        "First Floor Plan",
        notes=[
            "All dimensions in feet and inches.",
            "Interior partitions assumed 3-5/8\" metal studs.",
            "Drywall: 5/8\" Type X, full height to grid.",
            "Ceiling grid: 2x4 acoustical tile, 9'-6\" AFF.",
        ],
    )
    # Underlay traced sketch for exact matching
    trace1 = ROOT / "assets" / "sketches" / "trace" / "floor_trace.png"
    if trace1.exists():
        c.drawImage(ImageReader(str(trace1)), 120, 160, width=520, height=360, mask='auto')
    draw_floor_plan_scaled(
        c,
        origin_x=120,
        origin_y=160,
        scale=scale,
        walls=[outer, bath, stairs],
        labels=[
            ("Bath", bath_width * 0.2, bath_depth * 0.4),
            ("Stairs", first_width - stair_width * 0.8, first_length - stair_depth * 0.5),
            ("Entry", first_width * 0.8, 0.3),
        ],
        title="First Floor Plan (scaled)",
    )

    # Dimension lines
    draw_dim_line(c, 120, 140, 120 + (first_width + bump_depth) * scale, 140, '13\'-4 3/4"')
    draw_dim_line(c, 100, 160, 100, 160 + first_length * scale, '28\'-3 1/2"')

    # Door schedule block
    c.setFont("Helvetica-Bold", 10)
    c.drawString(780, 150, "Door Schedule")
    c.setFont("Helvetica", 9)
    c.drawString(780, 135, "D1: 3'-0\" x 7'-0\" HM door")
    c.drawString(780, 122, "D2: Sliding plastic doorway")

    c.showPage()

    # Second floor geometry
    second_width = parse_feet("10' 7\"") + parse_feet("8' 4\"")
    second_length = parse_feet("13' 11\"")
    hall_height = parse_feet("2' 6\"")
    hall_y = second_length / 2 - hall_height / 2
    top_left_width = parse_feet("10' 7\"")
    top_left_depth = parse_feet("7' 0\"")
    top_right_width = parse_feet("8' 4\"")
    top_right_depth = parse_feet("10' 4 3/4\"")

    outer2 = [
        (0, 0),
        (second_width, 0),
        (second_width, second_length),
        (0, second_length),
        (0, 0),
    ]
    hall = [
        (0, hall_y),
        (second_width, hall_y),
        (second_width, hall_y + hall_height),
        (0, hall_y + hall_height),
        (0, hall_y),
    ]
    top_left = [
        (0, second_length - top_left_depth),
        (top_left_width, second_length - top_left_depth),
        (top_left_width, second_length),
        (0, second_length),
        (0, second_length - top_left_depth),
    ]
    top_right = [
        (second_width - top_right_width, second_length - top_right_depth),
        (second_width, second_length - top_right_depth),
        (second_width, second_length),
        (second_width - top_right_width, second_length),
        (second_width - top_right_width, second_length - top_right_depth),
    ]

    title_block("A2", "Second Floor Plan")
    trace2 = ROOT / "assets" / "sketches" / "trace" / "download_trace.png"
    if trace2.exists():
        c.drawImage(ImageReader(str(trace2)), 120, 160, width=520, height=360, mask='auto')
    draw_floor_plan_scaled(
        c,
        origin_x=120,
        origin_y=160,
        scale=scale,
        walls=[outer2, hall, top_left, top_right],
        labels=[
            ("Hall / Stairs", second_width * 0.4, hall_y + hall_height * 0.4),
            ("Upper Left", top_left_width * 0.2, second_length - top_left_depth * 0.5),
            ("Upper Right", second_width - top_right_width * 0.8, second_length - top_right_depth * 0.5),
        ],
        title="Second Floor Plan (scaled)",
    )

    draw_dim_line(c, 120, 140, 120 + second_width * scale, 140, '18\'-11"')
    draw_dim_line(c, 100, 160, 100, 160 + second_length * scale, '13\'-11"')

    c.setFont("Helvetica-Bold", 10)
    c.drawString(780, 150, "Door Schedule")
    c.setFont("Helvetica", 9)
    c.drawString(780, 135, "D1: 3'-0\" x 7'-0\" HM door")
    c.drawString(780, 122, "D2: Sliding plastic doorway")

    c.save()


def build_blueprint_floor_pdf(path: Path, floor: str) -> None:
    width_pt = 36 * inch
    height_pt = 24 * inch
    c = canvas.Canvas(str(path), pagesize=(width_pt, height_pt))
    logo_path = ROOT / "assets" / "logos" / "clean" / "rlc_clean.png"

    def title_block(sheet: str, title: str, notes: list[str] | None = None) -> None:
        c.setStrokeColor(colors.black)
        c.rect(24, 24, width_pt - 48, height_pt - 48, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, height_pt - 40, title)
        c.setFont("Helvetica", 10)
        c.drawString(40, height_pt - 56, "Royal Lee Construction Solutions LLC")
        c.drawString(40, height_pt - 70, "Jobsite: 522 Vermont St, Quincy, IL")
        c.drawString(40, height_pt - 84, "Scale: 1/4\" = 1'-0\" (print at 100%)")
        c.drawRightString(width_pt - 40, height_pt - 56, f"Sheet: {sheet}")
        c.drawRightString(width_pt - 40, height_pt - 70, datetime.now().strftime("%B %d, %Y"))
        if logo_path.exists():
            c.drawImage(ImageReader(str(logo_path)), width_pt - 210, height_pt - 130, width=160, height=90, mask='auto')
        if notes:
            c.setFont("Helvetica", 8)
            y = 110
            for line in notes:
                c.drawString(40, y, line)
                y += 10

    scale = 18.0

    if floor == "first":
        first_width = parse_feet("13' 4 3/4\"")
        first_length = parse_feet("28' 3 1/2\"")
        bump_depth = parse_feet("8 3/4\"")
        bump_height = parse_feet("6' 9 1/2\"")
        bath_width = parse_feet("4' 4 3/8\"")
        bath_depth = parse_feet("10' 0\"")
        stair_width = parse_feet("4' 5\"")
        stair_depth = parse_feet("13' 10 1/2\"")

        outer = [
            (0, 0),
            (first_width, 0),
            (first_width + bump_depth, 0),
            (first_width + bump_depth, bump_height),
            (first_width, bump_height),
            (first_width, first_length),
            (0, first_length),
            (0, 0),
        ]
        bath = [
            (0, 0),
            (bath_width, 0),
            (bath_width, bath_depth),
            (0, bath_depth),
            (0, 0),
        ]
        stairs = [
            (first_width - stair_width, first_length - stair_depth),
            (first_width, first_length - stair_depth),
            (first_width, first_length),
            (first_width - stair_width, first_length),
            (first_width - stair_width, first_length - stair_depth),
        ]

        title_block(
            "A1",
            "First Floor Plan",
            notes=[
                "All dimensions in feet and inches.",
                "Interior partitions assumed 3-5/8\" metal studs.",
                "Drywall: 5/8\" Type X, full height to grid.",
                "Ceiling grid: 2x4 acoustical tile, 9'-6\" AFF.",
            ],
        )

        trace1 = ROOT / "assets" / "sketches" / "trace" / "floor_trace.png"
        if trace1.exists():
            c.drawImage(ImageReader(str(trace1)), 120, 160, width=520, height=360, mask='auto')

        draw_floor_plan_scaled(
            c,
            origin_x=120,
            origin_y=160,
            scale=scale,
            walls=[outer, bath, stairs],
            labels=[
                ("Bath", bath_width * 0.2, bath_depth * 0.4),
                ("Stairs", first_width - stair_width * 0.8, first_length - stair_depth * 0.5),
                ("Entry", first_width * 0.8, 0.3),
            ],
            title="First Floor Plan (scaled)",
        )

        draw_dim_line(c, 120, 140, 120 + (first_width + bump_depth) * scale, 140, '13\'-4 3/4"')
        draw_dim_line(c, 100, 160, 100, 160 + first_length * scale, '28\'-3 1/2"')

        c.setFont("Helvetica-Bold", 10)
        c.drawString(780, 150, "Door Schedule")
        c.setFont("Helvetica", 9)
        c.drawString(780, 135, "D1: 3'-0\" x 7'-0\" HM door")
        c.drawString(780, 122, "D2: Sliding plastic doorway")
    else:
        second_width = parse_feet("10' 7\"") + parse_feet("8' 4\"")
        second_length = parse_feet("13' 11\"")
        hall_height = parse_feet("2' 6\"")
        hall_y = second_length / 2 - hall_height / 2
        top_left_width = parse_feet("10' 7\"")
        top_left_depth = parse_feet("7' 0\"")
        top_right_width = parse_feet("8' 4\"")
        top_right_depth = parse_feet("10' 4 3/4\"")

        outer2 = [
            (0, 0),
            (second_width, 0),
            (second_width, second_length),
            (0, second_length),
            (0, 0),
        ]
        hall = [
            (0, hall_y),
            (second_width, hall_y),
            (second_width, hall_y + hall_height),
            (0, hall_y + hall_height),
            (0, hall_y),
        ]
        top_left = [
            (0, second_length - top_left_depth),
            (top_left_width, second_length - top_left_depth),
            (top_left_width, second_length),
            (0, second_length),
            (0, second_length - top_left_depth),
        ]
        top_right = [
            (second_width - top_right_width, second_length - top_right_depth),
            (second_width, second_length - top_right_depth),
            (second_width, second_length),
            (second_width - top_right_width, second_length),
            (second_width - top_right_width, second_length - top_right_depth),
        ]

        title_block(
            "A2",
            "Second Floor Plan",
            notes=[
                "All dimensions in feet and inches.",
                "Interior partitions assumed 3-5/8\" metal studs.",
                "Drywall: 5/8\" Type X, full height to grid.",
                "Ceiling grid: 2x4 acoustical tile, 8'-6\" AFF.",
            ],
        )

        trace2 = ROOT / "assets" / "sketches" / "trace" / "download_trace.png"
        if trace2.exists():
            c.drawImage(ImageReader(str(trace2)), 120, 160, width=520, height=360, mask='auto')

        draw_floor_plan_scaled(
            c,
            origin_x=120,
            origin_y=160,
            scale=scale,
            walls=[outer2, hall, top_left, top_right],
            labels=[
                ("Hall / Stairs", second_width * 0.4, hall_y + hall_height * 0.4),
                ("Upper Left", top_left_width * 0.2, second_length - top_left_depth * 0.5),
                ("Upper Right", second_width - top_right_width * 0.8, second_length - top_right_depth * 0.5),
            ],
            title="Second Floor Plan (scaled)",
        )

        draw_dim_line(c, 120, 140, 120 + second_width * scale, 140, '18\'-11"')
        draw_dim_line(c, 100, 160, 100, 160 + second_length * scale, '13\'-11"')

        c.setFont("Helvetica-Bold", 10)
        c.drawString(780, 150, "Door Schedule")
        c.setFont("Helvetica", 9)
        c.drawString(780, 135, "D1: 3'-0\" x 7'-0\" HM door")
        c.drawString(780, 122, "D2: Sliding plastic doorway")

    c.save()


if __name__ == "__main__":
    main()

