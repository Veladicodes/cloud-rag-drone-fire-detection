# Research Overview & Methodologies

This directory holds the theoretical studies, literature reviews, and design arguments that support the development of the Retrieval-Augmented Drone framework.

---

## Research Subsections

For detailed investigations, please select a section below. All nine research documents in this directory are indexed here.

### Scope & Questions

### [Objectives](objectives.md)
- Primary and specific research objectives, expected research contributions, and academic deliverables.

### [Research Questions](research-questions.md)
- The three research questions (RQ1 edge detection, RQ2 hybrid ingestion resilience, RQ3 grounded RAG planning) with per-question focus areas.

### Literature & Gaps

### [Literature Survey](literature-survey.md)
- Reviews fifteen publications, split 5 / 5 / 5 across the three researchers, covering UAV swarms, YOLO edge detection, sensor-network early warning, human/public alerting, and Retrieval-Augmented Generation (RAG) in wildfire management.

### [Gap Analysis](gap-analysis.md)
- Presents three independent per-researcher analyses (R1 papers 1–5, R2 papers 6–10, R3 papers 11–15), each in a distinct voice, converging on a consolidated gap statement and proposed solution.

### Methodology & Data

### [Methodology](methodology.md)
- Scientific research design (independent / dependent / controlled variables), conceptual workflow, data-flow channels, edge-vs-cloud processing split, RAG grounding maths, and the experimental verification plan.

### [Datasets](datasets.md)
- Specifications, selection criteria, expected train/validation/test splits, and limitations of the FLAME and FireNet datasets, plus the preprocessing and augmentation plan.

### Technical Briefs

### [YOLO Object Detection Brief](yolo-detection.md)
- Analyzes YOLOv8/v9 neural network layers, loss calculations (CIoU, BCE, DFL), and edge hardware resource profiles.

### [Retrieval-Augmented Response Brief](rag-response.md)
- Details the text chunking parameters, FAISS distance calculations, and LangChain prompt templates used to guide emergency responses.

### Audit

### [Review-1 Compliance Report](compliance-report.md)
- Maps every faculty evaluation requirement to a file in the repository, records the audit verdict, and (post-remediation) logs the delta from the previous submission attempt.
