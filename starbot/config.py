"""Configuration utilities for StarBot."""

from __future__ import annotations

import os
from functools import lru_cache
from urllib.parse import urlparse

from pydantic import BaseModel, Field, ValidationError, field_validator


_ENV_TO_FIELD = {
    "DISCORD_TOKEN": "discord_token",
    "WEATHER_API_KEY": "weather_api_key",
    "OLLAMA_HOST": "ollama_host",
    "FAISS_INDEX_PATH": "faiss_index_path",
    "RESPONSE_TIMEOUT_SECONDS": "response_timeout_seconds",
    "MAX_CONTEXT_MESSAGES": "max_context_messages",
}


class Settings(BaseModel):
    """Application configuration sourced from environment variables."""

    discord_token: str = Field(default="", description="Discord bot token")
    weather_api_key: str | None = Field(default=None, description="Weather API key")
    ollama_host: str = Field(default="http://localhost:11434", description="Base URL for the Ollama server")
    faiss_index_path: str = Field(default="data/memory.index", description="Path to the FAISS index file")
    response_timeout_seconds: float = Field(default=8.0, ge=0.1, le=120.0, description="Timeout for LLM calls in seconds")
    max_context_messages: int = Field(default=8, ge=1, le=100, description="Sliding window size for short-term memory")

    @field_validator("discord_token")
    @classmethod
    def trim_token(cls, value: str) -> str:
        """Normalize optional Discord token values."""
        return value.strip()

    @field_validator("ollama_host")
    @classmethod
    def validate_ollama_host(cls, value: str) -> str:
        """Ensure the Ollama host is a valid HTTP(S) URL."""
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("OLLAMA_HOST must be an absolute HTTP(S) URL")
        return value

    @field_validator("faiss_index_path")
    @classmethod
    def validate_index_path(cls, value: str) -> str:
        """Ensure the FAISS index path is populated."""
        if not value.strip():
            raise ValueError("FAISS_INDEX_PATH must not be empty")
        return value

    @classmethod
    def load(cls) -> "Settings":
        """Load configuration from environment variables with validation."""
        try:
            return cls(**_coerce_environment())
        except ValidationError as exc:  # pragma: no cover - defensive guard
            errors = "; ".join(err.get("msg", "invalid configuration") for err in exc.errors())
            raise RuntimeError(f"Invalid StarBot configuration: {errors}") from exc


def _iter_environment() -> dict[str, str | None]:
    """Collect environment variables used by the settings model."""
    return {key: os.environ.get(key) for key in _ENV_TO_FIELD}


def _coerce_environment() -> dict[str, str]:
    """Return environment values excluding missing keys."""
    raw = _iter_environment()
    settings_dict: dict[str, str] = {}
    for env_key, value in raw.items():
        if value is None:
            continue
        field_key = _ENV_TO_FIELD[env_key]
        settings_dict[field_key] = value
    return settings_dict


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings(**_coerce_environment())


settings = get_settings()