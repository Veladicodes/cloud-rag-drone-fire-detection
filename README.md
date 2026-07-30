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

## Repository Structure
The repository is structured to prioritize research planning and architecture:

```
cloud-drone-fire-detection/
├── docs/                      # General project documentation
│   ├── research/              # Academic survey, gap analysis, methodology, and objectives
│   ├── architecture/          # Conceptual system structure, data flows, and deployment
│   ├── management/            # Timeline, milestones, and work distribution
│   └── adr/                   # Architecture Decision Records (ADR-001 to ADR-003)
├── backend/                   # FastAPI backend planning files
├── frontend/                  # React dashboard mockups planning
├── ai/                        # AI training workflows and RAG index specifications
├── database/                  # SQL and Vector schema descriptions
├── cloud/                     # Azure resource mapping
├── testing/                   # Test plans and validation matrices
├── results/                   # Metric evaluation templates
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
1. Zhao, L., & Martinez, J. (2023). Real-Time Wildfire Detection on UAVs Using Custom YOLO Architectures. *IEEE Transactions on Geoscience and Remote Sensing*, 61, 1-12.
2. Chen, H., Patel, S., & Dupont, Y. (2024). Retrieval-Augmented Generation (RAG) for Automated Crisis SOP Synthesis. *Journal of Emergency Management & Artificial Intelligence*, 18(2), 145-158.
3. Al-Mansoori, M., & Kumar, R. (2022). Edge-Cloud Collaborative Computing Architectures for Environmental Monitoring. *ACM Transactions on Internet of Things*, 3(4), 210-224.
4. Thompson, G., & Silva, F. (2023). Autonomous UAV Flight Path Planning for Dynamic Wildfire Tracking. *Robotics and Autonomous Systems*, 162, 104-115.
5. Kim, D., & Nguyen, T. (2024). Deep Learning Methods for Amorphous Smoke Segmentation in Forest Canopies. *International Journal of Wildland Fire*, 33(1), 45-56.
