from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

try:  # Optional rendered QA path.
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.edge.options import Options
except ModuleNotFoundError:  # Static fallback keeps QA usable in lean Codex runtimes.
    webdriver = None
    By = None
    Options = None


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SITE = REPO_ROOT / "focus_ai" / "published" / "public_site"
REPORT_DIR = REPO_ROOT / "docs"

REMOTE_PAGES: list[tuple[str, str]] = [
    ("home", "https://www.thefocuscorp.com/"),
    ("landing", "https://www.thefocuscorp.com/landing.html"),
    ("store", "https://www.thefocuscorp.com/store.html"),
    ("books", "https://www.thefocuscorp.com/books.html"),
    ("focus_negotium", "https://www.thefocuscorp.com/focus-negotium.html"),
    ("focus_records", "https://www.thefocuscorp.com/focus-records.html"),
    ("construction", "https://www.thefocuscorp.com/royal-lee-construction.html"),
]

LOCAL_PAGES: list[tuple[str, str]] = [
    ("home", "index.html"),
    ("landing", "landing.html"),
    ("store", "store.html"),
    ("books", "books.html"),
    ("focus_negotium", "focus-negotium.html"),
    ("focus_records", "focus-records.html"),
    ("construction", "royal-lee-construction.html"),
    ("rlc_package", "rlc-office-package.html"),
]

FORBIDDEN_TERMS = [
    "ai engine",
    "openai",
    "anthropic",
    "gemini",
    "private console",
]

REQUIRED_TERMS = [
    "Focus Negotium Inc",
    "Focus Records LLC",
    "Royal Lee Construction Solutions LLC",
    "2172576222",
    "books",
    "services",
]


def _make_driver(width: int, height: int, mobile: bool):
    if webdriver is None or Options is None:
        raise RuntimeError("Selenium is not installed")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--log-level=3")
    if mobile:
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
    )
    return webdriver.Edge(options=options)


def _collect_page_state(driver, url: str) -> dict[str, object]:
    if By is None:
        raise RuntimeError("Selenium is not installed")
    driver.get(url)
    driver.implicitly_wait(2)
    body = driver.find_element(By.TAG_NAME, "body").text
    lowered = body.lower()
    overflow = driver.execute_script(
        "return Math.max(0, document.documentElement.scrollWidth - window.innerWidth);"
    )
    button_labels: list[str] = []
    for element in driver.find_elements(By.CSS_SELECTOR, ".button-row a")[:8]:
        label = element.text.strip() or (element.get_attribute("textContent") or "").strip()
        if label:
            button_labels.append(label)
    return {
        "overflow": int(overflow),
        "buttons": button_labels[:4],
        "forbidden_hits": [token for token in FORBIDDEN_TERMS if token in lowered],
        "snippet": body[:320],
    }


def _strip_tags(html: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def _local_links(page_path: Path, html: str) -> tuple[list[str], list[str]]:
    links = re.findall(r"""href=["']([^"']+)["']""", html)
    local_links: list[str] = []
    missing: list[str] = []
    for href in links:
        if (
            href.startswith(("http://", "https://", "mailto:", "tel:", "#"))
            or href.startswith("data:")
            or "{" in href
        ):
            continue
        target = (page_path.parent / href.split("#", 1)[0]).resolve()
        if href.endswith("/") or not target.suffix:
            target = target / "index.html"
        local_links.append(href)
        if not target.exists():
            missing.append(href)
    return local_links, missing


def _collect_static_page_state(name: str, relative_path: str) -> dict[str, object]:
    page_path = PUBLIC_SITE / relative_path
    html = page_path.read_text(encoding="utf-8")
    body = _strip_tags(html)
    lowered = body.lower()
    links, missing_links = _local_links(page_path, html)
    return {
        "mode": "static_local",
        "source": str(page_path),
        "bytes": page_path.stat().st_size,
        "local_links": len(links),
        "missing_links": missing_links,
        "forbidden_hits": [token for token in FORBIDDEN_TERMS if token in lowered],
        "required_hits": [token for token in REQUIRED_TERMS if token.lower() in lowered],
        "snippet": body[:320],
    }


def render_report(data: dict[str, dict[str, object]]) -> str:
    lines = [
        "# TheFocusCorp Public QA",
        "",
        "Verified with rendered browser checks when Selenium is available, otherwise with local static bundle checks.",
        "",
    ]
    for name, result in data.items():
        lines.append(f"## {name}")
        for optional_key in ["mode", "source", "bytes", "overflow", "local_links"]:
            if optional_key in result:
                lines.append(f"- {optional_key}: `{result[optional_key]}`")
        if "buttons" in result:
            lines.append(f"- buttons: {', '.join(f'`{item}`' for item in result['buttons']) or 'none'}")
        if "missing_links" in result:
            lines.append(f"- missing links: {', '.join(f'`{item}`' for item in result['missing_links']) or 'none'}")
        if "required_hits" in result:
            lines.append(f"- required hits: {', '.join(f'`{item}`' for item in result['required_hits']) or 'none'}")
        lines.append(f"- forbidden hits: {', '.join(f'`{item}`' for item in result['forbidden_hits']) or 'none'}")
        lines.append(f"- snippet: `{result['snippet']}`")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    results: dict[str, dict[str, object]] = {}
    if webdriver is None:
        if not PUBLIC_SITE.exists():
            raise SystemExit(f"Missing local public site bundle: {PUBLIC_SITE}")
        for name, relative_path in LOCAL_PAGES:
            results[name] = _collect_static_page_state(name, relative_path)
    else:
        desktop_driver = _make_driver(1440, 1600, mobile=False)
        mobile_driver = _make_driver(390, 844, mobile=True)
        try:
            for name, url in REMOTE_PAGES:
                results[f"{name}_desktop"] = _collect_page_state(desktop_driver, url)
                results[f"{name}_mobile"] = _collect_page_state(mobile_driver, url)
        finally:
            desktop_driver.quit()
            mobile_driver.quit()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "thefocuscorp_public_qa_rendered.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    (REPORT_DIR / "thefocuscorp_public_qa_rendered.md").write_text(
        render_report(results), encoding="utf-8"
    )
    print(f"Wrote QA artifacts to {REPORT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
