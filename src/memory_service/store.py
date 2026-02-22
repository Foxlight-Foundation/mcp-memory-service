from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                metadata TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def add(self, text: str, metadata: dict[str, Any] | None = None) -> Memory:
        metadata = metadata or {}
        emb = embed_text(text)
        cur = self.conn.execute(
            "INSERT INTO memories(text, metadata, embedding) VALUES (?, ?, ?)",
            (text, json.dumps(metadata), json.dumps(emb)),
        )
        self.conn.commit()
        return Memory(id=cur.lastrowid, text=text, metadata=metadata)

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        q_emb = embed_text(query)
        rows = self.conn.execute("SELECT id, text, metadata, embedding FROM memories").fetchall()
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
