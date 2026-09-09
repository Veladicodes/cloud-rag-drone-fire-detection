# Master Completion Brief — Phase 3 (Real Data, Real LLM, Real Azure)
## Cloud-Based Retrieval-Augmented Drone Framework for Early Forest Fire Detection and Response Planning
### Repo: `cloud-drone-fire-detection`

**Context:** Phase 1 (docs, 15 papers, human-alert architecture) and Phase 2 (working local
prototype — FastAPI, SQLite, FAISS RAG, mocked LLM, mocked alerts, React dashboard, 9/9 tests
passing) are both complete and verified — see the prior session's work log and
`docs/research/compliance-report.md` §5 Review-2 Progress Log. This brief closes the three
remaining `PENDING` items from that log: real dataset + real YOLO training, real LLM generation,
and real Azure deployment. It also closes the two outstanding citation `TODO(verify)` markers
(papers 8 and 15).

**This is a human-in-the-loop brief.** Several steps require the student to create accounts,
accept licenses, or provide credentials that Claude Code cannot obtain on its own. Wherever that's
true, the section says so explicitly and tells the student exactly what to go get, before handing
back to Claude Code to wire it in. Do not attempt to bypass an account-creation step by fabricating
data or mocking something this brief says should now be real — that defeats the entire purpose of
this pass.

Work order: §1 (dataset) → §2 (real YOLO training + eval) → §3 (real LLM) → §4 (citation
TODOs) → §5 (Azure deployment) → §6 (final honest verification + report update). Commit after
each section, same discipline as before.

---

## 1. Get the real datasets — STUDENT ACTION REQUIRED FIRST

Claude Code cannot download these itself — both require a free account and manual acceptance of
terms on an external platform (IEEE DataPort has no public API for bulk download without login,
and GitHub Releases work fine for FireNet but the student should still verify the license).

### 1.1 FLAME dataset (primary — this is what the project's own docs already cite)

- Go to **IEEE DataPort**: https://ieee-dataport.org/open-access/flame-dataset-aerial-imagery-pile-burn-detection-using-drones-uavs
- Create a free IEEE account if you don't have one (no payment required — FLAME is open access).
- Download the dataset. Citation for your records: Shamsoshoara, A., Afghah, F., Razi, A., Zheng,
  L., Fulé, P. & Blasch, E. (2020). "The FLAME dataset: Aerial Imagery Pile burn detection using
  drones (UAVs)." IEEE DataPort. DOI: 10.21227/qad6-r683.
- The dataset has multiple sub-items (raw video, thermal, frame-level Fire/No-Fire classification
  sets, segmentation masks). For this project's YOLO detector, you specifically need the
  **frame-level Fire/No-Fire classification image sets** (matches what `docs/research/
  datasets.md` already documents: 47,992 frames, 33,594/7,199/7,199 split). Reference
  implementation for structure: https://github.com/AlirezaShamsoshoara/Fire-Detection-UAV-Aerial-Image-Classification-Segmentation-UnmannedAerialVehicle
- Extract into `data/flame/` in the repo, matching the folder structure `run_yolo_eval.py` already
  expects (check the script's existing path constants — it was written in Phase 2 anticipating
  this exact drop-in).

### 1.2 FireNet dataset (secondary — smoke-specific, smaller, no account needed)

- Direct download, no login required: https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/fire-dataset.zip
- This is a 502-image annotated set (412 train / 90 val) from the FireNet project (DeepQuest AI /
  Olafenwa Moses). It's a smaller, secondary set — use it as documented in
  `docs/research/datasets.md` (12,380 frames figure in that doc referred to a differently-sized
  FireNet-family set; if the actual downloaded set is 502 images, **update datasets.md to the real
  number** rather than leaving a stale figure — see §6 honesty check below).
- Extract into `data/firenet/`.

### 1.3 Once both are downloaded, hand back to Claude Code

Tell Claude Code: "FLAME is in `data/flame/`, FireNet is in `data/firenet/`, proceed to §2 of
this brief." Claude Code should NOT proceed past this point until it has confirmed real image
files exist at both paths (not just empty directories) — check file counts and print them before
continuing, so a false-positive "done" doesn't get committed.

