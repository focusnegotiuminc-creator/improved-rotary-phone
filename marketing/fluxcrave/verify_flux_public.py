#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "docs" / "manifests" / "flux_public_qa_report.md"


@dataclass
class CheckResult:
    label: str
    url: str
    title: str
    current_url: str
    passed: bool
    notes: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_driver(*, width: int, height: int, user_agent: str | None = None) -> webdriver.Edge:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--window-size={width},{height}")
    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")
    return webdriver.Edge(options=options)


def page_text(driver: webdriver.Edge) -> str:
    return driver.find_element(By.TAG_NAME, "body").text


def run_check(label: str, url: str, *, mobile: bool = False) -> CheckResult:
    user_agent = None
    width, height = (1440, 2200)
    if mobile:
        user_agent = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
        )
        width, height = (390, 844)
    driver = build_driver(width=width, height=height, user_agent=user_agent)
    notes: list[str] = []
    try:
        driver.get(url)
        time.sleep(4)
        text = page_text(driver)
        title = driver.title
        current_url = driver.current_url
        passed = True

        if "fluxcrave.com" not in current_url:
            passed = False
            notes.append(f"unexpected current_url={current_url}")
        if "Wix" in title or "Powered and secured by Wix" in text:
            passed = False
            notes.append("Wix branding still visible")

        if "/menu/" in url:
            if mobile:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.35)")
                time.sleep(1.5)
                text = page_text(driver)
            required = {
                "The Flux Capacitor": "missing Flux Capacitor",
                "Whole Chicken Wings": "missing Whole Chicken Wings",
                "Lemon Shaker": "missing Lemon Shaker",
            }
            for token, message in required.items():
                if token not in text:
                    passed = False
                    notes.append(message)
            banned_patterns = {
                r"\$": "pricing still visible",
                r"\b[Dd]essert\b": "dessert still visible",
                r"\b[Ll]emonade\b": "lemonade still visible",
                r"Wings & Tenders": "old wings label still visible",
                r"Fish, Sides & Sips": "old fish/sips label still visible",
            }
            for pattern, message in banned_patterns.items():
                if re.search(pattern, text):
                    passed = False
                    notes.append(message)

        if "/visit/" in url:
            images = driver.find_elements(By.TAG_NAME, "img")
            qr_visible = any("qr-order" in (img.get_attribute("src") or "") and img.is_displayed() for img in images)
            if not qr_visible:
                passed = False
                notes.append("QR image not visible")

        if mobile:
            overflow = driver.execute_script(
                "return Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - window.innerWidth"
            )
            if overflow > 0:
                passed = False
                notes.append(f"horizontal overflow={overflow}")

        return CheckResult(label=label, url=url, title=title, current_url=current_url, passed=passed, notes=notes)
    finally:
        driver.quit()


def write_report(results: list[CheckResult]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Flux Public QA Report",
        "",
        f"Generated: {utc_now()}",
        "",
        "| Check | Result | Title | URL | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        notes = "; ".join(result.notes) if result.notes else "ok"
        lines.append(
            f"| {result.label} | {'PASS' if result.passed else 'FAIL'} | {result.title} | `{result.current_url}` | {notes} |"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    checks = [
        run_check("desktop-apex-home", "https://fluxcrave.com/?qa=desktop-home"),
        run_check("desktop-www-home", "https://www.fluxcrave.com/?qa=desktop-home"),
        run_check("desktop-www-menu", "https://www.fluxcrave.com/menu/?qa=desktop-menu"),
        run_check("desktop-www-visit", "https://www.fluxcrave.com/visit/?qa=desktop-visit"),
        run_check("mobile-www-home", "https://www.fluxcrave.com/?qa=mobile-home", mobile=True),
        run_check("mobile-www-menu", "https://www.fluxcrave.com/menu/?qa=mobile-menu", mobile=True),
    ]
    write_report(checks)
    print(json.dumps([result.__dict__ for result in checks], indent=2))
    return 0 if all(result.passed for result in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
