# Work Distribution

This document details the responsibilities, deliverables, ownership, and expected outcomes for each researcher.

---

## Researcher 1: AI & Computer Vision Specialist

### Responsibilities
- Evaluating, configuring, and training deep learning models (YOLOv8/v9) on aerial datasets.
- Preprocessing and augmenting the FLAME and FireNet image datasets.
- Quantizing trained models to TensorRT format to run on simulated edge devices.

### Deliverables
- Preprocessed training/validation datasets with synthetic canopy smoke augmentations.
- Custom YOLO training scripts, parameter settings, and loss output charts.
- Exported TensorRT engine files and edge inference latency metrics reports.

### Milestones & Dates
- **Milestone CV-1 (Week 4)**: Finalize dataset preprocessing and formatting.
- **Milestone CV-2 (Week 7)**: Complete initial YOLOv8/v9 baseline model training.
- **Milestone CV-3 (Week 10)**: Quantize models to TensorRT and record FPS performance metrics.

### Expected Outcome
A lightweight, high-performance object detection model that achieves $\ge 88\%$ mAP and runs at $\ge 30$ FPS on simulated edge hardware.

---

## Researcher 2: Cloud & Database Architect

### Responsibilities
- Designing the relational database schemas in Azure SQL and file layouts in Blob Storage.
- Designing the FastAPI ingestion service to handle telemetry streams.
- Setting up the Azure network topology (Virtual Network, Subnets, Private Endpoints, Key Vault).

### Deliverables
- Relational schema diagrams, table indexes, and database migration scripts.
- FastAPI backend routes configuration and WebSocket server implementation designs.
- Infrastructure-as-Code (IaC) configuration templates for Azure resource provisioning.

### Milestones & Dates
- **Milestone CL-1 (Week 4)**: Finalize relational database schemas and endpoint specifications.
- **Milestone CL-2 (Week 7)**: Design backend routes and WebSocket ingestion systems.
- **Milestone CL-3 (Week 10)**: Define Azure VNet routing rules and security parameters.

### Expected Outcome
A secure, scalable ingestion framework capable of handling parallel telemetry updates and images with minimal latency.

---

## Researcher 3: Cognitive Systems & UI Specialist

### Responsibilities
- Designing the RAG pipeline using LangChain and the FAISS vector database.
- Formatting Standard Operating Procedures (SOPs) into vector search segments.
- Designing the prompt templates and evaluating output consistency.
- Modeling the React dashboard pages, map widgets, and plan presentation layouts.

### Deliverables
- Chunked and vectorized SOP guides stored in a FAISS index format.
- LangChain prompt configurations and evaluation reports detailing model response accuracy.
- Layout wireframes for the web dashboard displaying drone locations, active alerts, and checklists.

### Milestones & Dates
- **Milestone CG-1 (Week 4)**: Ingest, chunk, and index SOP documents into the vector database.
- **Milestone CG-2 (Week 7)**: Complete LangChain prompt engineering and RAG pipeline configurations.
- **Milestone CG-3 (Week 10)**: Design React dashboard wireframes and WebSocket UI sync modules.

### Expected Outcome
A grounded response planning system that generates accurate checklists from incident variables while preventing hallucinations.
