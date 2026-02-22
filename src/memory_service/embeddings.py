from __future__ import annotations

import hashlib
import math
from typing import Iterable


def embed_text(text: str, dims: int = 64) -> list[float]:
    """Simple deterministic embedding for local bootstrap use.

    Uses repeated SHA256 hashing to produce a fixed-size vector in [-1, 1].
    """
    text = text.strip().lower()
    if not text:
        return [0.0] * dims

    out: list[float] = []
    seed = text.encode("utf-8")
    counter = 0
    while len(out) < dims:
        digest = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
        counter += 1
        for i in range(0, len(digest), 4):
            chunk = digest[i : i + 4]
            if len(chunk) < 4:
                continue
            n = int.from_bytes(chunk, "big", signed=False)
            out.append((n / 2**31) - 1.0)
            if len(out) >= dims:
                break

    # L2 normalize
    norm = math.sqrt(sum(v * v for v in out))
    if norm == 0:
        return out
    return [v / norm for v in out]


def cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    av = list(a)
    bv = list(b)
    if len(av) != len(bv) or not av:
        return 0.0
    return float(sum(x * y for x, y in zip(av, bv)))
