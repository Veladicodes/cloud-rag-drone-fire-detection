# Literature Survey

This document reviews fifteen academic publications relevant to the integration of UAV surveillance, deep learning object detection, cloud-native telemetry, human alerting, and Retrieval-Augmented Generation (RAG) in wildfire management. Per the course rubric, the survey is split **5 / 5 / 5** across the three researchers, and each researcher produces their **own independent** gap analysis for their five assigned papers:

- **Papers 1–5** — Researcher 1 (AI & Computer Vision): edge detection, smoke segmentation, flight-path robotics.
- **Papers 6–10** — Researcher 2 (Cloud & Database): UAV swarm coordination, sensor-network early-warning, human/public alerting.
- **Papers 11–15** — Researcher 3 (Cognitive Systems & UI): RAG grounding, edge-inference limits, notification-system integration.

Each researcher's independent analysis is in [`gap-analysis.md`](gap-analysis.md).

> **Citation note.** The five original citations for papers 1–5 (Zhao & Martinez 2023,
> Chen/Patel/Dupont 2024, Al-Mansoori & Kumar 2022, Thompson & Silva 2023, Kim & Nguyen 2024)
> could not be verified via web search and have been **replaced with real, DOI-verified
> publications** on the same five topics. Paper 2's exact author list is still
> `TODO(verify)` (the DOI resolves). Papers 6–15 were supplied as a verified list (8 and 15
> carry field-level `TODO(verify)`).

---

## Paper 1: Multiscale Wildfire and Smoke Detection in Complex Drone Forest Environments Based on YOLOv8

### Citation
- **Authors**: Zhu, W., Niu, S., Yue, J., & Zhou, Y.
- **Journal/Conference**: *Scientific Reports* (Nature), 15
- **Year**: 2025
- **DOI**: 10.1038/s41598-025-86239-w
- **Title**: *Multiscale wildfire and smoke detection in complex drone forest environments based on YOLOv8*

### Methodology
The authors add multiscale feature-enhancement modules to YOLOv8 for drone-captured forest imagery, targeting small and partially occluded fire and smoke regions against cluttered canopy backgrounds. They train and evaluate on drone forest fire/smoke datasets and compare against the baseline YOLOv8 and other lightweight detectors.

### Key Findings
- The multiscale modifications improve detection of small-scale and occluded fire/smoke over baseline YOLOv8.
- Complex canopy backgrounds remain the dominant source of false positives and missed detections.
- The model is positioned as lightweight enough for near-real-time drone use.

### Research Gap Identified
The contribution is a better detector. Its output is bounding boxes and class scores; there is no downstream layer that turns a detection into a coordinated response, retrieves operating protocols, or notifies responders.

---

## Paper 2: A RAG-Based Multi-Agent LLM System for Natural Hazard Resilience and Adaptation

### Citation
- **Authors**: TODO(verify) exact author list — DOI resolves to the published article.
- **Journal/Conference**: *npj Climate Action* (Nature), 4
- **Year**: 2025
- **DOI**: 10.1038/s44168-025-00254-1 (preprint: arXiv:2504.17200)
- **Title**: *A RAG-Based Multi-Agent LLM System for Natural Hazard Resilience and Adaptation* (the wildfire-focused configuration is presented as "WildfireGPT")

### Methodology
A multi-agent RAG pipeline: a user-profile agent captures the decision-maker's context, a planning agent formulates a customized action plan, and an analyst agent retrieves and interprets domain material (climate projections, observational datasets, scientific literature) through a retrieval layer before the LLM answers.

### Key Findings
- Grounding the LLM in retrieved domain sources produces customized, source-referenced hazard action plans rather than generic advice.
- The multi-agent split (profile / plan / analyse) keeps each retrieval query focused and the output auditable.

### Research Gap Identified
Retrieval is over curated datasets and documents assembled ahead of time. There is no automated trigger from a live detection event, no ingestion of real-time sensor or drone telemetry into the query, and no mechanism that dispatches the plan to people in the field.

---

## Paper 3: IoT-Based Edge Computing (IoTEC) for Improved Environmental Monitoring

### Citation
- **Authors**: Roostaei, J., & Wager, Y. Z.
- **Journal/Conference**: *Sustainable Computing: Informatics and Systems*, 39, article 100870
- **Year**: 2023
- **DOI**: 10.1016/j.suscom.2023.100870
- **Title**: *IoT-based edge computing (IoTEC) for improved environmental monitoring*

### Methodology
Couples IoT sensor networks with edge servers that run local pre-processing and machine-learning inference. Evaluated on two pilot deployments (vapour-intrusion monitoring and wastewater-based algae cultivation), comparing data latency, energy consumption, and economic cost against conventional cloud-only sensor monitoring.

### Key Findings
- Edge pre-processing reduces data transmission and end-to-end latency.
- It improves energy- and cost-efficiency of the monitoring system.
- ML deployed on the edge servers supports advanced on-site data processing.

### Research Gap Identified
The workload is scalar environmental sensing. There is no aerial or video modality, and no cognitive / language layer that converts a detected anomaly into an operational response plan.

---

## Paper 4: Real-Time Wildfire Monitoring with a Fleet of UAVs

### Citation
- **Authors**: Bailon-Ruiz, R., Bit-Monnot, A., & Lacroix, S.
- **Journal/Conference**: *Robotics and Autonomous Systems*, 152, article 104071
- **Year**: 2022
- **DOI**: 10.1016/j.robot.2022.104071
- **Title**: *Real-time wildfire monitoring with a fleet of UAVs*

### Methodology
Plans observation trajectories for a fleet of UAVs so that firefighters receive precise, up-to-date maps of a propagating wildfire front. Couples a fire-propagation model with a multi-UAV trajectory planner that decides where and when each UAV should observe.

### Key Findings
- A coordinated fleet produces more precise and more current fire-front information than uncoordinated or fixed-pattern flights.
- The planner accounts for fire-spread prediction uncertainty when allocating observation effort.

### Research Gap Identified
The work is observation and planning robotics. It does not persist the collected front data to a cloud incident store, nor use the flight telemetry to retrieve localized response procedures — the map is produced, the response step is left to humans.

---

## Paper 5: DeepSmoke — Deep Learning Model for Smoke Detection and Segmentation in Outdoor Environments

### Citation
- **Authors**: Khan, S., Muhammad, K., Hussain, T., Del Ser, J., Cuzzolin, F., Bhattacharyya, S., Akhtar, Z., & de Albuquerque, V. H. C.
- **Journal/Conference**: *Expert Systems with Applications*, 182, article 115125
- **Year**: 2021
- **DOI**: 10.1016/j.eswa.2021.115125
- **Title**: *DeepSmoke: Deep learning model for smoke detection and segmentation in outdoor environments*

### Methodology
A two-stage pipeline: an EfficientNet-based classifier first detects the presence of smoke, then a DeepLabv3+ semantic-segmentation network localizes the smoke region at pixel level. Trained and evaluated on outdoor smoke imagery, with attention to the indoor-vs-outdoor generalization gap.

### Key Findings
- Combining detection with segmentation improves smoke localization over detection-only baselines.
- Pixel-level segmentation is more robust than bounding boxes for the diffuse, ill-defined boundaries of smoke.
- Outdoor scenes (haze, cloud, variable lighting) remain substantially harder than indoor.

### Research Gap Identified
Evaluation is entirely image-level (IoU, pixel accuracy). There is no ingestion pipeline and no path from a segmented smoke region to a response plan or an alert.

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
