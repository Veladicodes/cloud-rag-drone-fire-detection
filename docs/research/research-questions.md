# Research Questions

This document outlines the three primary Research Questions (RQs) that define the scientific focus of this project. Each question maps to a key architectural component: Edge Detection, Cloud-Native Ingestion, and RAG Planning.

---

## Research Question 1 (RQ1) - Edge Detection & Optimization
> *"How can lightweight single-stage deep learning models (YOLOv8/v9) be optimized to classify amorphous smoke columns under canopy obstruction while operating within the compute constraints of onboard drone hardware?"*

### Focus Areas
- **Feature Extraction**: Investigating backbone networks (CSPDarknet vs. GELAN) to capture fine-grained, diffuse smoke edges.
- **Quantization Optimization**: Quantizing model weights to FP16 and INT8 formats using TensorRT and measuring the impact on classification accuracy and inference latency ($FPS$).
- **Canopy Occlusion**: Evaluating classification robustness when smoke columns are partially obscured by tree branches.

---

## Research Question 2 (RQ2) - Hybrid Ingestion Resilience
> *"To what extent does a hybrid edge-cloud ingestion topology reduce network bandwidth requirements and improve data transmission resilience compared to continuous raw video transmission during aerial monitoring operations?"*

### Focus Areas
- **Bandwidth Optimization**: Measuring data transmission savings by sending low-overhead metadata alerts instead of continuous video streams.
- **Fail-Safe Synchronization**: Evaluating edge buffer queue algorithms and measuring data loss rates during simulated communication drops.
- **WebSocket Throughput**: Benchmarking telemetry delivery times to the dashboard under multi-UAV parallel streaming conditions.

---

## Research Question 3 (RQ3) - Grounded response Planning (RAG)
> *"In what ways does Retrieval-Augmented Generation (RAG) using FAISS index constraints eliminate hallucinated actions in AI-generated response plans compared to zero-shot LLM prompts?"*

### Focus Areas
- **Retrieval Precision**: Testing vector similarity matching using L2 distance and Cosine similarity formulas against a database of wildfire SOPs.
- **Hallucination Mitigation**: Measuring LLM prompt adherence when instructed to return fallback codes under low-context scenarios.
- **Synthesized Checklist Quality**: Evaluating the completeness of response checklists (evacuation boundaries, resource allocation) using semantic comparison metrics (BERTScore).
