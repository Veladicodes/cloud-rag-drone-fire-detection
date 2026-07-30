# Project Milestones & Validation Gates

This document defines the key milestones and academic validation gates used to evaluate project progress.

---

## 1. Milestones Overview

```
Week 1-3          Week 4-5          Week 6-7          Week 8-9          Week 10-11         Week 12
 ┌───┐             ┌───┐             ┌───┐             ┌───┐             ┌───┐              ┌───┐
 │M1 │ ──────────> │M2 │ ──────────> │M3 │ ──────────> │M4 │ ──────────> │M5 │ ───────────> │M6 │
 └───┘             └───┘             └───┘             └───┘             └───┘              └───┘
Literature       Dataset          Architecture      App Ingestion      System             Review-1
Survey           Study            Design            Plans             Testing            Audit
```

- **M1: Literature & Scope Definition (Week 1-3)**: Compile the literature survey, define research gaps, and establish project objectives.
- **M2: Data Acquisition & Preprocessing (Week 4-5)**: Source FLAME and FireNet datasets, partition images, and draft pre-processing methodologies.
- **M3: Architecture & Security Planning (Week 6-7)**: Author ADRs and draft VNet subnets and UML sequence diagrams.
- **M4: Application Ingestion Plans (Week 8-9)**: Draft FastAPI routing endpoints and RAG LangChain prompt schemas.
- **M5: System Testing Design (Week 10-11)**: Outline experimental setups for model precision, network latency, and response consistency.
- **M6: Review-1 Audit & Packaging (Week 12)**: Perform compliance audits, prepare presentation materials, and package the repository.

---

## 2. Academic Validation Gates

| Phase | Evaluation Criteria | Academic Validation Gate | Target Quality Metric |
| :--- | :--- | :--- | :--- |
| **Edge Detection** | Bounding box spatial accuracy | Validation Gate CV-1 | $mAP@0.5 \ge 88.0\%$ on validation set |
| **Edge Speed** | Onboard processing rate | Validation Gate CV-2 | $FPS \ge 30$ on TensorRT simulated hardware |
| **Ingestion** | Ingest telemetry overhead | Validation Gate CL-1 | Bandwidth utilization reduced by $\ge 70\%$ |
| **RAG Precision** | Context retrieval recall | Validation Gate CG-1 | $k$-NN context retrieval recall $\ge 90\%$ |
| **RAG Safety** | Checklist hallucination rate | Validation Gate CG-2 | Hallucination rate $\le 1.0\%$ under test prompts |
