"""LLM integration helpers for StarBot."""

from __future__ import annotations

from typing import Sequence

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import Generation
from langchain_ollama import ChatOllama

from .config import settings


class LLMClient:
    """Wrapper around LangChain's Ollama chat model."""

    def __init__(self, model: str = "gemma3:1b") -> None:
        self.model_name = model
        self.client = ChatOllama(
            model=self.model_name,
            base_url=settings.ollama_host,
            temperature=0.2,
            timeout=settings.response_timeout_seconds,
        )

    def generate(self, prompt: str, context: Sequence[str]) -> str:
        """Generate a response for the given prompt and context."""

        messages: list[BaseMessage] = [
            SystemMessage(content="You are StarBot, a friendly and concise Discord assistant."),
        ]
        for chunk in context:
            messages.append(SystemMessage(content=f"Context: {chunk}"))
        messages.append(HumanMessage(content=prompt))
        response: Generation = self.client.invoke(messages)  # type: ignore[assignment]
        return str(response.text)


llm_client = LLMClient()
