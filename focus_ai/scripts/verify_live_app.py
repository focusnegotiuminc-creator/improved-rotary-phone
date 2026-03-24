#!/usr/bin/env python3
"""Check whether a deployed public app URL is reachable."""

from __future__ import annotations

import os
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PATHS = ["/", "/ebooks/index.html", "/landing.html"]


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

    all_ok = True
    for path in PATHS:
        target = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
        ok, detail = _check(target)
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {target} -> {detail}")
        all_ok = all_ok and ok

    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
