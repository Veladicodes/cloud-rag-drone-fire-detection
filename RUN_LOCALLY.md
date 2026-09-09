# Run the prototype locally

Everything runs as plain local processes — **no Docker, no Azure account, no API
keys**. Every "cloud" component is a local stand-in; the map of stand-in → real
Azure service is in [`cloud/README_LOCAL_MODE.md`](cloud/README_LOCAL_MODE.md).

## 0. One-time setup

```bash
python -m venv .venv && . .venv/Scripts/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt                      # core + sentence-transformers
# optional extras (real edge detector / real local LLM):
pip install ultralytics                              # else YOLO runs in STUB mode
cp .env.example .env
```

## 1. Build the SOP vector index (FAISS)

```bash
python -m ai.rag.ingest
```

Indexes `data/knowledge-base/sample_sops/` with `sentence-transformers/all-mpnet-base-v2`
(768-dim). First run downloads the model (~420 MB). Set `EMBED_MODE=hash` in `.env`
to skip the model entirely (non-semantic fallback — CI only).

## 2. Seed the database

```bash
python -m database.seed              # 3 mock drones
python -m database.seed --incident   # + one worked incident with a plan (nice for a first look)
```

## 3. Start the backend (terminal A)

```bash
uvicorn backend.main:app --reload --port 8000
```

Health check: <http://127.0.0.1:8000/health> · API docs: <http://127.0.0.1:8000/docs>

> Note: run from the **repo root** (`uvicorn backend.main:app`), not from inside
> `backend/`, because the code is a multi-package project (`backend`, `database`,
> `ai`, `cloud`).

## 4. Start the dashboard (terminal B)

```bash
cd frontend
npm install
npm run dev            # http://localhost:5173
```

## 5. Run the drone simulator (terminal C)

```bash
python testing/simulate_drone.py --iterations 30 --incident-every 6
```

## What you should see

simulated drone → placeholder YOLO detection → `POST /api/v1/incidents` →
**immediate `[MOCK SMS]` logged** (before RAG) → RAG plan generated
(`[MOCK LLM OUTPUT]` unless `LLM_MODE=local`) → **enriched `[MOCK SMS/PUSH]` logged**
→ dashboard map, alert feed, and response-plan viewer all update live.

Mock alert log: `logs/alerts.log`.

## Tests

```bash
python -m pytest testing/unit -q
```

`testing/unit/test_incidents_route.py` is the automated end-to-end proof: it POSTs
a synthetic incident and asserts an `alerts` row **and** a `response_plans` row are
created, with the immediate alert no later than the enriched one.
