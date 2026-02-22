# mcp-memory-service

Local-first memory service with HTTP API, designed for Foxlight/OpenClaw workflows.

## Endpoints
- `GET /api/health`
- `POST /api/memories`
- `POST /api/memories/search`

## Local run
```bash
python -m pip install -e .[dev]
uvicorn memory_service.app:app --host 0.0.0.0 --port 8000
```

## Test
```bash
pytest --cov=. --cov-fail-under=70
```

## Docker
```bash
docker build -t mcp-memory-service .
docker run -p 8000:8000 mcp-memory-service
```
