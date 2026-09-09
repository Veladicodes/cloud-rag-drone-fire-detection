"""Embedding backend for the RAG index.

Primary: ``sentence-transformers/all-mpnet-base-v2`` (768-dim) — matches
``docs/research/rag-response.md``. Runs fully locally, no API key.

Fallback: ``HashEmbedder`` — a deterministic, **non-semantic** 768-dim vector
derived from token hashes. It exists only so the pipeline and CI can run with
zero ML dependencies. Retrieval quality with the fallback is meaningless; it is
always logged loudly.
"""
from __future__ import annotations

import hashlib
import logging

import numpy as np

from backend.core.config import get_settings

log = logging.getLogger(__name__)
EMBED_DIM = 768


class HashEmbedder:
    mode = "hash-fallback (NON-SEMANTIC)"

    def encode(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), EMBED_DIM), dtype="float32")
        for i, text in enumerate(texts):
            for tok in text.lower().split():
                h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
                out[i, h % EMBED_DIM] += 1.0
            norm = np.linalg.norm(out[i]) or 1.0
            out[i] /= norm
        return out


class _SentenceTransformerEmbedder:
    mode = "sentence-transformers/all-mpnet-base-v2 (768-dim)"

    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    def encode(self, texts: list[str]) -> np.ndarray:
        return np.asarray(
            self._model.encode(texts, normalize_embeddings=True), dtype="float32"
        )


_cached = None


def get_embedder():
    """Return a singleton embedder honouring EMBED_MODE (auto | hash)."""
    global _cached
    if _cached is not None:
        return _cached

    mode = get_settings().embed_mode.lower()
    if mode != "hash":
        try:
            _cached = _SentenceTransformerEmbedder()
            log.info("Embedder: %s", _cached.mode)
            return _cached
        except Exception as exc:  # noqa: BLE001
            log.warning("sentence-transformers unavailable (%s) -> hash fallback", exc)

    _cached = HashEmbedder()
    log.warning("Embedder: %s", _cached.mode)
    return _cached
