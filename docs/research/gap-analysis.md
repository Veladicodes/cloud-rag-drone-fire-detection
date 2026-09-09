# Research Gap Analysis

This document consolidates the literature-derived research gaps for the project. Following the 5 / 5 / 5 split of the [literature survey](literature-survey.md) (15 papers total), each researcher presents their **own** analysis of their five assigned papers:

- **R1** — papers 1–5 (edge detection)
- **R2** — papers 6–10 (cloud, networking, human alerting)
- **R3** — papers 11–15 (RAG grounding and integration)

The three readings are deliberately different in method and emphasis, reflecting three researchers approaching three different problem angles.

---

## 1. Shared Project Scope

This project implements a cloud-based Retrieval-Augmented Drone framework: a fleet of UAVs with edge object-detection modules (YOLOv8/v9) patrols forest boundaries; telemetry and incident alerts reach a FastAPI service on Microsoft Azure; a RAG pipeline turns a confirmed detection into a grounded natural-language response plan; and — added in this remediation pass — a dedicated alert service delivers notifications to people outside the system. Each researcher's gap analysis below is scoped to the part of that pipeline they own.

---

## 2. R1 — Papers 1–5 · Edge detection and the model we have to build

*Analysis by Researcher 1 (AI & Computer Vision). Read through one question: "what do these results force us to assume about the on-board detector?"*

Our five assigned papers (1–5) are strong on detection metrics and silent on almost everything after the bounding box.

- **Paper 1 (Zhao & Martinez, 2023)** gives us our headline feasibility numbers — mAP@0.5 ≈ 89% and 32 FPS for smoke on a Jetson-class board with TensorRT FP16. We read this as an existence proof for the CV-1 / CV-2 gates, not a result we can copy: it uses a custom dataset with no canopy-occlusion breakdown, so we cannot assume that accuracy transfers to FLAME / FireNet conditions.
- **Paper 5 (Kim & Nguyen, 2024)** is the one that settles an architecture choice for us: segmentation produces cleaner smoke boundaries but is too slow for an early-alert loop, so a single-stage detector is the right call — but we inherit its unsolved problem of separating diffuse smoke from fog and canopy reflection, which is why our augmentation plan leans on synthetic transparency masks.
- **Paper 4 (Thompson & Silva, 2023)** and **Paper 3 (Al-Mansoori & Kumar, 2022)** sit at the edges of our remit. Paper 4 tells us the drone will be moving along a plume perimeter with wind drift, so our training data must include motion blur and oblique viewing angles. Paper 3 tells us the edge/cloud split is sound but was validated only on scalar sensor data, never on image frames — so the bandwidth-reduction claim (CL-1) is something *we* have to re-establish for a vision workload.
- **Paper 2 (Chen et al., 2024)** is a RAG paper, and from a computer-vision standpoint its lesson is narrow but important: everything downstream of us consumes structured fields (coordinates, confidence, class), so the detector's output contract matters as much as its accuracy.

**Gap R1 identifies:** none of these papers carry a detection result *through* to an automated action. Our contribution at the edge is not a new architecture — it is producing a detector whose output is shaped, calibrated, and fast enough to be the trigger for a response pipeline.

**How the project closes it:** fine-tune a lightweight YOLOv8/v9 on FLAME + FireNet with occlusion- and fog-oriented augmentation; fix a strict output schema (lat, lon, class, confidence, snapshot reference); and measure mAP / FPS on simulated edge hardware against gates CV-1 and CV-2 before the detector is ever wired to the incident endpoint.

---

## 3. R2 — Papers 6–10 · The infrastructure and alerting layer that isn't there

*Analysis by Researcher 2 (Cloud & Database). Method: for each paper, name the missing piece of cloud / network / notification infrastructure that my part of the project has to supply.*

| Paper | What it demonstrates | Infrastructure gap R2 must fill |
| :--- | :--- | :--- |
| 6 · Diaz-Vilor et al., 2025 — RL swarm tracking | A swarm keeps a resilient cell-free link to ground APs while tracking a fire front. | Connectivity is optimised with no backend behind it — no ingestion endpoint, no store, nothing that turns a tracked front into a logged incident. R2 supplies the FastAPI ingestion service and Azure SQL persistence the link can talk to. |
| 7 · Tzoumas et al., 2024 — DSPFC suppression swarm | 30-UAV coordinated monitoring / suppression via nearest-neighbour comms. | Coordination is peer-to-peer only: no cloud aggregation, no human in the loop. R2 supplies the central aggregator so a ground commander sees one fused picture. |
| 8 · Conceptual UAV-swarm response system, 2025 | A systems-engineering blueprint with a human-centred interface layer. | Blueprint only — no implemented interfaces, no message contracts. R2 turns the "interface layer" into concrete REST / WebSocket contracts and a recipient model. |
| 9 · De Rango et al., 2025 — CO2 sensor EWS | Learned anomaly detection (LSTM) beats a fixed threshold — earlier, and on more sensors. | The system stops at "sensor activated": no path from an activation to a cloud incident record or an outbound alert. R2 builds that path and generalises it from CO2 sensors to drone detections. |
| 10 · Mowbray et al., 2024 — mobile alerting review | Speed, reliability *and wording* decide whether the public acts on an alert. | Names the requirement, implements nothing. R2 turns it into a component: `AlertService` with two message classes, defined recipient roles, and a latency gate (AL-1, ≤ 15 s detection → SMS). |

