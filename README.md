# StarBot

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
```

### Configuration
Set the following environment variables:
- `DISCORD_TOKEN` (required)
- `WEATHER_API_KEY` (optional)
- `OLLAMA_HOST` (default `http://localhost:11434`)
- `FAISS_INDEX_PATH` (default `data/memory.index`)
- `RESPONSE_TIMEOUT_SECONDS` (default `8`)
- `MAX_CONTEXT_MESSAGES` (default `8`)

### Running Locally
```bash
python main.py
```

## Docker
Build and run the container:
```bash
docker build -t starbot .
docker run --gpus all -e DISCORD_TOKEN=your_token -e WEATHER_API_KEY=your_key starbot
```

## Project Structure
```
starbot/
  agent.py
  config.py
  discord_bot.py
  llm.py
  memory.py
  tools.py
main.py
```

## Development
- Run the automated test suite with `pytest`
- Linting and testing are enforced via GitHub Actions CI
- Extend `starbot/tools.py` to add more integrations

## License
This project is licensed under the [MIT License](LICENSE).
