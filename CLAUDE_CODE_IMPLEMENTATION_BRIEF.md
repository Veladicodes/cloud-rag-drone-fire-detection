# Master Implementation Brief — Phase 2 (Working Prototype)
## Cloud-Based Retrieval-Augmented Drone Framework for Early Forest Fire Detection and Response Planning
### Repo: `cloud-drone-fire-detection`

**Context for whoever (Claude Code) executes this:** Review-1 was a verbal walkthrough only — the
professor asked the student to explain the project, no document audit happened. Nothing is
"locked." This means the Phase-I documentation gaps (literature survey at 5/15 papers, missing
human-alert layer in the architecture) and the Phase-II working-prototype build should both be
done in this pass, in the order below. Read this entire file before writing any code.

No Azure account exists yet. No LLM API key exists. No real dataset is downloaded yet. Everything
must run **locally on plain processes** (no Docker) using free/local substitutes that are
API-compatible or structurally identical to the real Azure services named in the architecture, so
swapping in real Azure later is a config change, not a rewrite.

---

## 0. Ground rules — read before doing anything

1. **Documentation fixes (Section 1 and 2 below) come first**, before any code. A working
   prototype built on top of a report that still says "5 papers" and has no human-alert
   architecture is a wasted effort — fix the paper trail first, then build.
2. **Every Azure service name in code/config must have a real Azure equivalent it will become**,
   documented in a comment at the top of the relevant file. Example: `# LOCAL STAND-IN FOR: Azure
   SQL Database. Swap DATABASE_URL env var to an Azure SQL connection string for production.`
   This is not optional — it's what makes this a legitimate cloud-computing course project rather
   than "a local app that mentions cloud services in the readme."
