import { useEffect, useState } from "react";
import { api } from "../services/api.js";

// Renders the RAG-generated checklist markdown for a chosen incident.
export default function ResponsePlanViewer({ incidents }) {
  const withPlan = incidents.filter((i) => i.has_plan);
  const [selected, setSelected] = useState(null);
  const [plan, setPlan] = useState(null);

  useEffect(() => {
    if (!selected && withPlan[0]) setSelected(withPlan[0].id);
  }, [withPlan, selected]);

  useEffect(() => {
    if (selected == null) return;
    api.plan(selected).then(setPlan).catch(() => setPlan(null));
  }, [selected]);

  return (
    <div>
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
          <p>
            <small>
              llm_mode: <b>{plan.llm_mode}</b>
              {plan.insufficient_context ? " — INSUFFICIENT_CONTEXT" : ""} · sources:{" "}
              {plan.retrieved_sources.map((s) => s.source).join(", ") || "none"}
            </small>
          </p>
          <pre className="plan">{plan.plan_markdown}</pre>
        </>
      )}
    </div>
  );
}
