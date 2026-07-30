# Architecture Decision Records (ADRs)

This directory hosts the Architecture Decision Records (ADRs) for the Cloud-Based Retrieval-Augmented Drone Framework. These records document key architectural design and technology choices, detailing the context, alternatives considered, and research-based justifications for each decision.

---

## ADR Index

All decisions are detailed in the following documents:

### [ADR-001: Object Detection Model Framework](ADR-001.md)
- **Scope**: Choosing the neural network architecture for early smoke and fire detection from drone aerial imagery.
- **Decision**: YOLOv8/v9 over standard Convolutional Neural Networks (CNNs) and Vision Transformers (ViTs).

### [ADR-002: Emergency Response Cognitive Engine (RAG)](ADR-002.md)
- **Scope**: Determining how the framework synthesizes standard operating procedures (SOPs) and tactical advice.
- **Decision**: Retrieval-Augmented Generation (RAG) using FAISS and LangChain over Large Language Model (LLM) fine-tuning.

### [ADR-003: Data Ingestion and Telemetry Processing Infrastructure](ADR-003.md)
- **Scope**: Selecting the cloud topology for processing drone telemetry streams and image frames.
- **Decision**: Hybrid edge-cloud ingestion topology over pure edge or pure cloud architectures.