---

## 2. Real YOLO fine-tuning and evaluation

Now that real data exists, replace the Phase-2 placeholder (pretrained COCO `yolov8n.pt` used
purely for output-shape testing) with an actually fine-tuned detector.

1. Write `ai/models/train_yolo.py`:
   - Loads `yolov8n.pt` as the base (matches ADR-001's chosen architecture).
   - Fine-tunes on the FLAME frame classification set (Fire / No-Fire) reformatted as a detection
     task — if FLAME's frame-level set is classification-only (whole-image label, no bounding
     boxes), you must either (a) use the segmentation-derived bounding boxes from FLAME's
     segmentation-mask subset if downloaded, or (b) clearly document that this pass trains a
     classifier-style single-box-per-image detector as an approximation, and flag this honestly in
     `results/README.md` rather than silently treating classification labels as if they were real
     bounding-box ground truth.
   - Respects the existing 70/15/15 split already documented (chronological by flight, to prevent
     frame leakage — this was already decided in Phase 1 and must not be silently changed).
   - Saves the fine-tuned weights to `ai/models/weights/wildfire_yolov8n.pt` (do not overwrite the
     original placeholder — keep both, and make `yolo_detector.py`'s config (`YOLO_MODE` in
     `backend/core/config.py`) switchable between `placeholder` and `finetuned`).
2. Run `ai/evaluation/run_yolo_eval.py` against the real held-out test split. This should now
   produce real mAP@0.5, mAP@0.5:0.95, and FPS numbers — no more `PENDING`.
3. Write the real numbers into `results/yolo-metrics/` and update `results/README.md`'s
   measured/pending table: move "real mAP/FPS" from PENDING to MEASURED, with the actual value and
   the exact command used to produce it (so the professor or a teammate can reproduce it).
4. Compare the real numbers against the CV-1/CV-2 validation gates already defined in
   `docs/management/milestones.md` (mAP@0.5 ≥ 88.0%, FPS ≥ 30) and state plainly in
   `results/README.md` whether the gates were met, partially met, or missed — **do not round up or
   soften a miss**. A documented miss with honest analysis of why (e.g. "47,992 frames but only
   dry-conifer bias per the dataset's own documented limitation" — this limitation is already
   written into `docs/research/datasets.md` from Phase 1) is worth more academically than an
   inflated number.
5. Update `ADR-001.md` with a short "Outcome" addendum noting the real measured result versus the
   original target, since ADRs in good engineering practice get revisited once a decision's
   real-world outcome is known.

---

## 3. Real LLM generation — STUDENT ACTION REQUIRED FIRST, then wire in

### 3.1 Get a free Gemini API key (student action)

- Go to **Google AI Studio**: https://aistudio.google.com/apikey
- Sign in with any Google account (free, no payment method required for the free tier).
- Click "Get API key" → "Create API key." Copy it.
- The free tier (as of the free-tier terms in effect at the time of this brief) gives generous
  rate-limited access to Gemini's Flash-tier models with no billing setup — more than sufficient
  for demo-scale RAG generation. Confirm current limits at
  https://ai.google.dev/gemini-api/docs/rate-limits since free-tier terms can change; do not
  assume the numbers in this brief are still exact by the time you read it.
- Put the key in your local `.env` file (NEVER commit it): `GEMINI_API_KEY=your-key-here`.
  Confirm `.env` is in `.gitignore` (Phase 2 already added this — verify it's still there before
  proceeding).

### 3.2 Wire it into the RAG orchestrator (Claude Code, after student provides the key)

1. In `ai/rag/orchestrate.py`, add a new `LLM_MODE=gemini` branch alongside the existing `mock`
   and `local` modes (do not delete the mock mode — keep it as a no-key fallback for anyone
   cloning the repo without a key, and for CI/offline testing).
2. Use the `google-generativeai` Python package (add to `ai/requirements.txt`). Call a Flash-tier
   model (check current model names at the AI Studio docs at implementation time — model names
   like `gemini-1.5-flash` / `gemini-2.0-flash` change over time, so read the current
   `google-generativeai` quickstart rather than hardcoding a name from this brief that may be
   stale).
