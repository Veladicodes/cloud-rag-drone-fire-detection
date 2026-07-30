# Retrieval-Augmented Generation (RAG) for Incident Response

Deploying Large Language Models (LLMs) in safety-critical situations like forest fire containment requires absolute reliability. Standard LLMs are prone to hallucinating instructions, lack knowledge of localized geography, and are unaware of agency-specific Standard Operating Procedures (SOPs). This framework utilizes **Retrieval-Augmented Generation (RAG)** to ground the AI's responses in verified documentation.

---

## Technical Pipeline Architecture

The RAG workflow operates in two distinct phases: Offline Ingestion and Online Inference.

```
Offline Ingestion:
[ SOP Docs / Guidelines ] ──> [ Text Splitter ] ──> [ Embedding Model ] ──> [ FAISS Database ]

Online Inference:
[ Drone Detection Event ] ──┐
                            ├──> [ Query Builder ] ──> [ Vector Search ] ──> [ SOP Chunks ] ──┐
[ Weather API Data ] ───────┘                                                                │
                                                                                            ▼
[ LLM (GPT-4o) ] <──( Prompt Template + Context Chunks + Weather Info )─────────────────────┘
       │
       ▼
[ Actionable Response Plan ]
```

---

## 1. Offline Ingestion Pipeline

### Document Parsing & Chunking
- Regulatory guidelines and fire containment manuals are parsed from markdown and PDF formats.
- Texts are divided into chunks using a **Recursive Character Text Splitter** to ensure semantic boundaries are maintained.
- **Parameters**:
  - `chunk_size`: 500 characters.
  - `chunk_overlap`: 50 characters (ensuring contextual continuity across boundaries).

### Vector Embedding
- Each text chunk ($c_i$) is passed through an embedding model ($E$) to generate a high-dimensional vector:

$$\vec{v}_i = E(c_i) \quad \text{where } \vec{v}_i \in \mathbb{R}^{d} \text{ and } d = 768 \text{ or } 1536$$

- Default models include `sentence-transformers/all-mpnet-base-v2` (768 dimensions) or Azure OpenAI `text-embedding-3-small` (1536 dimensions).

### Vector Storage (FAISS)
- Vector arrays are indexed in **FAISS (Facebook AI Similarity Search)**.
- Flat L2 Indexing (`IndexFlatL2`) or Hierarchical Navigable Small World (`IndexHNSWFlat`) is utilized depending on document corpus scale.

---

## 2. Online Inference & Retrieval

When a fire incident is registered:
1. **Metadata Aggregation**: The system fetches current wind speed/direction, local temperature, and fuel levels at the incident's coordinates.
2. **Search Query Formulation**: The system generates a structured query: 
   *"Wildfire containment procedures under wind speed [W] km/h and high dry fuel density."*
3. **Similarity Search**: The query is embedded ($\vec{q} = E(q)$) and matched against the FAISS vector index using L2 distance:

$$d(\vec{q}, \vec{v}) = \sum_{k=1}^{d} (q_k - v_k)^2$$

4. **Context Construction**: The top $k$ (typically $k=3$) document chunks with the lowest distances are fetched.

---

## 3. LangChain Prompt Engineering

The retrieved chunks, telemetry coordinates, and weather variables are compiled into a prompt template:

### Conceptual Template Layout
- **System Constraints**: Restricts output synthesis to the provided context. If the context is insufficient, returns a fallback flag.
- **Incident Variables**: Variables representing coordinate location, wind heading, wind velocity, temperature, and fuel dryness.
- **Retrieved SOP Context**: Relevant document paragraphs matching the incident profile.
- **Output Schema**: Directives specifying the output layout (Evacuation zone range, containment priority vector, dispatch coordinates, safety protocols).

This structure mitigates safety risks by anchoring response generation to approved local manuals.
