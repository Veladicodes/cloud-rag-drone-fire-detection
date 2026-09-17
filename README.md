# Cloud-Based Retrieval-Augmented Drone Framework for Early Forest Fire Detection and Response Planning

---

## Abstract
This project outlines a cloud-native research framework designed for early-stage forest fire detection and automated tactical response planning. The proposed system integrates autonomous Unmanned Aerial Vehicle (UAV) patrols, edge-cloud collaborative deep learning, and Retrieval-Augmented Generation (RAG). By capturing real-time aerial imagery and applying YOLO-based classification models at the edge, the system flags early fire hazards. The resulting incident metadata is transmitted to a central FastAPI service hosted on Microsoft Azure. This service initiates a cognitive RAG pipeline, matching the incident coordinates, weather patterns, and local fuel indicators against indexed forestry Standard Operating Procedures (SOPs) stored in a FAISS vector database. The final output is an LLM-synthesized response guide sent to a web-based Emergency Response Dashboard. This unified approach eliminates the latency between hazard detection and coordinated dispatch planning.

---

## Motivation
Forest fires are catastrophic environmental events that require rapid and organized intervention to minimize ecological and economic damage. In the initial hours of a fire, containment actions are highly dependent on the speed of local alerts and the coordination of dispatchers. Although computer vision models have significantly advanced visual detection, their output is typically limited to bounding-box alerts. Responders are still forced to manually retrieve, review, and apply safety procedures from extensive printed guidelines, leading to critical communication lags. Developing an automated, context-grounded response system that links spatial indicators directly with regulatory checklists provides a novel way to reduce response latency and improve wildland firefighting coordination.

---

## Problem Statement
Traditional wildland fire monitoring methods (such as watchtowers and satellite scans) are constrained by low temporal resolution, visibility obstructions (cloud cover), and slow alert transmission. While drone networks offer high-frequency surveillance, existing frameworks separate detection from response coordination. A fire detected by a UAV remains an isolated classification. There is no automated framework to link the incident coordinates and current meteorological conditions directly with standard operating procedures to output an actionable containment guide. This gap between spatial detection and tactical planning delays deployment and increases the risk of fire spread.

---

## Current Challenges
1. **Amorphous Smoke Detection**: Early-stage smoke columns are diffuse, semi-transparent, and easily confused with fog, clouds, or canopy glare.
2. **Network Bandwidth Constraints**: Remote forest boundaries lack the network bandwidth required for continuous, high-definition video streaming.
3. **LLM Hallucinations in Emergency Planning**: Standard Large Language Models lack real-time local context and are prone to generating incorrect or unsafe instructions during crisis operations.
4. **Data Synchronization**: Synchronizing high-frequency drone telemetry metadata with relational databases during network pings and dropouts requires a resilient hybrid architecture.

---

## Literature Summary
Academic literature in this domain focuses on three isolated areas:
- **Vision-Based Fire Classifiers**: Custom YOLO models show high precision for flame and smoke recognition on edge computing boards, but do not provide post-detection tactical coordination.
- **RAG Systems**: Studies show that Retrieval-Augmented Generation reduces LLM hallucination rates and provides verifiable text sources in urban disaster contexts. However, these systems rely on manual text inputs instead of automated sensor integrations.
- **Edge-Cloud collaborative IoT**: Research establishes that processing raw images at the edge while archiving logs in the cloud reduces bandwidth utilization by over 70%, but these frameworks lack natural language cognitive layers.

---

## Research Gap
1. **Decoupling of Detection and Response**: Visual classification models are rarely integrated directly with automated response planning pipelines.
2. **Context-Blind LLM Planning**: Standard generative AI models do not incorporate real-time local variables (wind vectors, fuel levels, coordinates) when generating safety plans.
3. **Edge-Cloud Partitioning for RAG**: The partition of tasks between low-power edge UAV platforms and cloud-native vector search engines for real-time RAG planning remains unexplored.

---

## Research Questions
- **RQ1**: How can edge-based deep learning models (YOLOv8/v9) be optimized to classify amorphous smoke columns under canopy obstruction while operating within the compute constraints of UAV hardware?
- **RQ2**: To what extent does a hybrid edge-cloud ingestion topology reduce network bandwidth requirements compared to continuous raw video transmission during aerial monitoring operations?
- **RQ3**: In what ways does Retrieval-Augmented Generation (RAG) using FAISS index constraints eliminate hallucinated actions in AI-generated response plans compared to zero-shot LLM prompts?

