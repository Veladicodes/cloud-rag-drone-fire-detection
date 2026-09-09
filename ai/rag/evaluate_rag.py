"""RQ3 / gate CG-2 evaluation: measure the real RAG output's grounding and its
similarity to hand-written expert reference plans.

Metrics per incident:
  * bertscore_f1        BERTScore F1 (candidate vs expert reference), model-based
  * returned_insufficient   did the pipeline emit INSUFFICIENT_CONTEXT
  * cited_sources / retrieved_sources   the SOP files the plan cites vs. what was
                                        actually retrieved
  * hallucinated_source_rate   fraction of cited SOP files NOT in the retrieved set
                               (0.0 = every citation is grounded in retrieval)
  * uncited_claim_lines        content lines with no "(NN_*.txt)" citation
                               (rough upper bound on ungrounded statements)

    LLM_MODE=gemini python -m ai.rag.evaluate_rag

Respects the Gemini free-tier rate limit (5 req/min) with a delay between calls.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from ai.rag.orchestrate import _query_from, generate_plan
from ai.rag.retrieve import retrieve
from backend.core.config import REPO_ROOT, get_settings

REF_DIR = REPO_ROOT / "ai" / "rag" / "reference_plans"
OUT = REPO_ROOT / "results" / "rag-metrics"
CITE_RE = re.compile(r"\(?\b(\d{2}_[a-z_]+\.txt)\)?")
CALL_DELAY_S = 15  # >= 60/5 with margin


def _bertscore(cands: list[str], refs: list[str]) -> list[float]:
    from bert_score import score

    P, R, F1 = score(cands, refs, lang="en", model_type="distilbert-base-uncased",
                     rescale_with_baseline=False, verbose=False)
    return [round(float(x), 4) for x in F1]


def _line_grounding(plan: str) -> tuple[int, int]:
    cited = uncited = 0
    for ln in plan.splitlines():
        s = ln.strip().lstrip("-* ").strip()
        if len(s) < 25 or s.endswith(":") or s.lower() in {"evacuation", "containment", "crew safety"}:
            continue
        if CITE_RE.search(ln):
            cited += 1
        else:
            uncited += 1
    return cited, uncited


def main() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    cases = json.loads((REF_DIR / "incidents.json").read_text(encoding="utf-8"))

    rows, cands, refs = [], [], []
    for i, case in enumerate(cases):
        inc = case["incident"]
        ref = (REF_DIR / case["reference_file"]).read_text(encoding="utf-8").strip()
        retrieved = {h["source"] for h in retrieve(_query_from(inc), k=4)}
        res = generate_plan(inc, k=4)
        plan = res["plan_markdown"]
        insufficient = res["insufficient_context"] or plan.strip().upper().endswith("INSUFFICIENT_CONTEXT")

        cited = set(CITE_RE.findall(plan))
        hallu = sorted(cited - retrieved)
        hsr = round(len(hallu) / len(cited), 4) if cited else 0.0
        c_lines, u_lines = _line_grounding(plan)

        rows.append({
            "id": case["id"], "llm_mode": res["llm_mode"],
            "returned_insufficient": bool(insufficient),
            "retrieved_sources": sorted(retrieved),
            "cited_sources": sorted(cited),
            "hallucinated_sources": hallu,
            "hallucinated_source_rate": hsr,
            "cited_claim_lines": c_lines, "uncited_claim_lines": u_lines,
        })
        cands.append(plan)
        refs.append(ref)
        if res["llm_mode"] == "gemini" and i < len(cases) - 1:
            time.sleep(CALL_DELAY_S)

    try:
        f1s = _bertscore(cands, refs)
    except Exception as exc:  # noqa: BLE001
        f1s = [None] * len(rows)
        print(f"BERTScore unavailable ({exc}); F1 left null")
    for r, f in zip(rows, f1s):
        r["bertscore_f1"] = f

    scored = [r for r in rows if r["llm_mode"] == "gemini"]
    got_f1 = [r["bertscore_f1"] for r in scored if r["bertscore_f1"] is not None]
    summary = {
        "config": {"llm_mode": settings.llm_mode, "gemini_model": settings.gemini_model,
                   "k": 4, "n_incidents": len(rows), "n_scored_with_real_llm": len(scored)},
        "mean_bertscore_f1": round(sum(got_f1) / len(got_f1), 4) if got_f1 else None,
        "mean_hallucinated_source_rate": round(
            sum(r["hallucinated_source_rate"] for r in scored) / len(scored), 4) if scored else None,
        "insufficient_context_count": sum(r["returned_insufficient"] for r in scored),
        "total_uncited_claim_lines": sum(r["uncited_claim_lines"] for r in scored),
        "total_cited_claim_lines": sum(r["cited_claim_lines"] for r in scored),
        "gate_CG_2": "hallucination rate <= 1.0% under test prompts (milestones.md)",
        "per_incident": rows,
    }
    (OUT / "rag_eval.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "per_incident"}, indent=2))
    print(f"written: {OUT / 'rag_eval.json'}")
    return summary


if __name__ == "__main__":
    main()