3. Keep the exact same bounded-prompt structure already built in Phase 2 (incident variables +
   retrieved SOP chunks + `INSUFFICIENT_CONTEXT` fallback instruction) — do not loosen the prompt
   constraints just because a real model is now answering.
4. Update `backend/core/config.py`'s `LLM_MODE` default — keep it `mock` by default in
   `.env.example` (so a fresh clone still works with zero setup) but document the `gemini` option
   clearly with a comment showing exactly what env vars are needed.
5. Run the existing end-to-end integration test (`testing/unit/test_end_to_end.py` or equivalent
   from Phase 2) with `LLM_MODE=gemini` and confirm it still passes — the test's assertions about
   ordering (immediate alert before enriched) and data shape should not need to change, only the
   content of the generated plan will differ (real prose instead of `[MOCK LLM OUTPUT]`).
6. Update RQ3's evaluation: score the real Gemini output's hallucination rate using the BERTScore
   method already specified in `docs/research/methodology.md`, against the small human-expert
   reference set mentioned there. If no human-expert reference set exists yet, create a minimal
   one (3-5 hand-written "ideal" response plans for the sample SOP incidents already in the repo)
   rather than skipping the evaluation — this is the CG-2 validation gate and it's one of the
   project's three core research questions; it should not stay unmeasured if a real LLM is now
   available.
7. Update `results/README.md`: move real hallucination/grounding scores from PENDING to MEASURED.

---

## 4. Close the two citation TODO(verify) markers

