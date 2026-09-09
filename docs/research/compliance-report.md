# Review-1 Compliance Report

This report maps every university faculty requirement to the corresponding file in this repository to audit completeness before the formal Review-1 evaluation gate. It is deliberately honest about what is still open — a green row means the *planning artifact* exists, not that the system is built.

---

## 1. Compliance Matrix

| Evaluation Requirement | Status | Target File Pathway | Auditor Comments / Section Reference |
| :--- | :---: | :--- | :--- |
| **Meaningful Repository Name** | **Compliant** | `cloud-drone-fire-detection` | Lowercase, hyphen-separated, descriptive project name. |
| **Professional README** | **Compliant** | [README.md](file:///d:/cloud-drone-fire-detection/README.md) | Standard academic format, structured headings. |
| **Project Title** | **Compliant** | [README.md](file:///d:/cloud-drone-fire-detection/README.md#L1) | Section 1: Project Title. |
| **Team Members** | **Compliant** | [README.md](file:///d:/cloud-drone-fire-detection/README.md) | Section: Project Structure / Work Distribution (3 researchers). |
| **Problem Statement** | **Compliant** | [README.md](file:///d:/cloud-drone-fire-detection/README.md) | Section 4: Problem Statement. |
| **Objectives** | **Compliant** | [docs/research/objectives.md](file:///d:/cloud-drone-fire-detection/docs/research/objectives.md) | Formally defined primary and specific objectives. |
| **Proposed Framework** | **Compliant** | [README.md](file:///d:/cloud-drone-fire-detection/README.md) | Section 10: Proposed Framework. |
| **Proposed Architecture** | **Compliant** | [docs/architecture/architecture.md](file:///d:/cloud-drone-fire-detection/docs/architecture/architecture.md) | High-Level Architecture, component interactions, incl. the Public/Responder Alert Service layer. |
| **Technology Stack** | **Compliant** | [README.md](file:///d:/cloud-drone-fire-detection/README.md) | Section 12: Technology Stack. |
| **Dataset Details** | **Compliant** | [docs/research/datasets.md](file:///d:/cloud-drone-fire-detection/docs/research/datasets.md) | Analyzes FLAME & FireNet (sources, splits, limitations). |
| **Literature Survey (15 papers, 5 / 5 / 5)** | **Compliant** | [docs/research/literature-survey.md](file:///d:/cloud-drone-fire-detection/docs/research/literature-survey.md) | Fifteen entries, split 5 / 5 / 5 across the three researchers. The five original (unverifiable) citations for papers 1–5 have been **replaced with real, DOI-verified publications** on the same topics (authors + DOIs confirmed); the R1 gap analysis was updated to match. Papers 8 and 15 closed in Phase 3 (paper 15 replaced with the same authors' indexed FICC 2025 paper). **All 15 citations are DOI-verified.** |
| **Research Gap (per researcher)** | **Compliant** | [docs/research/gap-analysis.md](file:///d:/cloud-drone-fire-detection/docs/research/gap-analysis.md) | Three independent per-researcher analyses (R1 papers 1–5, R2 papers 6–10, R3 papers 11–15) in distinct voices, plus a consolidated gap statement and solution summary. |
| **Human Alerting Mechanism** | **Compliant** | [docs/architecture/alert-recipients.md](file:///d:/cloud-drone-fire-detection/docs/architecture/alert-recipients.md) | Recipient / channel / trigger / content matrix; immediate SMS dispatched in parallel with (not after) RAG; validation gate AL-1 (≤ 15 s). Reflected in both architecture diagrams and ADR-002 addendum. |
| **Folder Structure** | **Compliant** | [README.md](file:///d:/cloud-drone-fire-detection/README.md) | Section: Repository Structure (now includes `data/knowledge-base/` stub). |
| **Work Distribution** | **Compliant** | [docs/management/work-distribution.md](file:///d:/cloud-drone-fire-detection/docs/management/work-distribution.md) | Responsibilities, deliverables, dated milestones for each researcher. |
| **Architecture Diagram** | **Compliant** | [docs/architecture/component-diagram.md](file:///d:/cloud-drone-fire-detection/docs/architecture/component-diagram.md), [sequence-diagram.md](file:///d:/cloud-drone-fire-detection/docs/architecture/sequence-diagram.md) | Mermaid component + sequence diagrams; both re-rendered after adding the `AlertService` node and the non-gated immediate-alert path. |
| **Validation Gates** | **Compliant** | [docs/management/milestones.md](file:///d:/cloud-drone-fire-detection/docs/management/milestones.md) | Six academic validation gates: CV-1, CV-2, CL-1, CG-1, CG-2, AL-1, each with a numeric target. |
| **Placeholder README files** | **Compliant** | Everywhere | All 8 component directories plus `data/knowledge-base/` contain a README with purpose / future contents / owner / deliverables. |
| **Clean Organization** | **Compliant** | Root | No source code, mock scripts, or empty folders. `data/knowledge-base/` was intentionally restored as a documentation stub to resolve a dangling ADR-002 reference; it contains a README, not code. |
| **Internal Consistency** | **Compliant** | Cross-repo | `docs/architecture/README.md` index created (was a broken link); `docs/research/README.md` now indexes all 9 research docs; L2 distance formula reconciled between `methodology.md` and `rag-response.md`. |

**Total requirements audited: 20** (was 17; +Human Alerting Mechanism, +Validation Gates, +Internal Consistency).

---

## 2. Final Auditing Verdict

### **Is this repository ready for Review-1 submission?**
**YES.**

### **Reasons for Verdict**:
1. All 20 audited faculty evaluation requirements are mapped to markdown documentation within the repository.
2. The repository is a **planning deliverable**: it contains no source code, mock scripts, or empty folders. `data/`, `scripts/`, and `infra/` code folders were previously removed; `data/knowledge-base/` has since been restored as a **documentation stub only** (a README describing where SOP source files will live), resolving a dangling reference in ADR-002.
3. Every component directory contains a README explaining its purpose, future contents, owner, and expected deliverables.
4. Theoretical decisions are supported by Architecture Decision Records (ADR-001 to ADR-003), with ADR-002 extended by an addendum clarifying that RAG generates plan *content* while a separate service *delivers* alerts.
5. The professor's Review-1 concerns are addressed: the literature survey is now 15 papers split 5 / 5 / 5 with three independent gap analyses, and a concrete human-alerting layer (recipients, channels, triggers, latency gate AL-1) has been added to the architecture, diagrams, and ADRs.

### **Citation integrity (resolved):**
- The five original citations for papers 1–5 (Zhao & Martinez 2023; Chen/Patel/Dupont 2024; Al-Mansoori & Kumar 2022; Thompson & Silva 2023; Kim & Nguyen 2024) returned no matching record on an exact-title web search and were judged fabricated. No DOI was ever invented for them. They have been **replaced with real, DOI-verified publications** on the same five topics (multiscale YOLOv8 drone detection; multi-agent RAG for hazard planning; IoT edge computing for environmental monitoring; real-time UAV-fleet wildfire monitoring; DeepSmoke detection+segmentation), and the R1 gap analysis in `gap-analysis.md` was rewritten to reference the new papers. All five replacements have confirmed authors and resolving DOIs.

---

## 3. Recommended Improvements for Review-2
Upon successful Review-1 panel approval, the team should proceed with these actions:
1. *(Closed in Phase 3.)* Papers 8 and 15 citation `TODO(verify)` markers resolved — see the Phase-3 Completion Log below.
2. **Model Fine-Tuning**: Execute dataset download and augmentations on local compute nodes using YOLOv8 scripts.
3. **FastAPI Framework Ingestion Code**: Draft the backend ingestion controller classes, set up SQLAlchemy models, and establish connection pools.
4. **FAISS Local Mocking**: Chunk sample SOP documents into raw texts and write script modules to check query-embedding matching distances.
5. **Alert Service Prototype**: Implement a mocked SMS/notification dispatcher and measure detection → first-dispatch latency against gate AL-1.

---

## 4. Review-1 Remediation Log (this pass)

Changes applied in the remediation pass driven by `CLAUDE_CODE_MASTER_BRIEF.md`, so the delta from the previous submission attempt is visible at a glance.

### Section 1 — Literature survey 5 → 15 papers
- `literature-survey.md`: added papers 6–15 (verified list) with Method / Findings / Gap rows in the existing per-paper structure; intro rewritten to state the 5 / 5 / 5 split; `TODO(verify)` kept on papers 8 and 15; **citation-integrity warning added for papers 1–5**.
- `gap-analysis.md`: rebuilt as three independent per-researcher analyses (R1 papers 1–5, R2 papers 6–10, R3 papers 11–15) in deliberately distinct voices/structures, plus a consolidated gap statement and solution summary.
- Cleared stale "five publications" wording in `docs/README.md`, `docs/research/README.md`, this file's matrix row, and `project-timeline.md`; appended references 6–15 to the root README.

### Section 2 — Human alerting layer
- `architecture.md`: new **Public/Responder Alert Service** operational layer (Azure Communication Services SMS + Notification Hubs); immediate raw alert in parallel with RAG, enriched push after RAG; high-level diagram and interaction list updated.
- `ADR-002.md`: addendum — RAG produces plan *content*; a separate service *delivers* alerts; CG-2 vs AL-1 distinction.
- `component-diagram.md`: new `AlertService` class `«Azure Communication Services»` (`SendImmediateSMS` / `SendEnrichedPush` / `RegisterRecipient`); relations from `FastAPIGateway` (immediate) and `RAGService` (enriched).
- `sequence-diagram.md`: new `Alert` participant; `par` block showing the immediate SMS dispatched in parallel with DB/Blob/RAG, plus a note that it is not gated on the RAG round-trip; enriched send after the plan returns.
- `alert-recipients.md`: **new** — recipient/channel/trigger/content matrix answering "how delivered / who receives"; `TODO(verify)` on roster storage.
- `milestones.md`: new validation gate **AL-1** (detection → first SMS ≤ 15 s).

### Section 3 — Self-flagged inconsistencies
- Created `docs/architecture/README.md` index (fixes the broken link from `docs/README.md`).
- `docs/research/README.md` now indexes all nine research documents (added objectives, research-questions, methodology, datasets, this report).
- `rag-response.md`: L2 distance formula corrected to `√Σ(qₖ−vₖ)²`, matching `methodology.md`.
- Restored `data/knowledge-base/README.md` as a stub, resolving the dangling ADR-002 reference; added the folder to the root README structure.
- **Citations 1–5 web-verified → none found** (fabricated). No DOI invented. Subsequently **replaced with real, DOI-verified publications** (confirmed authors + DOIs) on the same five topics; per-paper Method/Findings/Gap rewritten, R1 gap analysis updated, README references updated, integrity warning downgraded to a resolved note.

### Section 4 — Verification pass
- Paper count confirmed = 15 (entries numbered 1–15).
- `gap-analysis.md` confirmed to have three non-overlapping researcher sections covering 5 papers each (15 total).
- Both Mermaid diagrams re-rendered (mermaid-cli): parse-clean; `AlertService` present in both; immediate-alert path confirmed not gated behind the RAG call.
- Repo-wide grep for stale "five papers" references: clear (only the intentional "five assigned papers per researcher" phrasing remains).
- This compliance matrix and verdict recounted and updated (17 → 20 requirements; human alerting = present; internal-consistency issues = fixed).

### Not touched (out of scope for this pass)
- `datasets.md`, technology stack, GitHub-workflow docs, `objectives.md` — previously assessed as strong.

---

## 5. Review-2 Progress Log (working prototype)

A local, runnable prototype was added on top of the (now remediated) documentation.
**Nothing here uses a real Azure service** — every cloud component is a clearly
labelled local stand-in (`cloud/README_LOCAL_MODE.md`). Runbook: `RUN_LOCALLY.md`.

### Implemented (real code, runs locally)
- **Backend** (`backend/`): FastAPI app — `WS /ws/telemetry`, `POST /api/v1/incidents`, `GET /api/v1/plans/{id}`, `GET /api/v1/incidents`, `GET /api/v1/alerts`, `/health`. SQLAlchemy 2.x models (`drones`, `telemetry`, `incidents`, `response_plans`, `alerts`) on SQLite, portable types only.
- **Blob stand-in** (`cloud/storage_local.py`): `save_blob` / `get_blob` with the same signatures a thin `azure-storage-blob` wrapper would have.
- **RAG pipeline** (`ai/rag/`): recursive 500/50 char chunker → embeddings (`sentence-transformers/all-mpnet-base-v2`, 768-dim; deterministic hash fallback for offline CI) → FAISS `IndexFlatL2` → top-k=3 retrieval reporting true L2 distance → LangChain-style bounded prompt with the `INSUFFICIENT_CONTEXT` fallback.
- **Alert service** (`backend/services/alert_service.py`): mocked SMS/push — logs `[MOCK SMS to <role>]` to console + `logs/alerts.log` + an `alerts` row. `send_immediate_alert` is invoked in `POST /api/v1/incidents` **before** the RAG call starts (AL-1 / ADR-002 addendum).
- **Edge detection** (`ai/models/yolo_detector.py`): pretrained COCO `yolov8n` as a **structural placeholder** (explicitly *not* wildfire-fine-tuned), with a dependency-free STUB detector fallback. Output contract: bbox / cls / confidence.
- **Dashboard** (`frontend/`): React + Vite — live telemetry map (Leaflet), alert feed, RAG response-plan viewer. Functional, not styled.
- **Simulator** (`testing/simulate_drone.py`): streams telemetry for N virtual drones and POSTs detections, so the whole pipeline demos with no hardware or dataset.
- **Tests** (`testing/unit/`): detector contract, RAG retrieval structure, WebSocket telemetry persistence, Blob-stand-in round-trip, and an end-to-end route test asserting an `alerts` row **and** a `response_plans` row are created with immediate-before-enriched ordering. **9 passing.**
- **Migrations**: real Alembic setup (`alembic.ini`, `database/migrations/env.py` wired to `Base.metadata` + `DATABASE_URL`, initial autogenerated revision); `alembic upgrade head` builds all five tables. `init_db()`/`create_all` remains the one-step path for the quick demo.
- **Sample frames** (`testing/sample_images/`): 4 clearly-labelled synthetic placeholder JPEGs (+ `generate.py`) so `run_yolo_eval` yields a real CPU throughput number (mAP stays `PENDING`) and the simulator can feed real files.
- **`Makefile`**: `setup / index / seed / migrate / backend / sim / test / frontend-build` targets mirroring `RUN_LOCALLY.md`.

### Mocked / placeholder (and why)
- **LLM** = `[MOCK LLM OUTPUT]` deterministic text (no API key / no Azure OpenAI). `LLM_MODE=local` tries a small `flan-t5` model; never returns unlabelled mock text.
- **YOLO weights** = COCO, not FLAME/FireNet-tuned (dataset not downloaded).
- **SMS/push** = log + DB row only (no Azure Communication Services account).
- **DB / Blob / host** = SQLite / local folder / bare processes (no Azure).

### Still pending real resources
Real mAP/FPS on FLAME (CV-1/CV-2), measured bandwidth delta (CL-1), retrieval-recall
set (CG-1), hallucination scoring with a real LLM (CG-2), and AL-1 against a real
SMS provider. Tracked in `results/README.md`.
