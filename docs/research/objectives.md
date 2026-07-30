# Project Objectives

This document defines the primary and specific objectives of the project, alongside expected research contributions and academic deliverables.

---

## 1. Primary Objective
To design and model a scalable, cloud-native framework that automates early forest fire detection and response planning by linking edge-based drone classification (YOLO) with cloud-hosted vector search engines (RAG).

---

## 2. Specific Objectives
1. **Model** a lightweight object detection model (YOLOv8/v9) optimized in PyTorch to detect smoke columns and flames from aerial imagery.
2. **Design** a hybrid ingestion service using FastAPI to manage WebSocket telemetry updates and store metadata in Azure SQL.
3. **Build** a RAG pipeline using LangChain and a FAISS index to retrieve SOP paragraphs based on environmental variables.
4. **Draft** a deployment architecture on Microsoft Azure using virtualized container compute and private endpoints.
5. **Structure** an interactive React-based dashboard mockup for emergency response visualization.

---

## 3. Expected Research Contributions
- **Direct Ingestion-Response Integration**: Connecting visual deep learning outputs directly to automated natural language response generation.
- **Context-Grounded Checklists**: Grounding emergency checklists in regulatory SOPs using coordinates and local weather factors.
- **Resilient Edge-Cloud Partitioning**: Defining a task split between drone edge hardware and cloud search engines to minimize bandwidth and preserve drone battery life.

---

## 4. Academic Deliverables
1. **Architecture Specifications**: Technical specifications detailing API contracts, database schemas, and VNet subnets.
2. **Evaluation Metrics Plan**: Benchmarks for measuring model accuracy (mAP), edge frame rates (FPS), and vector database matching quality.
3. **Mockup Dashboard Layouts**: Visual dashboard page outlines displaying drone locations, active alerts, and generated checklists.
4. **Research Briefs**: Literature surveys, gap analysis, and ADRs establishing the project's scientific validity.
