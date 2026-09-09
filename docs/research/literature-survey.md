# Literature Survey

This document reviews fifteen academic publications relevant to the integration of UAV surveillance, deep learning object detection, cloud-native telemetry, human alerting, and Retrieval-Augmented Generation (RAG) in wildfire management. Per the course rubric, the survey is split **5 / 5 / 5** across the three researchers, and each researcher produces their **own independent** gap analysis for their five assigned papers:

- **Papers 1–5** — Researcher 1 (AI & Computer Vision): edge detection, smoke segmentation, flight-path robotics.
- **Papers 6–10** — Researcher 2 (Cloud & Database): UAV swarm coordination, sensor-network early-warning, human/public alerting.
- **Papers 11–15** — Researcher 3 (Cognitive Systems & UI): RAG grounding, edge-inference limits, notification-system integration.

Each researcher's independent analysis is in [`gap-analysis.md`](gap-analysis.md).

> **⚠ CITATION INTEGRITY — TODO(verify): Papers 1–5 could not be verified.**
> A web search (exact-title, quoted) returned **no matching record** for any of the five
> original citations below — Zhao & Martinez (2023), Chen/Patel/Dupont (2024),
> Al-Mansoori & Kumar (2022), Thompson & Silva (2023), Kim & Nguyen (2024). Their titles,
> author pairs, and volume/page numbers appear to be placeholder/fabricated. **These entries
> must be replaced with real, findable papers (with real DOIs) or removed before any academic
> submission** — keeping an unverifiable citation is an integrity risk. No DOI has been
> invented for them. Papers 6–15 were supplied as a verified list (two carry their own
> `TODO(verify)` on specific fields).

---

## Paper 1: Real-Time Wildfire Detection on UAVs Using Custom YOLO Architectures

### Citation
- **Authors**: Zhao, L., & Martinez, J.
- **Journal/Conference**: *IEEE Transactions on Geoscience and Remote Sensing*
- **Year**: 2023
- **Title**: *Real-Time Wildfire Detection on UAVs Using Custom YOLO Architectures*

### Methodology
The authors propose a lightweight YOLOv8 implementation trained on a custom dataset of aerial forest fire images. The model was optimized using TensorRT quantization and deployed on an NVIDIA Jetson Nano onboard a quadcopter. They evaluate the trade-off between image input size and frame processing latency.

### Key Findings
- Achieved a Mean Average Precision (mAP@0.5) of 89.2% for smoke detection.
- Frame rates reached 32 FPS when utilizing FP16 precision.
- Confirmed that early smoke detection is highly sensitive to background canopy clutter.

### Research Gap Identified
The system is solely a detection tool. Once a fire is flagged, the model outputs bounding coordinates but lacks any mechanism to recommend tactical suppression steps, coordinate with neighboring UAVs, or retrieve operating protocols.

---

## Paper 2: Retrieval-Augmented Generation (RAG) for Automated Crisis SOP Synthesis

### Citation
- **Authors**: Chen, H., Patel, S., & Dupont, Y.
- **Journal/Conference**: *Journal of Emergency Management & Artificial Intelligence*
- **Year**: 2024
- **Title**: *Retrieval-Augmented Generation (RAG) for Automated Crisis SOP Synthesis*

### Methodology
This paper explores using LangChain and a vector database (ChromaDB) to retrieve Standard Operating Procedures during urban flooding events. The system embeds local guidelines and injects them into the context window of GPT-4 to generate response checklists for emergency coordinators.

### Key Findings
- Grounded generation reduced LLM hallucinations from 14.5% to under 0.8%.
- Prompt templates restricting response schemas yielded highly actionable, standardized plans.
- Proved that vector database recall accuracy is highly dependent on chunking strategies.

### Research Gap Identified
The model relies entirely on manual text inputs from operators. It lacks integration with real-time physical sensors, drone telemetry streams, or live meteorological APIs to guide the retrieval query.

---

## Paper 3: Edge-Cloud Collaborative Computing Architectures for Environmental Monitoring

### Citation
- **Authors**: Al-Mansoori, M., & Kumar, R.
- **Journal/Conference**: *ACM Transactions on Internet of Things*
- **Year**: 2022
- **Title**: *Edge-Cloud Collaborative Computing Architectures for Environmental Monitoring*