---

## Objectives

### Primary Objective
To design and model a scalable, cloud-native framework that automates early forest fire detection and response planning by linking edge-based drone classification (YOLO) with cloud-hosted vector search engines (RAG).

### Specific Objectives
1. **Optimize** lightweight YOLO models for early smoke classification on simulated edge nodes.
2. **Model** a hybrid ingestion service using FastAPI to manage WebSocket telemetry updates and store metadata in Azure SQL.
3. **Design** a RAG pipeline using LangChain and a FAISS index to retrieve SOP paragraphs based on environmental variables.
4. **Structure** an interactive React-based dashboard mockup for emergency response visualization.

---

## Proposed Framework
The system processes data in a sequential pipeline:

```
[ UAV Patrol ]
      │ (RGB Video Capture)
      ▼
[ YOLO Detection ] (Edge image processing)
      │ (Fire Flag, Coordinates, Snapshot)
      ▼
[ Azure Cloud ] (FastAPI Endpoint router)
      │
      ├──────────────────────────────┐
      ▼                              ▼
[ Blob Storage ]              [ Vector Database ] (SOP index chunks matched via FAISS)
(Snapshot JPEG archived)              │
                                     ▼
                              [ RAG Pipeline ] (LangChain prompt synthesis)
                                     │
                                     ▼
                              [ LLM (GPT-4o) ] (Response checklist generation)
                                     │
                                     ▼
                       [ Emergency Response Dashboard ] (UI visualization)
```

---

## Proposed Architecture
The conceptual architecture separates tasks into key operational layers:
- **UAV Ingestion Client**: Generates telemetry vectors and runs image preprocessing.
- **FastAPI Core Gateway**: Serves as the central data router, managing database connections and RAG execution threads.
- **Azure SQL Database**: Stores relational telemetry timeseries and logged incidents.
- **Azure Blob Storage**: Archives raw JPEG snapshots of fire boundaries.
- **FAISS Vector Index**: Holds vectorized chunks of wildland fire SOPs.
- **LangChain Orchestrator**: Merges weather statistics, coordinates, and SOP segments into prompt templates for LLM planning.
- **React Dashboard**: Renders drone telemetry charts, alerts feeds, and generated response guides.

---

## Technology Stack
- **Frontend**: React, TypeScript, Leaflet, Tailwind CSS.
- **Backend**: Python, FastAPI, Uvicorn, SQLAlchemy.
- **Cloud**: Microsoft Azure (Container Apps, Azure SQL, Blob Storage, Key Vault).
- **Database**: Azure SQL, FAISS (vector index).
- **Computer Vision**: PyTorch, YOLOv8/v9, TensorRT.
- **Machine Learning**: Sentence-Transformers, OpenAI API.
- **RAG**: LangChain.
- **Version Control**: Git, GitHub.
- **Development Tools**: VS Code, PowerShell.

---

## Dataset Details

### 1. FLAME (Fire & Smoke Dataset)
- **Purpose**: To train and evaluate the deep learning model on aerial forest fire RGB and thermal imagery.
- **Source**: IEEE Datasets (captured during prescribed forest burns in Arizona).
- **Type**: High-resolution image frames and video sequences.
- **Expected Usage**: Training the YOLO object detector for early flame classification.
- **Limitations**: Restricted to specific dry shrub canopies; lacks dense tropical forest canopy variations.

### 2. FireNet
- **Purpose**: To improve classification rates of early-stage smoke columns.
- **Source**: Open-source repository (annotated smoke datasets).
- **Type**: Normalized JPG frames with bounding box annotations.
- **Expected Usage**: Fine-tuning YOLO models to separate smoke columns from canopy fog.
- **Limitations**: Contains low-resolution imagery; requires extensive preprocessing and resolution scaling.

---

## Repository Structure & project status

