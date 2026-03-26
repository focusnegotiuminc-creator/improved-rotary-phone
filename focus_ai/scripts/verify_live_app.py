#!/usr/bin/env python3
"""Check whether a deployed app URL is reachable."""

from __future__ import annotations

import os
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

DEFAULT_PATHS = ["/", "/wp-admin", "/ebooks/index.html", "/landing.html"]


def _parse_paths(raw: str | None) -> list[str]:
    if not raw:
        return DEFAULT_PATHS
    paths = []
    for value in raw.split(","):
        value = value.strip()
        if not value:
            continue
        if not value.startswith("/"):
            value = f"/{value}"
        paths.append(value)
    return paths or DEFAULT_PATHS


def _check(url: str) -> tuple[bool, str]:
    req = Request(url, method="GET", headers={"User-Agent": "FocusAI-LiveCheck/1.0"})
    try:
        with urlopen(req, timeout=20) as response:
            status = response.status
            if 200 <= status < 400:
                return True, f"{status} OK"
            return False, f"{status}"
    except HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except URLError as exc:
        return False, f"URL error: {exc.reason}"


def main() -> int:
    base = os.getenv("FOCUS_APP_URL", "").strip()
    if not base:
        print("Missing FOCUS_APP_URL. Example:")
        print("  export FOCUS_APP_URL='https://example.com'")
        return 1

    paths = _parse_paths(os.getenv("FOCUS_APP_PATHS"))
    require_all = os.getenv("FOCUS_REQUIRE_ALL_PATHS", "1").strip().lower() not in {"0", "false", "no"}

    failures = 0
    for path in paths:
        target = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
        ok, detail = _check(target)
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {target} -> {detail}")
        if not ok:
            failures += 1

    if failures == 0:
        return 0
    if require_all:
        return 2
    print(f"Completed with {failures} failing path(s), but FOCUS_REQUIRE_ALL_PATHS is disabled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
