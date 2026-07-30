# Research Methodology

This document outlines the core scientific methodology, data workflows, system partition logic, and experimental metrics designed for the Cloud-Based Retrieval-Augmented Drone Framework.

---

## 1. Scientific Research Design
The study adopts an empirical, quantitative research design to evaluate the performance of a hybrid edge-cloud collaborative framework for wildland hazard monitoring and response support. The research is structured around three variables:
- **Independent Variables**: Input image resolution ($640 \times 640$), deep learning architecture configuration (YOLOv8 vs. YOLOv9), network packet-loss rate, and vector database chunking size.
- **Dependent Variables**: Bounding box localization precision ($mAP$), edge inference rate ($FPS$), raw data bandwidth compression factor, context retrieval recall ($k$-NN accuracy), and LLM response generation consistency (hallucination index).
- **Controlled Variables**: Simulated UAV flight path trajectory, weather context profile, and the baseline emergency Standard Operating Procedures (SOP) corpus.

---

## 2. Conceptual System Workflow
The overall workflow follows a closed-loop monitoring and planning paradigm:

```
[ UAV Video Feed ] ──> [ Edge YOLO Classifier ]
                            │
                            ▼ (If Fire Flag == True)
[ Asynchronous Message Queue ] ──> [ FastAPI Gateway ]
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
     [ Azure Storage Layer ]                              [ LangChain Query Builder ]
     - Structured logs (Azure SQL)                                 │
     - Imagery snapshots (Blob)                                    ▼
                                                          [ Vector Matching Engine ]
                                                          - FAISS similarity query
                                                          - Context chunk extraction
                                                                   │
                                                                   ▼
                                                          [ LLM Prompt Synthesis ]
                                                          - Bounded GPT-4o execution
                                                                   │
                                                                   ▼
                                                          [ Actionable SOP Checklist ]
```

---

## 3. Data Flow Architecture
The data flow is segmented into two telemetry channels to isolate control commands from media payloads:
1. **Low-Latency Telemetry Channel (WebSockets)**: Continuous flight metrics (GPS coordinates, altitude, battery percentage, bearing) are transmitted as lightweight JSON strings at 2 Hz directly to the cloud server, which caches them in memory and streams them to the monitoring dashboard.
2. **Event-Driven Detection Channel (REST HTTP)**: When a fire is detected, a multi-part payload (containing the boundary image slice, location tag, and confidence metric) is sent to a high-priority endpoint. This triggers Azure Blob Storage archiving and RAG query construction.

---

## 4. Edge vs. Cloud Processing Split

### Edge Processing (Onboard UAV)
- **Task Allocation**: Real-time image capture, tensor resizing ($640 \times 640 \times 3$), YOLO inference execution, and local log buffering.
- **Justification**: Eliminates transmission delay for immediate anomaly detection and prevents critical failures during network dropouts by buffering alerts locally.

### Cloud Processing (Azure Resource Boundary)
- **Task Allocation**: Relational database persistence, raw media archiving, FAISS vector search, and Large Language Model prompt synthesis.
- **Justification**: Offloads intensive vector search indexing and multi-billion parameter LLM inference from weight-constrained drone battery packs to virtualized compute resources.

---

## 5. RAG Workflow & Context Grounding
The RAG pipeline constraints the generative language model to prevent hallucinated instructions during safety-critical events:
1. **Ingestion**: Standard forestry SOPs are split using recursive character chunking (500-character blocks, 50-character overlap) and stored as high-dimensional vectors.
2. **Matching**: The query vector, containing local wind velocity and coordinates, is compared against the FAISS index using Euclidean distance measurements:

$$d(\vec{q}, \vec{v}) = \sqrt{\sum_{i=1}^{n} (q_i - v_i)^2}$$

3. **Prompt Bounding**: The extracted context blocks are passed to the LLM with system directives stating: *"If the provided context does not contain sufficient details to address the incident variables, return the code 'INSUFFICIENT_CONTEXT' and do not extrapolate."*

---

## 6. Experimental Verification & Evaluation Methodology
The framework will be validated using three experimental setups:
- **Object Detection Benchmarking**: Evaluating model precision and recalls on validation sets containing fire and smoke columns under varying lighting parameters.
- **Network Resilience Benchmarking**: Simulating communication dropouts and measuring packet-loss rates, synchronization lag, and local edge buffer capacity.
- **Response Plan Accuracy Benchmarking**: Scoring the generated checklists using semantic similarity comparison models (BERTScore) against a human-expert validated test set of responses.
