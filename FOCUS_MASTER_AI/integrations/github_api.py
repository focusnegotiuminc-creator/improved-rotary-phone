from __future__ import annotations

import os
from typing import Any

import requests


class GitHubClient:
    def __init__(self) -> None:
        self.token = os.getenv("GITHUB_TOKEN", "").strip()
        self.repo = os.getenv("GITHUB_REPO", "").strip()
        self.base_url = "https://api.github.com"

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def healthcheck(self) -> dict[str, Any]:
        if not self.token or not self.repo:
            return {
                "ok": False,
                "message": "Set GITHUB_TOKEN and GITHUB_REPO to enable GitHub integration.",
            }
        return {"ok": True, "message": f"GitHub configured for repo {self.repo}"}

    def create_issue(self, title: str, body: str) -> dict[str, Any]:
        if not self.token or not self.repo:
            return {
                "ok": False,
                "message": "Missing GITHUB_TOKEN or GITHUB_REPO.",
            }
        url = f"{self.base_url}/repos/{self.repo}/issues"
        payload = {"title": title, "body": body}
        try:
            response = requests.post(url, headers=self._headers(), json=payload, timeout=20)
            if response.ok:
                data = response.json()
                return {"ok": True, "issue_url": data.get("html_url")}
            return {"ok": False, "message": response.text[:300]}
        except requests.RequestException as exc:
            return {"ok": False, "message": f"GitHub request failed: {exc}"}

