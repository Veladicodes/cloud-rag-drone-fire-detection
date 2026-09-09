"""Online retrieval: embed a query, search the FAISS IndexFlatL2, return top-k chunks.

Distance is true L2 (Euclidean): d(q, v) = sqrt(sum_k (q_k - v_k)^2)
    — consistent with ``docs/research/methodology.md`` and ``rag-response.md``.
"""
from __future__ import annotations

import functools
import json
from pathlib import Path

import faiss
import numpy as np

from ai.rag.embeddings import get_embedder
from backend.core.config import get_settings

DEFAULT_K = 3


@functools.lru_cache(maxsize=1)
def _load(index_dir: str) -> tuple[faiss.Index, list[dict]]:
    d = Path(index_dir)
    index = faiss.read_index(str(d / "sop.index"))
    chunks = json.loads((d / "chunks.json").read_text(encoding="utf-8"))
    return index, chunks


def retrieve(query: str, k: int = DEFAULT_K, index_path: str | None = None) -> list[dict]:
    settings = get_settings()
    index_dir = str(settings.abspath(index_path or settings.faiss_index_path))
    index, chunks = _load(index_dir)

    qvec = get_embedder().encode([query]).astype("float32")
    sq_dist, idx = index.search(np.ascontiguousarray(qvec), min(k, index.ntotal))

    results: list[dict] = []
    for rank, (i, d2) in enumerate(zip(idx[0], sq_dist[0])):
        if i < 0:
            continue
        c = chunks[int(i)]
        results.append(
            {
                "rank": rank + 1,
                "source": c["source"],
                "chunk_id": c["id"],
                "text": c["text"],
                # IndexFlatL2 returns squared L2; report the true L2 distance.
                "l2_distance": float(np.sqrt(max(d2, 0.0))),
            }
        )
    return results
