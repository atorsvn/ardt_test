# Agents

## Core Agent: StarBot
| Attribute | Details |
|-----------|---------|
| Purpose | Help Discord users with Q&A and lightweight tasks |
| Model | gemma3:1b via Ollama |
| Memory | Sliding 4-message window + FAISS vector store |
| Tools | Discord API, Wikipedia search, weather API |
| Safety | Rate-limit per user, profanity filter |

### Behavior
- Respond within 2 seconds
- Keep answers under 100 words unless asked to expand
- Maintain friendly, encouraging tone

## Future Agents
- SchedulerAgent: manage recurring reminders
- MediaAgent: generate images or audio on request
