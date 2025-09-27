"""Conversation memory management leveraging FAISS for vector search."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable

import faiss
import numpy as np
from langchain_ollama import OllamaEmbeddings

from .config import settings


@dataclass
class Message:
    """Representation of a conversational message."""

    role: str
    author: str
    content: str


class ConversationMemory:
    """Hybrid memory that combines short-term windowing with FAISS recall."""

    def __init__(
        self,
        index_path: str,
        max_window: int,
        embedding_model: str = "nomic-embed-text",
    ) -> None:
        self.index_path = Path(index_path)
        self.metadata_path = self.index_path.with_suffix(".json")
        self.max_window = max_window
        self.embedding_model = embedding_model
        self.embeddings = OllamaEmbeddings(
            model=self.embedding_model,
            base_url=settings.ollama_host,
        )
        self.window: list[Message] = []
        self.index: faiss.Index | None = None
        self.metadata: list[Message] = []
        self._load()

    def _load(self) -> None:
        """Load FAISS index and metadata from disk when present."""

        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        if self.metadata_path.exists():
            data = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            self.metadata = [Message(**item) for item in data]

    def _persist(self) -> None:
        """Persist FAISS index and metadata to disk."""

        if self.index is not None:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.index_path))
            data = [message.__dict__ for message in self.metadata]
            self.metadata_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _embed(self, texts: Iterable[str]) -> np.ndarray:
        """Generate embeddings for a collection of texts."""

        vectors = self.embeddings.embed_documents(list(texts))
        return np.array(vectors, dtype="float32")

    def add_message(self, message: Message) -> None:
        """Record a message in both window and long-term memory."""

        self.window.append(message)
        self.window = self.window[-self.max_window :]

        vector = self._embed([message.content])
        if self.index is None:
            dimension = vector.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
        self.index.add(vector)
        self.metadata.append(message)
        self._persist()

    def similar_messages(self, query: str, limit: int = 5) -> list[Message]:
        """Retrieve messages similar to the query using FAISS search."""

        if self.index is None or not self.metadata:
            return []

        query_vector = self._embed([query])
        scores, indices = self.index.search(query_vector, min(limit, len(self.metadata)))
        results: list[Message] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append(self.metadata[idx])
        return results

    def window_messages(self) -> list[Message]:
        """Return the short-term conversational window."""

        return list(self.window)


memory = ConversationMemory(
    index_path=settings.faiss_index_path,
    max_window=settings.max_context_messages,
)