- **Phase 1** — research planning, 15-paper survey, architecture, ADRs, human-alert layer.
- **Phase 2** — working local prototype (FastAPI + SQLite/Alembic + FAISS RAG + React), 9/9 tests.
- **Phase 3** — **real** data, LLM, and cloud IaC:
  - **YOLO** fine-tuned on real data (`YOLO_MODE=finetuned`): FireNet-trained detector
    (`mAP@0.5 = 0.733`, CPU `37.3 FPS`) + a FLAME frame classifier. CV-1 (≥ 0.88) is
    **not met** — an honest data-scale limit, analysed in [`results/README.md`](results/README.md)
    and [`docs/adr/ADR-001.md`](docs/adr/ADR-001.md). Confusion matrix, PR curve, and sample
    detections on held-out images: [`results/README.md#1-yolo-detection--firenet-real-bounding-boxes`](results/README.md#1-yolo-detection--firenet-real-bounding-boxes).
  - **RAG** with real generation (`LLM_MODE=gemini`, Google Gemini Flash). RQ3/CG-2 measured:
    `0.0%` hallucinated-source rate, BERTScore F1 `0.83` vs expert plans.
  - **Latency** measured end-to-end: detect→alert→RAG plan pipeline **~73 ms** (mock LLM),
    real Gemini generation **~3.6 s** (the dominant cost once real generation replaces mock),
    telemetry throughput **~198 msg/s** across 10 concurrent simulated drones — see
    [`results/README.md#4-end-to-end-latency--throughput`](results/README.md#4-end-to-end-latency--throughput).
  - **Azure** — full Terraform ([`cloud/terraform/`](cloud/terraform/)) + real
    `storage_azure.py` / Azure-SQL code paths + [`cloud/DEPLOY.md`](cloud/DEPLOY.md) runbook.
    Provisioning is credential-gated (run it yourself).

Every cloud service still has a **local default** stand-in (`STORAGE_MODE` / `LLM_MODE` /
`YOLO_MODE` config flags) — see [`cloud/README_LOCAL_MODE.md`](cloud/README_LOCAL_MODE.md).
Run locally: [`RUN_LOCALLY.md`](RUN_LOCALLY.md). Deploy: [`cloud/DEPLOY.md`](cloud/DEPLOY.md).

```
cloud-drone-fire-detection/
├── docs/                      # Research docs, ADRs (ADR-001 has a Phase-3 outcome addendum), architecture, mgmt
├── backend/                   # FastAPI: main.py, api/ routes, core/ config+db, services/, Dockerfile
├── frontend/                  # React + Vite dashboard: map, alert feed, plan viewer
├── ai/                        # models/ (yolo_detector, prepare_*, train_yolo), rag/ (ingest·retrieve·orchestrate·evaluate), evaluation/
├── database/                  # SQLAlchemy models.py, Alembic migrations/, seed.py
├── data/                      # knowledge-base/ (SOPs, committed); flame/ + firenet/ (downloaded, git-ignored)
├── cloud/                     # storage_local|azure|dispatcher, terraform/, DEPLOY.md, README_LOCAL_MODE.md
├── testing/                   # simulate_drone.py (JSON WS), simulate_mavlink_drone.py (real MAVLink), unit/ tests, sample_images/, conftest.py
├── results/                   # MEASURED vs PENDING metrics + machine-written run outputs
└── presentation/              # Slide structures and poster designs
```

---

## Work Distribution
- **Researcher 1**: AI & Deep Learning (YOLO optimization, dataset preprocessing, and testing scripts design).
- **Researcher 2**: Cloud & Database (Azure provisioning schemas, VNet architecture, API routing, and DB seeding planning).
- **Researcher 3**: RAG & Systems (LangChain orchestration, FAISS vector indexing, prompt engineering, and UI component mockup planning).

---

## Project Timeline
- **Weeks 1-3**: Literature survey, paper review, and gap analysis.
- **Weeks 4-5**: Dataset acquisition, structural review, and pre-processing research.
- **Weeks 6-7**: System and network architecture design, and ADR compilation.
- **Weeks 8-9**: AI, database, and cloud routing specifications planning.
- **Weeks 10-11**: Testing strategy design and expected metric evaluation setup.
- **Week 12**: Review-1 compliance auditing and presentation deck preparation.

---

## Future Scope
1. **Dataset Augmentation**: Utilizing generative models to overlay synthetic smoke textures on canopy images.
2. **Hardware Deployment**: Implementing TensorRT engines on physical Jetson Orin Nano boards to test real-world inference latency.
3. **Dynamic Path Planning**: Integrating wind-drift telemetry parameters directly into autonomous flight paths.

---

## References

> Note: the five original citations 1–5 were unverifiable via web search and have been replaced with real, DOI-verified papers on the same topics (see `docs/research/literature-survey.md`). All 15 references are now DOI-verified.

1. Zhu, W., Niu, S., Yue, J., & Zhou, Y. (2025). Multiscale wildfire and smoke detection in complex drone forest environments based on YOLOv8. *Scientific Reports*, 15. https://doi.org/10.1038/s41598-025-86239-w
2. Xie, Y., Jiang, B., Mallick, T., Bergerson, J. D., Hutchison, J. K., Verner, D. R., Branham, J., Alexander, M. R., Ross, R. B., Feng, Y., Levy, L.-A., Su, W., & Taylor, C. J. (2025). A RAG-Based Multi-Agent LLM System for Natural Hazard Resilience and Adaptation (MARSHA). *npj Climate Action*. https://doi.org/10.1038/s44168-025-00254-1
3. Roostaei, J., & Wager, Y. Z. (2023). IoT-based edge computing (IoTEC) for improved environmental monitoring. *Sustainable Computing: Informatics and Systems*, 39, 100870. https://doi.org/10.1016/j.suscom.2023.100870
4. Bailon-Ruiz, R., Bit-Monnot, A., & Lacroix, S. (2022). Real-time wildfire monitoring with a fleet of UAVs. *Robotics and Autonomous Systems*, 152, 104071. https://doi.org/10.1016/j.robot.2022.104071
5. Khan, S., Muhammad, K., Hussain, T., Del Ser, J., Cuzzolin, F., Bhattacharyya, S., Akhtar, Z., & de Albuquerque, V. H. C. (2021). DeepSmoke: Deep learning model for smoke detection and segmentation in outdoor environments. *Expert Systems with Applications*, 182, 115125. https://doi.org/10.1016/j.eswa.2021.115125
6. Diaz-Vilor, C., Lozano, A., & Jafarkhani, H. (2025). A Reinforcement Learning Approach for Wildfire Tracking with UAV Swarms. *IEEE Transactions on Wireless Communications*.
7. Tzoumas, G., Salina, L., McConville, A., Richardson, T., & Hauert, S. (2024). Extinguishing Wildfires in Large Scale Scenarios Using Swarms of UAVs. In *Swarm Intelligence (ANTS 2024)*, Springer LNCS vol. 14987. https://doi.org/10.1007/978-3-031-70932-6_6
8. Tavakol Sadrabadi, M., Peiró, J., Innocente, M. S., & Rein, G. (2025). Conceptual design of a wildfire emergency response system empowered by swarms of unmanned aerial vehicles. *International Journal of Disaster Risk Reduction*, 124, 105493. https://doi.org/10.1016/j.ijdrr.2025.105493
9. De Rango, A., Furnari, L., Cortale, F., Senatore, A., & Mendicino, G. (2025). Wildfire Early Warning System Based on a Smart CO2 Sensors Network. *Sensors (MDPI)*, 25(7), 2012. https://doi.org/10.3390/s25072012
10. Mowbray, F., et al. (2024). A systematic review of the use of mobile alerting to inform the public about emergencies and the factors that influence the public response. *Journal of Contingencies and Crisis Management*, 32, e12499. https://doi.org/10.1111/1468-5973.12499
11. Rey, W. P., Adalin, S. A. S., Calanog, K. R. L., & Jimenez, G. W. R. (2024). Mamamayan: A Mobile Community-based Emergency Reporting and Notification System for the City of Makati in the Philippines. In *Proc. 2023 5th ICSED*, ACM, pp. 35-41.
12. Béchard, P., & Marquez Ayala, O. (2024). Reducing hallucination in structured outputs via Retrieval-Augmented Generation. In *Proc. 2024 NAACL-HLT, Industry Track*, pp. 228-238. https://doi.org/10.18653/v1/2024.naacl-industry.19
13. Vazquez, G., Zhai, S., & Yang, M. (2026). Edge-Friendly UAV Wildfire Smoke and Flame Detection Using Transfer Learning-Enhanced Lightweight Deep Learning Models. *MDPI* (PMC13210558).
14. Titu, M. F. S., Pavel, M. A., Michael, G. K. O., Babar, H., Aman, U., & Khan, R. (2024). Real-Time Fire Detection: Integrating Lightweight Deep Learning Models on Drones with Edge Computing. *Drones (MDPI)*, 8(9), Article 483. https://doi.org/10.3390/drones8090483
15. Soliman, H., & Haque, A. (2025). A Smart and Secure Wireless Sensor Network for Early Forest Fire Prediction: An Emulated Scenario Approach. In *Advances in Information and Communication (FICC 2025)*, LNNS vol. 1284, Springer. https://doi.org/10.1007/978-3-031-85363-0_44
