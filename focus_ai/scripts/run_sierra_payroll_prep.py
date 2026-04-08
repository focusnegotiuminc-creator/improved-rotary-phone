#!/usr/bin/env python3
"""Prepare Sierra payroll summary from the run input CSV.

This command validates known entries, computes confirmed subtotal, and lists
blocking fields required before final payroll submission.
"""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT_CSV = ROOT / "reports" / "2026-03-28_sierra_payroll_run_input.csv"
OUTPUT_MD = ROOT / "reports" / "2026-03-28_sierra_payroll_prep_output.md"


def main() -> int:
    if not INPUT_CSV.exists():
        print(f"Missing input CSV: {INPUT_CSV}")
        return 1

    subtotal = Decimal("0")
    blockers: list[str] = []
    lines: list[str] = []

    with INPUT_CSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            company = row.get("project", "").strip() or "Unknown Project"
            hours_raw = (row.get("total_hours") or "").strip()
            rate_raw = (row.get("pay_rate") or "").strip()

            if hours_raw and rate_raw:
                hours = Decimal(hours_raw)
                rate = Decimal(rate_raw)
                gross = hours * rate
                subtotal += gross
                lines.append(f"- {company}: {hours} x ${rate:.2f} = ${gross:.2f}")
            else:
                blockers.append(f"{company}: missing total_hours and/or pay_rate")

    report = [
        "# Sierra Payroll Prep Output",
        "",
        "## Confirmed gross lines",
        *lines,
        "",
        f"## Confirmed subtotal\n- ${subtotal:.2f}",
        "",
        "## Blocking items",
    ]

    if blockers:
        report.extend([f"- {item}" for item in blockers])
    else:
        report.append("- None")

    OUTPUT_MD.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Wrote payroll prep output: {OUTPUT_MD}")
    print(f"Confirmed subtotal: ${subtotal:.2f}")
    if blockers:
        print("Blocking items:")
        for item in blockers:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