3. **Never fabricate benchmark numbers.** Every metric that appears in `results/` must come from
   an actual run of actual code on actual (even if small/synthetic) data. If a number can't be
   produced yet (e.g., true mAP on FLAME because the dataset isn't downloaded), write
   `PENDING — requires FLAME dataset download` instead of inventing a plausible-looking number.
4. **Keep committing incrementally** per the existing Git branch workflow
   (`docs/management/` describes `feature/studentN` → `develop` → `main`). Do not do one giant
   commit. Structure commits so `git log` tells an honest story of build order matching this
   brief's section order.
5. Work in this order: §1 (paper trail fix) → §2 (architecture human-alert fix) → §3 (repo
   scaffolding for real code) → §4 (backend + DB) → §5 (YOLO edge simulation) → §6 (RAG pipeline)
   → §7 (alert service, mocked) → §8 (React dashboard) → §9 (integration test + demo script) →
   §10 (update docs to match what was actually built, honestly).

---

## 1. Fix the literature survey: 5 papers → 15 papers

This was already scoped in the prior brief (`CLAUDE_CODE_MASTER_BRIEF.md` if present in the repo
root — check for it and reuse its paper list verbatim if found, to avoid inconsistency). If that
file is not present, use this list (already verified against live sources — do not alter these
citation details):

Add as entries 6–15 in `docs/research/literature-survey.md`, same table format as existing 1–5:

6. Diaz-Vilor, C., Lozano, A. & Jafarkhani, H. (2025). "A Reinforcement Learning Approach for
   Wildfire Tracking With UAV Swarms." IEEE Transactions on Wireless Communications.
7. Tzoumas, G., Salina, L., McConville, A., Richardson, T. & Hauert, S. (2024). "Extinguishing
   Wildfires in Large Scale Scenarios Using Swarms of UAVs." Swarm Intelligence (ANTS 2024),
   Springer LNCS vol. 14987. DOI: 10.1007/978-3-031-70932-6_6.
8. (2025). "Conceptual design of a wildfire emergency response system empowered by swarms of
   unmanned aerial vehicles." ScienceDirect. TODO(verify): confirm exact authors from
   https://www.sciencedirect.com/science/article/pii/S2212420925003176.
9. De Rango, A., Furnari, L., Cortale, F., Senatore, A. & Mendicino, G. (2025). "Wildfire Early
   Warning System Based on a Smart CO2 Sensors Network." Sensors (MDPI), 25(7), 2012.
   DOI: 10.3390/s25072012.
10. Mowbray, F. et al. (2024). "A systematic review of the use of mobile alerting to inform the
    public about emergencies and the factors that influence the public response." Journal of
    Contingencies and Crisis Management, 32, e12499. DOI: 10.1111/1468-5973.12499.
11. Rey, W.P., Adalin, S.A.S., Calanog, K.R.L. & Jimenez, G.W.R. (2024). "Mamamayan: A Mobile
    Community-based Emergency Reporting and Notification System for the City of Makati in the
    Philippines." Proc. 2023 5th ICSED, ACM, pp. 35–41.
12. Béchard, P. & Marquez Ayala, O. (2024). "Reducing hallucination in structured outputs via
    Retrieval-Augmented Generation." Proc. NAACL-HLT 2024, Industry Track, pp. 228–238.
    DOI: 10.18653/v1/2024.naacl-industry.19.
13. Vazquez, G., Zhai, S. & Yang, M. (2026). "Edge-Friendly UAV Wildfire Smoke and Flame Detection
    Using Transfer Learning-Enhanced Lightweight Deep Learning Models." MDPI (PMC13210558).
14. Titu, M.F.S., Pavel, M.A., Michael, G.K.O., Babar, H., Aman, U. & Khan, R. (2024). "Real-Time
    Fire Detection: Integrating Lightweight Deep Learning Models on Drones with Edge Computing."
    Drones (MDPI), 8(9), Art. 483. DOI: 10.3390/drones8090483.
15. Soliman, H. & Haque, A. (2024). "A Wireless Sensor Network Application in Forest Fire Early
    Detection: A Smart and Secure Approach." Proc. 2024 ISML Conf., Hyderabad, pp. 106–111.
    TODO(verify): confirm exact DOI/ISBN from primary proceedings record.

For each, write Method / Key Findings / Gap Identified rows matching the existing table's level of
detail (2-3 sentences each), consistent with each paper's real abstract content — do not invent
numeric results not in the source.

Rewrite `docs/research/gap-analysis.md` as three sections, one per researcher (R1: papers 1–5,
R2: papers 6–10, R3: papers 11–15), each in a distinct voice/emphasis reflecting that researcher's
specialty (R1 = CV/edge, R2 = cloud/networking/alerting, R3 = RAG/UI/integration). See
`CLAUDE_CODE_MASTER_BRIEF.md` §1.2 for the detailed instruction if present; otherwise use your own
judgment but keep the three voices genuinely distinct.

Fix every stale "five papers" / "5 papers" reference repo-wide:
```bash
grep -rniE "five.paper|5 papers|five-paper" docs/ README.md
```

---

## 2. Fix the architecture: add the human-alert layer

The sequence and component diagrams currently stop at "Operator Dashboard" — no mechanism alerts
an actual person outside the system. This must be fixed in the docs AND reflected in the real code
built in §7.

In `docs/architecture/architecture.md`, add:
```
- **Public/Responder Alert Service** — sends two message classes to two recipient roles:
    1. Immediate raw alert (fired in parallel with DB/Blob writes, NOT after RAG completes) →
       forest ranger + fire department dispatch, via SMS-equivalent channel.
    2. Enriched response-plan notification (after RAG completes) → same recipients + affected-zone
       list, containing the generated checklist summary.
```

Update `docs/architecture/component-diagram.md` (add `AlertService` class + relations) and
`docs/architecture/sequence-diagram.md` (add `AlertService` participant + two message arrows, one
NOT gated behind the RAG round-trip). Create `docs/architecture/alert-recipients.md` with a
recipient/channel/trigger/content table. Full detail in `CLAUDE_CODE_MASTER_BRIEF.md` §2 if present.

Also fix the repo's self-flagged inconsistencies (broken `docs/architecture/README.md` link,
incomplete research index, L2-formula mismatch between `methodology.md` and `rag-response.md`,
dangling `data/knowledge-base/` reference in ADR-002). Full detail in
`CLAUDE_CODE_MASTER_BRIEF.md` §3 if present; otherwise use judgment consistent with existing repo
conventions (component-directory README stub pattern, etc.).

---

## 3. Repo scaffolding for real code

Populate the eight existing stub directories with real structure. Do not delete the existing
README.md in each — add real subdirectories/files alongside it.

```
backend/
  main.py                  # FastAPI app entrypoint
  api/
    routes_telemetry.py    # WebSocket telemetry ingestion endpoint
    routes_incidents.py    # POST /api/v1/incidents (detection events)
    routes_plans.py        # GET response plans
  core/
    config.py              # env-driven settings (DATABASE_URL, STORAGE_PATH, LLM_MODE, etc.)
    db.py                  # SQLAlchemy engine/session setup
  requirements.txt

database/
  models.py                # SQLAlchemy models: Drone, Telemetry, Incident, ResponsePlan
  migrations/               # Alembic migration scripts
  seed.py                  # inserts mock drone profiles + a sample incident for demo

cloud/
  README_LOCAL_MODE.md     # explains every "LOCAL STAND-IN FOR: Azure X" mapping in one place
  storage_local.py         # local-filesystem Blob Storage stand-in (save/get by container/key)

ai/
  models/
    yolo_detector.py        # loads pretrained YOLOv8n, runs inference, returns boxes+confidence
  rag/
    ingest.py               # chunks SOP text files, embeds, builds local FAISS index
    retrieve.py              # query embedding + FAISS top-k retrieval
    orchestrate.py           # LangChain prompt compilation + local LLM call
  evaluation/
    run_yolo_eval.py         # scriptable eval against whatever images exist locally

frontend/
  src/
    components/
      TelemetryMap.jsx
      AlertFeed.jsx
      ResponsePlanViewer.jsx
    hooks/
      useTelemetrySocket.js
    services/
      api.js
  package.json

testing/
  simulate_drone.py          # standalone script: pushes fake telemetry + occasionally POSTs a
                              # fake "detection" to backend, so the whole pipeline can be demoed
                              # without a real drone or real dataset
  unit/
    test_yolo_detector.py
    test_rag_retrieve.py
    test_incidents_route.py

results/
  README.md                 # explains what's measured vs PENDING and why
```

