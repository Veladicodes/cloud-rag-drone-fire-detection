"""FastAPI application entrypoint.

LOCAL STAND-IN FOR: the Azure Container Apps-hosted FastAPI Core Gateway
(docs/architecture/architecture.md). Run from the repo root:

    uvicorn backend.main:app --reload --port 8000
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

# Allow `python backend/main.py` as well as `uvicorn backend.main:app`.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from backend.api import routes_incidents, routes_plans, routes_telemetry  # noqa: E402
from backend.core.config import get_settings  # noqa: E402
from backend.core.db import init_db  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    logging.getLogger("main").info(
        "startup: db=%s llm_mode=%s embed_mode=%s yolo_mode=%s",
        settings.database_url, settings.llm_mode, settings.embed_mode, settings.yolo_mode,
    )
    yield


app = FastAPI(
    title="Cloud-Drone Fire Detection — local prototype", version="0.2.0", lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_telemetry.router)
app.include_router(routes_incidents.router)
app.include_router(routes_plans.router)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "llm_mode": settings.llm_mode,
        "embed_mode": settings.embed_mode,
        "yolo_mode": settings.yolo_mode,
        "note": "all cloud services are local stand-ins — see cloud/README_LOCAL_MODE.md",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
