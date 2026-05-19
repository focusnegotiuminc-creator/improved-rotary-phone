from __future__ import annotations

from types import SimpleNamespace

from FOCUS_MASTER_AI.integrations import openai_client


def test_call_gpt_without_api_key_sets_attention(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(openai_client, "bootstrap_runtime_env", lambda: None)

    result = openai_client.call_gpt("hello")

    assert result == "[OpenAI unavailable] OPENAI_API_KEY is not set."
    status = openai_client.get_openai_runtime_status()
    assert status["state"] == "attention"
    assert "not configured" in status["message"]


def test_call_gpt_classifies_provider_errors(monkeypatch):
    class FakeCompletions:
        @staticmethod
        def create(**_kwargs):
            raise RuntimeError("insufficient_quota: quota exceeded")

    class FakeClient:
        def __init__(self, **_kwargs):
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(openai_client, "bootstrap_runtime_env", lambda: None)
    monkeypatch.setattr(openai_client, "OpenAI", FakeClient)

    result = openai_client.call_gpt("hello")

    assert result == "[OpenAI unavailable] quota: OpenAI quota is exhausted for the configured account."
    status = openai_client.get_openai_runtime_status()
    assert status["state"] == "attention"
    assert status["message"] == "OpenAI quota is exhausted for the configured account."
