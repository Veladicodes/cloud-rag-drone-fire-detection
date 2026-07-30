# Literature Survey

This document reviews five key academic publications relevant to the integration of UAV surveillance, deep learning object detection, cloud-native telemetry, and Retrieval-Augmented Generation (RAG) in wildfire management.

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
