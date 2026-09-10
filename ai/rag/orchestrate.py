# LOCAL STAND-IN FOR: Azure OpenAI (GPT-4o) grounded response generation.
# Swap `_generate_local` / `_generate_mock` for an AzureOpenAI chat completion
# call when LLM_MODE=azure and credentials exist (from Key Vault).
"""RAG orchestration: retrieve SOP chunks -> compile a bounded prompt -> LLM.

Prompt structure matches ``docs/research/rag-response.md``: system constraint
(closed-book, ``INSUFFICIENT_CONTEXT`` fallback), incident variables
(coordinates, wind, temperature, fuel dryness), retrieved SOP context, and an
output schema (evacuation zone, containment priority, dispatch coords, safety).

Modes (LLM_MODE):
    mock   -> deterministic, prefixed "[MOCK LLM OUTPUT]" (never presented as real)
    local  -> a small local transformers model if it can load, else mock
    gemini -> Google Gemini Flash (real generation) via GEMINI_API_KEY; falls back
              to mock if the key or package is missing so a fresh clone still runs
"""
from __future__ import annotations

import json
import logging
import textwrap

from ai.rag.retrieve import retrieve
from backend.core.config import get_settings

log = logging.getLogger(__name__)

_SYSTEM = (
    "You are a wildland fire dispatch assistant. Answer ONLY using the SOP context "
    "provided. If the context does not contain enough detail for the incident "
    "variables, reply with exactly INSUFFICIENT_CONTEXT and nothing else. Do not "
    "extrapolate beyond the provided procedures."
)

_MIN_USABLE_L2 = 1.15  # above this best-match distance we treat context as insufficient


def build_prompt(incident: dict, chunks: list[dict]) -> str:
    context = "\n\n".join(f"[{c['source']} #{c['rank']}] {c['text']}" for c in chunks) or "(none)"
    return textwrap.dedent(
        f"""\
        SYSTEM: {_SYSTEM}

        INCIDENT VARIABLES:
          coordinates: ({incident['lat']:.5f}, {incident['lon']:.5f})
          detected: {incident.get('detected_class', 'smoke')} @ confidence {incident.get('confidence', 0):.2f}
          wind: {incident.get('wind_speed_kmh', 0):.0f} km/h from {incident.get('wind_dir_deg', 0):.0f} deg
          temperature: {incident.get('temperature_c', 0):.0f} C
          fuel dryness: {incident.get('fuel_dryness', 'unknown')}

        RETRIEVED SOP CONTEXT:
        {context}

        TASK: Using ONLY the retrieved procedures above, produce an ordered action
        checklist for THIS incident. Rules:
          - Every step must cite the SOP file it comes from, e.g. "(03_evacuation_zoning.txt)".
          - Where a procedure gives a formula or threshold (e.g. evacuation-arc radius
            vs wind speed, staging distance), apply it using the incident variables.
          - If the procedures do not cover something an operator would need, write
            "not covered by provided SOPs" for that item — do NOT invent it.
          - If the procedures cover essentially nothing relevant, output exactly
            INSUFFICIENT_CONTEXT.
        Group the steps under: Evacuation, Containment, Dispatch/Staging, Crew safety.
        """
    )


def _generate_mock(incident: dict, chunks: list[dict], insufficient: bool) -> str:
    if insufficient:
        return "[MOCK LLM OUTPUT] INSUFFICIENT_CONTEXT"
    cited = ", ".join(sorted({c["source"] for c in chunks})) or "none"
    wind = incident.get("wind_speed_kmh", 0)
    radius = 1.5 + wind / 20.0
    return textwrap.dedent(
        f"""\
        [MOCK LLM OUTPUT] -- deterministic stand-in for Azure OpenAI GPT-4o. NOT real generation.

        ## Response Checklist (grounded in: {cited})

        ### 1. Evacuation zone range
        - Establish a {radius:.1f} km downwind evacuation arc from ({incident['lat']:.4f}, {incident['lon']:.4f}),
          biased along bearing {incident.get('wind_dir_deg', 0):.0f} deg.

        ### 2. Containment priority vector
        - Anchor on the flank opposite the wind; hold the downwind head last.
        - Fuel dryness "{incident.get('fuel_dryness', 'unknown')}" -> {"aggressive" if incident.get('fuel_dryness') == 'high' else "standard"} line spacing.

        ### 3. Dispatch coordinates
        - Staging: ({incident['lat'] + 0.01:.4f}, {incident['lon'] - 0.01:.4f}) (upwind, road-accessible).

        ### 4. Safety protocols
        - LCES in place before engagement; re-brief on wind shift > 30 deg.
        - Per retrieved SOP chunks (top L2 distance {chunks[0]['l2_distance']:.3f}).
        """
    )


