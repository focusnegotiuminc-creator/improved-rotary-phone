import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    make_webhook_url: str = os.getenv("MAKE_WEBHOOK_URL", "")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_repo: str = os.getenv("GITHUB_REPO", "")
    replit_runner_url: str = os.getenv("REPLIT_RUNNER_URL", "")
    default_openai_model: str = os.getenv("DEFAULT_OPENAI_MODEL", "gpt-4.1-mini")


def get_settings() -> Settings:
    return Settings()

