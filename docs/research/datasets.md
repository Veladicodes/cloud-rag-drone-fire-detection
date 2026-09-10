# Research Datasets

This document details the specifications, selection criteria, expected splits, and limitations of the datasets chosen to validate the object detection pipeline.

---

## 1. Dataset 1: FLAME (Fire & Smoke Dataset)

### Purpose
To train and evaluate the deep learning model on high-resolution drone-captured imagery of active wildland fire zones.

### Dataset Source
- **Authors**: Shamsoshoara, A., Afghah, F., Razi, A., Zheng, L., Fulé, P., & Blasch, E. (2020). *The FLAME dataset: Aerial Imagery Pile burn detection using drones (UAVs).* IEEE DataPort. DOI: 10.21227/qad6-r683.
- **Format**: IEEE DataPort, open access (free IEEE account required).
- **Link/Availability**: <https://ieee-dataport.org/open-access/flame-dataset-aerial-imagery-pile-burn-detection-using-drones-uavs>

### Number of Images
- **Total Frames**: 47,992 frames (extracted from aerial video sequences).
- **Type**: RGB frames. (The full FLAME release also includes raw video, thermal video, and segmentation-mask sub-items; this project uses only the frame-level Fire / No-Fire classification image set.)

### Classes
1. `Fire` — whole-frame label: flame visible in the frame.
2. `No_Fire` — whole-frame label: background forest canopy, mountains, sky.

> **As downloaded (Phase 3).** The frame-level classification set is **classification-only** —
> the label is the parent folder (`Fire/` or `No_Fire/`), there are **no bounding boxes**.
> Real counts on disk: **Training 39,375** (Fire 25,018 / No_Fire 14,357) + **Test 8,617**
> (Fire 5,137 / No_Fire 3,480) = **47,992** — matches the documented total exactly. Frames are
> pre-resized to **254 × 254** RGB in this release.

### Expected Train/Validation/Test Split
Target parameters (70 / 15 / 15, chronological by flight to prevent frame leakage):
- **Training Set**: 70% (approximately 33,594 frames).
- **Validation Set**: 15% (approximately 7,199 frames).
- **Testing Set**: 15% (approximately 7,199 frames).

> **As downloaded.** FLAME ships a `Training/` set and a `Test/` set only — no separate
> validation folder. Phase-3 training therefore holds out the **last ~15% of `Training/`
> (deterministic slice)** as the validation set and evaluates final metrics on the untouched
> `Test/` set. The chronological-by-flight intent is approximated by a deterministic ordered
> slice; the deviation is recorded in `ADR-001.md`'s outcome addendum.

### Image Resolution
- **As downloaded**: 254 × 254 RGB (already resized in this FLAME sub-item).
- **Target Network Resolution**: 640 × 640 for YOLOv8/v9 training (`imgsz=640`); YOLO letterboxes the 254 px frames up to this size.

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
- **Project**: FireNET (DeepQuest AI / Olafenwa Moses), release v1.0.
- **Download**: <https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/fire-dataset.zip> (direct, no login).

### Number of Images
> **Corrected in Phase 3.** An earlier draft of this document listed **12,380** annotated frames;
> that figure referred to a differently-sized FireNet-family set and was never the set actually
> obtained. The real downloaded set is **502 images with 502 Pascal-VOC XML annotation files**.

- **Total Images**: **502** annotated frames (train 412 / validation 90).
- **Type**: RGB frames with Pascal-VOC bounding-box annotations (`.xml`).

### Classes
1. `fire` — a single bounding-box class (flame region). *(No separate `smoke` / `background` classes in this release.)*

### Train/Validation Split (as shipped)
- **Training Set**: 412 images (`data/firenet/train/`).
- **Validation Set**: 90 images (`data/firenet/validation/`).
- No dedicated test split is shipped; FireNet is used here as a **secondary, smoke/flame
  bounding-box** set to complement FLAME's whole-frame labels.

### Image Resolution
- **Raw Resolution**: mixed / small (e.g. a sample frame is 272 × 185).
- **Target Network Resolution**: 640 × 640 (`imgsz=640`) with YOLO letterboxing.

### Selection Justification
FireNet supplies **real bounding-box ground truth** for flame regions — which the FLAME
classification set lacks — so it is the set that lets the detector learn localisation rather
than whole-frame presence/absence. It also spans varied atmospheric conditions (haze, overcast).

### Limitations
- **Small**: 502 images total — enough to demonstrate a real detection-training loop, not enough for a production detector.
- **Resolution Variance**: many instances are low-resolution, which degrades bounding-box regression.
- **Single class**: only `fire`; no dedicated `smoke` boxes despite the project name.
- **Mixed viewpoint**: some frames are ground-level, not aerial.

---

## 3. Future Preprocessing & Augmentation Plan
During the model training phase, the following transformations will be applied to improve accuracy:
1. **Geometric Augmentations**: Random cropping, horizontal flipping, and perspective shear to simulate drone movements.
2. **Color Augmentations**: Saturation, brightness, and contrast modifications to simulate varying weather and lighting.
3. **Synthetic Plume Synthesis**: Overlaying semi-transparent synthetic smoke textures on canopy frames to expand the smoke training dataset.
