# Proposed Architecture

This document details the high-level design, conceptual layers, and interactions between the components of the drone forest fire detection framework.

---

## 1. High-Level Architecture
The architecture splits tasks between low-power edge UAVs and virtualized cloud compute:

```
[ UAV Client ] ──(Telemetry & Incidents)──> [ Azure App Service API ]
                                                    │
                 ┌──────────────────────────────────┴──────────────────────────────────┐
                 ▼                                                                     ▼
      [ Azure Storage Layer ]                                                 [ RAG Planning Service ]
  ┌───────────────────────────────────┐                                 ┌───────────────────────────────────┐
  │ - Azure SQL (Structured telemetry)│                                 │ - FAISS Vector Index (Local SOPs)  │
  │ - Azure Blob (Image Snapshots)    │                                 │ - LangChain Ingestion & Prompting │
  └───────────────────────────────────┘                                 └───────────────────────────────────┘
                 │                                                                     │
                 └──────────────────────────────────┬──────────────────────────────────┘
                                                    ▼
                                     [ React Dashboard UI ]
```

---

## 2. Component Descriptions

### UAV Client Node
- **Responsibility**: Manages flight control, reads GPS metrics, captures video frames, and executes YOLO-based classification locally. It acts as the primary data producer.

### FastAPI Application Service
- **Responsibility**: Exposes endpoints to receive telemetry and alerts. It routes database writes, coordinates RAG execution, and streams real-time updates to the dashboard via WebSockets.

### Azure SQL Database
- **Responsibility**: Stores structured relational data, including drone profiles, flight trajectories, and incident logs.

### Azure Blob Storage
- **Responsibility**: Archives image snapshots containing identified flame or smoke bounding boxes.

### FAISS Vector Index
- **Responsibility**: Stores high-dimensional vector embeddings of regional forest fire SOPs to enable fast similarity search.

### LangChain Orchestrator
- **Responsibility**: Manages the prompt compiler. It retrieves matching SOP text chunks and formats them with weather variables into bounded prompts for the Large Language Model.

---

## 3. Component Interactions
1. **Telemetry Feed**: The UAV Client pushes JSON pings to the API via WebSockets. The API writes these pings to Azure SQL and broadcasts them to the React Dashboard.
2. **Alert Sequence**: If the edge model flags fire, the UAV POSTs coordinates and a JPEG snapshot to the API. The API saves the image to Blob Storage, logs the incident in Azure SQL, and triggers the RAG sequence.
3. **Response Synthesis**: The RAG service queries FAISS, combines the retrieved SOP blocks with weather variables, and queries the LLM. The generated checklist is stored in Azure SQL and pushed to the React Dashboard.