Also create at repo root:
```
.env.example        # all config vars needed, with comments explaining local-vs-Azure meaning
requirements.txt    # top-level, or reference backend/requirements.txt + ai/requirements.txt
RUN_LOCALLY.md       # exact copy-pasteable commands to run backend, frontend, and the simulator
```

---

## 4. Backend + database (local stand-in for Azure SQL + Blob)

- Use **SQLite** via SQLAlchemy for local dev (`DATABASE_URL=sqlite:///./local.db` in
  `.env.example`), with models written so the same models work unmodified against Azure SQL later
  (avoid SQLite-only column types).
- Tables per the existing class diagram: `drones`, `telemetry`, `incidents`, `response_plans`.
- Blob Storage stand-in: a `storage/` folder on disk, with `storage_local.py` exposing
  `save_blob(container, key, bytes)` / `get_blob(container, key)` — same function signatures a
  real `azure-storage-blob` wrapper would have, so swapping later means changing the import, not
  the call sites.
- FastAPI routes:
  - `WS /ws/telemetry` — accepts JSON telemetry pings, writes to `telemetry` table, broadcasts to
    connected dashboard clients.
  - `POST /api/v1/incidents` — accepts `{lat, lon, confidence, image_base64}`, saves image via
    `storage_local.save_blob`, writes `incidents` row, immediately calls the mocked alert service
    (§7) with the raw alert (do NOT wait for RAG here), then asynchronously triggers the RAG
    pipeline (§6) and writes its output to `response_plans` when done, then calls the alert
    service again with the enriched notification.
  - `GET /api/v1/plans/{incident_id}` — returns the generated plan once ready.
- Run `database/seed.py` to insert 2–3 mock drones and confirm the schema works before moving on.

---

## 5. YOLO edge-detection simulation

No real FLAME/FireNet data yet, so:
- Use `ultralytics` pip package, load a pretrained `yolov8n.pt` (general COCO weights) as a
  placeholder detector — **do not claim this is fine-tuned for wildfire smoke**; be explicit in
  code comments and in `results/README.md` that this is a structural placeholder until the real
  dataset is downloaded and fine-tuning (per ADR-001, `yolo-detection.md`) is actually run.
- `yolo_detector.py` should still produce the right *shape* of output (bounding boxes + class +
  confidence) so the rest of the pipeline (incident creation, alert triggering, RAG context) can
  be built and tested end-to-end against realistic-looking data now.
- `testing/simulate_drone.py` should feed a handful of sample images (either genuinely free stock
  wildfire-smoke images the student downloads separately, or clearly-labeled synthetic/placeholder
  images generated for testing) through the detector, and POST any detection above a confidence
  threshold to `/api/v1/incidents`.
- Write `run_yolo_eval.py` so that the moment real FLAME/FireNet data is dropped into a
  `data/flame/` folder, running the script produces real mAP/FPS numbers into `results/`. Until
  then, running it against whatever sample images exist should still work and print
  `PENDING — full FLAME/FireNet evaluation` alongside whatever partial numbers it *can* produce.

---

## 6. RAG pipeline (local, no API key required)

- **Embeddings**: use `sentence-transformers` (`all-mpnet-base-v2`, matches what's already
  specified in `docs/research/rag-response.md` — 768-dim) — this runs fully locally, no API key.
- **Vector index**: FAISS `IndexFlatL2`, matching the existing methodology doc. Confirm the L2
  formula fix from §2 is reflected consistently in code comments too.
- **SOP corpus**: since no real regional SOP documents exist yet, create
  `data/knowledge-base/sample_sops/` with 3–5 short, clearly-labeled **illustrative** wildfire
  containment/evacuation SOP text files (general public-domain wildfire safety guidance is fine to
  summarize in your own words — do not copy verbatim from any copyrighted source; write original
  illustrative procedure text based on general, well-known wildfire safety practice). Label the
  folder README clearly: "Sample SOPs for pipeline testing — replace with real regional SOP
  documents before production/Review-2 final demo."
