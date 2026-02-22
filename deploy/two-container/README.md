# Foxlight Two-Container Memory Stack

This stack is optimized for a dedicated mini:

1. `qdrant` (persistent vector store)
2. `memory-manager` (HTTP memory API)

## Quick start

```bash
cd deploy/two-container
cp .env.example .env
# edit .env as needed

docker compose up -d --build
```

## Health checks

```bash
curl http://localhost:${MEMORY_MANAGER_PORT:-8000}/api/health
curl http://localhost:${QDRANT_HTTP_PORT:-6333}/healthz
```

## Portainer deploy

- Create a new stack in Portainer.
- Paste `docker-compose.yml`.
- Add env values from `.env.example` in the stack UI.
- Deploy.

## LAN access

- Expose only to trusted LAN.
- Keep `qdrant` internal if possible (do not expose publicly).
- Put `memory-manager` behind a reverse proxy/auth if you need broader access.

## OpenClaw wiring

Point OpenClaw/plugin tools to:

- Memory Manager: `http://<mini-ip>:8000`
- Qdrant (internal to manager): `qdrant:6333`

## Notes

- Current memory-manager implementation stores memory in local SQLite for MVP behavior.
- Qdrant is deployed now to keep data infra stable and ready for vector-native evolution.
- Next implementation step: route search/write through Qdrant + Ollama embeddings.
