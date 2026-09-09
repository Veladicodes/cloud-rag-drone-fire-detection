# System Architecture Specification

This directory holds the conceptual architecture for the Cloud-Based Retrieval-Augmented Drone Framework: component structure, data flows, deployment topology, and the human-alerting layer.

---

## Index

- [architecture.md](architecture.md) — High-level design: edge/cloud task split, component responsibilities (UAV client, FastAPI gateway, Azure SQL, Blob, FAISS, LangChain orchestrator, Public/Responder Alert Service), and the three-plus-one interaction flows.
- [component-diagram.md](component-diagram.md) — Mermaid `classDiagram` of the structural modules and their relations, including the `AlertService` class.
- [sequence-diagram.md](sequence-diagram.md) — Mermaid sequence diagram of the telemetry streaming loop and the incident detection → parallel alert → RAG planning sequence.
- [deployment-overview.md](deployment-overview.md) — Azure VNet zoning (frontend / backend / database subnets), component hosting, and access control (NSGs, Managed Identities, Key Vault).
- [alert-recipients.md](alert-recipients.md) — Recipient / channel / trigger / content matrix for the alert service: how notifications are delivered and who receives them.
