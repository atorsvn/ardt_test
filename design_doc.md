# Design & Architecture

## High-Level Architecture
```
Discord → Command Router → StarBot Agent → 
   ├─ Ollama LLM (gemma3:1b)
   ├─ FAISS Vector Store
   └─ External APIs (weather, wiki)
```

## Key Decisions (ADRs)
- **Use FAISS** for persistent semantic memory
- **Deploy with Docker** for portability
- **Python + discord.py** chosen for ecosystem & reliability

## Scaling
- Horizontal scaling with multiple bot shards
- Option to add Redis pub/sub if traffic spikes