- **Paper 8** ("Conceptual design of a wildfire emergency response system empowered by swarms of
  unmanned aerial vehicles," ScienceDirect): fetch
  https://www.sciencedirect.com/science/article/pii/S2212420925003176 and confirm the exact author
  names, publication month, and journal name. Update `literature-survey.md` entry 8 with the
  confirmed details and remove the TODO marker.
- **Paper 15** (Soliman & Haque, "A Wireless Sensor Network Application in Forest Fire Early
  Detection," ISML 2024): search the ISML 2024 proceedings (IEEE Xplore or the conference's own
  site) for the exact DOI and page range. If it cannot be found in a primary proceedings index
  after a genuine search, **do not leave a fabricated-looking specific page range** — either find
  a real replacement paper on the same theme (ground sensor network wildfire detection, 2023-2026,
  peer-reviewed) the same way the five fabricated citations were replaced in the completion pass,
  or clearly mark it as a preprint/non-indexed source if that's what it actually is.

---

## 5. Real Azure deployment — STUDENT ACTION REQUIRED FIRST, then wire in

### 5.1 Get Azure access (student action)

- Apply for **Azure for Students**: https://azure.microsoft.com/free/students — no credit card
  required, verified via your university email. Confirm current credit amount/terms at signup
  since these change.
- Once approved, note your subscription ID — you'll need it for the CLI steps below.

### 5.2 Deploy the already-designed architecture (Claude Code, after student confirms Azure access)

The deployment topology was already fully designed in Phase 1 — `docs/architecture/
deployment-overview.md` specifies the VNet zoning (frontend/backend/database subnets), Container
Apps for hosting, Azure SQL Serverless, Blob Storage with Hot→Cool lifecycle, Key Vault, and
Managed Identity. This section is about actually provisioning it, not redesigning it.

1. Write Infrastructure-as-Code under `cloud/terraform/` (or Bicep, if the student/team prefers —
   check `docs/adr/` for whether an IaC tool was already decided; if not, Terraform is reasonable
   given it's already referenced in the component-directory stub for `cloud/`) implementing:
   - Resource group
   - VNet with the three subnets from `deployment-overview.md`
   - Azure SQL Database (Serverless tier, auto-pause) — replace SQLite
   - Storage Account with Blob container (Hot tier, lifecycle rule → Cool after 30 days) — replace
     the local filesystem stand-in
   - Container Apps environment + one Container App for the FastAPI backend
   - Static Web App or a second Container App for the React frontend build
   - Key Vault for secrets (the Gemini API key, DB connection string)
   - System-assigned Managed Identity wired to Key Vault access, per the existing ADR
2. Update `cloud/storage_local.py`'s real counterpart: create `cloud/storage_azure.py`
   implementing the exact same `save_blob`/`get_blob` function signatures using
   `azure-storage-blob`, so `backend/services/pipeline.py` can switch implementations via a single
   config flag (`STORAGE_MODE=local` vs `STORAGE_MODE=azure`) without touching call sites — this
   was explicitly the point of building the local stand-in with matching signatures in Phase 2.
3. Update `backend/core/db.py`/`config.py` so `DATABASE_URL` can point at the provisioned Azure SQL
   connection string (via Key Vault reference or an env var during initial setup) instead of
   SQLite. Run Alembic migrations against the real Azure SQL instance and confirm all 5 tables +
   `alembic_version` are created (same check Phase 2 already did against SQLite).
4. Deploy the FastAPI backend and React frontend to their respective Container Apps / Static Web
   App. Confirm the deployed backend's `/health` endpoint responds, and that the deployed frontend
   can reach it (CORS config from Phase 2 will need the real deployed frontend origin added).
5. Update `cloud/README_LOCAL_MODE.md` — it currently maps local→Azure as a future intention; once
   deployed, add actual resource names/endpoints (not secrets) so the mapping is concrete, not
   hypothetical.

### 5.3 What to leave mocked even after real Azure exists

- **Azure Communication Services (SMS)**: setting up a real SMS-sending phone number typically
  requires additional identity verification and, in some regions, ongoing per-message cost beyond
  free trial credit. Unless the student explicitly wants to pursue this, it is reasonable to keep
  `alert_service.py`'s mock (console + log file + DB row) even in the "real Azure" deployment,
  clearly documented as the one remaining mocked component and why. This is an honest, defensible
  scope boundary for a student project — do not treat leaving this mocked as a failure.

---

## 6. Final honest verification pass

1. Re-run the full test suite against whichever configuration is now active (local SQLite or real
   Azure SQL, mock or real LLM) and record which configuration was tested.
2. Rewrite `results/README.md`'s measured/pending table one final time. By the end of this brief,
   it should show: real YOLO mAP/FPS (measured, gate met/missed stated honestly), real RAG
   hallucination/grounding score (measured), real Azure deployment (measured — backend/frontend
   actually reachable), and only genuinely irreducible items still PENDING (e.g. real SMS delivery
   if the team chose to keep that mocked per §5.3).
3. Add a final `## Phase-3 Completion Log` section to `docs/research/compliance-report.md`
   summarizing exactly what changed in this pass, in the same honest, specific style as the
   existing Review-1 Remediation Log and Review-2 Progress Log sections — do not write vague
   "everything is now complete" language; state exactly what's real, what's still a documented
   scope boundary, and why.
4. Update the root `README.md` one final time to reflect the fully realized system.
5. Confirm `datasets.md`'s stated frame counts match the actually-downloaded dataset sizes (see
   §1.2 note about FireNet's real 502-image count vs. the earlier documented 12,380 figure) — fix
   any mismatch rather than leaving stale numbers next to real results, since inconsistent numbers
   across a report are exactly the kind of thing a careful reviewer catches.

---

## What NOT to do

- Do not proceed with §2, §3, or §5's "wire in" steps before the student has actually completed
  the corresponding account/credential step. Ask and wait if it's unclear whether the dataset is
  downloaded or the API key exists.
- Do not fabricate a mAP, FPS, or hallucination score under any circumstance, even "as a
  placeholder to fill in later" — Phase 2 already established the discipline of PENDING over
  invented numbers; this phase is precisely where those PENDING items get replaced with truth, not
  with better-looking fiction.
- Do not silently change the previously-documented 70/15/15 chronological split, the RAG chunk
  size/overlap (500/50), or the FAISS index type — these were deliberate Phase-1 decisions with
  written justification in the ADRs; if real data forces a genuine change, update the relevant ADR
  with a dated addendum explaining why, rather than quietly diverging from what's documented.
- Do not treat "Azure is deployed" as license to delete the local-mode code paths — keep both
  configurations working (local for quick demos/offline dev, Azure for the real deployment demo),
  exactly as the `STORAGE_MODE`/`LLM_MODE`/`YOLO_MODE` config-flag pattern from Phase 2 already
  supports.
