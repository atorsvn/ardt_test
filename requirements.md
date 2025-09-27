# Requirements

## Functional
- ✅ Answer general questions using LLM + tool plugins
- ✅ Store chat context (vector + short-term window)
- ✅ Support Discord slash commands and DM replies

## Non-Functional
- Performance: <500 ms average response to Discord
- Reliability: 99% uptime target
- Security: No external data storage beyond FAISS index

## Constraints
- Must run on Docker with GPU acceleration
- Must deploy to a low-cost VPS (<$20/month)
