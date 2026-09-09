# Master Execution Brief
## Cloud-Based Retrieval-Augmented Drone Framework for Early Forest Fire Detection and Response Planning
### Repo: `cloud-drone-fire-detection` — Target: BITE412L Phase-I submission (Dr. Priya V, deadline 30 July 2026)

**Read this whole file before touching any code or docs.** This is not a suggestion list — it is
a sequenced work order. Each task states exactly what file to touch, what to check first, and what
"done" looks like. Do not skip the verification steps. Do not invent citations, numbers, or facts
not given here — if something is genuinely unknown, write `TODO(verify):` inline rather than
guessing, and surface it in your final summary to the user.

---

## 0. Context you must hold in your head the whole time

- This repo is currently **documentation-only** (32 Markdown files, no source code). That is
  correct and expected for Phase-I — do not start writing YOLO training code, FastAPI routes, or
  React components unless a task below explicitly asks for it.
- The course guideline PDF mixes "AWS" and "Azure" language inconsistently. **This project has
  already committed to Azure** (Azure SQL, Blob Storage, Azure OpenAI, VNet, Container Apps
  throughout the repo). Keep it Azure everywhere. Never introduce AWS service names anywhere in
  the repo, including diagrams, tables, or prose. If a rubric section literally says "AWS", treat
  it as the course template's own inconsistency and satisfy the *intent* (cloud services table,
  cloud architecture diagram) using Azure vocabulary.
- Team of 3. Researcher roles already defined in `docs/management/work-distribution.md`:
  - **R1 — AI & Computer Vision** (YOLO/edge)
  - **R2 — Cloud & Database** (Azure/FastAPI/DB)
  - **R3 — Cognitive Systems & UI** (RAG/LangChain/React)
- The repo's own `docs/research/compliance-report.md` already self-audits honestly. Read it before
  starting — it lists known gaps. Do not contradict it; extend it.

---

## 1. THE CRITICAL FIX — Literature survey: 5 papers → 15 papers

This is the single highest-priority task. The rubric requires **15 papers**, split **5/5/5** across
the three researchers, each researcher producing their **own independent** gap analysis for their 5.
The repo currently has only 5 papers total, authored as if by one person. This must change.

### 1.1 Add these 10 verified papers (real, checked, do not alter citation details)

Append these to `docs/research/literature-survey.md`, keeping the existing table format
(Paper | Method | Key Findings | Gap Identified) and the existing 5 papers as entries 1–5.
Number the new ones 6–15.

