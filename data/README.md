# `data/`

| Subfolder | Committed? | Contents |
| :--- | :--- | :--- |
| `knowledge-base/` | **yes** | SOP source docs for the RAG/FAISS index (`sample_sops/` illustrative texts). |
| `flame/` | no (git-ignored) | FLAME dataset — student-downloaded. |
| `firenet/` | no (git-ignored) | FireNet dataset — student-downloaded. |

The datasets are large and license-gated, so they are **not** in git. Download them
from the sources below and extract into the paths shown.

## FLAME (primary) — `data/flame/`

Source: Shamsoshoara et al. (2020), *The FLAME dataset*, IEEE DataPort, DOI `10.21227/qad6-r683`
(open access, free IEEE account). Use the **frame-level Fire / No-Fire classification** sub-item.

```
data/flame/
├── Training/
│   ├── Fire/       25,018 jpg
│   └── No_Fire/    14,357 jpg
└── Test/
    ├── Fire/        5,137 jpg
    └── No_Fire/     3,480 jpg
```
Total 47,992 frames, 254×254 RGB, **classification-only** (label = folder name, no bounding boxes).
Validation set is held out from `Training/` at train time (FLAME ships no val folder).

## FireNet (secondary) — `data/firenet/`

Source: FireNET project (Olafenwa Moses), release v1.0 —
`https://github.com/OlafenwaMoses/FireNET/releases/download/v1.0/fire-dataset.zip` (direct, no login).

```
data/firenet/
├── train/
│   ├── images/        412 jpg
│   └── annotations/   412 xml   (Pascal VOC, class "fire")
└── validation/
    ├── images/         90 jpg
    └── annotations/     90 xml
```
502 images total — real bounding-box ground truth for the `fire` class.

See `docs/research/datasets.md` for the full specification and known limitations.
