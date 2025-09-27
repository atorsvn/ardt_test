# Tech Implementation

## Build
- Python 3.11
- Requirements: langchain, faiss-cpu, discord.py, ollama

## APIs & Integration
- Discord Bot Token (env var)
- Weather API key
- Local Ollama server with gemma3:1b pulled

## Deployment
1. `docker build -t starbot .`
2. `docker run --gpus all -e DISCORD_TOKEN=xxx starbot`

## CI/CD
- GitHub Actions for lint + test on every push
- Automatic Docker image publish on `main` branch merge