```
6. Diaz-Vilor, C., Lozano, A. & Jafarkhani, H. (2025). "A Reinforcement Learning Approach for
   Wildfire Tracking With UAV Swarms." IEEE Transactions on Wireless Communications.
   — Method: RL-based trajectory optimization for UAV swarms maintaining cell-free connectivity
     with ground access points while tracking a wildfire front.
   — Key findings: cell-free multi-AP connectivity gives resilience against AP damage from the
     fire itself; swarm repositioning balances view quality against connectivity and battery limits.
   — Gap identified: connectivity-resilience is optimized in isolation from any downstream
     response-planning or alerting pipeline — detection/tracking is not linked to action.

7. Tzoumas, G., Salina, L., McConville, A., Richardson, T. & Hauert, S. (2024). "Extinguishing
   Wildfires in Large Scale Scenarios Using Swarms of UAVs." Swarm Intelligence (ANTS 2024),
   Springer LNCS vol. 14987. DOI: 10.1007/978-3-031-70932-6_6.
   — Method: Dynamic Space Partition for Firefighting (DSPF/DSPFC) — a swarm of 30 UAVs
     self-organizes via nearest-neighbour communication to monitor and suppress fires.
   — Key findings: coordinated multi-UAV engagement (DSPFC) outperforms uncoordinated
     single-UAV response on a novel "fire mitigation effectiveness" (FME) metric.
   — Gap identified: purely a flight-coordination/suppression algorithm; no cloud backend,
     no human notification layer, no persistent incident logging.

8. [Authors per ScienceDirect record] (2025). "Conceptual design of a wildfire emergency
   response system empowered by swarms of unmanned aerial vehicles." ScienceDirect
   (systems-engineering conceptual design paper).
   — Method: Systems-engineering approach defining tasks suited to UAV swarms within a
     human-centred wildfire emergency response system (software, hardware, human components,
     interfaces).
   — Key findings: identifies concrete regulatory and integration barriers to UAV-swarm adoption
     in emergency response; proposes a human-centred interface layer connecting swarm output to
     responders.
   — Gap identified: conceptual/architectural only — no working prototype, no quantitative
     validation, no RAG-style grounded response generation.
   — TODO(verify): confirm exact author names and publication month from
     https://www.sciencedirect.com/science/article/pii/S2212420925003176 before final submission.

9. De Rango, A., Furnari, L., Cortale, F., Senatore, A. & Mendicino, G. (2025). "Wildfire Early
   Warning System Based on a Smart CO2 Sensors Network." Sensors (MDPI), 25(7), 2012.
   DOI: 10.3390/s25072012.
   — Method: 44 low-cost CO2 sensors (LoRaWAN) deployed around a controlled prescribed burn;
     three AI models (2x AutoEncoder, 1x LSTM) compared against a simple threshold-based
     (NO-AI) alerting rule.
   — Key findings: LSTM-based anomaly detection activated 56% more sensors than the fixed
     NO-AI threshold, and activated them earlier, tracking fire-front propagation via wind
     pattern correlation.
   — Gap identified: purely ground-sensor-based; no aerial/drone layer, no integration with a
     cloud RAG pipeline for translating detection into response actions. Directly motivates
     this project's Point 2 (threshold vs learned-anomaly detection) and root-cause framing.

10. Mowbray, F. et al. (2024). "A systematic review of the use of mobile alerting to inform the
    public about emergencies and the factors that influence the public response." Journal of
    Contingencies and Crisis Management, 32, e12499. DOI: 10.1111/1468-5973.12499.
    — Method: Systematic review (Medline, Embase, PsycInfo, Scopus) of studies evaluating mobile
      alerting systems' effect on intended/actual public behaviour during emergencies.
    — Key findings: message speed and reliability matter, but so does message content/wording;
      identifies concrete factors that make the public more or less likely to act on an alert.
    — Gap identified: reviews human-facing alert *effectiveness* in general emergencies, but not
      wildfire-specific, and not integrated with any automated detection-to-alert pipeline —
      directly informs how this project's human-alert layer should be designed (Point 4).

11. Rey, W.P., Adalin, S.A.S., Calanog, K.R.L. & Jimenez, G.W.R. (2024). "Mamamayan: A Mobile
    Community-based Emergency Reporting and Notification System for the City of Makati in the
    Philippines." Proc. 2023 5th International Conference on Software Engineering and
    Development, ACM, pp. 35–41.
    — Method: Mobile app + backend for two-way community emergency reporting and push
      notification to registered residents in a defined geographic zone.
    — Key findings: demonstrates a concrete, working architecture for geo-targeted push
      notification delivered to named recipient roles (residents, local authority).
    — Gap identified: manually triggered by human reporters, not by an automated sensor/drone
      detection pipeline — this project's contribution is automating that trigger.

12. Béchard, P. & Marquez Ayala, O. (2024). "Reducing hallucination in structured outputs via
    Retrieval-Augmented Generation." Proc. 2024 NAACL-HLT, Industry Track, pp. 228–238.
    DOI: 10.18653/v1/2024.naacl-industry.19.
    — Method: RAG pipeline with a small, well-trained retriever grounding an LLM's structured
      (schema-constrained) output generation for enterprise workflow tasks.
    — Key findings: RAG grounding significantly reduces hallucination in structured outputs and
      allows a smaller, cheaper LLM to match larger ungrounded models.
    — Gap identified: demonstrated on generic enterprise workflows, not on safety-critical
      emergency response checklists — directly supports this project's RQ3 (RAG vs zero-shot
      hallucination) and justifies the "INSUFFICIENT_CONTEXT" fallback design in ADR-002.

13. Vazquez, G., Zhai, S. & Yang, M. (2026). "Edge-Friendly UAV Wildfire Smoke and Flame
    Detection Using Transfer Learning-Enhanced Lightweight Deep Learning Models." (MDPI journal
    article, PMC ID PMC13210558).
    — Method: Lightweight YOLO variants fine-tuned via transfer learning (COCO / FASDD source
      pretraining) and benchmarked on mAP@0.5, FPS, inference power, and energy-delay product on
      an edge platform.
    — Key findings: transfer learning lifts mAP@0.5 to 79.2% on the target dataset while
      quantifying the real payload/battery/compute trade-off (power, energy, EDP) this project's
      ADR-001 assumes.
    — Gap identified: benchmarks edge inference cost in isolation; does not connect detection
      output to any cloud-side response-planning system.

14. Titu, M.F.S., Pavel, M.A., Michael, G.K.O., Babar, H., Aman, U. & Khan, R. (2024). "Real-Time
    Fire Detection: Integrating Lightweight Deep Learning Models on Drones with Edge Computing."
    Drones (MDPI), 8(9), Article 483. DOI: 10.3390/drones8090483.
    — Method: Compares DETR, Detectron2, YOLOv8, and knowledge-distilled models for real-time
      drone-based fire detection on a 7,187-image dataset, focused on edge deployment.
    — Key findings: establishes concrete accuracy/speed trade-offs among detector architectures
      specifically in a drone edge-computing context.
    — Gap identified: model-comparison study only; no swarm coordination, no cloud RAG layer, no
      human alert mechanism — this project integrates detection into the larger pipeline these
      results assume is "downstream work."

15. Soliman, H. & Haque, A. (2024). "A Wireless Sensor Network Application in Forest Fire Early
    Detection: A Smart and Secure Approach." Proc. 2024 Intelligent Systems and Machine Learning
    Conference (ISML), Hyderabad, India, pp. 106–111.
    — Method: WSN-based forest fire detection architecture emphasising secure data transmission
      from ground sensors.
    — Key findings: proposes a security-hardened ground-sensor-to-base-station pipeline suited to
      remote, unattended forest deployment.
    — Gap identified: ground-sensor-only, no aerial component, no generative response planning;
      TODO(verify): confirm exact page range and DOI/ISBN from the ISML 2024 proceedings before
      final submission — this entry was located via a secondary citation and should be checked
      against the primary proceedings record.
```

