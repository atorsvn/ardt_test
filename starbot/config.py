"""Configuration utilities for StarBot."""

from dataclasses import dataclass
import os


@dataclass
class Settings:
    """Application configuration sourced from environment variables."""

    discord_token: str
    weather_api_key: str | None
    ollama_host: str
    faiss_index_path: str
    response_timeout_seconds: float
    max_context_messages: int

    @classmethod
    def load(cls) -> "Settings":
        """Load configuration from environment variables with defaults."""

        return cls(
            discord_token=os.environ.get("DISCORD_TOKEN", ""),
            weather_api_key=os.environ.get("WEATHER_API_KEY"),
            ollama_host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
            faiss_index_path=os.environ.get("FAISS_INDEX_PATH", "data/memory.index"),
            response_timeout_seconds=float(os.environ.get("RESPONSE_TIMEOUT_SECONDS", "8")),
            max_context_messages=int(os.environ.get("MAX_CONTEXT_MESSAGES", "8")),
        )


settings = Settings.load()