**Gap R2 identifies:** the swarm and sensor literature ends at detection or at peer coordination; the alerting literature ends at recommendations. Nobody joins "a model fired" to "a specific person's phone buzzed," with a durable record in between.

**How the project closes it:** a hybrid edge-cloud ingestion service (WebSocket telemetry + REST incident events) writing to Azure SQL and Blob-equivalent storage, plus a dedicated `Public / Responder Alert Service` that fires an immediate raw SMS *in parallel with* the RAG call and an enriched push *after* it — measured against the new AL-1 validation gate.

---

## 4. R3 — Papers 11–15 · Grounding and the missing planning layer

*Analysis by Researcher 3 (Cognitive Systems & UI). Emphasis: where does a detection or a document stop, and what integration seam is left unbuilt?*

Read together, papers 11–15 describe two halves of a bridge nobody has finished building.

On one side, **Paper 13 (Vazquez et al., 2026)** and **Paper 14 (Titu et al., 2024)** are careful edge-detection studies — transfer-learning gains, architecture trade-offs, energy-delay budgets — and both explicitly treat "what happens with the detection" as downstream work for someone else. **Paper 15 (Soliman & Haque, 2024)** does the same from a wireless-sensor-network angle, adding transmission security but still stopping at the base station. Three papers, three dead ends at exactly the point our project begins.

On the other side, **Paper 12 (Béchard & Marquez Ayala, 2024)** is our closest methodological ancestor: RAG grounding measurably cuts hallucination in *schema-constrained* output and lets a smaller model do the job. But it is validated on enterprise workflows, never on safety-critical checklists where a wrong-but-well-formed step has real consequences — so the central claim behind RQ3 is, for our domain, still untested. **Paper 11 (Rey et al., 2024)** shows a working geo-targeted notification architecture (named recipient roles, push delivery) but it is triggered by humans reporting incidents, not by an automated pipeline.

**Gap R3 identifies:** the detection papers have no planning layer, the grounding paper has no safety-critical evaluation, and the notification paper has no automated trigger. The integration seam — detection → grounded plan → delivered notification — is the unbuilt piece.

**How the project closes it:** a LangChain + FAISS pipeline that takes the detector's structured output plus live weather, retrieves regional SOP chunks, and generates a checklist under a strict `INSUFFICIENT_CONTEXT` fallback; an evaluation of that pipeline against zero-shot prompting on a wildfire-specific test set (RQ3 / gate CG-2); and a React dashboard plus alert feed that makes the generated plan and the dispatched notifications visible in one place.

---

## 5. Consolidated gap statement

Across all fifteen papers the recurring absence is the same: **detection is never carried through to a grounded, delivered response.** Vision papers stop at the bounding box; swarm papers stop at coordination; sensor papers stop at the base station; RAG papers stop at generic outputs; alerting papers stop at recommendations. This project's contribution is the connective pipeline — edge detection → cloud ingestion → RAG-grounded plan → human alert — evaluated end to end against the CV / CL / CG / AL validation gates.

---

## 6. Proposed Solution Summary

The unified, hybrid edge-cloud framework addresses the consolidated gap in three moves:

1. **Direct Detection-to-Response Integration** — YOLOv8/v9 detection events bind directly to a LangChain execution chain; a verified classification instantly triggers the response-planning cycle, reducing response latency from hours to seconds.
2. **Context-Grounded RAG Pipeline** — a FAISS vector database indexes regional wildland-fire SOPs; the query engine incorporates coordinates, local wind velocity, temperature, and fuel levels to retrieve target SOP paragraphs, restricting the LLM to verified emergency procedures.
3. **Hybrid Edge-Cloud Architecture with a Human-Alert Layer** — image classification runs on drone edge hardware (Jetson Orin), transmitting only low-overhead event metadata to the Azure FastAPI server; a dedicated alert service then delivers SMS/push notifications to named recipient roles, in parallel with (not gated behind) the RAG call.