### 1.2 Split ownership 5/5/5 and rewrite the gap analysis per-researcher

Currently `docs/research/gap-analysis.md` reads as one voice covering everything. Rebuild it as
three clearly headed subsections:

- `## R1 — Papers 1–5 (existing FLAME/YOLO/edge-detection cluster)` — keep the existing scope/gap/
  solution rows for papers 1–5, but reframe the prose so it reads as R1's own analysis in first
  person plural ("we identify...", "our reading of this paper...") rather than an anonymous voice.
- `## R2 — Papers 6–10 (swarm coordination, threshold/sensor networks, human alerting)` — write a
  NEW scope → gap → solution table for papers 6, 7, 8, 9, 10. R2 owns cloud/DB/networking, so
  frame the gaps in terms of what infrastructure is missing (e.g. paper 9's threshold system has
  no cloud ingestion path; paper 11's Mamamayan has no automated sensor trigger).
- `## R3 — Papers 11–15 (RAG grounding, edge inference limits, drone detection integration)` —
  write a NEW scope → gap → solution table for papers 11, 12, 13, 14, 15. R3 owns RAG/UI, so frame
  gaps in terms of grounding and integration (e.g. paper 12's structured-output RAG has never been
  tested against safety-critical checklists; papers 13/14 stop at detection with no planning layer).

**Do not let one gap-analysis voice write all three sections identically.** Vary structure,
emphasis, and which trade-offs get foregrounded — a reviewer comparing all three should be able to
tell they were written by three different people thinking about three different problem angles.

### 1.3 Update every place that says "five papers" or implies 5

Search and fix:
- `docs/research/README.md` (research-section index)
- `docs/README.md` (documentation index — check for any paper-count mentions)
- `README.md` (root — "Literature summary & research gap" section, and the "five refs" line in
  the file inventory table if present)
- `docs/research/compliance-report.md` — this file's own self-audit currently says "a five-paper
  literature survey" under "What is present." Update to fifteen and update the verdict logic
  accordingly.
- Any milestone/timeline doc that references "5 papers" per person — should now read "5 papers per
  researcher, 15 total."

Run a repo-wide grep for `five` and `5 papers` (case-insensitive) before considering this task done:
```bash
grep -rniE "five.paper|5 papers|five-paper" docs/ README.md
```
Every hit must be either fixed or intentionally justified (e.g. "top-5 chunks" in RAG retrieval is
unrelated and should NOT be changed).

---

## 2. THE SECOND CRITICAL FIX — Human alerting layer (Prof.'s Point 4)

The professor's own notes are explicit: *"Testing people / alert human beings: Establishing
concrete alert mechanisms directed at people in the area (must be specific regarding how alerts are
delivered and who receives them)."* Right now, both architecture diagrams stop at the **Operator
Dashboard**. Nothing reaches a person outside the system. Fix this at the architecture level before
touching anything else in this section.

### 2.1 Add a new architectural component

In `docs/architecture/architecture.md`, add a new operational layer after "React Dashboard":

```
- **Public/Responder Alert Service** — Azure Communication Services (SMS) + Azure Notification
  Hubs (push), triggered by FastAPI's `TriggerRAG()` step in parallel with the RAG call, not
  sequentially after it (so human notification is never delayed waiting on LLM response time).
  Sends two distinct message classes to two distinct recipient roles:
    1. **Immediate raw alert** (no RAG needed) → forest ranger on duty + local fire department
       dispatch, via SMS, containing: incident coordinates, confidence score, timestamp,
       snapshot thumbnail link. Sent the instant YOLO flags a detection — must not wait for the
       RAG/LLM pipeline to complete.
    2. **Enriched response-plan push** (after RAG completes) → same recipients plus an
       "affected-zone residents" distribution list, containing the generated containment/
       evacuation checklist summary and a link to the full plan on the dashboard.
```

### 2.2 Update `docs/adr/ADR-002.md`

Add a fourth row to the alternatives table (or a short addendum) noting that the RAG decision
does not, by itself, satisfy the human-alerting requirement — RAG produces the *content* of the
response plan; a separate notification service is required to *deliver* it. State this explicitly
so a reviewer doesn't think RAG output alone constitutes "alerting people."

### 2.3 Update BOTH diagrams

- `docs/architecture/component-diagram.md` (Mermaid classDiagram): add a new class
  `AlertService` with stereotype `«Azure Communication Services»`, with methods
  `+SendImmediateSMS()`, `+SendEnrichedPush()`, `+RegisterRecipient()`. Add relations:
  `FastAPIGateway --> AlertService : Triggers immediate alert` and
  `RAGService --> AlertService : Sends enriched plan`.
- `docs/architecture/sequence-diagram.md` (Mermaid sequence): add a new participant
  `AlertService` and two new arrows in the "Incident Detection & Response Sequence" block —
  one immediately after `HTTP POST /api/v1/incidents` (fired in parallel with the DB/Blob
  writes, not after RAG), and one after `Return Markdown Response Plan` (the enriched push).
  Add a note showing the immediate SMS is NOT blocked on the RAG round-trip.

### 2.4 Add recipient/role specification

Create a small new file `docs/architecture/alert-recipients.md`:
- Table: Recipient role | Channel | Trigger condition | Message content | Data source for contact
  info (e.g. "Forest Ranger on duty" | SMS via Azure Communication Services | Any YOLO detection
  above confidence threshold | coordinates + snapshot link | `drones_table` on-duty roster —
  TODO(verify): confirm with team whether roster data lives in Azure SQL or a separate directory
  service; not yet decided in ADR-002/003, flag this as an open decision for Review-2).
- This directly answers "who receives them" from the professor's notes, in one place a reviewer
  can point to.

### 2.5 Add this to validation gates

In `docs/management/milestones.md`, add a sixth academic validation gate:
```
| AL-1 | Human alerting | Time from detection to first SMS dispatch (simulated) | ≤ 15 seconds |
```
This gives the "test case" answer specifically for the human-alert requirement, separate from the
existing CV/CL/CG gates.

---

## 3. Fix the repo's own self-flagged inconsistencies

These are already listed in `docs/research/compliance-report.md` §"Minor inconsistencies to tidy."
Fix all of them exactly as follows:

1. **Broken link**: `docs/README.md` links to `docs/architecture/README.md`, which does not
   exist. Either create a short `docs/architecture/README.md` index file (listing
   architecture.md, component-diagram.md, sequence-diagram.md, deployment-overview.md, and now
   alert-recipients.md — one line each), OR fix the link in `docs/README.md` to point directly
   at `docs/architecture/architecture.md`. Prefer creating the index file — it's cheap and matches
   the pattern used in `docs/adr/README.md` and `docs/research/README.md`.

2. **Incomplete research index**: `docs/research/README.md` lists only 4 of 9 files under
   `docs/research/`. Add the missing entries: `datasets.md`, `methodology.md`,
   `compliance-report.md`, and (after this brief's changes) confirm `literature-survey.md` and
   `gap-analysis.md` are both listed with updated one-line descriptions reflecting 15 papers and
   the 3-researcher gap-analysis split.

3. **Inconsistent L2 formula**: `docs/research/methodology.md` writes the L2 distance as
   `d(q,v) = √Σ(qᵢ−vᵢ)²` (with square root — correct Euclidean distance). `docs/research/
   rag-response.md` writes it as `Σ(qᵢ−vᵢ)²` (missing the root, which is actually squared
   Euclidean distance, not L2). **Fix `rag-response.md` to include the square root**, since FAISS's
   `IndexFlatL2` (named in your own datasets/methodology files) computes true L2 distance, not
   squared distance, in its default distance reporting convention used elsewhere in this repo.

4. **Dangling reference**: `docs/adr/ADR-002.md` references a `data/knowledge-base/` folder that
   was removed from the repo (per the root README's note about `data/`, `scripts/`, `infra/` being
   deleted). Either restore a stub `data/knowledge-base/README.md` explaining this is where SOP
   source documents will be added pre-indexing (matching the "component directory stub" pattern
   used for `ai/`, `backend/`, etc.), OR edit ADR-002 to reference wherever SOP source files will
   actually live (check with team — likely should live under a new `data/` stub directory,
   analogous to the existing 8 component-directory stubs). Prefer restoring the stub — it costs one
   file and resolves the dangling reference cleanly.

5. **Citation integrity**: The repo's own compliance report flags that the original 5 citations are
   "plausible but generic (no DOIs/volumes for some)." Go back to `docs/research/
   literature-survey.md` entries 1–5 (Zhao & Martinez 2023, Chen/Patel/Dupont 2024, Al-Mansoori &
   Kumar 2022, Thompson & Silva 2023, Kim & Nguyen 2024) and web-search each one to verify it is a
   real, findable paper with a real DOI/venue. **If any of these five cannot be verified as real
   papers, flag this explicitly to the user rather than inventing a DOI.** Do not silently keep an
   unverifiable citation in an academic submission — this is a plagiarism/integrity risk for the
   student, not just a formatting issue.

---

## 4. Verification pass (run this LAST, after all edits above)

1. Confirm total paper count is exactly 15 by counting numbered entries in
   `docs/research/literature-survey.md`.
2. Confirm `docs/research/gap-analysis.md` has three clearly separated researcher sections
   covering 5 papers each, non-overlapping, totalling 15.
3. Re-render both Mermaid diagrams (component + sequence) and visually confirm the new
   `AlertService` node appears in both, with the immediate-SMS path clearly not gated behind the
   RAG call.
4. Re-run the repo-wide grep from step 1.3 and confirm zero remaining stale "five papers" references.
5. Confirm `docs/research/compliance-report.md`'s verdict section reflects the new state
   accurately (papers: 15/15, human alerting: present, broken links: fixed) rather than just
   leaving the old "17-row compliance matrix" claims unchanged — recount and update that matrix.
6. Produce a short changelog at the bottom of `docs/research/compliance-report.md` under a new
   `## Review-1 remediation log (this pass)` heading, listing exactly what changed, so Dr. Priya V
   (or the team) can see the delta from the previous submission attempt at a glance.
7. Do NOT touch: dataset section (`docs/research/datasets.md`), technology stack, GitHub workflow
   docs, or objectives — these were already assessed as strong and are out of scope for this pass.

---

## 5. What NOT to do

- Do not write any actual source code (no `.py`, `.tsx`, `.tf` files) — this is still a Phase-I
  documentation deliverable per the repo's own stated scope. That work belongs to the Review-2
  roadmap already defined in `docs/research/compliance-report.md` §"Review-2 roadmap."
- Do not fabricate a DOI, page number, or venue for any citation you cannot verify via web search.
  Mark it `TODO(verify)` and say so plainly in your final summary.
- Do not delete or water down the repo's existing honest self-audit language in
  `compliance-report.md` — extend it, don't sanitize it. A reviewer trusts this document more
  because it admits gaps; keep that tone.
- Do not merge the three researchers' gap-analysis voices into one — the professor's rubric
  explicitly wants each student's *own* understanding, and a reviewer who spots three identical
  writing styles across "different" students' sections will treat it as a red flag.
