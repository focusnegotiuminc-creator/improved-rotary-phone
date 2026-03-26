import datetime
from pathlib import Path

FILES = [
    "research/research_database.md",
    "claims/verified_claims.md",
    "book/book_outline.md",
    "book/manuscript.md",
    "geometry/geometry_diagrams.md",
    "construction/construction_optimization.md",
    "compliance/compliance_report.md",
    "alignment/frequency_alignment.md",
    "marketing/marketing_automation.md",
    "final_product/final_book_manuscript.md",
]


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def section_for(path: str) -> str:
    timestamp = utc_now()
    if path.startswith("research/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "- Added research follow-up placeholder\n"
            "- Next source target: peer-reviewed architecture dataset\n"
        )
    if path.startswith("claims/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "- Added new claim verification slot\n"
            "- Confidence calibration pending\n"
        )
    if path.startswith("book/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "### New Section Stub\n"
            "- Insight:\n"
            "- Applied Architecture Example:\n"
            "- Monetization Note:\n"
        )
    if path.startswith("geometry/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "- Added geometry concept placeholder for next iteration\n"
            "- Include CAD-ready dimensions in upcoming pass\n"
        )
    if path.startswith("construction/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "- Optimization test case queued\n"
            "- Material + labor assumptions to validate\n"
        )
    if path.startswith("compliance/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "- Compliance review checkpoint added\n"
            "- Jurisdiction mapping required before release\n"
        )
    if path.startswith("alignment/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "- Alignment exercise slot added\n"
            "- Add practitioner guidance notes\n"
        )
    if path.startswith("marketing/"):
        return (
            f"\n\n## Update Check ({timestamp})\n"
            "- Funnel experiment placeholder added\n"
            "- Track click-through and conversion metrics\n"
        )
    return f"\n\n## Update Check ({timestamp})\n- General system refresh logged\n"


def update_files() -> None:
    root = Path(__file__).resolve().parent.parent
    for relative in FILES:
        file_path = root / relative
        if file_path.exists():
            with file_path.open("a", encoding="utf-8") as handle:
                handle.write(section_for(relative))


if __name__ == "__main__":
    update_files()
