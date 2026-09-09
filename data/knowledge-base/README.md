# Knowledge Base Directory

## 1. Purpose
This folder is the source location for the Standard Operating Procedure (SOP) documents that the RAG pipeline indexes. It resolves the reference to `data/knowledge-base/` in [ADR-002](../../docs/adr/ADR-002.md): SOP source files are added here, and the FAISS vector index is (re)built from their contents.

---

## 2. Future Contents
- `sops/`: Regional wildland-fire containment and evacuation SOP documents (Markdown / PDF), one file per procedure or manual section.
- `sample_sops/`: Small, clearly labelled **illustrative** SOP text used for pipeline testing before real regional documents are licensed/obtained.
- `index_manifest.md`: Records which source files are included in the current FAISS index build, with chunk parameters (`chunk_size` 500, `chunk_overlap` 50).

---

## 3. Responsible Member
- **Primary Owner**: Researcher 3 (Cognitive Systems & UI Specialist)

---

## 4. Expected Deliverables
- A curated corpus of regional SOP documents cleared for use.
- A reproducible ingestion step: drop a document here, rebuild the index, and the RAG response logic updates without retraining (per ADR-002).
- An index manifest mapping each indexed chunk back to its source document for dashboard traceability.

---

> **Status**: Stub directory for Phase-I. No real SOP corpus is committed yet. Replace `sample_sops/` with real regional SOP documents before the Review-2 final demo.