- **LLM**: since no API key exists, use a small local model via `transformers` or `ollama` if
  available in the environment (check what's actually installable given network restrictions —
  `pip install transformers torch` should work from PyPI). If no local generative model can
  reasonably run in this environment, `orchestrate.py` must have a clearly-labeled **mock mode**
  that returns a deterministic, clearly-fake-labeled structured response (e.g. prefixed
  `[MOCK LLM OUTPUT]`) — never silently pretend a mocked response is real generation output. Try
  the real local model path first; fall back to mock mode only if it genuinely can't run, and log
  which mode is active.
- Prompt template should match the structure in `docs/research/rag-response.md` (coordinates,
  wind, temperature, fuel dryness, retrieved SOP chunks, `INSUFFICIENT_CONTEXT` fallback
  instruction).

---

## 7. Alert service (mocked SMS/notification)

- `alert_service.py` (put under `backend/core/` or a new `backend/services/` folder) with two
  functions: `send_immediate_alert(recipient_role, incident)` and
  `send_enriched_plan(recipient_role, incident, plan)`.
- **Mock the actual delivery** — no real Twilio/Azure Communication Services account exists. Each
  function should log a clearly-formatted line (e.g. `[MOCK SMS to forest_ranger_on_duty]: Fire
  detected at (34.05, -118.24), confidence 0.91, ...`) to both console and a `logs/alerts.log`
  file, AND write a row to a new `alerts` table so the dashboard can display "alerts sent" in the
  UI even though no real SMS goes anywhere.
- File header comment: `# LOCAL MOCK FOR: Azure Communication Services (SMS) + Azure Notification
  Hubs (push). Swap send_* function bodies for real Azure SDK calls when credentials exist.`
- Confirm in `POST /api/v1/incidents` that `send_immediate_alert` is called BEFORE the RAG call
  starts (not after), matching the architecture fix in §2 — this is a real requirement from the
  professor's brief (alerts must not wait on LLM latency), not just a nice-to-have.

---

## 8. React dashboard

Minimal but real (not a static mockup):
- `TelemetryMap.jsx` — connects to `WS /ws/telemetry`, shows drone positions on a simple map
  (Leaflet is fine, matches tech stack doc) updating live from the simulator.
- `AlertFeed.jsx` — polls or subscribes to incidents/alerts, shows a live list as they come in
  from `simulate_drone.py` triggering detections.
- `ResponsePlanViewer.jsx` — once a plan is ready for an incident, renders the generated
  checklist markdown.
- Keep styling simple (functional, not polished) — the point of this pass is a working, honest
  demo, not visual design.

---

## 9. Integration test + demo script

Create `RUN_LOCALLY.md` with exact steps:
```
1. cd backend && pip install -r requirements.txt
2. python database/seed.py
3. uvicorn main:app --reload --port 8000
4. cd frontend && npm install && npm start
5. In a third terminal: python testing/simulate_drone.py
```
Running steps 3–5 together should produce a visible, end-to-end demo: simulated drone → detection
→ incident created → immediate mock alert logged → RAG plan generated (or mock-labeled) →
enriched mock alert logged → dashboard shows telemetry, alert feed, and response plan updating
live. This is the artifact the student will actually demo to the professor — it must genuinely
run, not just look like it would run.

Write one integration test (`testing/unit/test_incidents_route.py` or a separate
`test_end_to_end.py`) that spins up the FastAPI app, POSTs a synthetic incident, and asserts an
`alerts` row and a `response_plans` row both get created — this is the automated proof the pipeline
actually works, referenced in `results/`.

---

## 10. Update documentation to match what was actually built (be honest)

- `results/README.md`: state plainly what's measured (e.g. end-to-end latency from POST to first
  mock-SMS log line, RAG retrieval top-k recall on the sample SOP corpus) vs `PENDING` (real YOLO
  mAP on FLAME, real Azure deployment, real SMS delivery).
- Update `docs/research/compliance-report.md` with a new `## Review-2 progress log` section:
  what got implemented, what's mocked and why, what's still pending real Azure/dataset access.
  Keep the repo's existing honest tone — do not overstate what a mocked local prototype
  demonstrates versus a deployed cloud system.
- Update the root `README.md`'s "no implementation code yet" framing (from the original
  Review-1 repository report) — this is no longer true after this pass; correct it plainly.

---

## What NOT to do

- Do not claim any real Azure service was used or tested — everything cloud-named in this pass is
  a local stand-in, clearly labeled as such everywhere.
- Do not fabricate YOLO accuracy numbers before real FLAME/FireNet data is used — use `PENDING`.
- Do not silently return mock LLM output without labeling it `[MOCK LLM OUTPUT]` inline.
- Do not skip the §1/§2 documentation fixes to jump straight to code — the professor's rubric
  concerns from Review-1 are still open and matter as much as the working prototype.
