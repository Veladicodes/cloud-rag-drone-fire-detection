"""Offline ingestion: SOP text files -> chunks -> embeddings -> FAISS IndexFlatL2.

Parameters match ``docs/research/rag-response.md``:
    chunk_size = 500 characters, chunk_overlap = 50 characters.

Run directly to (re)build the index:
    python -m ai.rag.ingest
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import faiss
import numpy as np

from ai.rag.embeddings import get_embedder
from backend.core.config import get_settings

log = logging.getLogger(__name__)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
_SEPARATORS = ["\n\n", "\n", ". ", " "]


def _split_recursive(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Small recursive-character splitter (semantic boundaries first, then hard cut)."""
    text = text.strip()
    if len(text) <= size:
        return [text] if text else []

    for sep in _SEPARATORS:
        if sep in text:
            parts, buf, chunks = text.split(sep), "", []
            for part in parts:
                candidate = f"{buf}{sep}{part}" if buf else part
                if len(candidate) <= size:
                    buf = candidate
                else:
                    if buf:
                        chunks.append(buf)
                    buf = part if len(part) <= size else part[:size]
            if buf:
                chunks.append(buf)
            # stitch overlap
            with_overlap: list[str] = []
            for i, ch in enumerate(chunks):
                if i and overlap:
                    with_overlap.append((chunks[i - 1][-overlap:] + " " + ch).strip())
                else:
                    with_overlap.append(ch)
            return with_overlap

    # no separator found: hard windows
    step = size - overlap
    return [text[i : i + size] for i in range(0, len(text), step)]


def build_index(kb_path: str | None = None, index_path: str | None = None) -> dict:
    settings = get_settings()
    kb = settings.abspath(kb_path or settings.kb_path)
    out_dir = settings.abspath(index_path or settings.faiss_index_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    docs = sorted(
        p for p in [*kb.glob("*.txt"), *kb.glob("*.md")] if p.name.lower() != "readme.md"
    )
    if not docs:
        raise FileNotFoundError(f"No .txt/.md SOP files found in {kb}")

    chunks: list[dict] = []
    for doc in docs:
        for j, piece in enumerate(_split_recursive(doc.read_text(encoding="utf-8"))):
            chunks.append({"id": f"{doc.stem}#{j}", "source": doc.name, "text": piece})

    embedder = get_embedder()
    vectors = embedder.encode([c["text"] for c in chunks])
    index = faiss.IndexFlatL2(vectors.shape[1])  # true L2 (Euclidean) distance
    index.add(np.ascontiguousarray(vectors, dtype="float32"))

    faiss.write_index(index, str(out_dir / "sop.index"))
    (out_dir / "chunks.json").write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    meta = {
        "documents": [d.name for d in docs],
        "chunk_count": len(chunks),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "embedder": embedder.mode,
        "dim": int(vectors.shape[1]),
    }
    (out_dir / "manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    log.info("FAISS index built: %s", meta)
    return meta


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    print(json.dumps(build_index(), indent=2))
