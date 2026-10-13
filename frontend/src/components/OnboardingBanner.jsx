import { useState } from "react";

const STEPS = [
  { n: 1, title: "Detect", desc: "Drone-side YOLO flags fire/smoke" },
  { n: 2, title: "Immediate Alert", desc: "Mock SMS fires instantly — before any AI" },
  { n: 3, title: "RAG Plan", desc: "Grounded response checklist, cited to real SOPs" },
  { n: 4, title: "Live Dashboard", desc: "Everything streams here over WebSocket" },
];

// Dismissible "how this works" strip — no persistence, reappears on reload by design.
export default function OnboardingBanner() {
  const [dismissed, setDismissed] = useState(false);
  if (dismissed) return null;

  return (
    <div className="onboarding">
      <div className="onboarding-steps">
        {STEPS.map((s, i) => (
          <div className="onboarding-step" key={s.n}>
            <div className="onboarding-num">{s.n}</div>
            <div>
              <div className="onboarding-title">{s.title}</div>
              <div className="onboarding-desc">{s.desc}</div>
            </div>
            {i < STEPS.length - 1 && <span className="onboarding-arrow">→</span>}
          </div>
        ))}
      </div>
      <button className="onboarding-dismiss" onClick={() => setDismissed(true)}>
        ✕
      </button>
    </div>
  );
}
