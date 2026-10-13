import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { api } from "../services/api.js";

// Renders the RAG-generated checklist markdown for a chosen incident.
// When focusIncidentId is set, auto-switches to that incident's plan.
export default function ResponsePlanViewer({ incidents, focusIncidentId, onFocusIncident }) {
  const withPlan = incidents.filter((i) => i.has_plan);
  const [selected, setSelected] = useState(null);
  const [plan, setPlan] = useState(null);

  useEffect(() => {
    if (!selected && withPlan[0]) setSelected(withPlan[0].id);
  }, [withPlan, selected]);

  useEffect(() => {
    if (focusIncidentId != null) setSelected(focusIncidentId);
  }, [focusIncidentId]);

  useEffect(() => {
    if (selected == null) return;
    api.plan(selected).then(setPlan).catch(() => setPlan(null));
  }, [selected]);

  return (
    <div>
      {focusIncidentId != null && (
        <div className="plan-meta" style={{ marginBottom: 8 }}>
          showing incident #{focusIncidentId}{" "}
          <button style={{ width: "auto", display: "inline", padding: "2px 8px" }} onClick={() => onFocusIncident?.(null)}>
            back to all
          </button>
        </div>
      )}
      <select value={selected ?? ""} onChange={(e) => setSelected(Number(e.target.value))}>
        <option value="" disabled>
          pick an incident
        </option>
        {withPlan.map((i) => (
          <option key={i.id} value={i.id}>
            #{i.id} — {i.detected_class} {Number(i.confidence).toFixed(2)}
          </option>
        ))}
      </select>
      {plan && (
        <>
          {plan.llm_mode === "mock" && (
            <span className="mock-banner">⚠ mock LLM output — deterministic stand-in, not real generation</span>
          )}
          <div className="plan-meta">
            llm_mode: <b>{plan.llm_mode}</b>
            {plan.insufficient_context ? " — INSUFFICIENT_CONTEXT" : ""}
            <div style={{ marginTop: 6 }}>
              {plan.retrieved_sources.length === 0 && "no sources retrieved"}
              {[...new Set(plan.retrieved_sources.map((s) => s.source))].map((src) => (
                <span className="source-chip" key={src}>
                  {src}
                </span>
              ))}
            </div>
          </div>
          <div className="plan-markdown">
            <ReactMarkdown>{plan.plan_markdown}</ReactMarkdown>
          </div>
        </>
      )}
    </div>
  );
}
