import { useEffect, useState } from "react";
import { api } from "../services/api.js";

// Editable alert-recipient directory — phone/email per role, backed by the
// real Recipient table (default phone comes from the backend, not hardcoded here).
export default function RecipientSettingsPanel() {
  const [recipients, setRecipients] = useState([]);
  const [drafts, setDrafts] = useState({});
  const [status, setStatus] = useState({});

  useEffect(() => {
    api.recipients().then((rows) => {
      setRecipients(rows);
      setDrafts(Object.fromEntries(rows.map((r) => [r.role, { phone_number: r.phone_number, email: r.email }])));
    }).catch(() => {});
  }, []);

  const save = async (role) => {
    setStatus((s) => ({ ...s, [role]: "saving" }));
    try {
      const updated = await api.updateRecipient(role, drafts[role]);
      setRecipients((rows) => rows.map((r) => (r.role === role ? updated : r)));
      setStatus((s) => ({ ...s, [role]: "saved" }));
      setTimeout(() => setStatus((s) => ({ ...s, [role]: null })), 2000);
    } catch {
      setStatus((s) => ({ ...s, [role]: "error" }));
    }
  };

  return (
    <div className="recipient-list">
      {recipients.map((r) => (
        <div className="recipient-row" key={r.role}>
          <div className="recipient-role">{r.role.replaceAll("_", " ")}</div>
          <input
            type="tel"
            placeholder="+919487038353"
            value={drafts[r.role]?.phone_number ?? ""}
            onChange={(e) =>
              setDrafts((d) => ({ ...d, [r.role]: { ...d[r.role], phone_number: e.target.value } }))
            }
          />
          <input
            type="email"
            placeholder="email (fallback channel)"
            value={drafts[r.role]?.email ?? ""}
            onChange={(e) => setDrafts((d) => ({ ...d, [r.role]: { ...d[r.role], email: e.target.value } }))}
          />
          <button onClick={() => save(r.role)} disabled={status[r.role] === "saving"}>
            {status[r.role] === "saved" ? "✓ saved" : status[r.role] === "error" ? "error" : "save"}
          </button>
        </div>
      ))}
      {recipients.length === 0 && <div className="empty">loading recipients…</div>}
    </div>
  );
}
