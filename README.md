StarBot is a Discord assistant that responds to user questions using an Ollama-hosted LLM, a FAISS-powered memory, and lightweight tool integrations for weather and Wikipedia lookups.

## Features
- Fast Discord responses (<500 ms target) with short context windowing
- Long-term semantic recall via FAISS vector search
- Weather and Wikipedia integrations for up-to-date answers
- Dockerized deployment with GPU support for Ollama

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (for deployment)
- Running Ollama server with the `gemma3:1b` and `nomic-embed-text` models pulled
- Discord Bot Token and optional Weather API key

### Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .