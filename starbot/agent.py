"""Core StarBot agent orchestration."""

from __future__ import annotations

from collections.abc import Sequence
import logging

from . import memory
from .llm import llm_client
from .memory import Message
from .tools import ToolError, weather_tool, wikipedia_tool

logger = logging.getLogger(__name__)


class StarBotAgent:
    """High-level agent responsible for fulfilling user requests."""

    def __init__(self) -> None:
        self.memory = memory.memory
        self.llm = llm_client

    def _context_strings(self, recent: Sequence[Message], similar: Sequence[Message]) -> list[str]:
        """Build natural-language context strings for the LLM."""

        context: list[str] = []
        for message in recent:
            context.append(f"Recent {message.role} {message.author}: {message.content}")
        for message in similar:
            context.append(f"Related {message.role} {message.author}: {message.content}")
        return context

    def _tool_response(self, prompt: str) -> str | None:
        """Attempt to satisfy the prompt using external tools."""

        lowered = prompt.lower()
        if "weather" in lowered and weather_tool.available():
            location = prompt.split("weather", 1)[-1].strip() or "current location"
            try:
                result = weather_tool.run(location)
                return result.format()
            except ToolError as exc:  # pragma: no cover - network failure path
                logger.warning("Weather tool failed: %s", exc)
                return "I couldn't retrieve the weather right now."
        if any(keyword in lowered for keyword in ("who is", "what is", "wikipedia")):
            query = prompt.replace("wikipedia", "").strip()
            if not query:
                query = prompt
            try:
                return wikipedia_tool.search(query)
            except ToolError as exc:  # pragma: no cover - network failure path
                logger.warning("Wikipedia tool failed: %s", exc)
                return "I couldn't find details on that topic."
        return None

    def generate_reply(self, author: str, prompt: str) -> str:
        """Create a reply by combining memory, tools, and the LLM."""

        user_message = Message(role="user", author=author, content=prompt)
        self.memory.add_message(user_message)

        recent = self.memory.window_messages()
        similar = self.memory.similar_messages(prompt)
        context = self._context_strings(recent, similar)

        tool_result = self._tool_response(prompt)
        if tool_result:
            reply = tool_result
        else:
            reply = self.llm.generate(prompt, context)

        assistant_message = Message(role="assistant", author="StarBot", content=reply)
        self.memory.add_message(assistant_message)
        return reply


agent = StarBotAgent()