def _generate_local(prompt: str) -> str | None:
    try:
        from transformers import pipeline  # noqa: PLC0415

        gen = pipeline("text2text-generation", model="google/flan-t5-small")
        out = gen(prompt, max_new_tokens=256)[0]["generated_text"]
        return f"[LOCAL MODEL: flan-t5-small]\n\n{out}"
    except Exception as exc:  # noqa: BLE001
        log.warning("local LLM unavailable (%s) -> mock mode", exc)
        return None


def _generate_gemini(prompt: str) -> str | None:
    """Real generation via Google Gemini Flash. Bounded prompt is unchanged.

    Uses the current `google-genai` SDK (the older `google-generativeai` package
    named in the brief is now deprecated/unmaintained and mis-parses newer models).
    """
    s = get_settings()
    if not s.gemini_api_key:
        log.warning("LLM_MODE=gemini but GEMINI_API_KEY is empty -> mock fallback")
        return None
    try:
        from google import genai  # noqa: PLC0415
        from google.genai import types  # noqa: PLC0415

        client = genai.Client(api_key=s.gemini_api_key)
        cfg_kwargs = dict(
            system_instruction=_SYSTEM,
            temperature=0.2,
            max_output_tokens=2048,
        )
        # 2.5+ Flash is a "thinking" model; a small thinking budget keeps output
        # tokens for the actual checklist instead of internal reasoning.
        try:
            cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
        except Exception:  # noqa: BLE001 - older SDK / model without thinking
            pass
        resp = client.models.generate_content(
            model=s.gemini_model, contents=prompt,
            config=types.GenerateContentConfig(**cfg_kwargs),
        )
        text = (resp.text or "").strip()
        return text or None
    except Exception as exc:  # noqa: BLE001
        log.warning("Gemini call failed (%s) -> mock fallback", exc)
        return None


def generate_plan(incident: dict, k: int = 3) -> dict:
    chunks = retrieve(_query_from(incident), k=k)
    best = chunks[0]["l2_distance"] if chunks else float("inf")
    insufficient = (not chunks) or best > _MIN_USABLE_L2

    mode = get_settings().llm_mode.lower()
    prompt = build_prompt(incident, chunks)

    # A real model still honours the INSUFFICIENT_CONTEXT gate: if retrieval is weak
    # we do not spend an API call, we return the fallback directly.
    if mode == "gemini" and not insufficient:
        out = _generate_gemini(prompt)
        if out is not None:
            return _result(out, "gemini", chunks, insufficient)
    elif mode == "gemini" and insufficient:
        return _result("INSUFFICIENT_CONTEXT", "gemini", chunks, insufficient)

    if mode == "local" and not insufficient:
        local = _generate_local(prompt)
        if local is not None:
            return _result(local, "local", chunks, insufficient)

    fallback_mode = "mock" if mode == "mock" else "mock(fallback)"
    return _result(_generate_mock(incident, chunks, insufficient), fallback_mode, chunks, insufficient)


def _query_from(incident: dict) -> str:
    return (
        f"Wildfire containment and evacuation procedures under wind speed "
        f"{incident.get('wind_speed_kmh', 0):.0f} km/h, temperature "
        f"{incident.get('temperature_c', 0):.0f} C, {incident.get('fuel_dryness', 'moderate')} fuel dryness."
    )


def _result(plan_md: str, mode: str, chunks: list[dict], insufficient: bool) -> dict:
    return {
        "plan_markdown": plan_md,
        "llm_mode": mode,
        "insufficient_context": bool(insufficient),
        "retrieved_sources": json.dumps(
            [{"source": c["source"], "l2_distance": c["l2_distance"]} for c in chunks]
        ),
    }
