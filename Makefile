# Convenience targets for the local prototype. See RUN_LOCALLY.md for detail.
# Every target runs plain local processes -- no Docker, no Azure.
.PHONY: setup index seed migrate backend sim test frontend-build clean

setup:              ## install python deps + copy .env
	python -m pip install -r requirements.txt
	@test -f .env || cp .env.example .env

index:              ## build the FAISS SOP index
	python -m ai.rag.ingest

seed:               ## create the DB + 3 mock drones (add ARGS=--incident for a worked example)
	python -m database.seed $(ARGS)

migrate:            ## apply Alembic migrations (alternative to seed's create_all)
	python -m alembic upgrade head

backend:            ## run the API on :8000
	python -m uvicorn backend.main:app --reload --port 8000

sim:                ## run the drone simulator against a running backend
	python testing/simulate_drone.py --iterations 30 --incident-every 6

test:               ## run the test suite
	python -m pytest testing/unit -q

frontend-build:     ## install + production-build the dashboard
	cd frontend && npm install && npm run build

clean:              ## remove local runtime artifacts
	rm -f local.db logs/alerts.log
	rm -rf storage ai/rag/faiss_index results/yolo-metrics/last_run.json
