# Research Documentation Index

This directory contains research planning documentation, literature surveys, architecture decision records, and system frameworks designed to support academic validation and marking rubrics.

---

## Directory Index

### 1. Architecture Decision Records (ADRs)
- [ADR Index & Introduction](adr/README.md): Overview of major design decisions.
  - [ADR-001: Object Detection Model Framework](adr/ADR-001.md): Rationale behind using YOLOv8/v9 over traditional classifiers or ViTs.
  - [ADR-002: Emergency Response Cognitive Engine](adr/ADR-002.md): Decision to use RAG with FAISS and LangChain instead of LLM fine-tuning.
  - [ADR-003: Data Ingestion and Telemetry Ingestion Infrastructure](adr/ADR-003.md): Selection of a hybrid edge-cloud processing topology.

### 2. Core Research Documentation
- [Research Overview](research/README.md): Index of research briefs and methodologies.
- [Literature Survey](research/literature-survey.md): Complete survey of fifteen academic publications (5 per researcher, 15 total) on UAV swarms, YOLO edge detection, sensor-network early warning, human alerting, and RAG architectures.
- [Gap Analysis](research/gap-analysis.md): Logical structure outlining the Current Project Scope $\to$ Identified Research Gaps $\to$ Proposed Solutions.
- [YOLOv8 Detection Brief](research/yolo-detection.md): Analytical breakdown of machine learning loss parameters and edge hardware compatibility.
- [RAG Response Brief](research/rag-response.md): Explanation of text embeddings, FAISS search formulas, and LangChain prompt layouts.

### 3. System Architecture Specification
- [System Architecture](architecture/README.md): Diagram mapping edge telemetry signals to cloud databases and frontend visualization nodes, detailed conceptual data entities, and asynchronous sync loops.
