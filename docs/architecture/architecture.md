# Proposed Architecture

This document details the high-level design, conceptual layers, and interactions between the components of the drone forest fire detection framework.

---

## 1. High-Level Architecture
The architecture splits tasks between low-power edge UAVs and virtualized cloud compute:

```
[ UAV Client ] ──(Telemetry & Incidents)──> [ Azure App Service API ]
                                                    │
                 ┌──────────────────────────────────┼──────────────────────────────────┐
                 ▼                                   ▼                                  ▼
      [ Azure Storage Layer ]            [ Alert Service ]                    [ RAG Planning Service ]
  ┌───────────────────────────────────┐  ┌──────────────────────────────┐  ┌───────────────────────────────────┐
  │ - Azure SQL (Structured telemetry)│  │ Azure Communication Services │  │ - FAISS Vector Index (Local SOPs)  │
  │ - Azure Blob (Image Snapshots)    │  │ (SMS) + Notification Hubs    │  │ - LangChain Ingestion & Prompting │
  └───────────────────────────────────┘  │ 1. Immediate raw alert       │  └───────────────────────────────────┘
                 │                        │    (parallel, no RAG wait)   │                   │
                 │                        │ 2. Enriched plan push        │ <────────────────-┘
                 │                        │    (after RAG completes)     │   (enriched plan summary)
                 │                        └──────────────────────────────┘
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

### Public/Responder Alert Service
- **Responsibility**: Delivers notifications to people **outside** the system. Implemented with Azure Communication Services (SMS) + Azure Notification Hubs (push), and triggered by the FastAPI gateway **in parallel with** the `TriggerRAG()` step — not sequentially after it — so human notification is never delayed waiting on LLM response time. It sends two distinct message classes to two distinct recipient roles:
  1. **Immediate raw alert** (no RAG needed) → forest ranger on duty + local fire department dispatch, via SMS, containing: incident coordinates, confidence score, timestamp, snapshot thumbnail link. Sent the instant YOLO flags a detection — must not wait for the RAG/LLM pipeline to complete.
  2. **Enriched response-plan push** (after RAG completes) → the same recipients plus an "affected-zone residents" distribution list, containing the generated containment/evacuation checklist summary and a link to the full plan on the dashboard.
- **Recipient/role specification**: see [`alert-recipients.md`](alert-recipients.md).

---

## 3. Component Interactions
1. **Telemetry Feed**: The UAV Client pushes JSON pings to the API via WebSockets. The API writes these pings to Azure SQL and broadcasts them to the React Dashboard.
2. **Alert Sequence**: If the edge model flags fire, the UAV POSTs coordinates and a JPEG snapshot to the API. The API **immediately triggers the Alert Service raw alert (in parallel, not waiting for RAG)**, saves the image to Blob Storage, logs the incident in Azure SQL, and triggers the RAG sequence.
3. **Response Synthesis**: The RAG service queries FAISS, combines the retrieved SOP blocks with weather variables, and queries the LLM. The generated checklist is stored in Azure SQL and pushed to the React Dashboard.
4. **Human Notification**: The Alert Service sends an immediate SMS to the on-duty forest ranger and fire-department dispatch the instant a detection is logged, then — once the RAG plan is ready — an enriched push (containment/evacuation summary + dashboard link) to those recipients plus an affected-zone residents list. The immediate alert path is never gated on the RAG round-trip. Measured by validation gate **AL-1** (see `../management/milestones.md`).
