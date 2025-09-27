"""Tests covering StarBot's external tool helpers."""

from __future__ import annotations

from typing import Any

import pytest
from requests import RequestException

from starbot.tools import ToolError, WeatherResult, WeatherTool, WikipediaTool


class _DummyResponse:
    """Simple stand-in for ``requests.Response`` objects used in tests."""

    def __init__(self, *, status_code: int = 200, payload: dict[str, Any] | None = None, text: str = "OK") -> None:
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self) -> dict[str, Any]:
        return self._payload


def test_weather_tool_requires_api_key() -> None:
    """Running the weather tool without an API key should error."""

    tool = WeatherTool(api_key=None)

    with pytest.raises(ToolError):
        tool.run("Berlin")


def test_weather_tool_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Weather responses are mapped into ``WeatherResult`` instances."""

    tool = WeatherTool(api_key="token")

    def fake_get(url: str, params: dict[str, Any], timeout: int) -> _DummyResponse:
        assert url == tool.base_url
        assert params["q"] == "Berlin"
        return _DummyResponse(
            payload={
                "location": {"name": "Berlin"},
                "current": {"temp_c": 21.5, "condition": {"text": "Sunny"}},
            }
        )

    monkeypatch.setattr("starbot.tools.requests.get", fake_get)

    result = tool.run("Berlin")

    assert isinstance(result, WeatherResult)
    assert result.format() == "Weather in Berlin: Sunny, 21.5°C"


def test_weather_tool_network_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Network failures are wrapped as ``ToolError`` exceptions."""

    tool = WeatherTool(api_key="token")

    def raising_get(*_: Any, **__: Any) -> None:
        raise RequestException("boom")

    monkeypatch.setattr("starbot.tools.requests.get", raising_get)

    with pytest.raises(ToolError):
        tool.run("Berlin")


def test_wikipedia_tool_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """The Wikipedia tool returns the lead paragraph of the top result."""

    tool = WikipediaTool()

    def fake_get(url: str, params: dict[str, Any], timeout: int) -> _DummyResponse:
        assert "wikipedia.org" in url
        return _DummyResponse(
            payload={
                "query": {
                    "pages": {
                        "1": {
                            "title": "Berlin",
                            "extract": "Berlin is the capital of Germany.",
                        }
                    }
                }
            }
        )

    monkeypatch.setattr("starbot.tools.requests.get", fake_get)

    summary = tool.search("Berlin")

    assert summary.startswith("Berlin: Berlin is the capital")


def test_wikipedia_tool_handles_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Non-200 HTTP status codes raise ``ToolError``."""

    tool = WikipediaTool()

    monkeypatch.setattr(
        "starbot.tools.requests.get",
        lambda *_, **__: _DummyResponse(status_code=500, text="Internal Server Error"),
    )

    with pytest.raises(ToolError):
        tool.search("Berlin")
