from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .embeddings import cosine_similarity, embed_text


@dataclass
class Memory:
    id: int
    text: str
    metadata: dict[str, Any]


class MemoryStore:
    def __init__(self, db_path: str = "data/memory.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        try:
            yield conn
        finally:
            conn.close()

    def _init(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    embedding TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add(self, text: str, metadata: dict[str, Any] | None = None) -> Memory:
        metadata = metadata or {}
        emb = embed_text(text)
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO memories(text, metadata, embedding) VALUES (?, ?, ?)",
                (text, json.dumps(metadata), json.dumps(emb)),
            )
            conn.commit()
            return Memory(id=cur.lastrowid, text=text, metadata=metadata)

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        q_emb = embed_text(query)
        with self._connect() as conn:
            rows = conn.execute("SELECT id, text, metadata, embedding FROM memories").fetchall()

        scored: list[dict[str, Any]] = []
        for row in rows:
            emb = json.loads(row["embedding"])
            score = cosine_similarity(q_emb, emb)
            scored.append(
                {
                    "id": row["id"],
                    "text": row["text"],
                    "metadata": json.loads(row["metadata"]),
                    "score": round(score, 6),
                }
            )
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[: max(1, min(limit, 50))]