### Methodology
The study introduces a hybrid architecture dividing tasks between low-power edge gateways and a central Microsoft Azure cloud. Edge nodes handle raw sensor filtering and immediate anomaly classification, while the cloud processes historical database aggregations and heavy analytical tasks.

### Key Findings
- Reduced network bandwidth utilization by 74% compared to continuous raw data uploading.
- Confirmed that asynchronous local buffers prevent data loss during network dropouts.
- Described standard protocols for edge-to-cloud metadata synchronization.

### Research Gap Identified
The framework only evaluates scalar environmental data (temperature, gas levels). It does not analyze multi-modal telemetry streams, video frames, or interface with cognitive language models for operational decision support.

---

## Paper 4: Autonomous UAV Flight Path Planning for Dynamic Wildfire Tracking

### Citation
- **Authors**: Thompson, G., & Silva, F.
- **Journal/Conference**: *Robotics and Autonomous Systems*
- **Year**: 2023
- **Title**: *Autonomous UAV Flight Path Planning for Dynamic Wildfire Tracking*

### Methodology
Presents a path-planning algorithm that dynamically adjusts drone flight vectors based on wind speed and fire boundary predictions. The model uses a localized predictive model to steer the drone along the perimeter of active smoke plumes.

### Key Findings
- Increased perimeter coverage efficiency by 41% compared to fixed grid patrol flights.
- Documented wind-drift telemetry challenges and compass compensation metrics.
- Evaluated the impact of battery depletion thresholds on mission duration.

### Research Gap Identified
Focus is restricted to flight path robotics. The paper does not address how the collected telemetry and fire coordinates are shared with cloud databases, or how localized response guidelines are retrieved based on the flight telemetry.

---

## Paper 5: Deep Learning Methods for Amorphous Smoke Segmentation in Forest Canopies

### Citation
- **Authors**: Kim, D., & Nguyen, T.
- **Journal/Conference**: *International Journal of Wildland Fire*
- **Year**: 2024
- **Title**: *Deep Learning Methods for Amorphous Smoke Segmentation in Forest Canopies*

### Methodology
Evaluates semantic segmentation networks (U-Net, SegNet) and object detectors (YOLO) for detecting early-stage smoke plumes. Focuses on the difficulty of separating white/gray smoke pixels from fog and canopy reflection.

### Key Findings
- Segmentation models provide superior shape boundaries but require high processing latency.
- Bounding box detectors (YOLO) provide faster alerts, which is critical for early detection.
- Data augmentation using synthetic transparency masks improves accuracy in fog-prone areas.

### Research Gap Identified
The study is restricted to image processing metrics (Intersection over Union, Pixel Accuracy). The research does not provide a scalable ingestion pipeline or explore how these detections are converted into emergency management plans.

---

# Papers 6–10 — Researcher 2 (Cloud, Database & Alerting)

## Paper 6: A Reinforcement Learning Approach for Wildfire Tracking With UAV Swarms

### Citation
- **Authors**: Diaz-Vilor, C., Lozano, A., & Jafarkhani, H.
- **Journal/Conference**: *IEEE Transactions on Wireless Communications*
- **Year**: 2025
- **Title**: *A Reinforcement Learning Approach for Wildfire Tracking With UAV Swarms*

### Methodology
Reinforcement-learning-based trajectory optimization for UAV swarms that must maintain a cell-free connectivity link to ground access points (APs) while tracking a moving wildfire front. The learned policy balances imaging view quality against connectivity and battery limits.

### Key Findings
- Cell-free multi-AP connectivity provides resilience against APs being damaged by the fire itself.
- Swarm repositioning trades off view quality against link quality and remaining battery.

### Research Gap Identified
Connectivity resilience is optimized in isolation from any downstream response-planning or alerting pipeline — detection and tracking are never linked to an action or notification layer.

---

## Paper 7: Extinguishing Wildfires in Large Scale Scenarios Using Swarms of UAVs

### Citation
- **Authors**: Tzoumas, G., Salina, L., McConville, A., Richardson, T., & Hauert, S.
- **Journal/Conference**: *Swarm Intelligence (ANTS 2024)*, Springer LNCS vol. 14987
- **Year**: 2024
- **DOI**: 10.1007/978-3-031-70932-6_6
- **Title**: *Extinguishing Wildfires in Large Scale Scenarios Using Swarms of UAVs*

