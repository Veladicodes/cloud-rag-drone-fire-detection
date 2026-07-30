# Research Gap Analysis

This document outlines the core scientific framework of this research project: **Current Project Status** $\to$ **Identified Research Gaps** $\to$ **Proposed Solutions**.

---

## 1. Current Project Scope

This project implements a cloud-based Retrieval-Augmented Drone framework. The design encompasses a fleet of unmanned aerial vehicles (UAVs) equipped with edge object detection modules (YOLOv8/v9) that patrol forest boundaries. Telemetry and incident alerts are transmitted to a central FastAPI service deployed on Microsoft Azure, which triggers a RAG pipeline to generate natural language action guides for fire dispatchers.

---

## 2. Research Gaps

Despite advances in wildfire observation, literature highlights three critical research gaps:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Detection-Response Decoupling                                            │
│    - Current systems flag fires but do not generate instant response plans. │
└───────────────────────┬─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. Context-Blind Recommendations                                            │
│    - Generic LLMs do not account for local weather, canopy, or SOPs.        │
└───────────────────────┬─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. Cloud-Only Latency & Bandwidth Issues                                     │
│    - Video streaming over deep forests is blocked by bandwidth limitations.  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Gap 1: Decoupling of Autonomous Detection and Tactical Response Planning
- *Context*: Existing research focus is heavily biased towards computer vision detection models (pixel accuracy, bounding box speed). Once a fire is detected, human operators must manually reference static, paper-based Standard Operating Procedures (SOPs).
- *Research Gap*: There is a lack of automated, integrated systems that connect the *immediate classification* of a fire directly to a *cognitively generated tactical response plan*.

### Gap 2: Context-Blind AI in Crisis Operations
- *Context*: Using generative AI for disaster response is a growing field. However, standard LLMs are trained on general internet data and lack access to private localized SOPs, wind patterns, or terrain layouts.
- *Research Gap*: Generic LLMs hallucinate response protocols or output unsafe generalities. No current framework integrates local sensor readings (coordinates, wind vectors) directly with vector search libraries (FAISS) to constrain LLM synthesis during wildland fire emergencies.

### Gap 3: Bandwidth Bottlenecks in Pure Cloud Ingestion
- *Context*: High-definition drone video streaming requires substantial, continuous bandwidth. In remote forests, cellular connections are spotty or non-existent.
- *Research Gap*: Pure-cloud frameworks fail due to transmission latency and link drops, while pure-edge frameworks lack the global coordination needed to manage multi-UAV patrol flights. A hybrid edge-cloud ingestion paradigm optimized for RAG operations remains unexplored.

---

## 3. Proposed Solution

This research proposes a unified, hybrid edge-cloud framework structured to address the identified gaps:

1. **Direct Detection-to-Response Integration (Addressing Gap 1)**:
   - The framework binds YOLOv8 detection events directly to a LangChain execution chain. A verified classification instantly triggers the response planning cycle, reducing response latency from hours to seconds.
2. **Context-Grounded RAG Pipeline (Addressing Gap 2)**:
   - A FAISS vector database indexes regional wildland fire SOPs. The query engine incorporates coordinates, local wind velocity, temperature, and fuel levels to retrieve target SOP paragraphs. This context restricts the LLM to verified emergency procedures, eliminating hallucination risks.
3. **Hybrid Edge-Cloud Architecture (Addressing Gap 3)**:
   - Image classification runs locally on drone edge hardware (Jetson Orin), transmitting only low-overhead event metadata (coordinates, confidence, compressed snapshot) to the Azure FastAPI server. This minimizes bandwidth requirements and enables offline edge operation during network blackouts.
