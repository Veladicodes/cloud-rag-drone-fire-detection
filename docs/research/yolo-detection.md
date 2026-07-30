# YOLO Object Detection for Early Forest Fire Detection

Early-stage forest fire detection poses unique computer vision challenges. Smoke plumes are highly diffuse, variable in density, and easily confused with meteorological clouds or dust. Flames are often obscured by the canopy in early stages. Therefore, deploying advanced object detection frameworks like **YOLO** (You Only Look Once) is critical for real-time aerial surveillance.

---

## Model Selection & Architecture

The framework relies on **YOLOv8** (and optionally **YOLOv9**) optimized with **PyTorch**. The architecture features:
1. **Backbone**: Modified CSPDarknet53 for feature extraction, utilizing Cross-Stage Partial networks to capture fine-grained textures (e.g., wispy smoke plumes) while keeping parameter counts low.
2. **Neck**: Path Aggregation Network (PANet) or Feature Pyramid Network (FPN) to aggregate features across various scale resolutions, ensuring small-scale, distant smoke plumes are detected.
3. **Head**: Anchor-free decoupled detection head. Decoupling classification and regression tasks speeds up convergence and increases detection precision for overlapping objects.

---

## Dataset Optimization & Preprocessing

Drones capture aerial perspectives that differ significantly from ground-based datasets. Our proposed dataset prep includes:
- **Perspective Transformations**: Random scale, translation, rotation, and shear to simulate drone roll, pitch, and yaw adjustments.
- **Color Adjustments**: Modifying contrast, saturation, and hue to simulate varying lighting conditions (dawn, dusk, high noon) and forest colors.
- **Aerial Smoke Synthesis**: Overlaying semi-transparent synthetic smoke textures on canopy images to augment sparse real-world training instances.
- **Resolution**: Input frames are standardized to $640 \times 640$ pixels for optimal balance between spatial feature retention and processing speed.

---

## Loss Functions

The YOLO model optimizes parameters using a composite loss function:

$$L_{\text{total}} = \lambda_{\text{box}} L_{\text{CIoU}} + \lambda_{\text{cls}} L_{\text{BCE}} + \lambda_{\text{dfl}} L_{\text{DFL}}$$

Where:
1. **Complete Intersection over Union ($L_{\text{CIoU}}$)**: Computes bounding box regression overlap, aspect ratio, and center distance alignment to ensure accurate fire boundary predictions.
2. **Binary Cross-Entropy ($L_{\text{cls}}$)**: Measures classification errors between smoke, fire, and background classes.
3. **Distribution Focal Loss ($L_{\text{DFL}}$)**: Optimizes the regression of bounding box edges near high uncertainty zones (highly relevant for diffuse smoke boundaries).

---

## Edge vs. Cloud Processing

| Processing Location | Hardware Stack | Strengths | Weaknesses |
| :--- | :--- | :--- | :--- |
| **Edge Processing (Onboard UAV)** | NVIDIA Jetson Orin Nano / NX | Zero transmission latency; functions in zones with no network coverage; reduced bandwidth needs. | Constrained battery life; limited to smaller model architectures (YOLOv8-nano/small). |
| **Cloud Processing (Azure VM)** | Azure NC-series GPU VMs (e.g., NVIDIA A10G) | Can run complex ensembles (YOLOv8-medium/large); no battery drain on UAV; easy deployment updates. | Requires stable long-range LTE/satellite connection; higher video stream latency. |

---

## Target Evaluation Metrics

Performance targets for the research-grade system are defined as follows:

- **mAP@0.5**: $\ge 88.0\%$ (indicating high localization and classification success at standard thresholds).
- **mAP@0.5:0.95**: $\ge 62.0\%$ (evaluating strict spatial accuracy of bounding boxes).
- **Inference Speed**: $\ge 30$ Frames Per Second (FPS) on Jetson Orin boards using TensorRT quantization.