### Methodology
Proposes Dynamic Space Partition for Firefighting (DSPF) and its coordinated variant (DSPFC): a swarm of 30 UAVs self-organizes through nearest-neighbour communication to monitor and suppress fires.

### Key Findings
- Coordinated multi-UAV engagement (DSPFC) outperforms uncoordinated single-UAV response on a novel "fire mitigation effectiveness" (FME) metric.

### Research Gap Identified
Purely a flight-coordination and suppression algorithm: no cloud backend, no human notification layer, and no persistent incident logging.

---

## Paper 8: Conceptual Design of a Wildfire Emergency Response System Empowered by Swarms of UAVs

### Citation
- **Authors**: TODO(verify) — confirm exact author names and publication month from https://www.sciencedirect.com/science/article/pii/S2212420925003176
- **Journal/Conference**: ScienceDirect (systems-engineering conceptual design paper)
- **Year**: 2025
- **Title**: *Conceptual design of a wildfire emergency response system empowered by swarms of unmanned aerial vehicles*

### Methodology
A systems-engineering approach that defines the tasks best suited to UAV swarms within a human-centred wildfire emergency response system, spanning software, hardware, human components, and their interfaces.

### Key Findings
- Identifies concrete regulatory and integration barriers to UAV-swarm adoption in emergency response.
- Proposes a human-centred interface layer connecting swarm output to responders.

### Research Gap Identified
Conceptual and architectural only — no working prototype, no quantitative validation, and no RAG-style grounded response generation.

---

## Paper 9: Wildfire Early Warning System Based on a Smart CO2 Sensors Network

### Citation
- **Authors**: De Rango, A., Furnari, L., Cortale, F., Senatore, A., & Mendicino, G.
- **Journal/Conference**: *Sensors (MDPI)*, 25(7), 2012
- **Year**: 2025
- **DOI**: 10.3390/s25072012
- **Title**: *Wildfire Early Warning System Based on a Smart CO2 Sensors Network*

### Methodology
44 low-cost CO2 sensors (LoRaWAN) deployed around a controlled prescribed burn. Three AI models (two AutoEncoders, one LSTM) are compared against a simple threshold-based (NO-AI) alerting rule.

### Key Findings
- LSTM-based anomaly detection activated 56% more sensors than the fixed NO-AI threshold, and activated them earlier.
- Fire-front propagation was tracked through wind-pattern correlation across the sensor grid.

### Research Gap Identified
Purely ground-sensor-based: no aerial/drone layer, and no integration with a cloud RAG pipeline for translating a detection into response actions. Directly motivates this project's threshold-vs-learned-anomaly framing and its root-cause reasoning.

---

## Paper 10: A Systematic Review of the Use of Mobile Alerting to Inform the Public About Emergencies

### Citation
- **Authors**: Mowbray, F., et al.
- **Journal/Conference**: *Journal of Contingencies and Crisis Management*, 32, e12499
- **Year**: 2024
- **DOI**: 10.1111/1468-5973.12499
- **Title**: *A systematic review of the use of mobile alerting to inform the public about emergencies and the factors that influence the public response*

### Methodology
A systematic review (Medline, Embase, PsycInfo, Scopus) of studies evaluating how mobile alerting systems affect intended and actual public behaviour during emergencies.

### Key Findings
- Message speed and reliability matter — but so does message content and wording.
- Identifies concrete factors that make the public more or less likely to act on an alert.

### Research Gap Identified
Reviews human-facing alert effectiveness for general emergencies — not wildfire-specific, and not integrated with any automated detection-to-alert pipeline. Directly informs how this project's human-alert layer should be designed (recipient roles, message classes, latency).

---

# Papers 11–15 — Researcher 3 (Cognitive Systems, RAG & UI)

## Paper 11: Mamamayan — A Mobile Community-based Emergency Reporting and Notification System

### Citation
- **Authors**: Rey, W. P., Adalin, S. A. S., Calanog, K. R. L., & Jimenez, G. W. R.
- **Journal/Conference**: *Proc. 2023 5th International Conference on Software Engineering and Development (ICSED)*, ACM, pp. 35–41
- **Year**: 2024
- **Title**: *Mamamayan: A Mobile Community-based Emergency Reporting and Notification System for the City of Makati in the Philippines*

### Methodology
A mobile app plus backend for two-way community emergency reporting and push notification to registered residents within a defined geographic zone.

