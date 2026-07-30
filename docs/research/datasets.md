# Research Datasets

This document details the specifications, selection criteria, expected splits, and limitations of the datasets chosen to validate the object detection pipeline.

---

## 1. Dataset 1: FLAME (Fire & Smoke Dataset)

### Purpose
To train and evaluate the deep learning model on high-resolution drone-captured imagery of active wildland fire zones.

### Dataset Source
- **Authors**: Kehel et al. (Northern Arizona University).
- **Format**: IEEE Datasets Repository.
- **Link/Availability**: Open-access academic distribution.

### Number of Images
- **Total Frames**: 47,992 frames (extracted from aerial video sequences).
- **Type**: RGB frames alongside matching thermal video frames.

### Classes
1. `Fire` (or flame boundaries).
2. `No-Fire` (representing standard background forest canopy, mountains, and sky).

### Expected Train/Validation/Test Split
To ensure robust evaluation and prevent model overfitting, the dataset is split using target parameters:
- **Training Set**: 70% (approximately 33,594 frames).
- **Validation Set**: 15% (approximately 7,199 frames).
- **Testing Set**: 15% (approximately 7,199 frames).
*Frames are split chronologically across different flights to prevent frame leakage from adjacent video segments.*

### Image Resolution
- **Raw Resolution**: $3840 \times 2160$ (4K UHD) and $1920 \times 1080$ (Full HD).
- **Target Network Resolution**: Quantized to $640 \times 640$ pixels during preprocessing to match the input tensor requirements of YOLOv8/v9.

### Selection Justification
FLAME provides real-world aerial perspectives from drone flights during actual prescribed forest burns. This gives the model realistic features like canopy occlusion, motion blur, and altitude scale variations, which ground-based datasets lack.

### Limitations
- **Canopy Bias**: Imagery is restricted to Arizona dry coniferous forest zones; features do not represent deciduous, humid, or tropical canopy characteristics.
- **Class Imbalance**: High overlap between sequential frames can bias accuracy metrics if validation splits are not strictly partitioned by separate flights.

---

## 2. Dataset 2: FireNet

### Purpose
To improve classification rates of early-stage smoke columns, which are often semi-transparent and hard to identify.

### Dataset Source
- **Format**: Open-source academic repository (annotated smoke datasets).
- **Availability**: Public domain.

### Number of Images
- **Total Images**: 12,380 annotated frames.
- **Type**: Normalized RGB frames.

### Classes
1. `Smoke` (representing diffuse smoke plumes, columns, and clouds).
2. `Fire` (flame regions).
3. `Background` (non-hazardous elements).

### Expected Train/Validation/Test Split
- **Training Set**: 70% (approximately 8,666 images).
- **Validation Set**: 15% (approximately 1,857 images).
- **Testing Set**: 15% (approximately 1,857 images).

### Image Resolution
- **Raw Resolution**: Mixed resolutions ranging from $320 \times 240$ to $1024 \times 768$ pixels.
- **Target Network Resolution**: Interpolated and padded to $640 \times 640$ pixels.

### Selection Justification
FireNet features a wide range of early-stage smoke columns under varying atmospheric conditions (fog, dust, haze, overcast skies). This is critical to training the model to distinguish smoke from standard forest fog.

### Limitations
- **Resolution Variance**: The low resolution of some training instances can degrade bounding box regressions.
- **Lack of Aerial Metadata**: Some images are captured from ground watchtowers, which requires augmentation to simulate drone angles.

---

## 3. Future Preprocessing & Augmentation Plan
During the model training phase, the following transformations will be applied to improve accuracy:
1. **Geometric Augmentations**: Random cropping, horizontal flipping, and perspective shear to simulate drone movements.
2. **Color Augmentations**: Saturation, brightness, and contrast modifications to simulate varying weather and lighting.
3. **Synthetic Plume Synthesis**: Overlaying semi-transparent synthetic smoke textures on canopy frames to expand the smoke training dataset.
