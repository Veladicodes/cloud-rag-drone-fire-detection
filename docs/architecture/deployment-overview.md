# Deployment Overview

This document outlines the deployment design and network architecture for hosting the drone framework on Microsoft Azure.

---

## 1. Network Zoning and Security (Virtual Network)

To isolate database assets and AI services from the public internet, resources are grouped into a secured **Virtual Network (VNet)**:

```
[ Public Network ]
       │ (HTTPS Traffic Only)
       ▼
 ┌─ Azure VNet Security Boundary ───────────────────────────────────────────────┐
 │                                                                              │
 │  ┌─ Frontend Subnet (Public Gateway) ─────────────────────────────────────┐  │
 │  │ - Azure Application Gateway (SSL Termination)                          │  │
 │  └────────────────────────────────────────────────────────────────────────┘  │
 │                                                                              │
 │  ┌─ Backend Subnet (Private Compute Zone) ────────────────────────────────┐  │
 │  │ - Azure Container Apps (FastAPI API Instance)                          │  │
 │  └────────────────────────────────────────────────────────────────────────┘  │
 │                                                                              │
 │  ┌─ Database Subnet (Private Link Zone) ──────────────────────────────────┐  │
 │  │ - Azure SQL Database (Accessible only via Private Link)                │  │
 │  │ - Azure Blob Storage Endpoint                                          │  │
 │  └────────────────────────────────────────────────────────────────────────┘  │
 │                                                                              │
 └──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Hosting

### Compute Sub-System
- **Azure Container Apps**: Hosts the backend FastAPI server and frontend React dashboard inside private subnets.
- **Azure Container Registry (ACR)**: Stores built container images securely.

### Data Sub-System
- **Azure SQL Database (Serverless)**: Relational database configured with Auto-Pause to minimize operational costs when there are no active patrols.
- **Azure Blob Storage (LRS)**: Hot tier storage for immediate incident snapshots, with lifecycles configured to move files to Cool storage after 30 days.

### Cognitive Sub-System
- **Azure OpenAI Service**: Accesses GPT-4o models using Azure Private Endpoints to ensure prompt data remains within the private network boundaries.

---

## 3. Data Protection and Access Control
1. **Network Security Groups (NSGs)**: Filter traffic between subnets. The Database Subnet only accepts connections originating from the Backend Subnet.
2. **Managed Identities (Azure AD)**: Replaces hardcoded passwords. The Container App uses a System-Assigned Managed Identity to read from Azure SQL and Blob Storage.
3. **Azure Key Vault**: Stores API keys (e.g., Azure OpenAI) and injects them as secure environment variables at runtime.