### Key Findings
- Demonstrates a concrete, working architecture for geo-targeted push notification delivered to named recipient roles (residents, local authority).

### Research Gap Identified
Triggered manually by human reporters rather than by an automated sensor/drone detection pipeline — automating that trigger is precisely this project's contribution.

---

## Paper 12: Reducing Hallucination in Structured Outputs via Retrieval-Augmented Generation

### Citation
- **Authors**: Béchard, P., & Marquez Ayala, O.
- **Journal/Conference**: *Proc. 2024 NAACL-HLT, Industry Track*, pp. 228–238
- **Year**: 2024
- **DOI**: 10.18653/v1/2024.naacl-industry.19
- **Title**: *Reducing hallucination in structured outputs via Retrieval-Augmented Generation*

### Methodology
A RAG pipeline with a small, well-trained retriever grounds an LLM's structured (schema-constrained) output generation for enterprise workflow tasks.

### Key Findings
- RAG grounding significantly reduces hallucination in structured outputs.
- It lets a smaller, cheaper LLM match larger ungrounded models.

### Research Gap Identified
Demonstrated on generic enterprise workflows, not on safety-critical emergency-response checklists — directly supports RQ3 (RAG vs zero-shot hallucination) and justifies the `INSUFFICIENT_CONTEXT` fallback design in ADR-002.

---

## Paper 13: Edge-Friendly UAV Wildfire Smoke and Flame Detection Using Transfer Learning-Enhanced Lightweight Deep Learning Models

### Citation
- **Authors**: Vazquez, G., Zhai, S., & Yang, M.
- **Journal/Conference**: MDPI journal article (PMC ID PMC13210558)
- **Year**: 2026
- **Title**: *Edge-Friendly UAV Wildfire Smoke and Flame Detection Using Transfer Learning-Enhanced Lightweight Deep Learning Models*

### Methodology
Lightweight YOLO variants fine-tuned via transfer learning (COCO / FASDD source pretraining) and benchmarked on mAP@0.5, FPS, inference power, and energy-delay product (EDP) on an edge platform.

### Key Findings
- Transfer learning lifts mAP@0.5 to 79.2% on the target dataset.
- Quantifies the real payload / battery / compute trade-off (power, energy, EDP) that ADR-001 assumes.

### Research Gap Identified
Benchmarks edge inference cost in isolation; does not connect detection output to any cloud-side response-planning system.

---

## Paper 14: Real-Time Fire Detection — Integrating Lightweight Deep Learning Models on Drones with Edge Computing

### Citation
- **Authors**: Titu, M. F. S., Pavel, M. A., Michael, G. K. O., Babar, H., Aman, U., & Khan, R.
- **Journal/Conference**: *Drones (MDPI)*, 8(9), Article 483
- **Year**: 2024
- **DOI**: 10.3390/drones8090483
- **Title**: *Real-Time Fire Detection: Integrating Lightweight Deep Learning Models on Drones with Edge Computing*

### Methodology
Compares DETR, Detectron2, YOLOv8, and knowledge-distilled models for real-time drone-based fire detection on a 7,187-image dataset, focused on edge deployment.

### Key Findings
- Establishes concrete accuracy / speed trade-offs among detector architectures specifically in a drone edge-computing context.

### Research Gap Identified
A model-comparison study only: no swarm coordination, no cloud RAG layer, no human alert mechanism. This project integrates detection into the larger pipeline these results treat as downstream work.

---

## Paper 15: A Wireless Sensor Network Application in Forest Fire Early Detection — A Smart and Secure Approach

### Citation
- **Authors**: Soliman, H., & Haque, A.
- **Journal/Conference**: *Proc. 2024 Intelligent Systems and Machine Learning Conference (ISML)*, Hyderabad, India, pp. 106–111
- **Year**: 2024
- **DOI/ISBN**: TODO(verify) — confirm exact page range and DOI/ISBN from the primary ISML 2024 proceedings record; this entry was located via a secondary citation.
- **Title**: *A Wireless Sensor Network Application in Forest Fire Early Detection: A Smart and Secure Approach*

### Methodology
A WSN-based forest-fire detection architecture that emphasises secure data transmission from ground sensors to the base station.

### Key Findings
- Proposes a security-hardened ground-sensor-to-base-station pipeline suited to remote, unattended forest deployment.

### Research Gap Identified
Ground-sensor-only: no aerial component and no generative response planning.
