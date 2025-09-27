"""Tests for StarBot configuration helpers."""

from __future__ import annotations

import pytest

from starbot import config


_ENV_KEYS: tuple[str, ...] = (
    "DISCORD_TOKEN",
    "WEATHER_API_KEY",
    "OLLAMA_HOST",
    "FAISS_INDEX_PATH",
    "RESPONSE_TIMEOUT_SECONDS",
    "MAX_CONTEXT_MESSAGES",
)


def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in _ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    config.get_settings.cache_clear()  # type: ignore[attr-defined]


def test_settings_loads_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default values are returned when environment variables are absent."""

    _clear_env(monkeypatch)
    settings = config.Settings.load()

    assert settings.discord_token == ""
    assert settings.ollama_host == "http://localhost:11434"
    assert settings.max_context_messages == 8
    assert settings.response_timeout_seconds == 8.0


def test_settings_rejects_invalid_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """An invalid Ollama host raises a user-friendly runtime error."""

    _clear_env(monkeypatch)
    monkeypatch.setenv("OLLAMA_HOST", "ftp://localhost:21")

    with pytest.raises(RuntimeError) as excinfo:
        config.Settings.load()

    assert "OLLAMA_HOST" in str(excinfo.value)


def test_settings_trim_discord_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Discord tokens are stripped of accidental whitespace."""

    _clear_env(monkeypatch)
    monkeypatch.setenv("DISCORD_TOKEN", "  my-token ")

    settings = config.Settings.load()

    assert settings.discord_token == "my-token"
