from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .store import MemoryStore

app = FastAPI(title="MCP Memory Service", version="0.1.0")
store = MemoryStore(db_path=os.getenv("MEMORY_DB_PATH", "data/memory.db"))


class AddMemoryRequest(BaseModel):
    text: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=50)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/memories")
def add_memory(payload: AddMemoryRequest) -> dict[str, Any]:
    mem = store.add(payload.text, payload.metadata)
    return {"id": mem.id, "text": mem.text, "metadata": mem.metadata}


@app.post("/api/memories/search")
def search_memory(payload: SearchRequest) -> dict[str, Any]:
    matches = store.search(payload.query, payload.limit)
    return {"matches": matches}
