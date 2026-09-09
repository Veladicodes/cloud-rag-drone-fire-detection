"""RAG retrieval structural checks against the sample-SOP FAISS index."""
from __future__ import annotations

import json

from ai.rag.orchestrate import generate_plan
from ai.rag.retrieve import retrieve


def test_retrieve_returns_k_ranked_chunks(rag_index):
    hits = retrieve("evacuation zone downwind arc sizing under wind", k=3)
    assert 1 <= len(hits) <= 3
    assert [h["rank"] for h in hits] == list(range(1, len(hits) + 1))
    # true L2 distance, non-negative, non-decreasing with rank
    dists = [h["l2_distance"] for h in hits]
    assert all(d >= 0 for d in dists)
    assert dists == sorted(dists)
    assert all(h["source"].endswith((".txt", ".md")) for h in hits)


def test_generate_plan_shape_and_grounding(rag_index):
    out = generate_plan({
        "lat": 34.07, "lon": -118.24, "detected_class": "smoke", "confidence": 0.9,
        "wind_speed_kmh": 22, "wind_dir_deg": 200, "temperature_c": 33, "fuel_dryness": "high",
    })
    assert set(out) == {"plan_markdown", "llm_mode", "insufficient_context", "retrieved_sources"}
    assert out["llm_mode"].startswith("mock")
    assert "[MOCK LLM OUTPUT]" in out["plan_markdown"]  # never unlabelled
    json.loads(out["retrieved_sources"])  # valid JSON list
