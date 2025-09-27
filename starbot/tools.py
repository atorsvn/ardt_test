"""External tool integrations for StarBot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
from requests import RequestException

from .config import settings


class ToolError(RuntimeError):
    """Raised when a tool invocation fails."""


@dataclass
class WeatherResult:
    """Weather API response model."""

    location: str
    description: str
    temperature_c: float

    def format(self) -> str:
        """Format the weather result for display."""

        return f"Weather in {self.location}: {self.description}, {self.temperature_c:.1f}°C"


class WeatherTool:
    """Simple weather lookup using the WeatherAPI.com service."""

    base_url = "https://api.weatherapi.com/v1/current.json"

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    def available(self) -> bool:
        """Return True if the tool has the credentials required to run."""

        return bool(self.api_key)

    def run(self, location: str) -> WeatherResult:
        """Fetch the current weather for the provided location."""

        if not self.available():
            raise ToolError("Weather API key missing.")
        params = {"key": self.api_key, "q": location, "aqi": "no"}
        try:
            # Use a timeout for network resilience
            response = requests.get(self.base_url, params=params, timeout=5)
        except RequestException as exc:  # pragma: no cover - network failure path
            raise ToolError("Weather service unreachable.") from exc

        if response.status_code != 200:
            raise ToolError(f"Weather API error: {response.status_code} {response.text}")

        payload: dict[str, Any] = response.json()
        current = payload.get("current", {})
        condition = current.get("condition", {})

        return WeatherResult(
            location=payload.get("location", {}).get("name", location),
            description=condition.get("text", "Unavailable"),
            temperature_c=float(current.get("temp_c", 0.0)),
        )


class WikipediaTool:
    """Minimal Wikipedia search integration."""

    base_url = "https://en.wikipedia.org/w/api.php"

    def search(self, query: str) -> str:
        """Return the lead paragraph of the top Wikipedia article for the query."""

        params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "format": "json",
            "generator": "search",
            "gsrnamespace": 0,
            "gsrlimit": 1,
            "gsrsearch": query,
        }

        try:
            # Use a timeout for network resilience
            response = requests.get(self.base_url, params=params, timeout=5)
        except RequestException as exc:  # pragma: no cover - network failure path
            raise ToolError("Wikipedia service unreachable.") from exc

        if response.status_code != 200:
            raise ToolError(f"Wikipedia API error: {response.status_code} {response.text}")

        payload: dict[str, Any] = response.json()
        pages = payload.get("query", {}).get("pages", {})

        if not pages:
            raise ToolError("No Wikipedia results found.")

        page = next(iter(pages.values()))
        title = page.get("title", "Unknown")
        extract = page.get("extract", "No summary available.")

        return f"{title}: {extract}"


weather_tool = WeatherTool(settings.weather_api_key)
wikipedia_tool = WikipediaTool()
